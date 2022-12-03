import random
import requests
import time
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def flatten(xss: list) -> list:
    return [x for xs in xss for x in xs]


def get_linktree(meshcodeui: str) -> list:
    tree_numbers = None
    parsed_id = None
    parser = ET.XMLParser(encoding="utf-8")

    for attempt in range(3):
        try:
            response1 = requests.get(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=mesh&term=" + meshcodeui)

            root = ET.fromstring(response1.content, parser=parser)
            find = root.findall(".//Id")
            for element in find:
                if element.text[:1] == "6":
                    parsed_id = element.text
                elif element.text[:1] == "2":
                    parsed_id = element.text
                else:
                    return None
            break
        except:
            print(f"get_linktree error, attempt {attempt+1}. Retry...")
            time.sleep(1)
    else:
        print(f"{meshcodeui} not found in MeSH database after 3 attempts. Skipping...")
        return None

    for attempt in range(3):
        try:
            response2 = requests.get(
                f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=mesh&id={parsed_id}")
            successfull = True
            break
        except:
            print(f"get_linktree error, attempt {attempt+1}. Retry...")
            time.sleep(1)
    else:
        print(f"{parsed_id} not found in MeSH database after 3 attempts. Skipping...")
        return None

    if successfull:
        lines = response2.text.splitlines()
        finished = False
        while not finished:
            if len(lines) <= 1:
                finished = True
            else:
                for line in lines:
                    if "Tree Number(s)" in line:
                        lst = line.split(":")
                        tree_numbers = flatten([num.split()
                                                for num in lst[1].split(",")])
                        finished = True
                        break
                    elif "line" == "":
                        finished = True
                        break
                    elif "ID+list+is+empty" in line:
                        finished = True
                        break
                    elif "error" in line:
                        finished = True
                        break
                    elif "backend-exception" in line:
                        finished = True
                        break
                    else:
                        pass
        return tree_numbers


def get_pmids(searchterm: str, max_results: int, randomize: bool) -> list:
    response = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
                            '?tool=Masterthesis'
                            '&email=mail@breitfeld.net'
                            '&term=' + searchterm +
                            '&RetMax=100000')
    soup = BeautifulSoup(response.text, features='xml')
    soup_ids = soup.find_all('Id')
    souped_pmids = [pmid.text for pmid in soup_ids]
    print(f"Found {len(souped_pmids)} articles for {searchterm}")
    if randomize:
        random.seed(42)
        return random.sample(souped_pmids, max_results)
    else:
        return souped_pmids


def get_article(pmid: str) -> object:
    response = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&rettype=abstract&id=' + str(pmid))
    return response


def chunks(lst: list, n: int) -> list:
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
