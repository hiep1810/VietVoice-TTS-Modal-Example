import requests

# Define the API endpoint
url = "http://127.0.0.1:8000/synthesize"

# Define the request payload
payload = {
    "text": "Xin chào, đây là một bài kiểm tra.",
    "gender": "female",
    "area": "northern",
    "emotion": "neutral",
    "group": "story"
}

# Send the POST request
response = requests.post(url, json=payload)

# Check the response status code
if response.status_code == 200:
    # Save the audio file
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("API test successful. Audio saved to output.wav")
else:
    print(f"API test failed with status code: {response.status_code}")
    print(response.text)
