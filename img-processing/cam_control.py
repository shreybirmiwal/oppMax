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
from firebase_admin import credentials, storage, firestore
import keyboard

load_dotenv()
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'], 
)

cred = credentials.Certificate("oppmax2-b6131-firebase-adminsdk-f54eu-55e4f49b28.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'oppmax2-b6131.appspot.com'
})
db = firestore.client()


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
                        "detail": "low",
                    },
                },

            ]},
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    return response.model_dump_json(indent=2)


def uploadFirebase(image_path):
    bucket = storage.bucket()
    blob = bucket.blob(image_path)
    blob.upload_from_filename(image_path)
    blob.make_public()
    return blob.public_url


def saveInfo(data, img_url, timestamp):
    data = json.loads(data)


    activity = data["Activity"]
    healthScore = data["healthScore"]
    careerScore = data["careerScore"]
    socialScore = data["socialScore"]
    alternateActivity = data["alternateActivity"]

    data = {
        "activity": activity,
        "healthScore": healthScore,
        "careerScore": careerScore,
        "socialScore": socialScore,
        "alternateActivity": alternateActivity,
        "img_url": img_url,
        "timestamp": timestamp
    }

    db.collection("data").document(timestamp).set(data)




    
# every 60 seconds
# def main():
#     while True:
#         image_path = capture_image()
#         if image_path:

#             img_url = uploadFirebase(image_path)
        
#             response = ask_gpt(img_url)
            
#             print(response)
#             print("Image captured and processed.")

#         time.sleep(60)


#whenever user presses button
def main():
    while True:
        if keyboard.is_pressed('space'):  # Wait for the spacebar to be pressed
            image_path = capture_image()
            if image_path:
                img_url = uploadFirebase(image_path) #upload firebase
                response = ask_gpt(img_url) #ask gpt
                
                # save to firebase
                response = json.loads(response)
                data = (response["choices"][0]["message"]["content"])
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                saveInfo(data, img_url, timestamp)


                print("Image captured and processed.")
            time.sleep(1) 



if __name__ == "__main__":
    main()