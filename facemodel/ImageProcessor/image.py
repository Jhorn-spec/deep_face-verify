def get_image_id(image):
        pass

def process_image_id(image):
        pass

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