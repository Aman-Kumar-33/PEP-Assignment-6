def calculate_incoscore(user_data):
    """
    Calculates score based on user attributes.
    Weights can be adjusted based on project requirements.
    """
    score = 0
    score += (user_data.research_papers * 50)
    score += (user_data.hackathons_count * 30)
    score += (user_data.internships_count * 20)
    
    # Optional: Bonus for having many interests
    if user_data.domain_interests:
        score += len(user_data.domain_interests) * 5
        
    return float(score)