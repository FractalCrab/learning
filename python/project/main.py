from PyPDF2 import PdfReader
from pathlib import Path
from pprint import pprint

# reader = PdfReader("")

path = Path("/Users/abhi/Desktop/job/learning/python/test_data")

reader = None 

for file in path.iterdir():
    if file.suffix==".pdf":
        reader = PdfReader(str(file))


page = reader.pages[0]
text : = page.extract_text(0)

pprint(text)