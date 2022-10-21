from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import sys

def get_to_philosophy(startingUrl):
    MAX_HOPS, TARGET, counter = 100, "Philosophy", 0
    response = requests.get(startingUrl)
    webpage = BeautifulSoup(response.content, 'html5lib')
    header = webpage.find(id='firstHeading').span.text # Header of the article
    while header != TARGET and counter < MAX_HOPS:
        content = webpage.find(
            id='mw-content-text').find(class_="mw-parser-output")
        nextUrl = None
        stack = []
        for paragraph in content.find_all("p", recursive=False):
            if nextUrl:
                break
            for element in paragraph.children:
                if isinstance(element, NavigableString):
                    [stack.append("(") for i in range(element.count("("))]
                    [stack.pop() for i in range(element.count(")"))]
                 
                if isinstance(element, Tag) and (element.name == "a" or ((element.name == "b" or element.name == "i") and element.find("a"))) and not stack:
                    if (element.name == "b" or element.name == "i"):
                        element = element.find("a")
                    nextWiki = element.get("href")
                    if "/wiki/" not in nextWiki:
                        continue
                    nextUrl = f'https://en.wikipedia.org{nextWiki}'
                    print(nextUrl)
                    break

        response = requests.get(nextUrl)
        webpage = BeautifulSoup(response.content, 'html5lib')
        header = webpage.find(id='firstHeading').span.text  
        counter += 1
    print(f"MAX_HOPS of {MAX_HOPS} reached") if counter == MAX_HOPS else print(str(counter) + " hops")

if __name__ == '__main__':
    startingUrl = sys.argv[1]
    get_to_philosophy(startingUrl)
