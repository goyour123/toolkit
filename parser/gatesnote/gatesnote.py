import requests
import json
from bs4 import BeautifulSoup

url = "https://www.gatesnotes.com/api/TGNWebAPI/GetArticleSetByTopic?tags=reading%20list&books=true&articles=true"
hdr = {
  "Host":            "www.gatesnotes.com",
  "User-Agent":      "Mozilla/5.0",
  "Accept":          "application/json",
  "Accept-Encoding": "gzip, deflate, br",
  "Connection":      "keep-alive"
}

def main():
  res = requests.get(url, headers=hdr)
  articleDict = json.loads(res.json())
  for d in articleDict["ArticleList"]:
    print (d["Headline"])
    print (d["Date"])
    print (d["ArticleUrl"])

if __name__ == "__main__":
  main()
