from PyPDF2 import PdfReader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from prompts import pq
from openai import OpenAI
from langchain.chains import RetrievalQA
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
def extract_text(uploaded_file):
    pdf_reader=PdfReader(uploaded_file)
    x=''
    for page in pdf_reader.pages:
        x=x+page.extract_text()
    return x



#split stuff
def spliter(text,chunk_size,chunk_overlap):
    text_splitter=TokenTextSplitter(model_name="gpt-3.5-turbo-16k",chunk_size=chunk_size,chunk_overlap=chunk_overlap)

    text_chunk = text_splitter.split_text(text)
    doc=[Document(page_content=t) for t in text_chunk]

    return doc

def initialize_llm(model,temp):
    llm=ChatOpenAI(model=model,temperature=temp)
    return llm

def questions_generator(llm,chain_type,doc):
    questions_chain=load_summarize_chain(llm=llm,chain_type=chain_type,question_prompt=pq)
    questions=questions_chain.run(doc)
    return questions
def answer_generator(llm,doc,quero):
    prompter = PromptTemplate(
 input_variables=["question", "answer"],
 template="You are a study helper. If correct you tell so, otherwise give the necessary corrections. \nQuestion:{question}\n User's answer: {answer}")
    prompter.format(question=quero,answer=doc)
    chain = LLMChain(llm=llm,prompt=prompter)
    corrected=chain.run(question=quero,answer=doc)
    return corrected

def create_retrieval_qa_chain(doc,llm):
    embeddings = OpenAIEmbeddings()

    vector_database = Chroma.from_documents(documents=doc, embedding=embeddings)
    retrieval_qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_database.as_retriever())

    return retrieval_qa_chain

