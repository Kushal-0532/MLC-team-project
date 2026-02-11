import os
import time
import json
import datetime
from functools import lru_cache
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import RetrievalQA, LLMChain
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from prompts import pq, pqm, rag_prompt

class QuestionGenerationAgent:
    def __init__(self, llm):
        self.llm = llm

    def generate_questions(self, doc, chain_type="refine"):
        questions_chain = load_summarize_chain(llm=self.llm, chain_type=chain_type, question_prompt=pq)
        return questions_chain.run(doc)

class RetrievalAgent:
    def __init__(self, llm, embeddings):
        self.llm = llm
        self.embeddings = embeddings
        self.vectorstore = None
        self.qa_chain = None

    def create_vector_store(self, docs):
        # Task 4: ChromaDB with metadata (source, page, chunk_index)
        self.vectorstore = Chroma.from_documents(
            documents=docs, 
            embedding=self.embeddings,
            collection_name="study_buddy_chroma"
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
            chain_type_kwargs={"prompt": rag_prompt}
        )
        return self.vectorstore

    @lru_cache(maxsize=128)
    def query(self, question):
        # Task 3: @lru_cache for repeated queries
        if not self.qa_chain:
            return "Vector store not initialized."
        return self.qa_chain.run(question)

class EvaluationAgent:
    def __init__(self, llm):
        self.llm = llm

    def evaluate_user_answer(self, question, context, user_answer):
        chain = LLMChain(llm=self.llm, prompt=pqm)
        return chain.run(question=question, answer=context, user_answer=user_answer)

    def get_metrics(self, generated_answer, reference_context):
        from eval_metrics import MetricsTracker
        tracker = MetricsTracker()
        return tracker.calculate_basic_metrics(generated_answer, reference_context)

def save_metrics(doc_name, duration):
    # Task 2: Simple time tracking saved to JSON
    data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "document": doc_name,
        "duration": duration
    }
    metrics_file = "metrics.json"
    try:
        if os.path.exists(metrics_file):
            with open(metrics_file, "r") as f:
                metrics = json.load(f)
        else:
            metrics = []
    except (json.JSONDecodeError):
        metrics = []
    
    metrics.append(data)
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=4)
