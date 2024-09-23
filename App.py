from flask import Flask, render_template, request, jsonify, Response
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json
import os
import cv2
from fuzzywuzzy import process
import random

# Configuration Constants
TRAINING_DATA_DIR = 'training_data'
AI_RESPONSE_FILE = 'ai_response.json'
COMMON_MESSAGE_FILE = 'common_message.json'
MAX_SIMILARITY_THRESHOLD = 0.95
FUZZY_MATCH_THRESHOLD = 80

app = Flask(__name__)

# Initialize ChatBot
chatbot = ChatBot(
    'AI_History_Bot',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'maximum_similarity_threshold': MAX_SIMILARITY_THRESHOLD,
            'default_response': 'I am sorry, but I do not understand.'
        }
    ]
)

# Define paths
ai_response_path = os.path.join(TRAINING_DATA_DIR, AI_RESPONSE_FILE)
common_message_path = os.path.join(TRAINING_DATA_DIR, COMMON_MESSAGE_FILE)

# Check if files exist
if not os.path.exists(ai_response_path):
    print(f"File not found: {ai_response_path}")
    exit(1)

if not os.path.exists(common_message_path):
    print(f"File not found: {common_message_path}")
    exit(1)

# Load intents from JSON files
with open(ai_response_path, 'r') as aijson_file:
    ai_intents = json.load(aijson_file)

with open(common_message_path, 'r') as common_file:
    common_intents = json.load(common_file)

# Combine intents
all_intents = common_intents['intents'] + ai_intents['intents']


# Train the chatbot
def train_chatbot():
    trainer = ListTrainer(chatbot)
    for intent in all_intents:
        for pattern in intent['patterns']:
            trainer.train([pattern, intent['responses'][0]])


train_chatbot()


# Function to find the best matching answer using fuzzy matching
def find_best_match(question):
    all_patterns = [pattern for intent in all_intents for pattern in intent['patterns']]
    best_match, score = process.extractOne(question, all_patterns)
    print(f"Question: {question}, Best Match: {best_match}, Score: {score}")  # Debugging line

    if score > FUZZY_MATCH_THRESHOLD:
        for intent in all_intents:
            if best_match in intent['patterns']:
                index = intent['patterns'].index(best_match)
                print(f"Intent found: {intent}, Index: {index}")  # Debugging line

                # Return the response corresponding to the matched pattern
                if index < len(intent['responses']):
                    response = intent['responses'][index]
                else:
                    response = random.choice(intent['responses'])

                print(f"Response: {response}")  # Debugging line
                return response
    print("No suitable match found")  # Debugging line
    return "Sorry, I don't know the answer to that question."


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('message')
    response = find_best_match(user_input)
    return jsonify({'response': response})


# Function to generate video frames
def generate_frames():
    camera = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    print("ChatBot is ready to chat! (type 'exit' to stop)")
    app.run(debug=True)
