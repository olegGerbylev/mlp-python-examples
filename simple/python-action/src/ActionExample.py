from caila_gate.CailaActionSDK import CailaActionSDK
from caila_gate.proto import gate_pb2
from pydantic import BaseModel

class QuestionRequest:
    context: str
    answer: str

class QuestionResponse:
    question: str


class MyService:
    def get_schema(self):
        return {"main.proto": "content of a file"}

    def get_descriptor(self):
        return gate_pb2.ActionDescriptorProto(
            name="question-generator",
            fittable=False,
            methods={"predict": gate_pb2.MethodDescriptorProto(
                input={
                    "data": gate_pb2.ParamDescriptorProto(type="QuestionRequest"),
                    "config": gate_pb2.ParamDescriptorProto(type="QuestionRequest"),
                },
                output=gate_pb2.ParamDescriptorProto(type="QuestionResponse"),
            )}
        )

    def predict(self, data: QuestionRequest, config: None):
        return QuestionResponse(question=data.context + "-" + data.answer)


caila = CailaActionSDK()
caila.register_impl(MyService())
caila.start()
caila.block_until_shutdown()
