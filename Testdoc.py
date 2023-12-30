'''
Old code
reader = PyPDF2.PdfReader('put pdf destination here')     
peg=reader.get_object()
print(peg)
page = reader.pages[0] 
  '''


from openai import OpenAI

client = OpenAI(api_key="Put your api key here")

import PyPDF2
reader = PyPDF2.PdfReader('put pdf destination here')     
x=reader.pages[0]   #0 for first page
textfrmpdf=x.extract_text()

#Trying to understand this part
response = client.completions.create(model='gpt-3.5-turbo',prompt="Read this block of text and ask some questions about it: {0}".format(textfrmpdf))
questions = response["choices"][0]["text"].split("\n")
print(questions)
