import cv2
import time
from flask import Flask, render_template, Response

app = Flask(__name__)

# Load the face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialize webcam
video_cap = cv2.VideoCapture(0)

# Function to capture frames and detect faces
def detect_faces():
    while True:
        ret, frame = video_cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Encode the frame in JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            break
        frame = jpeg.tobytes()

        # Yield the frame as a multipart response (for MJPEG streaming)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Home route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Video feed route for streaming
@app.route('/video_feed')
def video_feed():
    return Response(detect_faces(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
