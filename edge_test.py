from selenium import webdriver
from selenium.webdriver.edge.service import Service

service = Service("msedgedriver.exe")

driver = webdriver.Edge(service=service)

driver.get("https://www.google.com")

print(driver.title)

driver.quit()