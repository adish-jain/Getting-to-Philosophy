from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import sys


def get_to_philosophy(startingUrl):
    """
    Param: startingUrl - a String value provided from the user representing the Url we start our journey to Philosophy from
    Return: None - prints out the number of hops it takes to get to Philosophy or a message mentioning MAX_HOPS was reached
    """
    MAX_HOPS, TARGET, counter = 100, "Philosophy", 0
    response = requests.get(startingUrl)
    webpage = BeautifulSoup(response.content, 'html5lib')
    # Header of the Wikipedia article
    header = webpage.find(id='firstHeading').span.text
    while header != TARGET and counter < MAX_HOPS:
        content = webpage.find(
            id='mw-content-text').find(class_="mw-parser-output")
        nextUrl = find_next_url(content)
        if not nextUrl:
            print("The Wikipedia article has no main text section to search from. Please try again with a different startingUrl.")
            return
        response = requests.get(nextUrl)
        webpage = BeautifulSoup(response.content, 'html5lib')
        header = webpage.find(id='firstHeading').span.text
        counter += 1
    print(f"MAX_HOPS of {MAX_HOPS} reached") if counter == MAX_HOPS else print(str(counter) + " hops")


def find_next_url(content):
    """
    Param: content - a BeautifulSoup4 object representing the main text of the Wikipedia article
    Return: String value - the first Wikipedia link found in the main text of the given Wikipedia article
    """
    # Use stack to keep track of parenthesization to exclude links within parentheses
    stack = []
    for paragraph in content.find_all("p", recursive=False):
        for element in paragraph.children:
            if isinstance(element, NavigableString):
                [stack.append("(") for i in range(element.count("("))]
                [stack.pop() for i in range(element.count(")"))]
            if is_valid_link(element) and not stack:
                if (element.name == "b" or element.name == "i"):
                    element = element.find("a")
                nextWiki = element.get("href")
                # We only want to consider this link as the nextUrl to go to if it is a link to another Wikipedia article
                if "/wiki/" not in nextWiki:
                    continue
                nextUrl = f'https://en.wikipedia.org{nextWiki}'
                print(nextUrl)
                return nextUrl


def is_valid_link(element):
    """
    Param: element - a BeautifulSoup4 element object 
    Return: Boolean value - True if the element is a bolded, italicized, or normal <a> Tag; False otherwise 
    """
    return isinstance(element, Tag) and (element.name == "a" or ((element.name == "b" or element.name == "i") and element.find("a")))


if __name__ == '__main__':
    startingUrl = sys.argv[1]
    get_to_philosophy(startingUrl)
