"""
Flask server for hosting Claude 4 model locally.

This server provides an API endpoint to interact with Claude 4 Opus model.
It accepts POST requests with messages and returns model responses.
"""

import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from utils.models import claude4_opus, model_response

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for local network access
CORS(app, origins="*")

# Configuration
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 5000       # Default Flask port
DEBUG = True      # Enable debug mode for development

@app.route('/')
def home():
    """Home endpoint to verify server is running."""
    return jsonify({
        'status': 'active',
        'service': 'Claude 4 Model Server',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            '/': 'Server status',
            '/chat': 'Send message to Claude 4 (POST)',
            '/health': 'Health check'
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint to interact with Claude 4 model.

    Expects JSON payload:
    {
        "message": "Your message here",
        "max_tokens": 8192 (optional),
        "model": "claude4" (optional, defaults to claude4)
    }

    Returns:
    {
        "response": "Model response",
        "model": "claude4",
        "timestamp": "2024-01-20T10:30:00",
        "status": "success"
    }
    """
    try:
        # Get request data
        data = request.get_json()

        # Validate required fields
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing required field: message',
                'status': 'error'
            }), 400

        message = data['message']
        max_tokens = data.get('max_tokens', 8192)
        model_name = data.get('model', 'claude4')

        # Log the request (optional)
        app.logger.info(f"Received request - Model: {model_name}, Message length: {len(message)}")

        # Get response from Claude 4
        try:
            response = model_response(
                prompt=message,
                model_name=model_name,
                max_tokens=max_tokens
            )
        except KeyError:
            return jsonify({
                'error': f'Invalid model name: {model_name}. Available models: claude4, claude35, claude37',
                'status': 'error'
            }), 400

        # Return successful response
        return jsonify({
            'response': response,
            'model': model_name,
            'timestamp': datetime.now().isoformat(),
            'status': 'success',
            'message_length': len(message),
            'response_length': len(response)
        })

    except Exception as e:
        # Handle any errors
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/chat', methods=['GET'])
def chat_info():
    """GET endpoint to provide information about the chat API."""
    return jsonify({
        'endpoint': '/chat',
        'method': 'POST',
        'description': 'Send a message to Claude 4 model',
        'request_format': {
            'message': 'string (required) - Your message to Claude',
            'max_tokens': 'integer (optional) - Maximum response tokens (default: 8192)',
            'model': 'string (optional) - Model to use: claude4, claude35, or claude37 (default: claude4)'
        },
        'response_format': {
            'response': 'string - Model response',
            'model': 'string - Model used',
            'timestamp': 'string - ISO format timestamp',
            'status': 'string - success or error',
            'message_length': 'integer - Length of input message',
            'response_length': 'integer - Length of response'
        },
        'example_request': {
            'message': 'What is the capital of France?',
            'max_tokens': 1000
        }
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error',
        'available_endpoints': ['/', '/chat', '/health']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500

if __name__ == '__main__':
    # Check if API key is set
    if not os.getenv("GENAI_GATEWAY_API_KEY"):
        print("WARNING: GENAI_GATEWAY_API_KEY environment variable is not set!")
        print("Please set it before running the server.")

    print(f"""
    ╔══════════════════════════════════════════╗
    ║      Claude 4 Flask Server Starting      ║
    ╚══════════════════════════════════════════╝

    Server Configuration:
    - Host: {HOST} (accessible from local network)
    - Port: {PORT}
    - Debug: {DEBUG}

    Available Endpoints:
    - GET  /         : Server status
    - GET  /health   : Health check
    - POST /chat     : Send message to Claude 4
    - GET  /chat     : Chat endpoint info

    Access from local network:
    - http://<your-local-ip>:{PORT}/chat

    To find your local IP:
    - macOS/Linux: ifconfig or ip addr
    - Windows: ipconfig

    Press CTRL+C to stop the server
    """)

    # Run the Flask app
    app.run(host=HOST, port=PORT, debug=DEBUG)