package randomsearch

import com.mlp.gate.DatasetInfoProto
import com.mlp.gate.ServiceInfoProto
import com.mlp.sdk.MlpClientSDK
import com.mlp.sdk.MlpServiceBase
import com.mlp.sdk.MlpServiceSDK
import com.mlp.sdk.Payload
import com.mlp.sdk.utils.JSON
import kotlinx.coroutines.*
import kotlinx.coroutines.sync.Semaphore
import kotlinx.coroutines.sync.withPermit
import org.slf4j.LoggerFactory
import randomsearch.storage.S3
import java.util.Random

data class Range(
    val min: Double, val max: Double
)

data class TerminationCriteria(
    val iterationCount: Int? = 100,
    val objectiveLossValue: Double? = null,
    val lossStagnationThreshold: Double? = null,
    val lossStagnationIterations: Int? = 10,
)

data class RSRequestData(
    val lossModel: String,

    val ranges: List<Range>,
    val initial: List<Double>,
    val dimForFit: Set<Int>,
    val stepSize: Int,
    val generationSize: Int,

    val initialRange: Double = 1.0,
    val rangeDecreasePerIteration: Double = 0.5,

    val terminationCriteria: TerminationCriteria
    )

data class LastPoint(
    val point: List<Double>,
    val loss: Double
)

data class RSResultData(
    val lastPoints: List<LastPoint>,
)

class EmptyData()


class RandomSearch: MlpServiceBase<Payload, RSRequestData, EmptyData, EmptyData, RSResultData>(
    FIT_DATA_EXAMPLE, FIT_CONFIG_EXAMPLE, REQUEST_EXAMPLE, REQUEST_EXAMPLE, RESPONSE_EXAMPLE) {
    val log = LoggerFactory.getLogger("RS")

    val ACCOUNT_ID = System.getenv().get("MLP_ACCOUNT_ID")!!
//    val s3 = S3()
    val grpcClient = MlpClientSDK()

    override fun fit(data: Payload, config: RSRequestData?,
                     modelDir: String,
                     previousModelDir: String?,
                     targetServiceInfo: ServiceInfoProto,
                     dataset: DatasetInfoProto
    ) {
        val res = randomsearch(config!!)


//        s3.save("$modelDir/$MODEL_FILENAME", JSON.stringify(res))
    }

    val semaphore = Semaphore(100)
    fun randomsearch(req: RSRequestData): RSResultData {
        val rnd = Random()
//        var hypos = (0 until req.stepSize).map {
//            Pair(req.ranges.map {
//                rnd.nextDouble() * (it.max - it.min) + it.min
//            }, Double.MAX_VALUE)
//        }
        var hypos = (0 until req.stepSize).map {
            Pair(req.ranges.mapIndexed { i, r ->
                if (req.dimForFit.contains(i)) {
                    val prev = req.initial[i]
                    val field = (r.max - r.min) * req.initialRange
                    val min = (prev - field / 2).coerceAtLeast(r.min)
                    val max = (prev + field / 2).coerceAtMost(r.max)
                    rnd.nextDouble() * (max - min) + min
                } else {
                    req.initial[i]
                }


            }, Double.MAX_VALUE)
        }
        var randomRange = req.initialRange

        var iterationCount = 0
        // цикл до наступления terminationCriteria
        while (true) {
            iterationCount++
            // перебираем точки, которые получили на предыдущем шаге и для каждой из них:
            val newHypos =
                runBlocking {
                hypos.map { prevPoint ->
                    async {
                    // генерируем новые точки с рандомным отступом в рамках разрешённого поля
                    val newPoints = (0 until req.generationSize).map {
                        req.ranges.mapIndexed { i, r ->
                            if (req.dimForFit.contains(i)) {
                                val prev = prevPoint.first[i]
                                val field = (r.max - r.min) * randomRange
                                val min = (prev - field / 2).coerceAtLeast(r.min)
                                val max = (prev + field / 2).coerceAtMost(r.max)

                                rnd.nextDouble() * (max - min) + min
                            } else {
                                req.initial[i]
                            }
                        }
                    }

                    // считаем loss для каждой точки
                    val res = newPoints.map { p ->
                        async {
                            kotlin.runCatching {
                        val lossRequest = LossFunctionRequest(p)
                            val res = try {
                                semaphore.withPermit {
                                    grpcClient.predict(ACCOUNT_ID, req.lossModel, JSON.stringify(lossRequest))
                                }
                            } catch (e: Exception) {
                                throw e
                            }
                        val lossResponse = JSON.parse(res, LossFunctionResponse::class.java)
                        Pair(p, lossResponse.loss)
                            }.getOrElse { Pair(p, Double.MAX_VALUE) }
                        }
                    }.awaitAll() + prevPoint
                    
                    // берём stepSize самых удачных
                    val z = res.sortedBy { it.second }.take(1)
                    z
                    }
                }.awaitAll().flatten()
            }

            log.info("Iteration: $iterationCount, best point: ${newHypos[0].first}, loss: ${newHypos[0].second}, range: $randomRange")

            // напишем тут ещё раз сортировку и взятие stepSize гипотез, чтобы можно было удобнее играться
            // обновляем точки для следующего шага
            hypos = newHypos.sortedBy { it.second }.take(req.stepSize)
            // обновляем размер диапазона поиска
            randomRange *= req.rangeDecreasePerIteration

            // проверим условия останова
            if (req.terminationCriteria.iterationCount != null && iterationCount >= req.terminationCriteria.iterationCount) {
                break
            }
            if (req.terminationCriteria.objectiveLossValue != null && hypos[0].second <= req.terminationCriteria.objectiveLossValue) {
                break
            }
            if (req.terminationCriteria.lossStagnationIterations != null && req.terminationCriteria.lossStagnationThreshold != null) {
                // TODO
                break
            }
        }
        log.info("Result points: ${hypos}")

        return RSResultData(hypos.map { LastPoint(it.first, it.second) })
    }

    override fun predict(request: EmptyData, config: EmptyData?): RSResultData {
//        val modelDataStr = s3.load(MODEL_FILENAME)!!
//        return JSON.parse(modelDataStr, RSResultData::class.java)
        throw RuntimeException()
    }

    companion object {
        val FIT_DATA_EXAMPLE = Payload("\"no matter\"")
        val FIT_CONFIG_EXAMPLE = RSRequestData(lossModel = "sample-loss",ranges = listOf(Range(0.0, 100.0), Range(0.0, 100.0)),stepSize = 10,generationSize = 10,initialRange = 1.0,rangeDecreasePerIteration = 0.98,terminationCriteria = TerminationCriteria(iterationCount = 100, objectiveLossValue = 0.01), dimForFit = setOf(), initial = listOf())

        val REQUEST_EXAMPLE = EmptyData()
        val RESPONSE_EXAMPLE = RSResultData(
            lastPoints = listOf()
        )

        val MODEL_FILENAME = "rs-result.json"
    }

}

fun main() {
    val rs = RandomSearch()
    rs.randomsearch(RSRequestData(
        lossModel = "opm-loss-local",

        ranges = listOf(Range(0.0, 10.0), Range(1.0, 1.0), Range(0.0, 10.0), Range(0.0, 100.0), Range(0.0, 10.0), Range(0.0, 10.0),
            Range(-1.0, 1.0), Range(-1.0, 1.0), Range(-1.0, 1.0), Range(-1.0, 1.0), Range(-1.0, 1.0), Range(-1.0, 1.0), Range(-1.0, 1.0), Range(-1.0, 1.0)
        ),
        initial = listOf(
//            0.2747823174694503,
//            1.0,
//            1.95, //1.540,
//            75.0,
//            1.3159821701196845,
//            3.639244363353831,
//            0.0, 0.009109298409282469, -0.03374649200850791, 0.01797256809388843, -0.0050513483804677005, 0.0, 0.0, 0.0
            0.2747823174694503, 1.0, 2.2328458938298787, 46.25297565535245, 5.3554289568477484, 6.654357880332785, -0.10873461940881894, -0.16415333862665035, 0.6419599810762641, -0.6914567392060917, -0.4190395854428973, 0.38385506778559875, -0.5277664585237826, 0.3803411077303045
        ),
        dimForFit = setOf(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13),

        stepSize = 10,
        generationSize = 100,
        initialRange = 0.3,
        rangeDecreasePerIteration = 0.95,
        terminationCriteria = TerminationCriteria(
            iterationCount = 100
        )
    ))

}


//
//fun main() {
//    val service =
//    if (System.getenv().get("TEST_LOSS") != null) {
//        SampleLoss()
//    } else {
//        RandomSearch()
//    }
//
//    val mlp = MlpServiceSDK(service)
//
//    mlp.start()
//    mlp.blockUntilShutdown()
//}
