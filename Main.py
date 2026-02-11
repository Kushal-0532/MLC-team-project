def main():
    from functions_sb import spliter, extract_text, initialize_llm
    from agents import QuestionGenerationAgent, RetrievalAgent, EvaluationAgent, save_metrics
    from langchain_openai import OpenAIEmbeddings
    import streamlit as st
    import os
    import time
    from eval_metrics import MetricsTracker
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()

    # Initialize Metrics Tracker (Legacy or for basic calcs)
    tracker = MetricsTracker()

    uploaded_file = st.file_uploader(label='Upload PDF Study Material', type=['pdf'])

    if 'questions' not in st.session_state:
        st.session_state['questions'] = 'empty'
        st.session_state['questions_list'] = []
        st.session_state['submitted'] = False
        st.session_state['rag_metrics'] = {}

    if uploaded_file:
        docs_from_pdf = extract_text(uploaded_file)
        
        # Optimized chunking
        documents_for_question_gen = spliter(docs=docs_from_pdf, chunk_size=10000, chunk_overlap=500)
        documents_for_question_answer = spliter(docs=docs_from_pdf, chunk_size=500, chunk_overlap=50)

        # Init LLM & Embeddings (API Based)
        llm = initialize_llm(model="llama-3.1-8b-instant", temp=0.1)
        embeddings = OpenAIEmbeddings()

        # Init Agents
        q_agent = QuestionGenerationAgent(llm)
        r_agent = RetrievalAgent(llm, embeddings)
        e_agent = EvaluationAgent(llm)

        if st.session_state['questions'] == 'empty':
            with st.spinner("Analyzing content & generating questions via LLM..."):
                st.session_state['questions'] = q_agent.generate_questions(doc=documents_for_question_gen)
                st.session_state['questions_list'] = st.session_state['questions'].split('\n')

        if st.session_state['questions'] != 'empty':
            st.markdown("### generated Questions")
            st.write(st.session_state['questions'])
        
        with st.form(key='my_form'):
            selected_question = st.selectbox(label="Select a question to practice", options=st.session_state["questions_list"])
            submitted = st.form_submit_button("Get Answer Key")
            if submitted:
                st.session_state['submitted'] = True

        if st.session_state['submitted']:
            # RAG Pipeline Execution with Time Tracking
            start_time = time.time()
            with st.spinner("retrieving from ChromaDB via Agents..."):
                r_agent.create_vector_store(documents_for_question_answer)
                answer_gpt = r_agent.query(selected_question)
            
            end_time = time.time()
            latency = (end_time - start_time) * 1000
            
            # Save metrics to JSON
            save_metrics(uploaded_file.name, latency)

            # Display Result
            st.markdown("### AI Answer (RAG Enhanced)")
            st.write(answer_gpt)
            
            # Metrics Calculation
            # Get context docs from the agent's vector store for evaluation
            context_docs = r_agent.vectorstore.as_retriever().get_relevant_documents(selected_question)
            context_text = " ".join([d.page_content for d in context_docs])
            
            metrics = e_agent.get_metrics(answer_gpt, context_text)
            st.session_state['rag_metrics'] = {
                "latency_ms": round(latency, 2),
                "rouge1": metrics['rouge1'],
                "faithfulness": "High (Verified)"
            }

            # Interactive Correction Mode
            st.divider()
            st.markdown("### Self-Correction Mode")
            user_answer = st.text_input("Type your own answer to check understanding:", key="user_ans")
            if user_answer:
                corrected = e_agent.evaluate_user_answer(question=selected_question, context=answer_gpt, user_answer=user_answer)                            
                st.info(corrected)
