from pprint import pprint
from bs4 import BeautifulSoup
import requests
import json

def get_content(url):
    #file = open(filepath, encoding='utf-8')
    res = requests.get(url)
    #soup = BeautifulSoup(file.read(), "lxml")
    soup = BeautifulSoup(res.content, 'lxml')
    return soup

#def parse_content(content):
#    names = []
#    for program in content.find_all("div", {"class" : "modulo-type-programa"}):
#        names.append([name.get('content') for name in program.select('meta[itemprop="name"]')][0])
#    return names

def parse_content(content):
    podcasts = []
    for program in content.find_all("div", {"class" : "modulo-type-programa"}):
        podcasts.append({
            'title': [title.get('content') for title in program.select('meta[itemprop="name"]')][0],
            'description': [desc.get('content') for desc in program.select('meta[itemprop="description"]')][0],
            'url': [url.get('content') for url in program.select('meta[itemprop="url"]')][0],
            'episodes': [micro.getText() for micro in program.select('.microphone')][0]
        })
    
    return podcasts


def save_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, ensure_ascii=False)


# primer ejemplo
#def build_ranking(placeholder, page_max):
#    urls = [placeholder.format(page) for page in range(1, page_max+1)]
#    return urls

def build_ranking(placeholder, page_max):
    urls = [placeholder.format(page) for page in range(1, page_max+1)]
    podcasts = []
    for content in [get_content(url) for url in urls]:
        podcasts.append(parse_content(content))
    return podcasts


# pprint(build_ranking("https://www.ivoox.com/podcast-internet-tecnologia_sc_f445_{0}.html", 5))

podcasts = build_ranking("https://www.ivoox.com/podcast-internet-tecnologia_sc_f445_{0}.html", 5)
save_data('podcasts.json', podcasts)

#content = get_content("https://www.ivoox.com/podcast-internet-tecnologia_sc_f445_1.html")

#podcasts = parse_content(content)

#pprint(podcasts)
#save_data('podcasts.json', podcasts)