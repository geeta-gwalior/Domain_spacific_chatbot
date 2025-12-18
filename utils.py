import pandas as pd
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from PIL import Image
import io

def clean_text(text: str) -> str:
    return text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")

def read_pdfs(files):
    text = ""
    for f in files:
        reader = PdfReader(f)
        for page in reader.pages:
            text += clean_text(page.extract_text() or "")
    return text

def read_csv_excel(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    return df.head(50).to_string()

def read_url(url):
    html = requests.get(url, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")
    return clean_text(soup.get_text(separator=" "))

def read_images(files):
    descriptions = []
    for f in files:
        img = Image.open(io.BytesIO(f.read()))
        descriptions.append(f"Image uploaded with size {img.size}")
    return "\n".join(descriptions)
