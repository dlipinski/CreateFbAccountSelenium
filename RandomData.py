from random import randint
from urllib.request import urlopen



first_names_female = list()
url = "https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/female.txt"
for line in urlopen(url):
    first_names_female.append(line.strip().decode())
    
first_names_male = list()
url = "https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/male.txt"
for line in urlopen(url):
    first_names_male.append(line.strip().decode())
    

last_names = list()
url = "https://raw.githubusercontent.com/colinangusmackay/Xander.PasswordValidator/master/src/Xander.PasswordValidator/Resources/Surnames.txt"
for line in urlopen(url):
    last_names.append(line.strip().decode())
    
def get_gender():
    return randint(1,2)

def get_first_name_female():
    return first_names_female[randint(0, len(first_names_female)-1)]

def get_first_name_male():
    return first_names_male[randint(0, len(first_names_male)-1)]

def get_firstname(gender):
    if gender == 1:
        return get_first_name_female()
    else:
        return get_first_name_male()

def get_last_name():
    return last_names[randint(0, len(last_names)-1)]

def get_year():
    return randint(1970,1999)

def get_month():
    return randint(1,12)

def get_day():
    return randint(1,28)




