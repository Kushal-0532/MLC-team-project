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

prompt = """
Generate 5 questions and their answers based on this text:
{0}
""".format(pdfText)

prompt_template = PromptTemplate(template=prompt, input_variables=["text"])

chain = LLMChain(llm=llm, prompt=prompt_template)


result = chain.run(pdfText)

print("\nGenerated questions:",result)
