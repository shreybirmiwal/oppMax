# Gen steps
#1. take pic every min
#2. process with LLM
    # extract: 1. activity description, 2. time, 3. health and self score, 4. career score, 5. social score, 6. alternate oppurtunity cost that was most benefit
#3. save to firebase database


  
import cv2
import time
from datetime import datetime
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import firebase_admin
from firebase_admin import credentials, storage

load_dotenv()
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'], 
)

cred = credentials.Certificate("oppmax-3247f-firebase-adminsdk-gqreh-e5638523f4.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'oppmax-3247f.appspot.com'
})


def capture_image():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return None

    ret, frame = cap.read()

    if ret:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"img/image_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}")
        cap.release()
        return filename
    else:
        print("Error: Could not read frame.")
        cap.release()
        return None



def ask_gpt(img_url):
    
    expected_format = {
        "Activity": "The Activity the user is doing in first person POV in 2-3 words",
        "healthScore": "A score (-10,10) representing how the activity affects the user's health",
        "careerScore": "A score (-10,10) representing how the activity affects the user's career",
        "socialScore": "A score (-10,10) representing how the activity affects the user's social life",
        "alternateActivity": "Alternative activity to optimize opportunity cost"
    }
    prompt = (
        f"This image is from the first person POV "
        "Please return: The Activity the user is doing in 2-3 words, "
        "A score from (-10,10) regarding the activity and the users' a) Health, b) career c) social. "
        "Lastly, include an alternative activity the user can do to maximize the time to optimize opportunity cost. "
        f"Return the response in JSON format. Expected format below: \n {json.dumps(expected_format, indent=2)}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},

                {
                "type": "image_url",
                    "image_url": {
                        "url": img_url,
                    },
                },

            ]},
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    return response


def uploadFirebase(image_path):
    bucket = storage.bucket()
    blob = bucket.blob(image_path)
    blob.upload_from_filename(image_path)
    blob.make_public()
    return blob.public_url

    

def main():
    while True:
        image_path = capture_image()
        if image_path:

            img_url = uploadFirebase(image_path)
        
            response = ask_gpt(img_url)
            
            print(response)
            print("Image captured and processed.")

        time.sleep(60)


if __name__ == "__main__":
    main()