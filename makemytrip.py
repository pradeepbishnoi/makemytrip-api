"""
MakeMyTrip Unofficial API
- to retrieve the Ticket price for a specific date (one-way)

@author Pradeep Bishnoi
@twitter pradeepbishnoi

"""

# From command line execute following command
# python makemytrip.py Bangalore Jaipur 

import urllib2
import json
import sys 
import re
from datetime import datetime, date, time
#from browse import Browse
import mapping as city

class MakeMyTrip(object):
    
    url_browse=""
    flights_data=""
    stoppage=""
    
    def __init__(self):
        pass
        
    def browse(self, url=""):
        print "Hitting : " , url
        self.url_browse=urllib2.urlopen(url).read()
        fil=open("out.txt","w")
        fil.write(self.url_browse)
        fil.close()
    
    def assert_text(self, check_text=""):
        return check_text in self.url_browse
        
    def read_line(self):
        flights_data=""
        i=0
        fil=open("out.txt","r")
        for line in fil.readlines():
            i=i+1
            if "flightsData" in line:
                flights_data=line
        #print "Total lines",i
        self.format_flights_data(flights_data)
        #self.getFlightTable(flights_data)
        
    def format_flights_data(self, flights_data):
        new_flights_data=flights_data.replace("var flightsData = ","").strip()
        new_flights_data=new_flights_data[:-1]
        fil=open("out.txt","w")
        fil.write(new_flights_data)
        fil.close()
        d=new_flights_data
        li = json.loads(d)
        self.create_json(li)
        #print type(new_flights_data)
            
    def get_extra_detail(self, flights_data):
        #date_size=len(flights_data)
        halt=flights_data[0]['f']
        layover=""
        for x in range(len(flights_data)):
            halt= halt + u"   \u2708   " + flights_data[x]['t'] + " ( " + flights_data[x]['du'] + " )"
            if x>0:
                layover= layover + flights_data[x]['f'] + "  ( " + flights_data[x]['lo'] + " )  "
        print halt
        return layover
        #return halt
        
    def create_json(self, l):
        # To list all the flight data, 
        #for i in range(len(l)): 
        # however i am listing only 10 flight data by using range(9)
        #Color code  GREEN \033[92m     BOLD \033[1m      END \033[0m
        tmp_size=len(l)
        if tmp_size>9:
            tmp_size=9
        for i in range(tmp_size):   
            print ""
            print u"\033[1m" + l[i]['le'][0]['an'] , u"\033[0m      \u20B9 \033[92m",  l[i]['af'], "\033[0m  in  ", l[i]['td']
            layover=self.get_extra_detail(l[i]['le']) 
            #ToDo
            print l[i]['le'][0]['fd'],  l[i]['le'][0]['fdt'], \
             u"  --->>  ", l[i]['le'][0]['fa'], l[i]['le'][0]['fat']
            print "\tStoppage : ", layover
            #print "Arrival : ", l[i]['le'][0]['fa'], l[i]['le'][0]['fat']
            print u"\u2982"*50
            #l=json.loads(x)
            

if __name__=="__main__":
    #print sys.argv[0], sys.argv[1], sys.argv[2]
    print
    print "="*30 
    origin="BLR"
    destination="JDH"
    j_date=date.today()
    j_date=str(j_date.day) + "/" + str(j_date.month) + "/" + str(j_date.year)
    for i in range(len(sys.argv)):
        if i==1:
            tmp=sys.argv[1].lower()
            origin=city.city_code[tmp]
        if i==2:
            tmp=sys.argv[2].lower()
            destination=city.city_code[tmp]
        if i==3:
            j_date=sys.argv[3]
    try:
        j_date=datetime.strptime(j_date,"%d/%m/%Y")
        #print dir(j_date), j_date.isoformat()
        my_date=j_date.strftime("%d-%m-%Y")
    except ValueError:
        print "Unable to parse the Input date."
        print "Please provide the date in  dd/mm/yyyy  format"
        sys.exit()
    print "Detail for ", origin, " to ", destination, " on ", my_date
    print "="*30
    bro = MakeMyTrip()
    url="http://flights.makemytrip.com/makemytrip/search/O/O/E/1/0/0/S/V0/" + origin + "_" + destination + "_" + my_date
    bro.browse(url)
    #bro.browse("http://flights.makemytrip.com/makemytrip/search/O/O/E/1/0/0/S/V0/BLR_JAI_05-02-2015")
    bro.read_line()
