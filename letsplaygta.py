import requests
import pyautogui
import base64
import time
import subprocess


# Function to take a screenshot
def take_screenshot():
    # Take a screenshot of the entire screen
    screenshot = pyautogui.screenshot()
    # Save the screenshot to a temporary file
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)
    return screenshot_path


# Function to encode the image as base64
def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read())
    return encoded_string.decode("utf-8")


# Function to send the image to the API
def send_to_api(image_data):
    api_url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llava",
        "prompt": """
        you are the character in the center of the screen
        you are palaying gta
        you need to do what every you can to decide
        first describe the scene
        then describe what you are going to do
        keep your response short and simple
        since you need to act fast!
        """,
        "stream": False,
        "images": [image_data],
    }
    response = requests.post(api_url, json=payload)
    # convert repsonse to json
    return response.json()["response"]


# Function to speak the API results
def speak_results(text):
    print(text)
    subprocess.run(["say", text])


# Main loop
while True:
    try:
        # wait for 5 seconds
        time.sleep(2)
        # say 'taking screenshot'
        speak_results("Taking screenshot")
        # Take a screenshot
        screenshot_path = take_screenshot()
        # Encode the image as base64
        encoded_image = encode_image(screenshot_path)
        # Send the image to the API
        api_response = send_to_api(encoded_image)
        # Speak the API results
        speak_results(api_response)
        # Wait for some time before taking the next screenshot
    except Exception as e:
        print("Error:", e)
