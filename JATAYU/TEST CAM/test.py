import os

file_path = "D:\PROJECT\JATAYU\shape_predictor_68_face_landmarks.dat.bz2"
if os.path.exists(file_path):
    print("Model file found!")
else:
    print("Error: Model file not found! Check the path.")
