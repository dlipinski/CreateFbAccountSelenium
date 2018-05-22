from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import sqlite3
from selenium.webdriver.common.keys import Keys
from MySelenium import humanInput, MAILPASSWORD,MAILLOGIN,MAILPASSWORD
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

def set_proff():
    ff_prof = webdriver.FirefoxProfile()
    #set some privacy settings
    ff_prof.set_preference( "places.history.enabled", False )
    ff_prof.set_preference( "privacy.clearOnShutdown.offlineApps", True )
    ff_prof.set_preference( "privacy.clearOnShutdown.passwords", True )
    ff_prof.set_preference( "privacy.clearOnShutdown.siteSettings", True )
    ff_prof.set_preference( "privacy.sanitize.sanitizeOnShutdown", True )
    ff_prof.set_preference( "signon.rememberSignons", False )
    ff_prof.set_preference( "network.cookie.lifetimePolicy", 2 )
    ff_prof.set_preference( "network.dns.disablePrefetch", True )
    ff_prof.set_preference( "network.http.sendRefererHeader", 0 )
    
    #set socks proxy
    """
    ff_prof.set_preference( "network.proxy.type", 1 )
    ff_prof.set_preference( "network.proxy.socks_version", 5 )
    ff_prof.set_preference( "network.proxy.socks", '127.0.0.1' )
    ff_prof.set_preference( "network.proxy.socks_port", 9050 )
    ff_prof.set_preference( "network.proxy.socks_remote_dns", True )
    """
    #get a huge speed increase by not downloading images
    ff_prof.set_preference( "permissions.default.image", 2 )
    return ff_prof

def run_driver(ff_prof):
    driver = webdriver.Firefox(ff_prof)
    return driver

def open_mail(driver):
    driver.get("https://generator.email")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//label[@for="toggler-2"]'))).click()
    
def open_fb(driver):
    driver.execute_script('''window.open("http://www.facebook.com","_blank");''')
    sleep(3)
    driver.switch_to_window(driver.window_handles[1])


    
    



def new_mail_address(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Generate new e-mail"]'))).click()
    mail_address = driver.find_element_by_id('email_ch_text').text
    return mail_address

def register_fb(driver,user,mail_address):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'firstname')))
    humanInput(driver.find_element_by_name("firstname"),user[1])
    humanInput(driver.find_element_by_name("lastname"),user[2])
    humanInput(driver.find_element_by_name("reg_email__"),mail_address)
    humanInput(driver.find_element_by_name("reg_email_confirmation__"),mail_address)
    humanInput(driver.find_element_by_name("reg_passwd__"),user[7])
    Select(driver.find_element_by_name("birthday_month")).select_by_value(str(user[4]))
    Select(driver.find_element_by_name("birthday_day")).select_by_value(str(user[5]))
    Select(driver.find_element_by_name("birthday_year")).select_by_value(str(user[3]))
    elem = driver.find_elements_by_name("sex")
    if user[0] == 1:
        elem[0].click()
    else:
        elem[1].click()
    driver.find_element_by_name("websubmit").click();
    
def switch_tab_mail(driver):
    sleep(3)
    driver.switch_to_window(driver.window_handles[0])

def switch_tab_fb(driver):
    sleep(3)
    driver.switch_to_window(driver.window_handles[1])
    
def get_verification_code(driver):
    WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.XPATH, '//div[@class="e7m subj_div_45g45gg"]')))
    verification_code = driver.find_element_by_xpath('//div[@class="e7m subj_div_45g45gg"]').text[:5]
    return verification_code

def verify_fb(driver, verification_code):
    driver.find_element_by_id("code_in_cliff").click()
    humanInput(driver.find_element_by_id("code_in_cliff"),verification_code)
    driver.find_element_by_name("confirm").click()
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//a[@class="_42ft _42fu layerCancel uiOverlayButton selected _42g- _42gy"]'))).click()


def logout_fb(driver):
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'userNavigationLabel'))).click()
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, '_54nh')))
    driver.find_elements_by_class_name('_54nh')[9].click()

def delete_mails(driver):
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'ptSelectConversation-label')))
    mails_to_remove = driver.find_elements_by_class_name("ptSelectConversation-label").click()
    for mail in mails_to_remove:
        mail.click()
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'pm_buttons-child fa fa-trash-o toolbar-btn-trash moveElement-btn-trash')))
    driver.find_element_by_class_name("pm_buttons-child fa fa-trash-o toolbar-btn-trash moveElement-btn-trash").click()

def remove_fb_mail(driver):
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, '_1k67 _cy7')))
    driver.find_element_by_id("userNavigationLabel").click()
    driver.find_element(By.XPATH, '//a[href="https://www.facebook.com/settings"]').click()

def open_db():
    conn = sqlite3.connect('project.db', isolation_level=None)
    return conn

def get_users(conn):
    users = conn.execute("SELECT GENDER,FIRSTNAME,LASTNAME,YEAR,MONTH,DAY,EMAIL,PASSWORD from USER")
    return users

def close_db(conn):
    conn.close()
    
def create_accounts(driver):
    conn = open_db()
    
    for user in get_users(conn):
        switch_tab_mail(driver)
        mail_address = new_mail_address(driver)
        switch_tab_fb(driver)
        register_fb(driver,user,mail_address)
        switch_tab_mail(driver)
        verification_code = get_verification_code(driver)
        switch_tab_fb(driver)
        verify_fb(driver, verification_code)
        logout_fb(driver)
    
    close_db(conn)

def main():
    driver = run_driver(set_proff())
    open_mail(driver)
    open_fb(driver)
    create_accounts(driver)
  
if __name__== "__main__":
    main()

#login: sugarmailman
#password: Sugar*Mail1Man


