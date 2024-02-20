import requests


def get_job_market_analysis(prompt):
    openai_api_key = 'your_openai_api_key_here'
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "text-davinci-003",  # Or whichever model you prefer
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 1000,
        "n": 1,
        "stop": None,
    }

    response = requests.post(
        "https://api.openai.com/v1/completions", json=data, headers=headers)

    if response.status_code == 200:
        content = response.json()
        return content.get('choices', [{}])[0].get('text', '')
    else:
        return "Error: Unable to fetch data from OpenAI."
