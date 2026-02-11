import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import RetrievalQA
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import VLite
from langchain_openai import OpenAIEmbeddings
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from prompts import pq, pqm, rag_prompt

def extract_text(uploaded_file):
    """Extracts text from PDF using PyPDF2 and returns list of Documents with page metadata."""
    pdf_reader = PdfReader(uploaded_file)
    docs = []
    for i, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        if text:
            docs.append(Document(page_content=text, metadata={"source": uploaded_file.name, "page": i + 1}))
    return docs

def spliter(docs, chunk_size, chunk_overlap):
    """Splits Documents using RecursiveCharacterTextSplitter and adds chunk metadata."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    # If docs is a string (legacy support), convert to Document
    if isinstance(docs, str):
        docs = [Document(page_content=docs)]
    
    split_docs = text_splitter.split_documents(docs)
    for i, doc in enumerate(split_docs):
        doc.metadata["chunk_index"] = i
    return split_docs

def initialize_llm(model, temp):
    """Initializes LLM (Groq/Mistral preferably, falls back to OpenAI)."""
    if os.environ.get("GROQ_API_KEY"):
        return ChatGroq(model_name=model, temperature=temp)
    return ChatOpenAI(model=model, temperature=temp)

def questions_generator(llm, chain_type, doc):
    """Generates questions using summarization chain."""
    questions_chain = load_summarize_chain(llm=llm, chain_type=chain_type, question_prompt=pq)
    questions = questions_chain.run(doc)
    return questions

def answer_generator(llm, doc, quero):
    """Verifies student answer against context."""
    chain = LLMChain(llm=llm, prompt=pqm)
    
    if isinstance(doc, list):
        context_text = " ".join([d.page_content for d in doc])
    else:
        context_text = str(doc)
        
    corrected = chain.run(question=quero, answer=context_text, user_answer=context_text) 
    return corrected

def create_retrieval_qa_chain(doc, llm):
    """
    Creates RAG pipeline using langchain's VLite integration
    """
    # Init embeddings (API based)
    embeddings = OpenAIEmbeddings()
    
    # Create VLite vector store from docs
    if doc:
        vectorstore = VLite.from_documents(
            documents=doc,
            embedding=embeddings,
            collection="study_buddy"
        )
    else:
        vectorstore = VLite(embedding=embeddings, collection="study_buddy")
    
    # Create QA Chain
    retrieval_qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        chain_type_kwargs={"prompt": rag_prompt}
    )
    
    return retrieval_qa_chain
