from selenium import webdriver
import sqlite3

driver = webdriver.Firefox()
conn = sqlite3.connect('project.db', isolation_level=None)
cursor = conn.execute("SELECT EMAIL,PASSWORD from USER")

for row in cursor:
    driver.get("https://app.openmailbox.org/login")
    driver.find_element_by_xpath("//button[@data-go='register']").click()
    driver.find_element_by_id("register_id").send_keys(row[0])
    driver.find_element_by_id("register_pw").send_keys(row[1])
    driver.find_element_by_id("register_vpw").send_keys(row[1])
    driver.find_element_by_id("register_id").click()
    driver.find_element_by_id("logout").click()
    
conn.close()

