from selenium import webdriver
from selenium.webdriver.support.ui import Select


firstname = "Frotka"
lastname = "Kazimierczka"
email = "kzimierczak@asdafswrd121.ru"
password = "kazimierczak12333"
month = "12"
day = "10"
year = "1990"
gender = "2"
username = firstname + lastname + gender +year  + month + day 
username = username[:30]
driver = webdriver.Firefox()


driver.get("http://www.google.com")
#open loging
driver.find_element_by_id("gb_70").click()
#open registration
driver.find_elements_by_class_name("CwaK9")[3].click()
#firstname
driver.find_element_by_id("firstName").send_keys(firstname)
#lastname
driver.find_element_by_id("lastName").send_keys(lastname)
#username (email
driver.find_element_by_id("username").send_keys(username)
#password
driver.find_element_by_name("Passwd").send_keys(password)
#password
driver.find_element_by_name("ConfirmPasswd").send_keys(password)
#dalej
driver.find_element_by_class_name("CwaK9").click()

"""
driver.get("http://www.facebook.com")
assert "Facebook" in driver.title

driver.find_element_by_name("firstname").send_keys(firstname)
driver.find_element_by_name("lastname").send_keys(lastname)
driver.find_element_by_name("reg_email__").send_keys(email)
driver.find_element_by_name("reg_email_confirmation__").send_keys(email)
driver.find_element_by_name("reg_passwd__").send_keys(pwd)
Select(driver.find_element_by_name("birthday_month")).select_by_value(month)
Select(driver.find_element_by_name("birthday_day")).select_by_value(day)
Select(driver.find_element_by_name("birthday_year")).select_by_value(year)
elem = driver.find_elements_by_name("sex")
if gender == 1:
    elem[0].click()
else:
    elem[1].click()
    
driver.find_element_by_name("websubmit").click();

    """
    
