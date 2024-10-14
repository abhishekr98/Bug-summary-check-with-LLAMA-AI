import requests
import re


def extract_location_fallback(title):
    # Simple rule-based extraction: find phrases like "near the X" or "at the Y"
    location_phrases = re.findall(r'\b(?:near|at|by|in|around|next to) [\w\s]+', title, re.IGNORECASE)
    if location_phrases:
        return ', '.join(location_phrases)
    return None


def classify_pal_components(title):
    url = "http://127.0.0.1:1234/v1/completions"  # Llama API

    # Simplified prompt with more direct instructions
    prompt = f"""
    Bug Title: "{title}"

    Classify the bug title into PAL format:

    Problem: 
    Action: 
    Location: 
    Is PAL format (True/False): 
    """

    payload = {
        "model": "llama-3.2-3b-instruct",  # Use your model identifier
        "prompt": prompt,
        "max_tokens": 100,
        "temperature": 0.0
    }

    try:
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            output = response.json()['choices'][0]['text'].strip()
            # Extract location from output
            if 'Location: ' in output:
                location = output.split("Location: ")[1].split("\n")[0].strip()
                # Fallback if location is missing
                if not location:
                    location = extract_location_fallback(title)
                    if location:
                        output = re.sub(r'Location:\s*', f'Location: {location}', output)
            return output
        else:
            print("Error in response:", response.status_code, response.text)
            return None
    except Exception as e:
        print("Error connecting to Llama API:", str(e))
        return None


def process_titles(titles):
    results = []
    for title in titles:
        output = classify_pal_components(title)
        results.append({
            'Title': title,
            'Classification': output.strip() if output else "Error in classification"
        })

    # Display results
    print("\nPAL Classification Results:")
    for result in results:
        print(f"Title: {result['Title']}")
        print(f"Classification:\n{result['Classification']}\n")


# Get custom titles from the user
user_titles = []
print("Enter bug titles (type 'done' when finished):")
while True:
    title = input("Title: ")
    if title.lower() == 'done':
        break
    user_titles.append(title)

# Process the custom titles
process_titles(user_titles)
