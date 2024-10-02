from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, send, emit
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize Flask-SocketIO
socketio = SocketIO(app)

# Serve the main page
@app.route('/')
def index():
    return render_template('index.html')

# Handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('index'))

# Serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Handle real-time chat messages
@socketio.on('chat_message')
def handle_chat_message(msg):
    # Broadcast the message to all connected clients
    send(msg, broadcast=True)


# Handle video sync events (play, pause, seek)
@socketio.on('video_event')
def handle_video_event(data):
    emit('video_event', data, broadcast=True)

# Handle video URL change event
@socketio.on('url_change')
def handle_url_change(url):
    emit('url_change', url, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
