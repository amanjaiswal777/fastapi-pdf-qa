import os
import json
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from pydantic import BaseModel
from pdf_extractor import extract_text_from_pdf
from query_llm import get_answer_from_gpt
from slack_client import post_to_slack
from typing import List, Optional

# Configure logging
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'service_logs.log'),
    level=logging.INFO,
    format='%(filename)s - %(funcName)s - %(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

class QuestionRequest(BaseModel):
    questions: List[str]

@app.post("/upload_pdf/")
async def upload_pdf(
    file: UploadFile = File(...),
    questions: List[str] = Form(...),
    post_to_slack_flag: Optional[bool] = Form(False)
):
    """
    Endpoint to upload a PDF file and process it to answer questions.

    Args:
        file (UploadFile): The uploaded PDF file.
        questions (List[str]): List of questions to answer based on the PDF content.
        post_to_slack_flag (Optional[bool]): Flag indicating whether to post results to Slack.

    Returns:
        dict: Dictionary containing the results of the questions and answers.
    """
    try:
        if not questions:
            raise HTTPException(status_code=400, detail="Questions are required")

        file_location = save_uploaded_file(file)
        text = extract_text_from_pdf(file_location)
        results = process_questions(text, questions)

        if post_to_slack_flag:
            post_to_slack_results(results)

        return {"results": results}

    except Exception as e:
        logger.error(f"Error in upload_pdf: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")

def save_uploaded_file(file: UploadFile) -> str:
    """
    Save the uploaded file to a temporary location.

    Args:
        file (UploadFile): The uploaded file.

    Returns:
        str: The file path of the saved file.
    """
    try:
        file_location = f"/tmp/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        logger.info(f"File saved to {file_location}")
        return file_location
    except Exception as e:
        logger.error(f"Error in save_uploaded_file: {e}")
        raise HTTPException(status_code=500, detail="Failed to save uploaded file")

def process_questions(text: str, questions: List[str]) -> dict:
    """
    Process the questions by querying the GPT model with the extracted text.

    Args:
        text (str): The extracted text from the PDF.
        questions (List[str]): List of questions to answer based on the text.

    Returns:
        dict: Dictionary containing the results of the questions and answers.
    """
    try:
        results = {}
        question_list = questions[0].strip().split(',')
        for question in question_list:
            if question:
                answer = get_answer_from_gpt(text, question)
                results[question] = answer
        logger.info(f"Processed questions: {results}")
        return results
    except Exception as e:
        logger.error(f"Error in process_questions: {e}")
        raise HTTPException(status_code=500, detail="Failed to process questions")

def post_to_slack_results(results: dict):
    """
    Post the results to Slack.

    Args:
        results (dict): Dictionary containing the results of the questions and answers.
    """
    try:
        json_results = json.dumps(results, indent=2)
        post_to_slack(f"Q&A Results:\n{json_results}")
        logger.info("Posted results to Slack")
    except Exception as e:
        logger.error(f"Error in post_to_slack_results: {e}")
        raise HTTPException(status_code=500, detail="Failed to post results to Slack")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
