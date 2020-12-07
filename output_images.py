import requests
import os

def convert_url_to_image(url):
    try:
        response = requests.get(url)
        return response.content
    except:
        return None

def output(image,filename):
    with open(filename + ".png","wb") as f:
        f.write(image)

#database_dict -> {name:[image_url,image_path]}
def run(database_dict):
    if not os.path.exists("images"):
        os.makedirs("images")
        
    for name in database_dict:
        image = convert_url_to_image(database_dict[name][0])
        if image is not None:
            output(image,database_dict[name][1])

    