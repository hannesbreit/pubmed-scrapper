import pandas as pd
from scrapper import get_pmids, get_article, get_linktree, chunks
import xml.etree.ElementTree as ET
import time


totalstart = time.time()

# Define searchterm for scrapping
SEARCHTERM = "\"Giant cell tumor of bone\""

# Query Pubmed API and create a list of lists in chunks of 100 elements each.
list_scrapped_pmids = get_pmids(SEARCHTERM, 10)
list_of_lists_scrapped_pmids = chunks(list_scrapped_pmids, 5)


edges_dict = []

for idx, lst in enumerate(list_of_lists_scrapped_pmids):
    roundstart = time.time()
    response = get_article(lst)
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
            for link in link_tree:
                target = ""
                for element in link.split("."):
                    if target != link:
                        target += element
                        if target == link:
                            edges_dict.append(
                                {'source': link, 'target': target, 'pmid': pmid, 'meshcode': meshcode})
                        elif target != link:
                            edges_dict.append(
                                {'source': link, 'target': target, 'pmid': pmid, 'meshcode': ""})
                            target += "."

    roundend = time.time()
    roundtime = roundend - roundstart
    print(f"Run {idx} took {roundtime.__round__(1)} seconds ")


dfedges = pd.DataFrame(edges_dict)
dfedges.to_csv('/workspaces/pubmed-scrapper/gephi/edges.csv',
               sep=';', index=False)

# dfnodes = pd.DataFrame(nodes_dict)
# dfnodes.drop_duplicates().to_csv('/workspaces/pubmed-scrapper/gephi/nodes.csv',
#                                  sep=';', index=False)


# with pd.option_context('display.max_rows', 2, 'display.max_columns', None):
#     print(dfedges)
#     print(dfnodes)

totalend = time.time()
total = totalend - totalstart
print(f"Script took {total.__round__(1)} seconds in total")
