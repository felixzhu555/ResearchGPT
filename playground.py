from bs4 import BeautifulSoup
import os
from pypdf import PdfReader

def html_to_string(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    return text

for filename in os.listdir("/Users/felix_3gpdyfd/ai hackathon/data")[:5]:
    fname = "/Users/felix_3gpdyfd/ai hackathon/data/" + filename
    reader = PdfReader(fname)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    print(text)
    # opens the file for reading
    # with open(fname, 'rb') as f:
    #     txt = f.read()
    #     print(chardet.detect(txt)["encoding"])
    #     # b''.join(txt).decode("utf-8")