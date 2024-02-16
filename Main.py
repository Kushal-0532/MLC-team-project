
def main():
    from functions_sb import spliter, extract_text,initialize_llm,questions_generator,create_retrieval_qa_chain, answer_generator
    import streamlit as st
    import os
    from openai import OpenAI
    key = "API goes here" 

    st.caption("Skynet")
    os.environ["OPENAI_API_KEY"]='API goes here'
    uploaded_file=st.file_uploader(label='Put your pdfs here!',type=['pdf'])


    if 'questions' not in st.session_state:
        st.session_state['questions'] = 'empty'
        st.session_state['seperated_question_list'] = 'empty'
        st.session_state['questions_to_answers'] = 'empty'
        st.session_state['submitted'] = 'empty'
    

    if uploaded_file:


        text_from_pdf = extract_text(uploaded_file)


        documents_for_question_gen = spliter(text=text_from_pdf, chunk_size=10000, chunk_overlap=200)

  #smol chunk size for less token cost
        documents_for_question_answer = spliter(text=text_from_pdf, chunk_size=1000, chunk_overlap=100)
    
    

       


        llm_question_answer = initialize_llm(model="gpt-3.5-turbo-16k", temp=0.1)

        if st.session_state['questions'] == 'empty':
            with st.spinner("Generating questions..."):
                st.session_state['questions'] = questions_generator(llm=llm_question_answer, chain_type="refine", doc=documents_for_question_gen)

        if st.session_state['questions'] != 'empty':
            st.write(st.session_state['questions'])
            st.session_state['questions_list'] = st.session_state['questions'].split('\n')
        submitted=""
        selected_list=[]
        with st.form(key='my_form'):
            selected_question = st.selectbox(label="Select a question",options=st.session_state["questions_list"])
            submitted = st.form_submit_button("Click me to select your question!")
            selected_list.append(selected_question)
            if submitted:
                st.session_state['submitted'] = True
        All_questions=st.session_state["questions_list"]
        
        if st.session_state['submitted']:
                with st.spinner("Thinking...."):
                    generate_answer_chain = create_retrieval_qa_chain(doc=documents_for_question_answer, llm=llm_question_answer)
                questions_answers = []
                for question in All_questions:
                    answer_gpt = generate_answer_chain.run(question)
                    questions_answers.append(f"{question}\n{answer_gpt}\n\n")
                to_download = "Questions and Answers:\n"
                to_download += "".join(questions_answers)
                
                st.download_button("Click me to download all answers!",to_download)

                print(question,answer_gpt)

                for question in selected_list:

                    answer = generate_answer_chain.run(question)

                    st.write(f"Question: {question}")
                    answer = st.text_input("Enter answer for {0}".format(question))
                    if answer:
                        documents_for_question_answer = spliter(text=answer, chunk_size=1000, chunk_overlap=100)
                        corrected=answer_generator(llm=llm_question_answer,doc=documents_for_question_answer,quero=question)                            
                        st.write(corrected)
                        st.write(f"Your answer: {answer}")
        
   

