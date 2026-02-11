from langchain.prompts import PromptTemplate

# Enhanced prompt for question generation
prompt_template_questions = """
You are an advanced AI Tutor for university students. 
Your goal is to prepare a student for their exam based on the provided study material.
Analyze the text below and generate comprehensive practice questions that test concept understanding.

------------
{text}
------------

Generate 5 high-quality questions (mix of conceptual, factual, and applied).

QUESTIONS:
"""
pq = PromptTemplate(template=prompt_template_questions, input_variables=["text"])

# Enhanced prompt for answer grading/correction
prompt_correction = """
You are a strict but helpful AI Teaching Assistant.
Evaluate the student's answer against the correct context.

Question: {question}
Context details from notes: {answer} (This is the ground truth)
Student's Answer: {user_answer}

Task:
1. Determine if the student's answer is factually correct based *only* on the context.
2. If correct, praise them briefly.
3. If incorrect or incomplete, provide the correct answer and explain the gap.

FEEDBACK:
"""
pqm = PromptTemplate(template=prompt_correction, input_variables=["question", "answer", "user_answer"])

# RAG specific prompt for Q&A
rag_template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Keep the answer concise and academic.

Context:
{context}

Question: {question}

Answer:"""
rag_prompt = PromptTemplate(template=rag_template, input_variables=["context", "question"])
