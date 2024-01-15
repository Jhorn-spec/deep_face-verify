from helpers import backends, detector, models, df_metrics, delete_representations, get_id
import cv2
from cv2 import VideoCapture
from deepface import DeepFace



def register_face(id):
    # check for duplicate id
    if id + '.jpg' in os.listdir(os.getcwd() + '/img_db/'):
        print("id already exists")
        check = input("Enter new id or enter 'x' to quit: ").lower()
        if check == 'x':
            print("exiting command...")
            return
        else:
            id = check
            
    cap = VideoCapture(0)

    while True:
        ret, frame = cap.read()
        face = detector(frame)
        if face:
            # crop and save image
            x,y,w,h = face[0]['facial_area'].values()
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)
            crop_img = frame[y:y+h, x:x+w]
            cv2.imshow('detect face', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif cv2.waitKey(1) & 0xFF == ord('c'):
                # save face
                face_path = "/img_db/"+id+".jpg"
                cv2.imwrite(face_path, crop_img)
                print(f" id {id} registered successfully")
                print(f"image stored in {face_path}")
                delete_representations()
                
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
            cv2.imshow('detect face', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows() 



def face_detect():
    cap = cv2.VideoCapture(0)
    dfs = []
    
    while True:
        ret, frame = cap.read()

        if ret == False:
            break
        
        face = detector(frame)
        if face is not None:
            # face detection and recognition logic
            x,y,w,h = face[0]['facial_area'].values()  
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255, 0), 3)
            # cv2.imshow('detect face', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('c'):
                df = DeepFace.find(img_path=frame, db_path="./img_db/", model_name=models[2], 
                                   distance_metric=df_metrics[2], enforce_detection=False)
                                #    detector_backend=backends[0])
                dfs.append(df)
                break

        cv2.imshow('display', frame)
                
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

    user_id = get_id(dfs)
    
    return user_id