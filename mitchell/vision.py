import cv2
import os
import numpy as np

def train_recognizer(data_path):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces = []
    labels = []
    label_dict = {}
    label_id = 0

    for person_name in os.listdir(data_path):
        person_path = os.path.join(data_path, person_name)
        if not os.path.isdir(person_path):
            continue

        if person_name not in label_dict:
            label_dict[person_name] = label_id
            label_id += 1

        for image_name in os.listdir(person_path):
            image_path = os.path.join(person_path, image_name)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            faces.append(image)
            labels.append(label_dict[person_name])

    face_recognizer.train(faces, np.array(labels))
    return face_recognizer, label_dict

def recognize_face(image_path, recognizer, label_dict):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi = image[y:y+h, x:x+w]
        label_id, confidence = recognizer.predict(roi)
        for name, id in label_dict.items():
            if id == label_id:
                label = name
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(image, f'{label} ({confidence:.2f})', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    cv2.imshow("Recognized Faces", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Train the recognizer
data_path = 'path_to_training_data'
recognizer, label_dict = train_recognizer(data_path)

# Recognize faces in a new image
image_path = 'path_to_test_image.jpg'
recognize_face(image_path, recognizer, label_dict)
