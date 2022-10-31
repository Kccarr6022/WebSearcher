"""
"""
from re import search
import sys, argparse
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from urllib.parse import urlparse
# to install Beautiful Soup: File-->Settings-->Project Interpretter and "add package"

# version number TODO: Load version library
# functions for dispatch table
version= 3.04

site = ""
query = ""


def search_google(searchterms):
    """_summary_

    Args:
        searchterms (str): Search terms for the query

    Returns:
        str: returns the build query string
    """
    searchterms = "+".join(searchterms.split())
    url = f"https://www.google.com/search?q={searchterms}"
    soup = BeautifulSoup(get_response(url), 'html.parser')

    for link in soup.findAll("a", href=True):
        if link.h3:
            follow = urlparse(link['href'][7:]).hostname
            if follow:
                return f"https://{follow}"
    return ""

def search_amazon(searchterms):
    """ Function to search amazon with BS4

    Args:
        searchterms (str): Terms used for the search

    Returns:
        str: The built query string
    """
    searchterms = "+".join(searchterms.split())
    url = f"https://www.amazon.com/s?k={searchterms}"

    soup = BeautifulSoup(get_response(url), 'html.parser')
    for link in soup.find_all("p"):
        print(link.text)
        return link.text
    return ""

def search_wiki(searchterms):
    """ Function to search wikipedia with BS4

    Args:
        searchterms (str): Terms used for the search

    Returns:
        str: The built query string
    """
    
    searchterms = "_".join(searchterms.split())
    
    url = f"https://en.wikipedia.org/wiki/{searchterms}_(disambiguation)"

    soup = BeautifulSoup(get_response(url), 'html.parser')
    for link in soup.find_all("li"):
        print(link.text)
        return link.text

def search_books(searchterms):
    """ Function to search books with BS4

    Args:
        searchterms (str): Terms used for the search

    Returns:
        str: The built query string
    """
    searchterms = "+".join(searchterms.split())
    url = f"https://www.gutenberg.org/ebooks/search/?query={searchterms}&submit_search=Search"

    soup = BeautifulSoup(get_response(url), 'html.parser')
    for link in soup.find_all("p"):
        print (link.text)
        return link.text

sites = {
    "google": search_google,
    "amazon": search_amazon,
    "wikipedia": search_wiki,
    "wiki": search_wiki,
    "gutenberg": search_books,
    "books": search_books
}

def init() -> str:
    sysargs = argparse.ArgumentParser(description="Loads passed url to file after initial cleaning (munging)")
    sysargs.add_argument("-v", "--version", action="version", version=f"current version is {version}")
    sysargs.add_argument("-s", "--site", help="This site to search (google, wikipedia, gutenberg, amazon)")
    sysargs.add_argument("-q", "--query", help="the term(s) to search for.")
    args = sysargs.parse_args()
    
    global site
    global query
    site = str(args.site).lower()

    
    for sitename in sites:
        if sitename.startswith(site):
            site = sitename

    try:
        if args.query:
            query = args.query
            return sites.get(site)(query)
        else:
            print("You must provide both the site (-s, --site) and query string ('-q, --q) to use this program.")
            quit(1)
    except (KeyError, TypeError) as ex:
        print(ex)
        print("acceptable sites to search for are: google, wikipedia(wiki), amazon, gutenberg(books)")
        quit(1)


def get_response(uri):

    try:
        response = requests.get(uri)
        response.raise_for_status()
    except HTTPError as httperr:
        print(f"HTTP error: {httperr}")
        sys.exit(1)
    except Exception as err:
        print(f"Something went really wrong!: {err}")
        sys.exit(1)
    
    return response.text

def main():

    url = init()

    if get_response(url):
        with open(f"{site}_{query}.txt", "w", encoding="utf-8") as f:
            f.write(get_response(url))
        print(get_response(url))
    else:
        print("First link was unfollowable or no links found")

if __name__ == '__main__':
    main()