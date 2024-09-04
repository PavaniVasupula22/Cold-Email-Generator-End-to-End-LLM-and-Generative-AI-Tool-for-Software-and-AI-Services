import re

def clean_text(text):
    # Strip HTML tags from the text
    text = re.sub(r'<[^>]+>', '', text)
    
    # Eliminate URLs
    text = re.sub(r'http[s]?://\S+', '', text)
    
    # Remove any non-alphanumeric characters, excluding spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Replace sequences of multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Trim leading and trailing spaces and ensure single spaces between words
    text = text.strip()
    
    return text
