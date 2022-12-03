import pandas as pd
import datetime
from scrapper import get_pmids, get_article, get_linktree, chunks
import xml.etree.ElementTree as ET
import time


totalstart = time.time()

# Define searchterm for scrapping
SEARCHTERM = '"Giant cell tumor of bone"[All Fields]'

# Query Pubmed API and create a list of lists in chunks of 100 elements each.
list_scrapped_pmids = get_pmids(SEARCHTERM, 2700, True)
list_of_lists_scrapped_pmids = chunks(list_scrapped_pmids, 5)
print(
    f"There were {len(list_scrapped_pmids)} PMIDs randomly picked to be scrapped.")

edges_dict = []

for idx, lst in enumerate(list_of_lists_scrapped_pmids):
    print(lst)
    roundstart = time.time()
    now = datetime.datetime.now()
    print(now.time())
    try:
        response = get_article(lst)
    except:
        print("get_article error. Skipping...")
        break
    root = ET.fromstring(response.content)

    for article in root.findall('PubmedArticle'):
        pmid = article.find("MedlineCitation//PMID").text
        title = article.find("MedlineCitation//ArticleTitle").text

        meshcodes = [code.text for code in article.findall(
            'MedlineCitation//DescriptorName')]

        meshcodesui = [code.attrib['UI'] for code in article.findall(
            'MedlineCitation//DescriptorName')]

        for (meshcode, meshcodeui) in zip(meshcodes, meshcodesui):
            link_tree = get_linktree(meshcodeui)
            if link_tree is None:
                pass
            else:
                for link in link_tree:
                    target = ""
                    for element in link.split("."):
                        if target != link:
                            target += element
                            if target == link:
                                edges_dict.append(
                                    {'source': link, 'target': target, 'pmid': pmid})
                            elif target != link:
                                edges_dict.append(
                                    {'source':
                                     link, 'target': target, 'pmid': pmid})
                                target += "."

    roundend = time.time()
    roundtime = roundend - roundstart
    print(f"Run {idx} took {roundtime.__round__(1)} seconds ")


dfedges = pd.DataFrame(edges_dict)
dfedges.to_csv('~/Desktop/pubmed-scrapper/gephi/GctbEdges.csv',
               sep=';', index=False)

totalend = time.time()
total = totalend - totalstart
print(f"Script took {total.__round__(1)} seconds in total")
