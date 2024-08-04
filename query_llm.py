import openai
import logging
from config import OPENAI_API_KEY
import os

# Configure logging
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'service_logs.log'),
    level=logging.INFO,
    format='%(filename)s - %(funcName)s - %(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

openai.api_key = OPENAI_API_KEY

def get_answer_and_confidence(text: str, question: str) -> tuple[str, str]:
    """Get answer and qualitative confidence from GPT-4o-mini."""
    try:
        answer = generate_answer(text, question)
        confidence = evaluate_confidence(text, question, answer)
        
        if confidence == 'low' or not answer or is_answer_irrelevant(answer):
            return "Data Not Available", confidence
        
        return answer, confidence
    except Exception as e:
        logger.error(f"Error in get_answer_and_confidence: {e}")
        return "Error", "low"

def generate_answer(text: str, question: str) -> str:
    """Generate answer from GPT-4o-mini."""
    prompt = f"Answer the following question based on the provided document:\n\nDocument:\n{text}\n\nQuestion: {question}\nAnswer:"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0
        )
        answer = response.choices[0].message['content'].strip()
        logger.info(f"Generated answer: {answer}")
        return answer
    except Exception as e:
        logger.error(f"Error in generate_answer: {e}")
        return ""

def evaluate_confidence(text: str, question: str, answer: str) -> str:
    """Evaluate the confidence of the generated answer."""
    prompt = f"Based on the provided document and the answer given, evaluate the confidence of the answer. Reply with 'high' if confident or 'low' if not confident.\n\nDocument:\n{text}\n\nQuestion: {question}\nAnswer: {answer}\n\nConfidence (high/low):"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,
            temperature=0
        )
        confidence = response.choices[0].message['content'].strip().lower()
        logger.info(f"Evaluated confidence: {confidence}")
        return confidence
    except Exception as e:
        logger.error(f"Error in evaluate_confidence: {e}")
        return "low"

def is_answer_irrelevant(answer: str) -> bool:
    """Check if the answer is irrelevant or does not make sense in the context."""
    irrelevant_patterns = [
        "My name is", "Hello", "How can I assist you", "I don't know", "I'm not sure", "Based on the provided document", "Data Not Available"
    ]
    return any(pattern in answer for pattern in irrelevant_patterns)

def get_answer_from_gpt(text: str, question: str) -> str:
    """Get the answer from GPT-4o-mini and evaluate its confidence."""
    try:
        answer, confidence = get_answer_and_confidence(text, question)
        if confidence == 'low':
            return "Data Not Available"
        return answer
    except Exception as e:
        logger.error(f"Error in get_answer_from_gpt: {e}")
        return "Error"
