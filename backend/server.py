# server.py for Python Flask Vulnerable Build (Insecure Error Handling)

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import sys
import traceback

app = Flask(__name__)


# In a real application, you would specify allowed origins for security.
CORS(app)

# --- THIS IS THE VULNERABLE ENDPOINT ---
@app.route('/api/error/trigger', methods=['POST'])
def trigger_error():
    print('--- RECEIVED REQUEST TO TRIGGER ERROR ---')
    data = request.get_json(silent=True)
    simulated_input = data.get('simulatedInput', 'null') if data else 'null'
    print(f'Input received from client: "{simulated_input}"')
    print('--- INTENTIONAL VULNERABILITY DEMO: Triggering Unhandled Exception for Insecure Error Handling ---')
    print('--- EXPECT TO SEE A DETAILED STACK TRACE IN BROWSER/CLIENT RESPONSE ---')

    # INTENTIONAL VULNERABILITY: Cause an unhandled exception
    result = 1 / 0 
    
    return jsonify({"message": "This should not be reached."}), 200


# --- VULNERABILITY: Simple Custom Error Handler to return consistent HTML/Text with stack trace ---
@app.errorhandler(500)
def handle_generic_500(e):
    error_trace = traceback.format_exc() 
    print(f"Internal Server Error (logged internally by handler, then exposed): {e}", file=sys.stderr)
    print("--- EXPOSING STACK TRACE TO CLIENT ---", file=sys.stderr)
    
    response_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>Internal Server Error: {e}<br>{error_trace}</pre>
</body>
</html>"""
    
    # Create the response. Flask-CORS, configured globally above, will now add the
    # Access-Control-Allow-Origin: * header automatically.
    response = Response(response_body, mimetype="text/html", status=500)
    
    return response


# Start the server and listen on the specified port
if __name__ == '__main__':
    print("Python Flask Unsecure Backend (Error Handling) listening on http://127.0.0.1:5002")
    print("Ready to demonstrate insecure error handling.")
    app.run(debug=True, port=5002) # debug=True for development, turn off in production!