package randomsearch

import com.mlp.sdk.*
import com.mlp.sdk.utils.JSON
import org.nd4j.linalg.factory.Nd4j
import org.nd4j.linalg.ops.transforms.Transforms

data class LossFunctionInitConfig(val points: List<List<Double>>)

data class LossFunctionRequest(
    val point: List<Double>
)

data class LossFunctionResponse(
    val loss: Double
)

class SampleLoss: MlpPredictServiceBase<LossFunctionRequest, LossFunctionResponse>(
    REQUEST_EXAMPLE, RESPONSE_EXAMPLE) {

    val init = JSON.parse(System.getenv()["SERVICE_CONFIG"]!!, LossFunctionInitConfig::class.java)
    val targetPoints = init.points.map {
        Nd4j.create(it)
    }

    override fun predict(request: LossFunctionRequest): LossFunctionResponse {
        val p = Nd4j.create(request.point)
        val res = targetPoints.map {
            Transforms.euclideanDistance(it, p)
        }.sorted()[0]
        return LossFunctionResponse(res)
    }

    companion object {
        val REQUEST_EXAMPLE = LossFunctionRequest(listOf(1.0, 1.0))
        val RESPONSE_EXAMPLE = LossFunctionResponse(10.0)
    }

}

