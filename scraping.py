import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import json
import itertools
from collections import defaultdict
import output_images

# def get_webpage(url):
#     html = requests.get(url)
#     soup = BeautifulSoup(html.content,"html.parser")

#     return soup

def get_name_and_image(url,soup,class_name="name",src_name="src"):
    name_sources = soup.find_all("p",class_=class_name)
    names = [s.text.replace("\n","").replace("/","-") for s in name_sources]
    image_sources = soup.find_all("p",class_="thumb")
    image_urls = [s.find("img")[src_name].replace("../","") if s.find("img") is not None else "" for s in image_sources] #sourceに対してfindが効かなかったため
    # print(len(image_urls),len(names))
    return names,image_urls

# def run(url):
#     soup = get_webpage(url)
#     names,image_urls = get_name_and_image(url,soup)
#     print(names,image_urls)

#memoです
def run(url):
    driver = webdriver.Chrome(executable_path='/home/artela/Downloads/chromedriver')
    #初期ページを入れる
    driver.get(url)
    all_names = []
    all_image_urls = []
    i = 1
    try:
        while True:
            #ページのスクレイピング
            html = driver.page_source.encode("utf-8")
            soup = BeautifulSoup(html,"html.parser")
            names,image_urls = get_name_and_image(url,soup)
            all_names.append(names)
            all_image_urls.append(image_urls)
            print("end " + str(i))
            sleep(5)
            print(names,image_urls)
            #次のページへ
            driver.find_element_by_link_text(">").click()
            i += 1
    except:
        print('cant catch next page:')
        print("finish")
        driver.quit()


    all_names = list(itertools.chain.from_iterable(all_names))
    all_image_urls = list(itertools.chain.from_iterable(all_image_urls))
    all_path = ["images/" + name for name in all_names]
    print("name len:{} and image_url len:{}".format(len(all_names),len(all_image_urls)))
    #dict型にして出力
    # output_dict = dict(zip(all_names,all_image_urls))
    d = defaultdict(list)
    for i,name in enumerate(all_names):
        d[name].append(all_image_urls[i])
        d[name].append(all_path[i])

    output_images.run(d)

    with open("databases.txt","w",encoding="utf-8") as f:
        json.dump(d,f,indent=4,ensure_ascii=False)

if __name__ == "__main__":
    run("https://vtuber-post.com/database/")


