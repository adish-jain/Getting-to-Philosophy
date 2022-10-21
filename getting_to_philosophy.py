from bs4 import BeautifulSoup
import requests
import sys
import re

# the issue right now is that when we remove the parantheses we remove the ability to make it a beautifulsoup again which makes it hard to access the first link
# but accessing the first link without removing the parentheses results in the wrong first link
# ideal state: remove parentheses without breaking the html so that you can still access the first link by making it a beautifulsoup again
def get_to_philosophy(startingUrl):
    MAX_HOPS, TARGET, counter = 100, "Philosophy", 0
    response = requests.get(startingUrl)
    webpage = BeautifulSoup(response.content, 'html5lib')
    header = webpage.find(id='firstHeading').span.text 
    while header != TARGET and counter < MAX_HOPS:
        content = webpage.find(
            id='mw-content-text').find(class_="mw-parser-output")
        firstParagraph = None

        for paragraph in content.find_all("p", recursive=False):
            paragraphText = remove_text_between_parens(str(paragraph))
            # paragraph = BeautifulSoup(paragraphText, 'html5lib')
            print(paragraphText)
            # print(type(paragraph))
            # alink = paragraph.find("a", recursive=False)
            # print(alink)
            print("")
            if "href" in paragraphText:
                firstParagraph = paragraphText
                break
        # paragraphText = str(paragraph)
        # print(firstParagraph)
        match = re.search(r'href=[\'"]?([^\'" >]+)', firstParagraph)
        print(match)
        nextWiki = match.group(1)
        nextUrl = f'https://en.wikipedia.org{nextWiki}'
        print(nextUrl)
        response = requests.get(nextUrl)
        webpage = BeautifulSoup(response.content, 'html5lib')
        header = webpage.find(id='firstHeading').span.text  # Header of the article
        counter += 1

# def find_next_link(startingUrl):


def remove_text_between_parens(text):
    n = 1  # run at least once
    while n:
        # remove non-nested/flat balanced parts
        text, n = re.subn(r'\([^()]*\)', '', text)
    return text


if __name__ == '__main__':
    startingUrl = sys.argv[1]
    get_to_philosophy(startingUrl)
