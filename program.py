from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain import LLMChain

openai_api_key = "put api key here" 

import PyPDF2

pdfFile = open('put .pdf destination here', 'rb')
pdfReader = PyPDF2.PdfReader(pdfFile)
pdfText = ''
for page in pdfReader.pages:
  pdfText += page.extract_text()

llm = OpenAI(model_name="text-davinci-003", openai_api_key=openai_api_key)

prompt_to_ask_gpt = """
Generate 5 questions and their answers based on this text:
{Textfrompdf}
"""
prompt_template = PromptTemplate(template=prompt_to_ask_gpt,input_variables=["Textfrompdf"])   #Prompt to be asked

chain = LLMChain(llm=llm, prompt=prompt_template)
Textfrompdf= pdfText

result = chain.run(Textfrompdf)

print("\nGenerated questions:",result)
