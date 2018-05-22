from selenium import webdriver
from random import uniform
from time import sleep


MAILLOGIN = 'sugarmailman'
MAILPASSWORD = 'Sugar*Mail1Man'

oneminute = 60

onehour = 60* 60

def humanInput(myInput,text):
    for character in text:
        sleep(uniform(0.05,0.10))
        myInput.send_keys(character)
        
        #new login:qwfsdgerhgdfhgfh
        #newpass: qwfsdgerhgdfhgfh1
        # oldpass: Sugar*Mail1Man