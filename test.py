import requests

response = requests.get(
    f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=mesh&id=D008407")


print(response.text)
