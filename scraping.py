import requests
from bs4 import BeautifulSoup

def get_webpage(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content,"html.parser")

    return soup

def get_name_and_image(url,soup,class_name="name",src_name="src"):
    name_sources = soup.find_all("p",class_=class_name)
    names = [s.text.replace("\n","") for s in name_sources]
    image_sources = soup.find_all("p",class_="thumb")
    image_urls = [s.find("img")[src_name].replace("../","") if s.find("img") is not None else "" for s in image_sources] #sourceに対してfindが効かなかったため

    # print(len(image_urls),len(names))
    return names,image_urls

def run(url):
    soup = get_webpage(url)
    names,image_urls = get_name_and_image(url,soup)
    print(names,image_urls)


if __name__ == "__main__":
    run("https://vtuber-post.com/database/")