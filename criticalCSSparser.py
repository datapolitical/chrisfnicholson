from bs4 import BeautifulSoup

with open("gh-pages/index.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")
print(soup.head.style.text, end='')