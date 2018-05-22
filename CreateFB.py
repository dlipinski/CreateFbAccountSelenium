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
from selenium.common.exceptions import NoSuchElementException
import datetime
import DataBase

def set_proff():
    """Returns: (FirefoxProfile) ff_prof --  firefox preferences
    Arguments:
    
    """
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
    """Returns: (webdriver) driver -- firefox driver
    Arguments:
    (FirefoxProfile) ff_prof -- firefox preferences
    """
    driver = webdriver.Firefox(ff_prof)
    return driver

def open_mail(driver):
    """Returns: nothing
    Arguments:
    (webdriver) driver --  firefox driver
    """
    driver.get("https://generator.email")
    #make sure fb will accept that mail
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//label[@for="toggler-2"]'))).click()
    
def open_fb(driver):
    """Returns: nothing
    Arguments:
    (webdriver) driver -- firefox driver
    """
    #open fb in new window
    driver.execute_script('''window.open("http://www.facebook.com","_blank");''')
    sleep(3)
    driver.switch_to_window(driver.window_handles[1])

def new_mail_address(driver):
    """Returns: (string) mail_address -- mail address from website
    Arguments:
    (webdriver) driver -- firefox driver
    """
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Generate new e-mail"]'))).click()
    mail_address = driver.find_element_by_id('email_ch_text').text
    return mail_address

def log(log):
    """Returns: nothing
    Arguments:
    (string) log -- text to be logged
    """
    now = datetime.datetime.now()
    print("[{0}:{1}:{2}] ".format(now.hour,now.minute,now.second))

def register_fb(driver,user,mail_address):
    """Returns: (Bool)
    Arguments:
    (webdriver) driver -- firefox driver
    (array) user -- row from db
    (string) mail_address -- mail from website
    """
    log("Trying to create fb account: {0} {1}, {2}-{3}-{4} ({5} : {6})".format(user[2],user[3],user[4],user[5],user[6],mail_address,user[8]))
    #wait for load inputs
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'firstname')))
    #insert firstname
    humanInput(driver.find_element_by_name("firstname"),user[2])
    #insert lastname
    humanInput(driver.find_element_by_name("lastname"),user[3])
    #insert email
    humanInput(driver.find_element_by_name("reg_email__"),mail_address)
    #insert emal confirmation
    humanInput(driver.find_element_by_name("reg_email_confirmation__"),mail_address)
    #insert password
    humanInput(driver.find_element_by_name("reg_passwd__"),user[8])
    #select birth month
    Select(driver.find_element_by_name("birthday_month")).select_by_value(str(user[5]))
    #select birth day
    Select(driver.find_element_by_name("birthday_day")).select_by_value(str(user[6]))
    #select birth year
    Select(driver.find_element_by_name("birthday_year")).select_by_value(str(user[4]))
    #select sex depends on gendes
    elem = driver.find_elements_by_name("sex")
    if user[1] == 1:
        elem[0].click()
    else:
        elem[1].click()
    #submit registration
    driver.find_element_by_name("websubmit").click();
    #wait and check if there is error (eg. 'your mail is incorrect' etc.)
    sleep(3)
    try:
        element=driver.find_element_by_id("reg_error_inner")
    except NoSuchElementException:
        log("Failed")
        return False
    log("Succes")
    return True
    
def switch_tab_mail(driver):
    """Returns: nothing
    Arguments:
    (webdriver) driver -- firefox driver
    """
    driver.switch_to_window(driver.window_handles[0])

def switch_tab_fb(driver):
    """Returns: nothing
    Arguments:
    (webdriver) driver -- firefox driver
    """
    driver.switch_to_window(driver.window_handles[1])
    
def get_verification_code(driver):
    """Returns: (string) verification_code -- code from mail to fb
    Arguments:
    (webdriver) driver -- firefox driver
    """
    #wait for new mail
    WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.XPATH, '//div[@class="e7m subj_div_45g45gg"]')))
    #get vrc from subcject of mail
    verification_code = driver.find_element_by_xpath('//div[@class="e7m subj_div_45g45gg"]').text[:5]
    return verification_code

def verify_fb(driver, verification_code):
    """Returns: nothing
    Arguments:
    (webdriver) driver -- firefox driver
    (string) verification_code -- code for verification
    """
    #click on input (robot stuff i guess)
    driver.find_element_by_id("code_in_cliff").click()
    #insert verification code to input
    humanInput(driver.find_element_by_id("code_in_cliff"),verification_code)
    #confirm verification
    driver.find_element_by_name("confirm").click()
    #click 'Okay'
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div/div/div/div[3]/div/a'))).click()
    
def logout_fb(driver):
    """Returns: nothing
    Arguments:
    (webdriver) driver -- firefox driver
    """
    #wait for and click top right to get list
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'userNavigationLabel'))).click()
    #wait for 'logout'
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, '_54nh')))
    #click 'logout'
    driver.find_elements_by_class_name('_54nh')[9].click()

def open_db():
    """Returns: (Connection) conn -- connection to operate
    Arguments:
    """
    conn = sqlite3.connect('project.db', isolation_level=None)
    return conn

def get_users(conn):
    """Returns:
    Arguments:
    (Connection) conn -- connection to get users from db
    """
    users = conn.execute("SELECT ID,GENDER,FIRSTNAME,LASTNAME,YEAR,MONTH,DAY,EMAIL,PASSWORD from USER")
    return users

def close_db(conn):
    """Returns:
    Arguments:
    (Connection) conn -- connection to close
    """
    conn.close()
    
def update_user_mail(conn,user,mail_address):
    """Returns:
    Arguments:
    (Connection) conn -- connection to get users from db
    (array) user -- row from db
    (string) mail_address -- mail from website
    """
    conn.execute("UPDATE USER SET EMAIL=? WHERE ID=?",(mail_address,user[0]))
    
def create_accounts(driver):
    """Returns:
    Arguments:
    (webdriver) driver -- firefox driver
    """
    conn = open_db()
    isFbOk = False
    for user in get_users(conn):
        while isFbOk == False:
            switch_tab_mail(driver)
            mail_address = new_mail_address(driver)
            update_user_mail(conn, user, mail_address)
            switch_tab_fb(driver)
            isFbOk = register_fb(driver,user,mail_address)
        switch_tab_mail(driver)
        verification_code = get_verification_code(driver)
        switch_tab_fb(driver)
        verify_fb(driver, verification_code)
        logout_fb(driver)
    close_db(conn)

def main():
    DataBase.reset()
    DataBase.fill()
    driver = run_driver(set_proff())
    open_mail(driver)
    open_fb(driver)
    create_accounts(driver)
  
if __name__== "__main__":
    main()

#login: sugarmailman
#password: Sugar*Mail1Man


