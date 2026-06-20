from .config import TOP_K
from .generator import generate_answer
from .retriever import Retriever


class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()

    def answer(self, question, top_k=TOP_K):
        contexts = self.retriever.retrieve(question, top_k)
        return generate_answer(question, contexts), contexts
