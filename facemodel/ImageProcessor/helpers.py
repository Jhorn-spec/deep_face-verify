
import os
import cv2
from cv2 import VideoCapture
from deepface import DeepFace
import matplotlib.pyplot as plt
import uuid

backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe',
  'yolov8',
  'yunet',
  'fastmtcnn',
]

df_metrics = ["cosine", "euclidean", "euclidean_l2"]

models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
]

def live_capture():
    cap = VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret == False:
            break

        face = detector(frame)
        if face:
            x,y,w,h = face[0]['facial_area'].values()
            crop_img = frame[y:y+h, x:x+w]
            cv2.imshow('display', frame)

            if cv2.waitKey(1) & 0xFF == ord('c'):
                face_path = os.path.join(os.getcwd(), '.temp')
                if not os.path.exists(face_path):
                    os.makedirs(face_path)

                for obj in os.listdir(face_path):
                    try:
                        obj_path = os.path.join(face_path, obj)
                        os.remove(obj_path)
                    except Exception as e:
                        print(e)
                        pass
                temp_file = os.path.join(face_path, '{}.jpg'.format(uuid.uuid1()))
                cv2.imwrite(temp_file, crop_img)
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            # if no face detected
            h,w = frame.shape[:2]
            text = 'Adjust face and brightness'
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontsize = 1  
            color = (0,255,0)
            thickness = 2
            text_size, _ = cv2.getTextSize(text, font, fontsize, thickness)

            x = (w - text_size[0]) // 2  
            y = (h + text_size[1]) // 2
            cv2.putText(frame, text, (x, y), font, fontsize, color, thickness)
            # cv2.putText(frame, text, (10, h - 20), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0,), 1)
            # cv2.putText(crop_img, 'Align face', (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.imshow('display', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            

        
    cap.release()
    cv2.destroyAllWindows()
    return temp_file


def check_duplicate(id):
    pass
    # if id+'.jpg' in os.listdir(os.getcwd() + '/img_db/'):
    #     return True
    # else:
    #     return False
    

def visulaize_frame(frame):
    # Convert BGR to RGB (OpenCV uses BGR by default)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the image using Matplotlib
    plt.imshow(image_rgb)
    plt.axis('off')  # Turn off axis labels
    plt.show()


def get_id(list_list_df):
    df = list_list_df[0][0]
    df['identity'] = df['identity'].apply(lambda x: x.split("/")[-1])
    name = df.iloc[0][0]
    return name


def delete_representations():
    for obj in os.listdir(os.getcwd() + '/img_db'):
        if obj.endswith('.pkl'):
            path = os.path.join(os.getcwd() + '/img_db/', obj)
            os.remove(path)
            print('previous representations deleted')
    return


def detector(frame, enforce=True):
    try:
        return DeepFace.extract_faces(frame, detector_backend=backends[0], enforce_detection=enforce)
    except Exception as e:
        # print(f"Image detection failed with error: {e}")
        return None
    

def detection(frame):
    try:
        dfs = DeepFace.find(img_path=frame, db_path="../images/img_db/", 
                            model_name="Facenet512", distance_metric="euclidean_l2")
        print('face found')
        return dfs
    except ValueError:
        print('face cannot be detected')
        return None




    
