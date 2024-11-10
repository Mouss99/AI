from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Define the route to upload video
@app.route('/upload-video', methods=['POST'])
def upload_video():
    
    # Input check
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
  
    # Check if the file is not empty
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Check file extension
    allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        return jsonify({"error": "Invalid file type, only video files are allowed"}), 400
    
    
    # Process the video file
    try:
        # Prepare the file for sending to another API
        video_file = file.stream.read()

        # Send the video file to another API (replace with your actual API URL)
        url = 'https://5866487b-1df3-4955-91c2-9c442416188f.mock.pstmn.io'  # Use a local endpoint for testing
        files = {'file': (file.filename, video_file, file.content_type)}

        # Send the file to the external API
        response = requests.post(url, files=files)

        # Check if the response from the external API is successful
        if response.status_code == 200:
            return jsonify({"message": "Video uploaded successfully!"}), 200
        else:
            return jsonify({"error": f"External API error: {response.text}"}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# 404 error for undefined routes
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(port=3000)

