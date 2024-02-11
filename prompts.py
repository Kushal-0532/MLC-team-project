from langchain.prompts import PromptTemplate

prompt_template_questions = """
You are an expert in creating practice questions based on study material.
Your goal is to prepare a student for their an exam. You do this by asking questions about the text below:

------------
{text}
------------

Create questions that will prepare the student for their exam. Make sure not to lose any important information.

QUESTIONS:
"""
pq = PromptTemplate(template=prompt_template_questions, input_variables=["text"])

prompt = "The question was: {question}\n\nMy answer: {user_answer}\n\nPlease correct any mistakes in my answer:"    
pqm = PromptTemplate(template=prompt,input_variables=["question","user_answer"])