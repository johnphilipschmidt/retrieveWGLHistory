# J. Philip Schmidt Mar 2018
# Python Program to retrieve WGL history from WGL site URL
# Usage:	python retrieveWglHistory.py
# Description
#	Missing history from statement needed to retrieve information from the net
#	Method:Convert dates to numerics, and map back to strings for search
#	URL needs numbers search needs a string for extraction from the td's...so...
#	Formatted for quick cut and paste into Excel.
#	Quick and dirty not meant for product release.


import urllib2
from bs4 import BeautifulSoup

def changeData(aDate):
    aString = "https://wglholdingsinc.gcs-web.com/historical-price-lookup?8c7bdd83-a726-4a84-b969-494be2477e47%5BWGL_N%5D%5Bdate_month%5D=##MONTH##&8c7bdd83-a726-4a84-b969-494be2477e47%5BWGL_N%5D%5Bdate_day%5D=##DAY##&8c7bdd83-a726-4a84-b969-494be2477e47%5BWGL_N%5D%5Bdate_year%5D=##YEAR##"
    month=aDate[0:2]
    day=aDate[2:4]
    year=aDate[4:8]
    newString = aString.replace("##MONTH##",month)
    newString = newString.replace("##YEAR##",year)
    newString = newString.replace("##DAY##",day)
    return newString



def monthsToStrings(argument):
    switcher = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }
    return switcher.get(argument, "nothing")


# dates to query upon
queryDates = [
    "02012001","05022001","11012001",
    "02012002","05022002","11012002",
    "02012003","05022003","11012003",
    "02012004","05022004","11012004",
    "02012005","05022005","11012005",
    "02012006","05022006","11012006",
    "02012008","05022008","11012008",
    "02012009","05022009","11012009",
    "02012010","05022010","11012010",
    "02012011","05022011","11012011",
    "02012012","05022012","11012012"
]
# For all the dates
for aDate in queryDates:
    #parse them into their repsective containers
    month=aDate[0:2]
    day=aDate[2:4]
    year=aDate[4:8]
    #get the Month String to "search" on
    theMonth= monthsToStrings(month)

    #parse the URL to make the URL query
    quote_page=changeData(aDate)
    #Open the page
    page = urllib2.urlopen(quote_page)

    #Soup the result to parse the html
    soup = BeautifulSoup(page, 'html.parser')

    # Find the tag in the page
    li=soup.select('table[class="nirtable historical-lookup collapse-table-wide"] td')
    #parse the elements by  index
    for idx, elem in enumerate(li):
        thiselem = elem
        nextelem = li[(idx + 1) % len(li)]
        #Is this one of our guys?
        if((theMonth+" "+day.replace("0","")) in str(nextelem) ):
            # get the one we want by date
            theDate=nextelem
            # Get the value of the date
            theValue= li[(idx + 2) % len(li)]
            # Remove the tags
            print "\""+str(theDate).replace("<td>","").replace("</td>","")+"\""+","+str(theValue).replace("<td>","").replace("</td>","").replace("$","")
print "End of line ########################################"