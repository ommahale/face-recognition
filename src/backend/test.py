from deepface import DeepFace

# Path to the input image
input_image = 'D:/code/DL/src/backend/input.jpg'

# Path to the face database
db_path = 'D:/code/DL/src/backend/db'

# Perform face recognition
result = DeepFace.find(input_image, db_path=db_path)

# Access the identity of the recognized face
if result:
    identity = result[0]['identity'][0].split('\\')[-2]
    print("Identity:", identity)
else:
    print("No face found in the input image.")