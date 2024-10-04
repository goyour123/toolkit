from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

def main():
  firefox_options = Options()
  service = Service()
  driver = webdriver.Firefox(service=service, options=firefox_options)

  try:
    driver.get("https://www.github.com/")
  finally:
    driver.quit()

if __name__ == "__main__":
  main()