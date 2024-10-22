import requests
from bs4 import BeautifulSoup
from scidownl.scihub import *
import pandas as pd


def download_scihubdownl(DOIs):
    out = 'paper'
    for doi in DOIs:
        try:
            SciHub(doi, out).download(choose_scihub_url_index=1)
        except:
            print("An exception occurred at DOI "+doi)
            rejected_dois.append(doi)

def download_scrap(DOIs):
    # URL from which pdfs to be downloaded
    url = DOIs

    # Requests URL and get response object
    response = requests.get(url)

    # Parse text obtained
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all hyperlinks present on webpage
    links = soup.find_all('a')

    i = 0

    # From all links check for pdf link and
    # if present download file
    for link in links:
        if ('.pdf' in link.get('href', [])):
            i += 1
            print("Downloading file: ", i)

            # Get response object for link
            response = requests.get(link.get('href'))

            # Write content in pdf file
            pdf = open("pdf" + str(i) + ".pdf", 'wb')
            pdf.write(response.content)
            pdf.close()
            print("File ", i, " downloaded")

    print("All PDF files downloaded")


if __name__ == '__main__':
    rejected_dois = []
    df = pd.read_csv('DOI.csv')
    df.rename(columns={df.columns[1]: "DOI"}, inplace=True)
    DOIs = df['DOI'].tolist()

    #for doi in DOIs:
    #    doi = "http://"+doi
    #    download_scrap(doi)

    download_scihubdownl(DOIs)
    rejected = pd.DataFrame(rejected_dois)
    rejected.to_csv('rejected_dois.csv')


