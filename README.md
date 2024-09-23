# Chatbot
This project is an AI-driven chatbot built using Flask and ChatterBot, designed to answer historical questions. The bot uses predefined patterns and responses stored in JSON files, combined with fuzzy string matching to ensure it can provide accurate answers even when user input is not exact.

Features
AI Chatbot: The bot is powered by the ChatterBot library, which allows it to respond to user queries based on training data.
Fuzzy Matching: The bot uses fuzzywuzzy to compare user input with stored patterns and find the closest match, ensuring relevant responses even when queries are slightly different from the expected input.
Customizable Training Data: The chatbot's knowledge is based on two JSON files (ai_response.json and common_message.json). These files contain predefined patterns and responses that can be easily expanded or customized to suit different use cases.
Flask Web Application: The chatbot is hosted through Flask, enabling it to be easily accessed via a web browser.


How It Works
ChatBot Training: The chatbot is trained using patterns and responses defined in the training_data folder. These JSON files provide the bot with the questions it can understand and the corresponding responses it should give.
Fuzzy Matching for Accuracy: The bot leverages fuzzy matching to compare the user's input with known patterns. If a close enough match is found, the bot provides a response; otherwise, it returns a default message.
User Interaction: Through the web interface, users can submit their questions. The chatbot then processes these inputs and replies with the best-matched response based on its training data.


File Structure
app.py: The main Flask application script that initializes and trains the chatbot.
training_data/: Folder containing the chatbot’s training data (ai_response.json and common_message.json).
templates/: Contains the HTML files for the web interface.
requirements.txt: List of dependencies required to run the chatbot.


Technologies Used
Flask: For building the web application.
ChatterBot: A Python library for building conversational agents.
FuzzyWuzzy: A library for performing fuzzy string matching to enhance response accuracy.



Future Improvements
Expand Training Data: Add more questions, patterns, and responses to make the chatbot more knowledgeable.
Improve NLP: Implement advanced natural language processing techniques for better understanding and responses.
User Feedback: Add functionality to allow users to provide feedback to improve response accuracy over time.(can you provide me a breaf discripton for my git)
