from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_match(resume_text, job_description):
    """
    Calculates similarity using Cosine Similarity on simple Count Vectors.
    resume_text includes the extracted kills, experience, etc.
    job_description includes title, desc, and required skills.
    
    Returns:
        score: float (percentage)
        matched_str: set/list of matched keywords (simplified)
        missing_str: set/list of missing keywords (simplified)
    """
    
    text_list = [resume_text, job_description]
    cv = CountVectorizer(stop_words='english')
    count_matrix = cv.fit_transform(text_list)
    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    
    # Simple keyword extraction for "Matched/Missing" display
    job_tokens = set(job_description.lower().split())
    resume_tokens = set(resume_text.lower().split())
    
    matched = job_tokens.intersection(resume_tokens)
    missing = job_tokens - resume_tokens
    
    # Filter only significant words (len > 3) for display
    matched = {w for w in matched if len(w) > 3}
    missing = {w for w in missing if len(w) > 3}

    return round(matchPercentage, 2), matched, missing
