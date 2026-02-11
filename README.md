# Study Buddy: Enterprise RAG Edition

Study Buddy is a sophisticated RAG (Retrieval-Augmented Generation) application designed to help university students prepare for exams. By processing PDF study materials, it generates practice questions, facilitates self-testing, and provides intelligent feedback based on the source text.

## 🚀 Features

- **Automated Question Generation**: Analyzes study materials to create a mix of conceptual, factual, and applied questions.
- **Intelligent RAG Pipeline**: Leverages vector databases and LLMs to retrieve precise context for answering questions.
- **Self-Correction Mode**: Grades student answers against the ground truth in the study material, providing detailed feedback and explanations.
- **Performance Analytics**: Tracks system performance, including query latency and ROUGE scores, visualized in a dedicated dashboard.
- **Multi-Model Support**: Optimized for Groq (Llama 3.1) for ultra-low latency, with fallback to OpenAI.

## 🛠 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Orchestration**: [LangChain](https://www.langchain.com/)
- **Vector Database**: [ChromaDB](https://www.trychroma.com/)
- **Embeddings**: [OpenAI](https://platform.openai.com/docs/guides/embeddings) (API-based, ensuring zero local compute for models)
- **LLM Providers**: [Groq](https://groq.com/) (Llama 3.1 8B), [OpenAI](https://openai.com/)
- **PDF Engine**: [PyPDF2](https://pypi.org/project/PyPDF2/)
- **Metrics**: `rouge-score`

## 📂 Project Structure

- `Main_ui.py`: The entry point for the Streamlit application and dashboard navigation.
- `Main.py`: Core logic for the study session, managing session state and agent interactions.
- `agents.py`: Implementation of specialized AI agents:
  - `QuestionGenerationAgent`: Handles context-aware question creation.
  - `RetrievalAgent`: Manages vector store operations and RAG-based Q&A.
  - `EvaluationAgent`: Performs answer grading and metric calculations.
- `functions_sb.py`: Utility functions for PDF processing, text splitting, and LLM initialization.
- `prompts.py`: Centralized management of LLM prompt templates.
- `eval_metrics.py`: Logic for calculating latency and text similarity metrics (ROUGE, F1).

## 📥 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Kushal0532/MLC-team-project.git
cd MLC-team-project
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file or export your API keys:
```bash
export GROQ_API_KEY="your_groq_api_key"
# OR
export OPENAI_API_KEY="your_openai_api_key"
```

### 4. Run the Application
```bash
streamlit run Main_ui.py
```

## 📊 Performance Monitoring
The application includes a "RAG Metrics" and "Usage Stats" dashboard to monitor:
- **Query Latency**: Response time in milliseconds.
- **ROUGE-1/ROUGE-L**: Measures the overlap between generated answers and source context.
- **Custom F1 Score**: Token-level overlap metrics.
- **System Logs**: History of queries and processing times stored in `metrics.json`.

## 🐳 Docker Support
A `Dockerfile` is provided for containerized deployment.
```bash
docker build -t study-buddy .
docker run -p 8501:8501 study-buddy
```
