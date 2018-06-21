from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pymysql
import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='fbgroupscraper',
                             charset='utf8')

def create_database(tblName):
    #Create a cursor for the database
    cur = connection.cursor()

    try:
        #Create a table in mysql???
        createsql = "CREATE TABLE %s ( \
          `member_id` int(11) DEFAULT NULL, \
          `fbname` varchar(255) DEFAULT NULL, \
          `fburl` varchar(255) DEFAULT NULL, \
          `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP \
        )" % (tblName)

        cur.execute(createsql)

    except pymysql.err.InternalError as e:
        code, msg = e.args
        if code == 1050:
            print(tblName, 'already exists')

def writedata(tablename, memberid, fbname, fburl):
    cur = connection.cursor()
    sql = "INSERT INTO %s(member_id, fbname, fburl) \
   VALUES ('%d', '%s', '%s' )" % (tablename, memberid, fbname, fburl)
  

    cur.execute(sql)

    connection.commit()


def getmember_info():
    link = (input("Enter the MEMBERS PAGE of the FB group URL: "))
    databasename = (input("Enter databasename name: "))
    create_database(databasename)

    driver = webdriver.Chrome(executable_path="/Users/clickontemp/Downloads/chromedriver")

    driver.get(link)

    input("Log into Facebook. Then press ENTER")



    asource = driver.page_source
    asoup = BeautifulSoup(asource, "html.parser")

    members = int(asoup.findAll("span",{"class":"_grt _50f8"})[0].text)


    membercon = asoup.findAll("div",{"id":"groupsMemberSection_recently_joined"})[0]
    listof = membercon.findAll("div",{"class":"clearfix _60rh _gse"})
    numsofar = 0
    numafter = 0

    page='unloaded'

    while page=='unloaded':
        numafter = numsofar
        source = driver.page_source
        soup = BeautifulSoup(source, "html.parser")
        membercon = soup.findAll("div",{"id":"groupsMemberSection_recently_joined"})[0]
        listof = membercon.findAll("div",{"class":"clearfix _60rh _gse"})
        numsofar = 0

        for i in listof:
            numsofar+= 1
        print(numsofar)
        if numsofar == numafter:
            page='loaded'

        else:
            driver.execute_script("window.scrollTo(0, 11111080)")
            time.sleep(1)




    print('all members loaded')
    memberid = 0
    for member in listof:
        memberid += 1
        print(memberid)
        fbname = member.findAll("div",{"class":"_60ri fsl fwb fcb"})[0].text.replace("'","")
        print(fbname)
        fburl = member.findAll("div",{"class":"_60ri fsl fwb fcb"})[0].a['href']
        print(fburl)
        writedata(databasename, memberid, fbname, fburl)

getmember_info()


connection.close()


