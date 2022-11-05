from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# load selenium safari webdriver
driver = webdriver.Chrome()
driver.get("https://meshb.nlm.nih.gov/treeView")

while driver.find_elements(By.XPATH, "//i[@onclick='openTree(this)' and(not(contains(@style,'none')))]"):
    driver.find_element(
        By.XPATH, "//i[@onclick='openTree(this)' and(not(contains(@style,'none')))]").click()
    time.sleep(0.5)
