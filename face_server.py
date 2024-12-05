import os
import json
import cv2
from time import sleep as wait
import time
try:
    from deepface import DeepFace
    import mediapipe as mp
except:
    os.system("pip install mediapipe deepface opencv-python-headless tensorflow")
    from deepface import DeepFace
    import mediapipe as mp

# Directory to store registered face images
FACE_DIR = "faces"
QUEUE_DIR = "faceserver_workspaces/queue/"
RESULT_DIR = "faceserver_workspaces/result/"

# Ensure directories exist
for directory in [FACE_DIR, QUEUE_DIR, RESULT_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Initialize Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

def preprocess_frame(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply Contrast Limited Adaptive Histogram Equalization (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized = clahe.apply(gray)
    return equalized

def detect_and_crop_face(frame):
    """Detect and crop a face from the frame, applying histogram equalization."""
    # Preprocess the frame for better lighting normalization
    preprocessed_frame = preprocess_frame(frame)  # Preprocessed frame is used for display or enhancement

    # Mediapipe detection works on the original frame
    with mp_face_detection.FaceDetection(min_detection_confidence=0.7) as face_detection:
        results = face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Use original frame here
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape  # Get dimensions from the original frame
                x, y, w, h = (
                    int(bboxC.xmin * iw),
                    int(bboxC.ymin * ih),
                    int(bboxC.width * iw),
                    int(bboxC.height * ih),
                )
                cropped_face = frame[y:y + h, x:x + w]  # Crop the original frame

                # Apply histogram equalization to the cropped face
                cropped_face_equalized = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2YCrCb)
                channels = list(cv2.split(cropped_face_equalized))
                channels[0] = cv2.equalizeHist(channels[0])  # Equalize the Y channel
                cropped_face_equalized = cv2.merge(channels)
                cropped_face_equalized = cv2.cvtColor(cropped_face_equalized, cv2.COLOR_YCrCb2BGR)

                return cropped_face_equalized  # Return the equalized cropped face
    return None  # Return None if no face is detected

def check_face(image_path):
    """
    Process a face image and check for a match in the faces directory.

    Returns:
        dict: A dictionary with 'error' and 'result' keys.
    """
    print(f"Checking face in {image_path}...")
    cap = cv2.VideoCapture(image_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        face = detect_and_crop_face(frame)
        if face is not None:
            matches = []
            for file_name in os.listdir(FACE_DIR):
                file_path = os.path.join(FACE_DIR, file_name)
                if os.path.isfile(file_path):
                    try:
                        result = DeepFace.verify(
                            face, file_path, enforce_detection=False
                        )
                        distance = result.get("distance", 1)  # Default to 1 if no distance is returned
                        similarity_threshold = 0.34
                        if result["verified"] and distance <= similarity_threshold:
                            matches.append(file_name.split(".")[0])  # File name without extension
                    except Exception as e:
                        print(f"Error verifying {file_name}: {e}")
            
            
            cap.release()
            cv2.destroyAllWindows()

            # Return results
            if matches:
                return {"error": False, "result": matches[0]}
            else:
                return {"error": False, "result": None}

        print("No face detected. Please adjust your position.")
        wait(1)  # Add slight delay before retrying

    cap.release()
    cv2.destroyAllWindows()
    return {"error": True, "result": None}

if __name__ == "__main__":
    print("Face server is running...")
    time_on_hold = int(time.time())
    while True:
        # Check for files in the queue directory
        current_files = os.listdir(QUEUE_DIR)
        if current_files:
            time_on_hold = int(time.time())
            for file_name in current_files:
                file_path = os.path.join(QUEUE_DIR, file_name)

                # Process the file
                result_json = check_face(file_path)
                print(f"Processed {file_name}: {result_json}")

                # Remove the processed file
                os.remove(file_path)

                # Save the result to a JSON file without the file extension in the name
                result_file_name = os.path.splitext(file_name)[0] + ".json"
                result_file_path = os.path.join(RESULT_DIR, result_file_name)
                with open(result_file_path, "w") as result_file:
                    json.dump(result_json, result_file)

        if int(time.time()) - time_on_hold > 10:
            # If there is no new facial recoginition request for more than 10s
            old_result_files = os.listdir(os.getcwd()+"/faceserver_workspaces/result/")
            for file in old_result_files:
                os.remove(os.getcwd()+"/faceserver_workspaces/result/"+file)
            time_on_hold = int(time.time())
            print(f"Refreshed result directory, which has {len(old_result_files)} temporary result files.")

        # print(int(time.time()) - time_on_hold)

        # Add a delay before checking the directory again
        wait(1)