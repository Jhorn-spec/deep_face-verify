import numpy as np
import os 

def get_image_id(image):
        pass

# If image database pre-exists
# run this function, 
# else... comment it out 
def store_embedding(IMG_PATH):
    data_embed = {}
    for dirs in os.listdir(IMG_PATH):
        if dirs not in data_embed.keys():
            data_embed[dirs] = []
        for obj in os.listdir(os.path.join(IMG_PATH, dirs)):
            path = os.path.join(IMG_PATH, dirs, obj)
            if path.endswith(".jpg"):
                try:
                    embed_arr = get_embedding(path)
                    data_embed[dirs].append(embed_arr)
                except ValueError:
                    print("Face detection error in dir {}".format(dirs))
                    

    return data_embed


def cosine_similarity(a, b):
    dot_product = np.dot(a,b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    similarity = dot_product / (norm_a * norm_b)

    return similarity

# Load the dictionary from the file using
# embed_dict = np.load('embed_dict.npz', allow_pickle=True)
def process_image_id(image_file, embed_dict):
    best_match = {'match':0.25}
    ID = None

    # get embedding from img_file
    img_embed_arr = get_embedding(image_file)

    for id, embeddings in embed_dict.items():
        if embeddings:
            for embedding in embeddings:
                similarity_check = cosine_similarity(img_embed_arr, embedding)
                if similarity_check < best_match['match']:
                    best_match[id] = id
                    best_match['embedding'] = embedding
                    best_match['match'] = similarity_check
                    ID = id
                    print("Match found")

    if ID is not None:
        return ID
    else:
        return "User not in database"
    # plot the user embedding