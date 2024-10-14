# backend/users/services.py

from openai import OpenAI
import os
from django.conf import settings


def perform_ai_grading(submitted_code, instructor_solution, grading_parameters=None):
    """
    Grades the submitted code using OpenAI's GPT-4.

    Parameters:
        submitted_code (str): The code submitted by the student.
        instructor_solution (str): The expected solution provided by the instructor.
        grading_parameters (dict, optional): Additional parameters for grading.

    Returns:
        tuple: (score (float), feedback (str))
    """
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    if not client:
        raise ValueError("OpenAI API key not set. Please set the OPENAI_API_KEY environment variable.")

    prompt = f"""
    You are an academic grading assistant.

    Grading Parameters:
    {grading_parameters}

    Instructor's Solution:
    ```
    {instructor_solution}
    ```

    Student's Submission:
    ```
    {submitted_code}
    ```

    Grading Criteria:
    {grading_parameters if grading_parameters else "Evaluate the submission based on correctness, efficiency, and code quality. Provide a score out of 100 and detailed feedback."}

    Provide the result in the following format:

    Score: <score>/100
    Feedback: <detailed feedback>
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are an academic grading assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3,  # Lower temperature for more deterministic output
            top_p=1,
            n=1,
            stop=None
        )
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return None, "AI grading failed due to an internal error."

    ai_output = response.choices[0].text.strip()

    # Parse the AI response
    score, feedback = parse_ai_response(ai_output)

    return score, feedback


def parse_ai_response(ai_output):
    """
    Parses the AI response to extract the score and feedback.

    Expected AI Response Format:
    Score: <score>/100
    Feedback: <feedback text>
    """
    try:
        lines = ai_output.split('\n')
        score_line = next((line for line in lines if 'score' in line.lower()), None)
        feedback_line = next((line for line in lines if 'feedback' in line.lower()), None)

        # Extract score
        if score_line:
            score_str = score_line.split(':')[1].split('/')[0].strip()
            score = float(score_str) if score_str else 0.0
        else:
            score = 0.0

        # Extract feedback
        if feedback_line:
            feedback = feedback_line.split(':', 1)[1].strip()
        else:
            feedback = ai_output  # Fallback to full AI output if feedback line is missing

    except Exception as e:
        print(f"Error parsing AI response: {e}")
        score = 0.0
        feedback = "Unable to parse AI feedback."

    return score, feedback
