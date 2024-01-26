from helpers import backends, detector, models, df_metrics, delete_representations, get_id, live_capture, visulaize_frame
import cv2
from cv2 import VideoCapture
from deepface import DeepFace
import os



def register_face(id, image_path=None, live = False):
    result = {"success": False, "message": "", "id": id, "image_path": ""}

    # check for duplicate id
    if id + '.jpg' in os.listdir(os.getcwd() + '/img_db/'):
        print("id already exists")
        result["message"] = "id already exists"
        check = input("Enter new id or enter 'x' to quit: ").lower()
        if check == 'x':
            print("exiting command...")
            result["message"] = "exiting command..."
            return result
        else:
            id = check
            
    if live:
        # take in image from cam
        cap = VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            face = detector(frame)
            if face:
                # crop and save image
                x, y , w, h = face[0]['facial_area'].values()
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)
                crop_img = frame[y:y+h, x:x+w]

                # Display the image with the detected face
                cv2.imshow('detect face', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    result["message"] = "quit detected. No face detected in the provided image"
                    break
                    
                if cv2.waitKey(1) & 0xFF == ord('c'):
                    # Save face
                    face_path = os.path.join(os.getcwd() + '/img_db/', id + '.jpg')
                    # face_path = "/img_db/"+id+".jpg"
                    cv2.imwrite(face_path, crop_img)
                    print(f" id {id} registered successfully")
                    print(f"image stored in {face_path}")

                    delete_representations()
                    result["success"] = True
                    result["message"] = f"id {id} registered successfully"
                    result["image_path"] = face_path
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
                    result["message"] = "quit detected. No face detected in the provided image"
                    break
                
        cv2.destroyAllWindows()
        cap.release()
        return result
                    

    # Load the image
    else:
        # check image_path is not None
        if image_path is None:
            result["message"] = "image_path is None"
            print(result["message"])
            return result
        
        frame = cv2.imread(image_path)

        # perform face detection
        face = detector(frame)
        if face:
            # crop and save image
            x, y , w, h = face[0]['facial_area'].values()
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)
            crop_img = frame[y:y+h, x:x+w]

            # Display the image with the detected face
            cv2.imshow('detect face', frame)
            # cv2.waitKey(0)

            # Save face
            face_path = os.path.join(os.getcwd() + '/img_db/', id + '.jpg')
            # face_path = "/img_db/"+id+".jpg"
            cv2.imwrite(face_path, crop_img)
            print(f" id {id} registered successfully")
            print(f"image stored in {face_path}")

            delete_representations()
            result["success"] = True
            result["message"] = f"id {id} registered successfully"
            result["image_path"] = face_path
            return result
        
        else:
            result["message"] = "No face detected in the provided image"
            print(result["message"])
            cv2.destroyAllWindows()
            return result


# detect face using static image
# take in the path to the image database
# image_path comes from live_capture function or
# local path to image
def face_detect(image_path, db_path):
    dfs = []
    try:
        df = DeepFace.find(img_path=image_path, db_path=db_path, model_name=models[2], 
                            distance_metric=df_metrics[2], enforce_detection=False)
                        #    detector_backend=backends[0])
        dfs.append(df)
    except Exception as e:
        print(f"Error in reading image: {e}")
    


    if dfs:
        try:
            user_id = get_id(dfs)
        except Exception as e:
            print(f"Error in get_id: {e}")
    else:
        user_id = None

    return user_id   


'''
use case of register_face function
you can either upload an image or take in live image from camera

register_face(id, image_path='path\to\image')
or
by setting live=True to use webcam
register_face(id, live=True)
'''