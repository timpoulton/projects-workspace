import requests  # For API calls to Gemini
import json  # For handling JSON data
import os  # For file paths, if needed

gemini_api_url = 'http://localhost:5002'  # Adjust if needed based on your setup

def generate_proposal(job_data):
    try:
        job_title = job_data.get('title', 'Untitled Job')
        job_description = job_data.get('description', '')
        budget = job_data.get('budget', 'Not specified')
        # Assuming a simple analysis for standalone mode
        analysis = {'pain_points': ['manual processes']}  # Minimal analysis; expand if needed
        prompt = f"""You are Timothy Poulton, a 20-year automation specialist and solo freelancer. Your goal is to write a short, highly believable, and personable Upwork proposal that feels like a real, thoughtful response—not a template or marketing pitch.\n\nJob Title: {job_title}\nBudget: {budget}\nDescription: {job_description[:500]}\n\nKey Pain Points Detected: {', '.join(analysis.get('pain_points', ['manual processes']))}\n\nWrite a proposal (100-150 words) that:\n1. Opens with a personal reference to the client's specific pain point or project detail (quote or paraphrase from their description).\n2. Shares a brief, real anecdote or insight from your experience (no generic numbers or claims, no made-up stats).\n3. Outlines a 2-3 step approach tailored to their situation (use their language, not generic automation talk).\n4. Closes with a natural, friendly invitation to connect (no hard sell, no 'perfect fit' language).\n\nUse "I" statements, sound like a real person, and make it clear you read their job post. Avoid anything that sounds like a template or sales pitch. Do not use generic claims like 'Having automated 200+ businesses' or 'Last month, I helped a similar client...'\n\nReturn only the proposal text, nothing else."""
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(gemini_api_url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            generated_text = result['candidates'][0]['content']['parts'][0]['text'].strip()
            proposal_url = 'http://localhost:5056/proposals/sample_proposal.html'  # Placeholder; update as needed
            return f"{generated_text} See full proposal at: {proposal_url}"
        else:
            return 'Error generating proposal.'
    except Exception as e:
        return f'Error: {str(e)}'

# Example usage
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        job_data = json.loads(sys.argv[1])  # Expect JSON string from scraper
        result = generate_proposal(job_data)
        print(result)  # Output the response text 