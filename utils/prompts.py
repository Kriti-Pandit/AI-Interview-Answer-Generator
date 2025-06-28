"""
Pre-defined prompts for interview answer generation
Formatted for Gemini API with resume + job description context
"""

BASIC_PROMPT = """
Generate a concise interview answer (3-5 sentences) using the following:

**Resume:**  
{resume_text}

**Job Description:**  
{job_description}

**Question:**  
{question}

Guidelines:
- Focus on matching 2-3 key skills from resume to job requirements
- Use STAR method (Situation-Task-Action-Result) for behavioral questions
- Keep tone professional but conversational
- Avoid generic phrases like "I'm a hard worker"
"""

QUESTION_SPECIFIC_PROMPTS = {
    "Tell me about yourself": """
    Create a 60-second elevator pitch covering:
    1. Current role/education (if fresher)
    2. 2 most relevant experiences from resume
    3. Why you're excited about this role
    
    Example structure:
    "I'm a [current role/student] with experience in [X, Y]. At [Company], I [achievement]. This role excites me because [alignment]."
    """,
    
    "Why should we hire you?": """
    Highlight:
    1. Top 3 skills matching the JD
    2. One quantifiable achievement
    3. How you'll solve their problems
    
    Template:
    "You should hire me because my [skill 1] and [skill 2] align with your need for [JD requirement]. At [Company], I [result]. I can help your team by [specific contribution]."
    """,
    
    "What's your greatest weakness?": """
    Use the 'improvement' framework:
    1. Name a real but non-critical weakness
    2. Show steps taken to improve
    3. Relate to growth mindset
    
    Example:
    "Early on, I struggled with [weakness]. However, I've taken [action] and now [positive outcome]. This shows my commitment to continuous improvement."
    """
}

def get_prompt(question, resume_text, job_description):
    """Returns the most appropriate prompt based on question type"""
    if question in QUESTION_SPECIFIC_PROMPTS:
        return QUESTION_SPECIFIC_PROMPTS[question] + f"\n\nResume:\n{resume_text}\n\nJD:\n{job_description}"
    return BASIC_PROMPT.format(
        resume_text=resume_text,
        job_description=job_description,
        question=question
    )