"""
Flask Messaging API Documentation

This Flask application provides endpoints to manage and retrieve messages.

Usage:
    1. Run the Flask application using the command: python <filename>.py
    2. Access the provided endpoints to interact with the messaging API.

Endpoints:
    1. GET /messages:
        - Retrieves the messages history as JSON.

    2. POST /send:
        - Sends a message. The message should be provided as a form parameter named 'message'.

Example Usage:
    1. Retrieve messages history:
        - GET /messages

    2. Send a message:
        - POST /send
        - Parameters:
            - message: The message content.

Attributes:
    app (Flask): The Flask application instance.

Functions:
    read_messages(): Reads messages from the file.
"""

from flask import Flask, jsonify, request
import json

app = Flask(__name__)

def read_messages():
    """
    Read messages from the file.

    Returns:
        dict: Dictionary containing messages.
    """
    try:
        with open("./messages/messages.txt", 'r') as file:
            data = json.load(file)
        print("Data read successfully from messages.txt")
        return data
    except FileNotFoundError:
        print("File not found at messages.txt")
        return {}
    except Exception as e:
        print("Error reading data from file:", e)
        return {}

messages_history = read_messages()

@app.route('/messages', methods=['GET'])
def get_messages():
    """
    Retrieve messages history.

    Returns:
        JSON: JSON response containing messages history.
    """
    if messages_history:
        return jsonify(messages_history)
    else:
        return jsonify({"error": "No messages history available"})

@app.route('/send', methods=['POST'])
def send_message():
    """
    Send a message.

    Returns:
        JSON: JSON response indicating the status of the request.
    """
    try:
        message = request.form.get('message')
        if message:
            # Process the message (e.g., save to file, send to other peers)
            print("Message received:", message)
            return jsonify({"status": "ok"})
        else:
            return jsonify({"error": "No message provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
