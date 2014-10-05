"""
MakeMyTrip Unofficial API
- to retrieve the Ticket price for a specific date (one-way)

@author: Pradeep Bishnoi
@twitter: pradeepbishnoi

"""

# From command line execute following command
# python makemytrip.py Bangalore Jaipur 

import urllib2
import json
import sys 
import re
from datetime import datetime, date, time
import mapping as city

BASE_URL="http://flights.makemytrip.com/makemytrip/"

class MakeMyTrip(object):
    
    def __init__(self):
        self.url_browse = ""
        self.flights_data = ""
        self.stoppage = ""
        self.arrival_time = ""
        self.trip_json = []
        
    def browse(self, url="", roundtrip=False):
        print url
        self.url_browse = urllib2.urlopen(url).read()
        fil = open("out.txt","w")
        fil.write(self.url_browse)
        fil.close()
        i = 0
        fil = open("out.txt","r")
        if roundtrip:
            json_list = json.loads(fil.read())
            #print json_list#['filterData']
            print "-"*50
            json_list = json.loads(json_list['fd'])
            return json_list
        for line in fil.readlines():
            i = i+1
            if "flightsData" in line:
                self.flights_data = line
                break
        temp_flights_data = self.flights_data.replace("var flightsData = ","").strip()
        temp_flights_data = temp_flights_data[:-1]
        fil = open("out.txt","w")
        fil.write(temp_flights_data)
        fil.close()
        json_list = json.loads(temp_flights_data)
        return json_list
    
    def create_json_oneway(self, dump_list):
        for i in range(len(dump_list)):
            temp = '{ "airline" : "' + dump_list[i]['le'][0]['an'] + '"'
            temp = temp + ', "price" : "' + str(dump_list[i]['af']) + '"'
            temp = temp + ', "total_time" : "' + str(dump_list[i]['td']) + '"'
            temp = temp + ', "depart_date" : "' + str(dump_list[i]['le'][0]['fd']) + '"'
            temp = temp + ', "depart_time" : "' + str(dump_list[i]['le'][0]['fdt']) + '"'
            temp_dump_list = dump_list[i]['le']
            for x in range(len(temp_dump_list)):
                if x == (len(temp_dump_list)-1):
                    temp = temp + ', "arrival_date" : "' + str(temp_dump_list[x]['fa']) + '"'
                    temp = temp + ', "arrival_time" : "' + str(temp_dump_list[x]['fat']) + '"}'
            self.trip_json.append(temp)
        return json.dumps(self.trip_json)
        
    def create_json_roundtrip(self, dump_list):
        #Todo : Complete this function to return the custom JSON as response 
        for i in range(len(dump_list)):
            return json.loads(['fd'])
        
    def journey_oneway(self, origin, destination, depart_date, adult=1, children=0, infant=0):
        adult = str(adult) if adult >= 1 else "1"
        children = str(children) if children >= 1 else str(children)
        infant = str(infant) if infant >= 1 else str(infant)
        new_url = BASE_URL + "search/O/O/E/" + adult +"/" + children + "/" + infant + "/S/V0/" + origin + "_" + destination + "_" + depart_date
        return self.browse(new_url)
    
    def journey_roundtrip(self, origin, destination, depart_date, return_date, adult=1, children=0, infant=0):
        new_url = BASE_URL + 'splitRTDataService.json?classType=E&deptDate=' + depart_date + '&fltMap=&fromCity='+ origin + '&noOfAdlts=' + str(adult) + \
        '&noOfChd=' + str(children) + '&noOfInfnt=' + str(infant) + '&returnDate=' + return_date + '&toCity=' + destination + '&tripType=R&tripTypeDup=R'
        return self.browse(new_url, True)
        
    #Todo: Get rid of this method
    def read_line(self):
        flights_data=""
        i = 0
        fil = open("out.txt","r")
        for line in fil.readlines():
            i = i+1
            if "flightsData" in line:
                flights_data = line
        #print "Total lines",i
        self.format_flights_data(flights_data)
        #self.getFlightTable(flights_data)
        
    #Todo: Get rid of this method
    def format_flights_data(self, flights_data):
        new_flights_data = flights_data.replace("var flightsData = ","").strip()
        new_flights_data = new_flights_data[:-1]
        fil = open("out.txt","w")
        fil.write(new_flights_data)
        fil.close()
        d = new_flights_data
        li = json.loads(d)
        self.create_json_oneway(li)
        #print type(new_flights_data)
            
    def get_extra_detail(self, flights_data):
        #date_size=len(flights_data)
        halt = flights_data[0]['f']
        layover = ""
        for x in range(len(flights_data)):
            halt = halt + u"   \u2708   " + flights_data[x]['t'] + " ( " + flights_data[x]['du'] + " )"
            if x > 0:
                layover = layover + flights_data[x]['f'] + "  ( " + flights_data[x]['lo'] + " )  "
            if x == (len(flights_data)-1):
                self.arrival_time = flights_data[x]['fa'] + " " +flights_data[x]['fat']
        print halt
        return layover
        #return halt
        
    def print_json(self, l):
        # To list all the flight data, 
        #for i in range(len(l)): 
        # however i am listing only 10 flight data by using range(9)
        #Color code  GREEN \033[92m     BOLD \033[1m      END \033[0m
        tmp_size = len(l)
        if tmp_size > 9:
            tmp_size = 9
        for i in range(tmp_size):   
            print ""
            print u"\033[1m" + l[i]['le'][0]['an'] , u"\033[0m      \u20B9 \033[92m", l[i]['af'], "\033[0m  in  ", l[i]['td']
            layover=self.get_extra_detail(l[i]['le']) 
            #ToDo
            print l[i]['le'][0]['fd'],  l[i]['le'][0]['fdt'], \
             u"  --->>  ", self.arrival_time
            print "\tStoppage : ", layover
            #print "Arrival : ", l[i]['le'][0]['fa'], l[i]['le'][0]['fat']
            print u"\u2982"*50
            #l=json.loads(x)
        
if __name__=="__main__":
    #print sys.argv[0], sys.argv[1], sys.argv[2]
    print
    print "="*30 
    origin = "MAA"
    destination = "CCJ"
    j_date = date.today()
    j_date = str(j_date.day) + "/" + str(j_date.month) + "/" + str(j_date.year)
    for i in range(len(sys.argv)):
        if i == 1:
            tmp = sys.argv[1].lower()
            origin = city.city_code[tmp]
        if i == 2:
            tmp = sys.argv[2].lower()
            destination = city.city_code[tmp]
        if i == 3:
            j_date = sys.argv[3]
    try:
        j_date = datetime.strptime(j_date,"%d/%m/%Y")
        #print dir(j_date), j_date.isoformat()
        my_date = j_date.strftime("%d-%m-%Y")
    except ValueError:
        print "Unable to parse the Input date."
        print "Please provide the date in  dd/mm/yyyy  format"
        sys.exit()
    print "Detail for ", origin, " to ", destination, " on ", my_date
    print "="*30
    bro = MakeMyTrip()
    
    # To print on console
    #bro.print_json(bro.journey_oneway(origin,destination,"12-12-2014"))
    
    # To return the JSON response from roundtrip API
    temp_jsn = bro.journey_roundtrip(origin, destination, "12/12/2014", "18/12/2014")
    for x in range(len(temp_jsn['departureFlights'])):
        revised_rate = temp_jsn['departureFlights'][x]['raf'] if temp_jsn['departureFlights'][x]['raf'] != 0.0 else temp_jsn['departureFlights'][x]['af']
        print temp_jsn['departureFlights'][x]['fi'], revised_rate, temp_jsn['departureFlights'][x]['td']
    print 
    #print temp_jsn['departureFlights'][1]['td']







'''

Comments for later reference :


Get Round trip details
http://flights.makemytrip.com/makemytrip/search/R/R/E/1/0/0/S/V0/MAA_STV_12-12-2014,STV_MAA_18-12-2014?lang=en 
http://flights.makemytrip.com/makemytrip/splitRTDataService.json?classType=E&deptDate=30%2F10%2F2014&fltMap=&fromCity=BLR&noOfAdlts=1&noOfChd=1&noOfInfnt=1&returnDate=06%2F11%2F2014&toCity=JDH&tripType=R&tripTypeDup=R

#bro.browse("http://flights.makemytrip.com/makemytrip/search/O/O/E/1/0/0/S/V0/BLR_JAI_05-02-2015")
             http://flights.makemytrip.com/makemytrip/search/O/O/E/1/0/0/S/V0/BLR_JDH_04-10-2014
For, Yatra.com search
#http://flight.yatra.com/air-search/dom2/trigger?type=O&viewName=normal&flexi=0&noOfSegments=1&origin=MAA&originCountry=IN&destination=JAI&destinationCountry=IN&flight_depart_date=02/10/2014&ADT=1&CHD=0&INF=0&class=Economy

Airline : "Jet"
Price : "123"
Total_Time : ""
Layover : {
    [],
    []
    }
'''