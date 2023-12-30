import PyPDF2

reader = PyPDF2.PdfReader('/home/kushal/Downloads/dfg.pdf') 
    
peg=reader.get_object()
print(peg)
page = reader.pages[0] 
  
# extracting text from page 
text = page.extract_text() 
print(text) 