








from functions_sb import spliter, extract_text,initialize_llm,questions_generator,create_retrieval_qa_chain, initialize_llm_answer_correct, answer_generator
import streamlit as st
import os
from openai import OpenAI
key = "API Goes here" 

st.title("Skynet the study Buddy")
os.environ["OPENAI_API_KEY"]='Api Goes here'
uploaded_file=st.file_uploader(label='Put your pdfs here!',type=['pdf'])


if 'questions' not in st.session_state:
    st.session_state['questions'] = 'empty'
    st.session_state['seperated_question_list'] = 'empty'
    st.session_state['questions_to_answers'] = 'empty'
    st.session_state['submitted'] = 'empty'


if uploaded_file:

    # Load data from pdf 
    text_from_pdf = extract_text(uploaded_file)

    # Split the text for question gen
    documents_for_question_gen = spliter(text=text_from_pdf, chunk_size=10000, chunk_overlap=200)

    # Split the text for question answering 
    documents_for_question_answer = spliter(text=text_from_pdf, chunk_size=1000, chunk_overlap=100)
    
    

        # Init llm for question generation
    llm_question_gen = initialize_llm(model="gpt-3.5-turbo-16k", temp=0.4)

    # Init llm for question answering
    llm_question_answer = initialize_llm(model="gpt-3.5-turbo-16k", temp=0.1)

    if st.session_state['questions'] == 'empty':
        with st.spinner("Generating questions..."):
            st.session_state['questions'] = questions_generator(llm=llm_question_answer, chain_type="refine", doc=documents_for_question_gen)

    if st.session_state['questions'] != 'empty':
        st.write(st.session_state['questions'])
        st.session_state['questions_list'] = st.session_state['questions'].split('\n')
        
    with st.form(key='my_form'):
        st.session_state['questions_to_answer'] = st.multiselect(label="Select questions to answer", options=st.session_state['questions_list']) 
        submitted = st.form_submit_button("Generate Answer")
        if submitted:
            st.session_state['submitted'] = True
    mpty=""
    if st.session_state['submitted']:
            with st.spinner("Generating answers..."):
                generate_answer_chain = create_retrieval_qa_chain(doc=documents_for_question_answer, llm=llm_question_answer)
                for question in st.session_state['questions_to_answer']:
                    answer = generate_answer_chain.run(question)
                    mpty=mpty.append(question,answer)
                st.download_button("Click here to download!",mpty)
                for question in st.session_state['questions_to_answer']:

                    answer = generate_answer_chain.run(question)

                    st.write(f"Question: {question}")
                    answer = st.text_input("Enter answer for {0}".format(question))
                    if answer:
                        documents_for_question_answer = spliter(text=answer, chunk_size=1000, chunk_overlap=100)
                        corrected=answer_generator(llm=llm_question_answer,doc=documents_for_question_answer,quero=question)
                        st.write(corrected)
                        st.write(f"Ideal answer: {answer}")
                
