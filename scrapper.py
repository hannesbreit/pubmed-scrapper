'''Scrapper Module'''
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def flatten(xss):
    """_summary_

    Args:
        xss (_type_): _description_

    Returns:
        _type_: _description_
    """
    return [x for xs in xss for x in xs]


def get_linktree(meshcodeui):
    """_summary_

    Args:
        meshcodeui (_type_): _description_

    Returns:
        _type_: _description_
    """
    tree_numbers = None

    response1 = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=mesh&term=" + meshcodeui)
    root = ET.fromstring(response1.content)
    find = root.findall(".//Id")
    for element in find:
        if element.text[:1] == "6":
            id = element.text
        elif element.text[:1] == "2":
            id = element.text
        else:
            pass

    response2 = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=mesh&id=" + str(id))
    lines = response2.text.splitlines()

    finished = False
    while not finished:
        for line in lines:
            if "Tree Number(s)" in line:
                lst = line.split(":")
                tree_numbers = flatten([num.split() for num in lst[1].split(",")])
                finished = True
                break

            
    return tree_numbers


def get_pmids(searchterm: str, max_results: int) -> list:
    """Queries Pubmed API for PMIDs

    Args:
        searchterm (string): enter a searchterm (string) which should be used for finding relevant PMIDs
        max_results (int): set the maximum size of results

    Returns:
        list: returns a list of found PMIDs
    """ 
    response = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
                            '?tool=Masterthesis'
                            '&email=mail@breitfeld.net'
                            '&term=' + searchterm +
                            '&RetMax=' + str(max_results))
    soup = BeautifulSoup(response.text, features='xml')
    soup_ids = soup.find_all('Id')
    souped_pmids = [pmid.text for pmid in soup_ids]
    return souped_pmids


def get_article(pmid: str):
    """Queries Pubmed efetch API

    Args:
        pmid (String): PMID of a Pubmed article formatted as string or integer.

    Returns:
        object: returns a response object from Requests library. Content is available through content or text method
        and should be XML formatted.
    """ 
    response = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&rettype=abstract&id=' + str(pmid))
    return response


def chunks(lst: list, n: int):
    """This function splits a lists to list of lists.

    Args:
        lst (list): List, which needs be chunked in multiple smaller lists.
        n (integer): Size of lists.

    Yields:
        list: returns a list of lists.
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# for element in get_linktree("D001843"):
#     print(element)
