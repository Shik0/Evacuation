import requests, parsedatetime as pdt
from bs4 import BeautifulSoup
import os,shutil,sys
from decouple import config

######## DECLARE ALL CONSTANT VARIABLES HERE ############

requests.urllib3.disable_warnings() # disable all warnings related to SSL connection
domain = config('domain_URL') # main URL to collect stuff info
dep_ID = [] # list is going to store all dep ID's

#gather all stuff information using their department numbers from intranet
dep_url = config('department_URL')

# List stuff by their department numbers and here dep number will be added by script
stuff_url = config('stuff_URL')

session = requests.Session()
loginUserName = config('loginUser')
loginUserPassword = config('loginPassword')
session.auth = (loginUserName, loginUserPassword)
stuff_departments = session.get(dep_url, verify=False)
cal = pdt.Calendar()

# Django variables
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Evacuation.settings")
import django
django.setup()
from apps.hse.models import StuffAll, Country #to store collected data in the database tables
from Evacuation import settings
######## END OF CONSTANTS ###############################
print(settings.PROJECT_DIR.child('static'))
sys.exit()
def convert_date(dt):
    months = {"Yanvar":"January","Fevral":"February","Mart":"March","Aprel":"April","May":"May",
            "İyun":"June","İyul":"July","Avqust":"August","Sentyabr":"September","Oktyabr":"October",
            "Noyabr":"November","Dekabr":"December"}
    dt_EN = dt.strip().split(" ")
    # get english version of months, if does not exists then return ogirinal month name
    dt_EN[1] = months.get(dt_EN[1],dt_EN[1])
    # return format YYYY-MM-DD
    return cal.parseDT(" ".join(dt_EN))[0].strftime('%Y-%m-%d')


def get_profile_pic(stuff_pic, conn_param):
    ####### assign user id from URL to the picture name, we find this id from URL using index
    left = stuff_pic.find("=") + 1
    right = stuff_pic.find("&")
    file_name = stuff_pic[left:right]
    # copy profile picture to the project media folder (change this part in the future)
    # this method is only done for the test purposes, do not use this in prod system
    resp = conn_param.get(stuff_pic, stream = True)
    with open(settings.MEDIA_ROOT + os.sep + 'profilepic'+ os.sep + '%s.jpg' % file_name, 'wb') as ff:
        shutil.copyfileobj(resp.raw, ff)
    del resp
    return "%s.jpg" % file_name

def findDepartments(conn_par):
    """
    This function creates a list which contain ID of Company departments.
    Here we connect to the company's intranet web page and collect required
    information about departments. BeautifulSoup is used to parse html pages.
    Function returns a list format.
    """
    conn_par.encoding = 'utf-8'
    dep_soup = BeautifulSoup(conn_par.text,'lxml')
    for hit_dep in dep_soup.findAll(attrs={'class' : 'departments'}):
        for href_dep in hit_dep.find_all('a'):
            url_dep = domain + href_dep.get('href')
            dep_ID.append(url_dep[url_dep.rfind('=') + 1:])
    return dep_ID

def companyStuff(_stuff_url,dep_lst,conn_par): #function receive two params : URL and dep list
    all_stuff = {} # company's all stuff
    # start point of stuff ID
    n = 0
    # get stuff list by their department url
    for dep in dep_lst:
        url = _stuff_url + dep
        r = conn_par.get(url, verify=False)
        r.encoding = 'utf-8'
        # parse received html pages
        stuff_soup = BeautifulSoup(r.text,'lxml')
        for hit in stuff_soup.findAll(attrs={'class' : 'middle'}):
            for hit in stuff_soup.findAll(attrs={'class' : 'staff'}):
                # stuff list
                for href in hit.find_all('a'):
                    url = domain + href.get('href')
                    r = conn_par.get(url,verify=False)
                    r.encoding = 'utf-8'
                    soup2 = BeautifulSoup(r.text,'lxml')
                    stuff = {}
                    # stuff details
                    for hit in soup2.findAll(attrs={'class' : 'middle'}):
                        #### BLOCK 3 - for debug ####
                        stuff["department_id"] = dep
                        try:
                            stuff["name"] = hit.find("div").find("div").find("div").contents[1] #stuff name
                            stuff["picture"] = get_profile_pic(domain + hit.img['src'], session) #profile picture name
                            stuff["department"] = hit.h1.string #department
                            stuff["position"] = hit.span.string # position
                        except:
                            print("Error occured, please check BLOCK 3!")
                        #### END OF BLOCK 3 ####

                        for i in range(1,len(hit.find("div").find_all("div", class_="profileKey"))):
                           stuff[hit.find("div").find_all("div", class_="profileKey")[i].string]  = hit.find("div").find_all("div", class_="profileVal")[i].string

                        all_stuff[n] = {"name":stuff.get("name",""), "picture": stuff.get("picture",""),
                                        "department": stuff.get("department",""), "department_id": stuff.get("department_id",""),
                                        "position": stuff.get("position",""), "email": stuff.get("Email",""),
                                        "phone": stuff.get("Telefon",""), "mobile": stuff.get("Mobil",""),
                                        "start_date": convert_date(stuff.get("İşə qəbul tarixi", ""))
                                          }
                        n += 1
    return all_stuff

if __name__ == "__main__":
    # go through every employee record and save them in the database
    # employees var is a dict : key = empid, value = all details
    employees = companyStuff(stuff_url, findDepartments(stuff_departments), session )
    emp_city = Country.objects.get(city="Baku")
    # departments located in the plant office
    # '2' is a Commercial department ID and some of employees from this dep work in the city office.
    #Employees workplaces need classification!
    plant_deps = [dep for dep in findDepartments(stuff_departments) if dep != '2']
    for emp in employees:
        if employees[emp]["name"][-1] == "v":
            gtype = "m"
        elif employees[emp]["name"][-1] == "a":
            gtype = "f"
        else:
            gtype = " "
        empnew = StuffAll(empid = emp, name = employees[emp]["name"], position = employees[emp]["position"],
                department = employees[emp]["department"], department_id = employees[emp]["department_id"],
                email = employees[emp]["email"], mobile = employees[emp]["mobile"],
                phone = employees[emp]["phone"], start_date = employees[emp]["start_date"],
                workplace = "po" if employees[emp]["department_id"] in plant_deps else "co",
                city = emp_city, profilepic = employees[emp]["picture"], genre = gtype
                )
        empnew.save()
