import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def classify_opportunity(text):
    candidate_labels = ["Artificial Intelligence", "Law", "Biomedical", "Engineering", "Business"]
    
    payload = {
        "inputs": text,
        "parameters": {"candidate_labels": candidate_labels}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        
        # Return the label with the highest score
        if "labels" in result:
            return result["labels"][0]
        return "Uncategorized"
    except Exception as e:
        print(f"AI Error: {e}")
        return "Uncategorized"