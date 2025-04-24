# RFP Analyzer

## Overview

**RFP Analyzer** is a web-based tool designed to extract and summarize key information from RFP (Request for Proposal) PDF documents. It automatically identifies and summarizes essential elements such as SFP, MAR, budget, and project duration, and presents both a concise summary and the relevant pages of the PDF through an interactive viewer.

## Features

- **PDF Upload via Web UI**: Easily upload one or more PDF files for analysis.
- **Automatic Information Extraction**: Detects and extracts SFP, MAR, budget, and time information using keyword filters and LLM-based summarization.
- **Summarized Results**: Presents extracted information in a clear, organized summary.
- **PDF Viewer with Highlighted Pages**: Displays the original PDF with navigation to pages containing relevant information.
- **Multi-Document Support**: Manage and review multiple uploaded documents within the interface.

## Folder & File Structure

- `web/rfp2.py`  
  Main Streamlit application providing the web interface for PDF upload, analysis, and result display.

- `common/pdf_extract.py`  
  Functions for reading PDF files and extracting relevant text based on keyword filters.

- `common/embedding_model.py`  
  Utilities for generating text embeddings using OpenAI or open-source models.

- `common/utils.py`  
  Prompt management, LLM inference, and HTML summary generation.

- `common/prompts.json`  
  Prompt templates for summarization and extraction tasks.

- `common/document_filter.json`  
  Keyword lists for filtering and extracting specific information from PDFs.

- `common/web_requirements.txt`  
  Python dependencies required to run the system.

- `data/`  
  Example PDF files for testing and demonstration.

- `docs/example.png`  
  Demo screenshot of the system.

## Installation

1. **Python Version**  
   Python 3.9 or higher is recommended.

2. **Install Dependencies**  
   ```
   pip install -r common/web_requirements.txt
   ```

3. **Set Up Environment Variables**  
   - Create a `.env` file in your project root.
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage

1. **Run the Application**
   ```
   streamlit run web/rfp2.py
   ```

2. **Analyze PDFs**
   - Open the web interface in your browser (Streamlit will provide a local URL).
   - Upload a PDF file using the sidebar.
   - Click **Analyze** to process the document.
   - View the summary and navigate relevant pages in the PDF viewer.
   - Use **View** to review previously uploaded documents.

## Configuration

- **Prompts & Filters**  
  - Customize extraction keywords in `common/document_filter.json`.
  - Edit summarization and extraction prompts in `common/prompts.json`.

- **Embedding Model**  
  - Switch between OpenAI and open-source embedding models in `common/embedding_model.py`.

## Extensibility

- Add new extraction filters by updating `common/document_filter.json` and corresponding prompts.
- Integrate additional LLMs or embedding models as needed by extending `common/embedding_model.py` and `common/utils.py`.


## License

This project is licensed under the [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)](https://creativecommons.org/licenses/by-nc-nd/4.0/).
