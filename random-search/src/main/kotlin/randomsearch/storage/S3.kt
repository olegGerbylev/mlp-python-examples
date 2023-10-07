package randomsearch.storage

import io.minio.GetObjectArgs
import io.minio.MinioClient
import io.minio.PutObjectArgs
import org.apache.commons.io.IOUtils

class S3(minioClient0: MinioClient? = null, bucket0: String? = null, val basePath: String = System.getenv("MLP_STORAGE_DIR")) {
    val minioClient: MinioClient
    val bucket: String

    init {
        minioClient = minioClient0 ?: MinioClient.builder()
            .endpoint(System.getenv("MLP_S3_ENDPOINT"))
            .credentials(System.getenv("MLP_S3_ACCESS_KEY"), System.getenv("MLP_S3_SECRET_KEY"))
            .region(System.getenv("MLP_S3_REGION") ?: "ru")
            .build()

        bucket = bucket0 ?: System.getenv("MLP_S3_BUCKET")
    }

    fun save(file: String, content: String) {
        with(IOUtils.toInputStream(content, Charsets.UTF_8)) {
            minioClient.putObject(
                PutObjectArgs.builder()
                    .bucket(bucket)
                    .`object`("$basePath/$file")
                    .stream(this, this.available().toLong(), -1)
                    .build()
            )
        }
    }

//    fun load(file: String): String? {
//        val modelResponseBytes = minioClient.getObject(
//            GetObjectArgs.builder()
//                .bucket(bucket)
//                .`object`("$basePath/$file")
//                .build()
//        ).readAllBytes()
//        if (modelResponseBytes.isEmpty()) {
//            return null
//        }
//        return String(modelResponseBytes)
//    }


}

