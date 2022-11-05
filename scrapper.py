
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def flatten(xss: list) -> list:
    return [x for xs in xss for x in xs]


def get_linktree(meshcodeui: str) -> list:
    tree_numbers = None
    parsed_id = None
    parser = ET.XMLParser(encoding="utf-8")

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
    except:
        print("get_linktree error, response1 failed. Skipping...")
        parsed_id = None
        return None

    if parsed_id is not None:

        try:
            response2 = requests.get(
                f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=mesh&id={parsed_id}")

            lines = response2.text.splitlines()

            finished = False
            while not finished:
                if len(lines) == 0:
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
                        elif "error" in line:
                            finished = True
                            break
                        elif "backend-exception" in line:
                            finished = True
                            break
                        else:
                            pass
        except:
            print("get_linktree error, response2 failed. Skipping...")
            pass

    return tree_numbers


def get_pmids(searchterm: str, max_results: int) -> list:
    response = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
                            '?tool=Masterthesis'
                            '&email=mail@breitfeld.net'
                            '&term=' + searchterm +
                            '&RetMax=' + str(max_results) +
                            '&mindate=2018' +
                            '&maxdate=2023')
    soup = BeautifulSoup(response.text, features='xml')
    soup_ids = soup.find_all('Id')
    souped_pmids = [pmid.text for pmid in soup_ids]
    return souped_pmids


def get_article(pmid: str) -> object:
    response = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&rettype=abstract&id=' + str(pmid))
    return response


def chunks(lst: list, n: int) -> list:
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# Testing
if __name__ == '__main__':
    for element in get_linktree("D001843"):
        print(element)
