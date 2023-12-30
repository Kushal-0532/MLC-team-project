'''
Old code
reader = PyPDF2.PdfReader('put pdf destination here')     
peg=reader.get_object()
print(peg)
page = reader.pages[0] 
  '''
# extracting text from page 
text = page.extract_text() 
print(text) 

from openai import OpenAI

client = OpenAI(api_key="Put your api key here")
import PyPDF2

pdfFile = open('Put your pdf destination here')
pdfReader = PyPDF2.PdfReader(pdfFile)
pdfText = ''
for page in pdfReader.pages:
  pdfText += page.extract_text()


response = client.completions.create(model='gpt-3.5-turbo',prompt=f"Read this block of text and ask some questions about it: {pdfText}")
questions = response["choices"][0]["text"].split("\n")
print(questions)
