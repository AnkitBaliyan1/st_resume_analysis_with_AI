# Resume Screening Assistance with AI

This project provides a solution for HR professionals to assist in the resume screening process using Artificial Intelligence (AI). It leverages advanced NLP techniques to analyze job descriptions and resumes, helping streamline the screening process and save time.

<img width="1076" alt="Screenshot 2024-02-19 at 1 18 11 PM" src="https://github.com/AnkitBaliyan1/st_resume_analysis_with_AI/assets/86275544/19042d03-10fe-4ca7-b90e-f9caaad329f2">

## Features

- **Job Description Analysis**: Users can input the job description text, which the system uses to identify relevant resumes.
- **Resume Upload**: Users can upload multiple resumes in PDF format.
- **Document Analysis**: The system processes the uploaded resumes, extracting text and metadata for analysis.
- **Vector Embeddings**: Utilizes OpenAI's embedding model to create vector representations of resume documents.
- **Pinecone Integration**: Integrates with Pinecone, a vector database service, to store and retrieve document embeddings efficiently.
- **Similar Document Retrieval**: Finds resumes similar to the provided job description using vector similarity search.
- **Summary Generation**: Generates summaries for relevant resumes to provide quick insights.
- **Streamlit Interface**: Offers a user-friendly interface built with Streamlit, making it easy to interact with the system.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/AnkitBaliyan1/st_resume_analysis_with_AI.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the project directory.
   - Define the following variables in the `.env` file:
     ```
     PINECONE_API_KEY=your_pinecone_api_key
     PINECONE_ENVIRONMENT=your_pinecone_environment
     PINECONE_INDEX=your_pinecone_index_name
     ```

## Usage

1. Run the application:
   ```
   streamlit run main.py
   ```

2. Access the application in your web browser.

3. Paste the job description text and upload the resumes in PDF format.

4. Click on "Help me with Analysis" to start the analysis process.

5. The system will display relevant resumes along with match scores and summaries.

## Contributors

- [AnkitBaliyan1](https://github.com/AnkitBaliyan1)

## Application link

Access the webapp app here: [link](https://resumeanalysiswithai-byankit.streamlit.app)
