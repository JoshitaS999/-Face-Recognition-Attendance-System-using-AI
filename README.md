#Face Recognition Attendance System-

A web-based attendance management application built with Python, Flask, OpenCV, and machine learning. It detects faces through a webcam, identifies registered students using a K-Nearest Neighbors (KNN) classifier, and records attendance with the student's name, roll number, and time.
Features
- Face detection: Uses the Haar Cascade frontal-face detector from OpenCV.
- Student registration: Captures face images from a webcam and saves them for model training.
- Face recognition: Trains a KNN classifier on registered face images.
- Automatic attendance: Marks a recognized student's attendance in a daily CSV file.
- Duplicate prevention: Avoids recording the same roll number more than once per day.
- Admin login: Uses a SQLite database and Werkzeug password hashing for administrator authentication.
- Admin dashboard: Displays attendance records and registered students.
- Student management: Supports retraining the recognition model and deleting registered student image folders.
- CSV attendance file: Stores daily attendance records.
Technology Stack
Technology	Purpose
Python	Main programming language
Flask	Web application and routes
OpenCV	Webcam access and face detection
Haar Cascade	Frontal-face detection
NumPy	Image-array processing
scikit-learn	K-Nearest Neighbors classifier
pandas	Reading and writing attendance data
joblib	Saving and loading the trained model
SQLite	Administrator credential storage
HTML/CSS	Web pages and dashboard


Project Structure
Face-Recognition-Attendance/
│
├── app.py
├── init_admin.py
├── requirements.txt
├── admin.db
├── haarcascade_frontalface_default.xml
│
├── Attendance/
│   └── Attendance-MM_DD_YY.csv
│
├── static/
│   ├── faces/
│   │   └── StudentName_RollNumber/
│   │       ├── StudentName_0.jpg
│   │       └── ...
│   └── face_recognition_model.pkl
│
└── templates/
    ├── index.html
    ├── login.html
    └── admin.html
Attendance/, static/, and static/faces/ are created by the application when needed. The HTML templates must be present in the templates/ folder. The trained model is generated after student face images have been registered.
Requirements
- Python 3.9 or later
- A working webcam for live registration and attendance
- Windows, macOS, or Linux
- The project files listed above, including the HTML templates
Installation and Setup
1. Clone or download the project
Open a terminal in the project directory.
2. Create a virtual environment
Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1
macOS/Linux:
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
For local webcam use, install the regular OpenCV package so that OpenCV's camera-window functions are available:
pip uninstall -y opencv-python-headless
pip install flask opencv-python numpy pandas scikit-learn joblib
The supplied requirements.txt lists opencv-python-headless. That package is intended for headless environments and may not support the cv2.imshow() windows used by the live webcam registration and attendance routes. Use opencv-python for the local desktop webcam workflow.
4. Initialize the administrator account
Run:
python init_admin.py
The initialization script creates the SQLite admin table if it does not exist and inserts the default administrator only if that username is not already present.

Default initial login:
- Username: admin
- Password: admin123
Change the default password and replace the hard-coded Flask secret key before using the application beyond local testing. Do not publish your database or credentials.
5. Run the application
python app.py
Open the application in your browser:

http://127.0.0.1:1000

Allow camera access/use when prompted by your operating system. The webcam is accessed by the Python application running on the computer, not by the browser page.
How to Use
1. Administrator login
1. Open the application.
2. Navigate to the login page.
3. Enter the administrator credentials.
4. After successful login, open the admin dashboard.
2. Register a student
1. Log in as administrator.
2. Open the student registration form.
3. Enter the student's name and roll number.
4. Submit the form and face the webcam.
5. The application captures face images and saves them under static/faces/StudentName_RollNumber/.
6. The KNN model is trained again and saved as static/face_recognition_model.pkl.
3. Mark attendance
1. Log in as administrator.
2. Start the attendance process from the dashboard.
3. The webcam opens and the application detects faces.
4. A detected face is passed to the trained KNN model for identification.
5. The student's attendance is added to that day's CSV file.
6. Press ESC in the OpenCV camera window to stop the process.
4. View and download attendance
The home page and administrator dashboard display the attendance records for the current date. Daily CSV files are stored in the Attendance/ directory.

The CSV format is:
Name,Roll,Time
StudentName,101,09:15:20
5. Manage registered students
The admin dashboard includes options to view registered students, retrain the face recognition model, and delete a student's stored face-image folder.
How Face Recognition Works
1. Image capture: The webcam captures frames of the student.
2. Face detection: Haar Cascade detects face regions in each frame.
3. Preprocessing: Detected face images are resized to 50 × 50 pixels.
4. Feature preparation: The resized image pixels are flattened into a one-dimensional array.
5. Model training: A KNN classifier is trained using the saved face images and their student labels.
6. Prediction: A newly detected face is passed to the trained model, which predicts a registered student label.
7. Attendance recording: The predicted student's name, roll number, and current time are written to the daily CSV file if that roll number has not already been recorded that day.
Important Notes and Limitations
- The application uses a basic KNN model trained on flattened pixel values. Recognition accuracy can vary with lighting, camera quality, face angle, and image conditions.
- The application does not include liveness detection, so it should not be treated as a secure identity-verification system.
- The live registration and attendance routes require a webcam connected to the machine running Flask.
- The project expects the HTML files index.html, login.html, and admin.html inside templates/. They were not included with the Python, requirements, and configuration files supplied for this README.
- The /upload route accepts an image upload, but the supplied code does not show authentication protection for that route.
- The current code uses a placeholder Flask secret key and enables Flask debug mode. These settings are suitable only for local development, not production.
- Face images and attendance records are personal data. Obtain appropriate consent, restrict access, and store them securely.
Troubleshooting
Problem	What to check
Webcam does not open	Check camera connection and permissions; close other apps using the camera.
cv2.imshow() or GUI error	Replace opencv-python-headless with opencv-python for local desktop use.
Model file not found	Register at least one student and ensure model training completes.
Template not found	Confirm the required HTML files are inside the templates/ directory.
Admin login fails	Run python init_admin.py and check that admin.db is in the project directory.
No attendance appears	Confirm a student is registered, the model exists, and the face is visible to the camera.


Future Enhancements
- Improve recognition using face embeddings and a modern face-recognition model.
- Add liveness detection.
- Add attendance reports by date, student, and class.
- Add export options and improved dashboard analytics.
- Add stronger input validation, authorization checks, CSRF protection, and secure configuration.
- Add tests and deployment-specific camera/upload workflows.
