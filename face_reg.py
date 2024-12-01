import os
try:
    import cv2
    from deepface import DeepFace
    import mediapipe as mp
except:
    os.system("pip install mediapipe deepface opencv-python-headless tensorflow tf-keras")
    import cv2
    from deepface import DeepFace
    import mediapipe as mp
    
# Directory to store registered face images
FACE_DIR = "faces"

# Ensure the faces directory exists
if not os.path.exists(FACE_DIR):
    os.makedirs(FACE_DIR)

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
    """Detect and crop the face area from the frame using Mediapipe."""
    processed_frame = preprocess_frame(frame)
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                cropped_face = frame[y:y+h, x:x+w]
                return cropped_face  # Return the cropped face
    return None  # Return None if no face is detected

def register_face():
    """Automatically capture a face image using the camera and save it to the faces directory."""
    cap = cv2.VideoCapture(0)
    print("Attempting to register a face...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to access the camera.")
            break

        # Detect and crop the face
        face = detect_and_crop_face(frame)
        if face is not None:
            # Automatically save the cropped face
            face_name = input("Enter a name for this face: ").strip()
            if face_name:
                file_path = os.path.join(FACE_DIR, f"{face_name}.jpg")
                cv2.imwrite(file_path, face)
                print(f"Face saved as {file_path}")
            else:
                print("Invalid name. Registration aborted.")
            break
        else:
            print("No face detected. Please adjust your position.")
            cv2.imshow("Register Face", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Registration canceled.")
                break

    cap.release()
    cv2.destroyAllWindows()

def check_face():
    """Automatically capture a face and check for a match in the faces directory."""
    cap = cv2.VideoCapture(0)
    print("Attempting to check the face...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to access the camera.")
            return {"error": True, "result": None}

        # Detect and crop the face
        face = detect_and_crop_face(frame)
        if face is not None:
            # Automatically check the face
            matches = []
            for file_name in os.listdir(FACE_DIR):
                file_path = os.path.join(FACE_DIR, file_name)
                if os.path.isfile(file_path):
                    try:
                        result = DeepFace.verify(face, file_path, enforce_detection=False)
                        if result["verified"]:
                            matches.append(file_name.split('.')[0])  # Use file name without extension
                    except Exception as e:
                        print(f"Error verifying {file_name}: {e}")
            
            cap.release()
            cv2.destroyAllWindows()

            # Return results
            if matches:
                return {"error": False, "result": matches[0]}  # Return the first match
            else:
                return {"error": False, "result": None}
        else:
            print("No face detected. Please adjust your position.")
            cv2.imshow("Check Face", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Check canceled.")
                break

    cap.release()
    cv2.destroyAllWindows()
    return {"error": True, "result": None}

def main():
    """Main function to switch between register and check modes."""
    print("Face Recognition System")
    print("1. Register a new face")
    print("2. Check face")
    print("q. Quit")
    
    while True:
        choice = input("Select an option: ").strip()
        if choice == '1':
            register_face()
        elif choice == '2':
            result = check_face()
            print("Result:", result)
        elif choice.lower() == 'q':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
