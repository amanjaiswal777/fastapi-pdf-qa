# FastAPI PDF Q&A Service

This project is a FastAPI-based web service that allows users to upload PDF documents, extract text from them, and query the content using OpenAI's GPT-4 model. The results can also be posted to a Slack channel.

## Features

- **REST API**: Upload a PDF document via a POST request through REST API.
- **Text Extraction**: Extract text from the uploaded PDF.
- **Question Answering**: Query the extracted text using GPT-4 to get answers.
- **Slack Integration**: Optionally post the Q&A results to a Slack channel.

## Project Structure

├── config.py
├── main.py
├── pdf_extractor.py
├── query_llm.py
├── requirements.txt
├── slack_client.py
├── Dockerfile
├── .env
└── log/
└── service_logs.log


- `config.py`: Handles configuration, loading environment variables, and setting up logging.
- `main.py`: The main FastAPI application file.
- `pdf_extractor.py`: Contains the function for extracting text from PDFs.
- `query_llm.py`: Handles interactions with OpenAI's GPT-4 model.
- `slack_client.py`: Contains the function for posting messages to Slack.
- `requirements.txt`: Lists the Python dependencies for the project.
- `Dockerfile`: Contains the instructions to build a Docker image for the application.
- `log/service_logs.log`: The log file directory and file.

## Installation

### Prerequisites

- Docker
- Docker Compose (optional)

### Docker Setup

1. **Build the Docker Image**:
    ```sh
    docker build -t fastapi-pdf-qa .
    ```

2. **Run the Docker Container**:
    ```sh
    docker run -d -p 8000:8000 --name fastapi-pdf-qa-container fastapi-pdf-qa
    ```

    Alternatively, you can use Docker Compose:
    ```sh
    docker-compose up -d
    ```

### Local Development Setup

If you prefer to run the application locally without Docker, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/amanjaiswal777/fastapi-pdf-qa/tree/main
    cd fastapi-pdf-qa
    ```

2. **Set up environment variables**:
    Create a `.env` file in the project root with the following content:
    ```
    OPENAI_API_KEY=your_openai_api_key
    SLACK_BOT_TOKEN=your_slack_bot_token
    SLACK_CHANNEL=your_slack_channel
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the FastAPI application**:
    ```sh
    uvicorn main:app --reload
    ```

## API Usage

### Upload PDF and get answers

- **Endpoint**: `POST /upload_pdf/`
- **Parameters**:
    - `file`: PDF file to upload.
    - `questions`: List of questions to query the PDF content.
    - `post_to_slack_flag` (optional): Boolean flag to indicate if results should be posted to Slack.

    **Example**:
    ```sh
    curl -X POST "http://localhost:8000/upload_pdf/" -F "file=@path_to_your_file.pdf" -F "questions=['What is the main topic?']" -F "post_to_slack_flag=true"
    ```

## Logging

Logs are saved to the `log/service_logs.log` file with the format `Filename - Function name - Date and time - Log level - Message`.

## License

This project is licensed under the MIT License. See the [LICENSE](https://opensource.org/license/mit) file for more details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI](https://www.openai.com/)
- [Slack SDK](https://slack.dev/python-slack-sdk/)
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)

---

# ANSWER TO THE QUESTIONS IN THE DOC

# Solution Accuracy Enhancements (List all the ways you can make the solution more accurate)

You can employ various techniques and technologies to enhance the accuracy and efficiency of the provided solution. Here's a detailed list of improvements and how they can be implemented:

## Vector Database or Graph Database

#### Vector Database
#### Graph Database (This can also be utilized)

## Query Analysis Techniques

#### Natural Language Processing (NLP)
#### Query Expansion

## Ingestion Optimization

#### Data Preprocessing
#### Metadata Enrichment

## Retrieval Optimization

#### Pre-Retrieval Optimization
#### Hybrid Search
#### Context Enrichment

## LLM Generation Optimization

#### Post-Retrieval Processing
#### Reranking Mechanism
#### Confidence Score
#### Response Generation (Finetune LLM for client-based structural output.)

## Enhance RAG (Retrieval-Augmented Generation) Functionality

#### Contextual Retrieval
#### Model Ensembles

## Scalability and Performance

#### Caching
#### Load Balancing

# Code Modularity, Scalability, and Production-Grade Improvements

To make the code more modular, scalable, and production-grade, consider the following:

## Modular

### Function-Based Approach
- Refactor the code to follow a more functional programming approach. Break down the monolithic code into smaller, reusable functions.
- Use dependency injection to manage dependencies and improve testability.

### Microservices Architecture
- Split the application into microservices, each responsible for a specific functionality (e.g., PDF extraction, query processing, Slack notifications).
- Use RESTful APIs with message queues for communication between services.

### Error Handling and Logging
- Implement consistent error handling and logging across all modules.
- Use a centralized logging service like ELK stack (Elasticsearch, Logstash, Kibana) for log aggregation and analysis.

## Scalable and Production-Grade (Devops Side Optimization)

### Infrastructure

#### Use Case 1 (1k-3k requests at an interval of 5 min)
- Deploy the system on CPU-based instances to minimize costs.
- Use auto-scaling groups to handle variable loads.

#### Use Case 2 (5k+ requests at an interval of 5 min with lower latency)
- Deploy on a mix of CPU and GPU-based instances to handle intensive processing tasks.
- Use load balancers to distribute traffic evenly across instances.
- Implement request queuing systems to manage high request volumes efficiently.

### Database Optimization
- If vectorDB approach is needed we can leverage the Opensearch or Milvus DB.
- If graphDB is required then we can leverage the Neo4J graphDB.

### Caching
- Use caching mechanisms like Redis or Memcached to store frequently accessed data and reduce load on the database.

### Containerization and Orchestration
- Containerize the application using Docker to ensure consistent environments across development, testing, and production and deploy in one of the orchestration platform.



Feel free to reach out if you have any questions or need further assistance!
