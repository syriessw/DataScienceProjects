# RAG LLM Project

This project demonstrates a Retrieval-Augmented Generation (RAG) pipeline using LangChain, Chroma, and PyPDFLoader. The workflow leverages **MiniLM** for embeddings and **Mistral** for text generation. The goal is to efficiently retrieve relevant information from documents and generate meaningful responses using a language model.

## Libraries Involved:
- **Langchain**: Provides an interface for building RAG pipelines and handling text-based tasks.
- **Chroma**: A vector database to store and query embeddings.
- **PyPDFLoader**: For loading and processing PDF documents.

## Models Used:
- **Embedding**: MiniLM (Locally saved version of MiniLM for embedding tasks)
- **Text-Generation**: Mistral (Hosted using Ollama for generating text)

---

## Project Steps:

### 1. Load PDFs with PyPDFLoader
   - Use `PyPDFLoader` to extract and load content from PDF files.

### 2. Utilize LangChain to Split Documents into Chunks
   - LangChain handles document chunking to ensure proper embedding generation and storage.

### 3. Save a Local Version of the MiniLM Model
   - MiniLM is used for embedding the document chunks. Ensure the model is saved locally for performance reasons.

### 4. Declare Embeddings with MiniLM
   - Load the MiniLM model to generate document embeddings for semantic search.

### 5. Set Up Persistent Chroma DB with MiniLM Embeddings
   - Use Chroma DB to store document embeddings with a persistent local database.

### 6. Add Document Chunks into Chroma DB
   - Add the chunked document embeddings to the Chroma DB for efficient retrieval later.

### 7. Create a PromptTemplate with LangChain
   - Set up a template to structure how the results are combined and returned when a query is made.

### 8. Search the Chroma DB for the Most Relevant Chunks (Embeddings)
   - When a query is made, Chroma will return the most relevant document chunks based on the embeddings.

### 9. Set Up Text-Generation Model Mistral
   - Leverage the Mistral model for generating text. Mistral will take the query and document context to generate a response.

### 10. Process Result Prompt and Format
   - Combine the query, document chunks, and generated text into a structured format for display or further use.

---

## Additional Functionality:

### Web Scraping for Recipes

1. **Scrape Web Pages for Recipe Information**
   - Use a web scraper to extract recipe content from websites.

2. **Use BeautifulSoupTransformer to Eliminate Tags**
   - Clean up the scraped data to remove unnecessary HTML tags and only retain text.

3. **Repeat Steps 6 to 10 from Above**
   - Embed the scraped data into Chroma DB, search for relevant content, and use the Mistral model for text generation.

---

## Installation & Setup

### Requirements:
1. Install necessary libraries:
   ```bash
   pip install langchain chromadb pypdf transformers torch beautifulsoup4
   ```
2. Download and set up the local MiniLM model and Mistral model.

## Running the Project:

1. Ensure all libraries and models are properly installed and downloaded.
2. Run the pipeline by loading documents (or scraped content) into the Chroma DB.
3. Use a query to retrieve document embeddings and generate meaningful text with the Mistral model

## Project Structure

├── data/
│   ├── pdfs/         # Store PDFs here
├── models/
│   ├── MiniLM/       # MiniLM embedding model
│   ├── Mistral/      # Mistral text-generation model (hosted locally or via Ollama)
├── chroma_db/        # Chroma DB for storing embeddings
├── src/
│   ├── pdf_loader.py
│   ├── query_pipeline.py
├── README.md         # Project documentation

## Future Enhancements

- Explore other embedding models such as BERT or Sentence Transformers.
- Optimize the pipeline for real-time document processing and querying.
- Expand the RAG pipeline to work with multi-modal data (text, images, etc.).

## Credits
This project is possible from the guided resouces of:
- https://www.youtube.com/watch?v=uj1VnDPR9xo (https://github.com/pixegami/rag-tutorial-v2/blob/main/query_data.py)
- https://medium.com/the-modern-scientist/building-generative-ai-applications-using-langchain-and-openai-apis-ee3212400630
- https://www.comet.com/site/blog/top-5-web-scraping-methods-including-using-llms/
- https://medium.com/@thakermadhav/build-your-own-rag-with-mistral-7b-and-langchain-97d0c92fa146
