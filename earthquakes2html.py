#!/usr/bin/env python
# Parse earthquake data files and output an HTML file.
# Requires PANDAS library, which is part of iPython distribution.
#
# Author: Hunter Gabbard <hunter.gabbard@ligo.org>
# Time-stamp: <2015-03-25 15:14:08 bnp>
#
# ./earthquakes2html.py 1109300301-1110423501

import sys
import os
import os.path
import pandas as pd
from time import gmtime, strftime
import commands
import string
import csv
import math
import time

#Current time calculation
#time = strftime("%Y-%m-%d %H:%M:%S")

# Column names to use in HTML table
col_names = ['GPS Time', 'Magnitude', 'P-phase Arrival', 'S-phase Arrival',
             'R- 2 km/s', 'R 3.5 km/s', 'R 5 km/s', 'R-wave amplitude in micro m/s',
             'Arrival floor', 'Departure ceil', 'EQ lat', 'EQ lon', 'EQ distance',
             'ifo']

# Function to open HTML file and output beginning of HTML file
def start_html_file(title, filename):
    file = open(filename, 'w')
    os.system('rm /home/hunter.gabbard/public_html/earthquake_mon/veto_segs.txt')
    file.write('<html>')
    file.write('<head><title>Earthquake data: </title></head>')
    file.write('<body>')
    file.write('<h4 style="position: absolute; z-index: -1; top: 0px; right: 15px;">Last updated: <script>document.write(document.lastModified)</script></h4>')
    file.write('<h1>Earthquake data: </h1>')
    return file

# Function to write end of HTML file and close file
def end_html_file(file):
    file.write('</body>')
    file.write('</html>')
    file.close()

def process_sub_dir(dir, file):
    # Attempt to open earthquakes.txt in dir
    efilename = os.path.join(dir, 'earthquakes.txt')
    seg = open('/home/hunter.gabbard/public_html/earthquake_mon/veto_segs.txt',  'a')
    tp = 0
    tRf = 0
    #Store values
    a = open(efilename,"r")
    global b
    b = a.readlines()
    global c1
    global c2
    global c3
    global c4
    c1 = b[0].split(" ")

    c2 = b[1].split(" ")
    c3 = b[2].split(" ")
    c4 = b[3].split(" ")
    print c1
    global latitude
    global longitude
    global GPS
    global Mag
    global P_phas
    global s_phas
    global R3
    global Ramp
    global EQ_dis
    global ifo
    latitude = c1[10]
    longitude = c1[11]
    GPS = c1[0]
    Mag = c1[1]
    P_phas = c1[2]
    s_phas = c1[3]
    R3 = c1[5]
    Ramp = c1[7]
    EQ_dis = c1[12]
    ifo = c1[13]


    try:
        input = open(efilename)
    except:
        print dir, 'does not contain an earthquakes.txt file!'
    else:
        # Get name of directory for table header
        local_title = os.path.basename(dir)
	conv_title = local_title.replace(local_title[:4], '')
	integer_title = int(conv_title)
	New_title = commands.getstatusoutput("lalapps_tconvert --local --zone=UTC %d" % (integer_title))
	
	link_time = commands.getstatusoutput("lalapps_tconvert --local --zone=UTC -f%%Y-%%m-%%d-%%H-%%M-%%S %d" % (integer_title))
        link_time = str(link_time)
        link_time = link_time.replace(link_time[:5], '')
        link_time = link_time.replace(link_time[19:], '')
        link_time = link_time.split("-")
        link_year = link_time[0]
	link_month = link_time[1]
        link_day = link_time[2]
        link_hour = link_time[3]
        link_minute = link_time[4]
        link_sec = link_time[5]
        link_sec_min1 = int(link_sec) - 5
        link_sec_plus1 = int(link_sec) + 5
	if link_sec_plus1 > 60:
                link_sec_plus1 = link_sec_plus1 - 60
                link_minute_plus1 = int(link_minute) + 1
                web_link = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=%s-%s-%s%%20%s%%3A%s%%3A%s&minmagnitude=3&endtime=%s-%s-%s%%20%s%%3A%s%%3A%s" % (link_year, link_month, link_day, link_hour, link_minute, link_sec_min1, link_year, link_month, link_day, link_hour, link_minute_plus1, link_sec_plus1)
        elif link_sec_min1 < 0:
                link_sec_min1 = link_sec_min1 + 60
                link_minute_min1 = int(link_minute) - 1
                web_link = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=%s-%s-%s%%20%s%%3A%s%%3A%s&minmagnitude=3&endtime=%s-%s-%s%%20%s%%3A%s%%3A%s" % (link_year, link_month, link_day, link_hour, link_minute_min1, link_sec_min1, link_year, link_month, link_day, link_hour, link_minute, link_sec_plus1)
        elif link_sec_plus1 > 60 and link_sec_min1 < 0:
                link_sec_plus1 = link_sec_plus1 - 60
                link_minute_plus1 = int(link_minute) + 1
                link_minute_min1 = int(link_minute) -1
                web_link = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=%s-%s-%s%%20%s%%3A%s%%3A%s&minmagnitude=3&endtime=%s-%s-%s%%20%s%%3A%s%%3A%s" % (link_year, link_month, link_day, link_hour, link_minute_min1, link_sec_min1, link_year, link_month, link_day, link_hour, link_minute_plus1, link_sec_plus1)

        else:
                web_link = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=%s-%s-%s%%20%s%%3A%s%%3A%s&minmagnitude=3&endtime=%s-%s-%s%%20%s%%3A%s%%3A%s" % (link_year, link_month, link_day, link_hour, link_minute, link_sec_min1, link_year, link_month, link_day, link_hour, link_minute, link_sec_plus1)

	#Getting csv files for human readable location
        os.system("rm /home/hunter.gabbard/public_html/earthquake_mon/event_csvs/event.csv")
        os.system("wget '%s' -O /home/hunter.gabbard/public_html/earthquake_mon/event_csvs/event.csv" % web_link)
        try:
                with open('/home/hunter.gabbard/public_html/earthquake_mon/event_csvs/event.csv', 'rb') as csvfile:
                        reader = csv.reader(csvfile)
                        reader = list(reader)
                        id = reader[1][11]
                        place = reader[1][13]
                        USGSmap_link = "http://earthquake.usgs.gov/earthquakes/eventpage/%s#general_summary" % id
        except:
                place = ""
                USGSmap_link = ""
                pass

	
	new_title = str(New_title)
	blah = new_title.replace(new_title[:5], '')
	event_title = blah.replace(blah[28:], '')

        # Read earthquakes.txt
        table = pd.read_table(efilename, sep=' ', names=col_names)

        # Write subtitle for table
	file.write('<hr style="border: 1px dashed black; margin-top: 20px;" />')
        file.write('<h3>Time: %s</h3>' % event_title)
	for i in range(len(c1)):
	    if i == 10:
		file.write('<h3>Location: %s; LAT: %s, LON: %s</h3>' % (place, c1[i], c1[11]))
	for i in range(len(c1)):
	    if i == 1:
		file.write('<h3>Magnitude: %s</h3>' % c1[i])
        file.write('<a href="%s" target="_blank">USGS event link</a>' % USGSmap_link)


        # Write actual table to HTML file
        file.write('<table border="5">')
        file.write('<th> ifo </th>  <th> P-phase Arrival Time </th> <th> S-phase Arrival Time </th> <th> R-wave Arrival Time </th> <th> R-Wave Velocity (micro m/s) </th> <th> EQ Distance (km) </th><th> GPS P-phase Arrival Time </th> <th> GPS S-phase Arrival Time </th> <th> GPS R-wave Arrival Time </th>')
        file.write('<tr>')
	for i in range(len(c1)):
            if i == 13:
                file.write('<td>' + c1[i] + '</td>')

        for i in range(len(c1)):
            if i == 2:
		PDT_time1 = float(c1[i]) - 28800
                PDT_time1 = int(PDT_time1)
                Hanford_title1 = commands.getstatusoutput("lalapps_tconvert --local --zone=PDT -f%%H:%%M:%%S %d" % (PDT_time1))
                han_title1 = str(Hanford_title1)
                hanford1 = han_title1.replace(han_title1[:5], '')
                hanford_title1 = hanford1.replace(hanford1[8:], '')
                file.write('<td> %s PST </td>' % hanford_title1)

        for i in range(len(c1)):
            if i == 3:
		PDT_time2 = float(c1[i]) - 28800
                PDT_time2 = int(PDT_time2)
                Hanford_title2 = commands.getstatusoutput("lalapps_tconvert --local --zone=PDT -f%%H:%%M:%%S %d" % (PDT_time2))
                han_title2 = str(Hanford_title2)
                hanford2 = han_title2.replace(han_title2[:5], '')
                hanford_title2 = hanford2.replace(hanford2[8:], '')
                file.write('<td> %s PST </td>' % hanford_title2)

	for i in range(len(c1)):
	    if i == 5:
		PDT_time4 = float(c1[i]) - 28800
                PDT_time4 = int(PDT_time4)
                Hanford_title4 = commands.getstatusoutput("lalapps_tconvert --local --zone=PDT -f%%H:%%M:%%S %d" % (PDT_time4))
                han_title4 = str(Hanford_title4)
                hanford4 = han_title4.replace(han_title4[:5], '')
                hanford_title4 = hanford4.replace(hanford4[8:], '')
                file.write('<td><b> %s PST </b></td>' % hanford_title4)

	for i in range(len(c1)):
            if i == 7:
                x7=float(c1[i]) * (10**6)
                c1[i]=str(x7)
		if x7 <= 0.1:
                    file.write('<td bgcolor="#00FF00">' + c1[i] + '</td>')
                elif x7 > 0.1 and x7 <= 0.155:
                    file.write('<td bgcolor="#FFFB00">' + c1[i] + '</td>')
                elif x7 > 0.155 and x7 < 0.5:
                    file.write('<td bgcolor="#FFA500">' + c1[i] + '</td>')
                elif x7 >= 0.5:
                    file.write('<td bgcolor="#FF0000">' + c1[i] + '</td>')

        for i in range(len(c1)):
	    if i == 12:
		x12=float(c1[i]) * (10**-3)
		c1[i]=str(x12)
		file.write('<td>' + c1[i] + '</td>')
	for i in range(len(c1)):
	    if i == 2:
		file.write('<td>' + c1[i] + '</td>')
		seg.write(str(int(math.floor(float(c1[i])))) + '\t')
	for i in range(len(c1)):
	    if i == 3:
		file.write('<td>' + c1[i] + '</td>')
	        	
	for i in range(len(c1)):
	    if i == 5:
		R_GPS = str(float(c1[i]) - 28800)
                tfinal = str(int(math.ceil(float(c1[2]) + (2*(float(c1[i])-float(c1[2]))))))
		dur_veto = str(int(math.ceil(2*(float(c1[i])-float(c1[2])))))
		file.write('<td>' + c1[i] + '</td>')
		seg.write(tfinal + '\t' + dur_veto + '\n') 
        file.write('</tr>')
        file.write('<tr>')
	for i in range(len(c2)):
            if i == 13:
                file.write('<td>' + c2[i] + '</td>')

        for i in range(len(c2)):
            if i == 2:
		CST_time1 = float(c2[i]) - 21600
                CST_time1 = int(CST_time1)
                Livingston_title1 = commands.getstatusoutput("lalapps_tconvert --local --zone=PDT -f%%H:%%M:%%S %d" % (CST_time1))
                liv_title1 = str(Livingston_title1)
                livingston1 = liv_title1.replace(liv_title1[:5], '')
                livingston_title1 = livingston1.replace(livingston1[8:], '')
                file.write('<td> %s CST</td>' % livingston_title1)

        for i in range(len(c2)):
            if i == 3:
		CST_time2 = float(c2[i]) - 21600
                CST_time2 = int(CST_time2)
                Livingston_title2 = commands.getstatusoutput("lalapps_tconvert --local --zone=PDT -f%%H:%%M:%%S %d" % (CST_time2))
                liv_title2 = str(Livingston_title2)
                livingston2 = liv_title2.replace(liv_title2[:5], '')
                livingston_title2 = livingston2.replace(livingston2[8:], '')
                file.write('<td> %s CST</td>' % livingston_title2)

        for i in range(len(c2)):
            if i == 5:
		CST_time4 = float(c2[i]) - 21600
                CST_time4 = int(CST_time4)
                Livingston_title4 = commands.getstatusoutput("lalapps_tconvert --local --zone=PDT -f%%H:%%M:%%S %d" % (CST_time4))
                liv_title4 = str(Livingston_title4)
                livingston4 = liv_title4.replace(liv_title4[:5], '')
                livingston_title4 = livingston4.replace(livingston4[8:], '')
                file.write('<td><b> %s CST</b></td>' % livingston_title4)

	for i in range(len(c2)):
            if i == 7:
                y7=float(c2[i]) * (10**6)
                c2[i]=str(y7)
		if y7 <= 0.1:
                    file.write('<td bgcolor="#00FF00">' + c2[i] + '</td>')
                elif y7 > 0.1 and y7 <= 0.155:
                    file.write('<td bgcolor="#FFFB00">' + c2[i] + '</td>')
                elif y7 > 0.155 and y7 < 0.5:
                    file.write('<td bgcolor="#FFA500">' + c2[i] + '</td>')
                elif y7 >= 0.5:
                    file.write('<td bgcolor="#FF0000">' + c2[i] + '</td>')
		    ctime = time.time()
                    alert_diff = float(ctime) - float(c2[5])
                    if alert_diff <= 600:
			file.write("<SCRIPT language=JavaScript>\n<!--\n//Lighting script\nvar flash=0\nfunction lightning()\n{flash=flash+1;\nif(flash==1){document.bgColor='white'; setTimeout(\"lightning()\",100);}\nif(flash==2){document.bgColor='red'; setTimeout(\"lightning()\",90);}\nif(flash==3){flash=0; setTimeout(\"lightning()\",100);}\n}\nsetTimeout(\"lightning()\",1);\n// --></SCRIPT>\n<!--\nThis script downloaded from www.JavaScriptBank.com\nCome to view and download over 2000+ free javascript at www.JavaScriptBank.com\n-->")
        for i in range(len(c2)):
	    if i == 12:
		y12=float(c2[i]) * (10**-3)
		c2[i]=str(y12)
		file.write('<td>' + c2[i] + '</td>')
	for i in range(len(c2)):
	    if i == 2:
		file.write('<td>' + c2[i] + '</td>')
		seg.write(str(int(math.floor(float(c2[i])))) + '\t')
	for i in range(len(c2)):
	    if i == 3:
		file.write('<td>' + c2[i] + '</td>')
	for i in range(len(c2)):
	    if i == 5:
		R1_GPS = str(float(c2[i]) - 21600)
		file.write('<td>' + c2[i] + '</td>') 
		tfinal = str(int(math.ceil(float(c2[2]) + (2*(float(c2[i])-float(c2[2]))))))
                dur_veto = str(int(math.ceil(2*(float(c2[i])-float(c2[2])))))
                seg.write(tfinal + '\t' + dur_veto + '\n')
        file.write('</tr>')
        file.write('<tr>')

	for i in range(len(c3)):
            if i == 13:
                file.write('<td>' + c3[i] + '</td>')

        for i in range(len(c3)):
            if i == 2:
		CEST_time1 = float(c3[i]) + 3600
                CEST_time1 = int(CEST_time1)
                Geo_title1 = commands.getstatusoutput("lalapps_tconvert --local --zone=PDT -f%%H:%%M:%%S %d" % (CEST_time1))
                G_title1 = str(Geo_title1)
                geo1 = G_title1.replace(G_title1[:5], '')
                geo_title1 = geo1.replace(geo1[8:], '')
                file.write('<td> %s CET </td>' % geo_title1)

        for i in range(len(c3)):
            if i == 3:
		CEST_time2 = float(c3[i]) + 3600
                CEST_time2 = int(CEST_time2)
                Geo_title2 = commands.getstatusoutput("lalapps_tconvert --local --zone=PDT -f%%H:%%M:%%S %d" % (CEST_time2))
                G_title2 = str(Geo_title2)
                geo2 = G_title2.replace(G_title2[:5], '')
                geo_title2 = geo2.replace(geo2[8:], '')
                file.write('<td> %s CET </td>' % geo_title2)


        for i in range(len(c3)):
            if i == 5:
		CEST_time4 = float(c3[i]) + 3600
                CEST_time4 = int(CEST_time4)
                Geo_title4 = commands.getstatusoutput("lalapps_tconvert --local --zone=PDT -f%%H:%%M:%%S %d" % (CEST_time4))
                G_title4 = str(Geo_title4)
                geo4 = G_title4.replace(G_title4[:5], '')
                geo_title4 = geo4.replace(geo4[8:], '')
                file.write('<td><b> %s CET </b></td>' % geo_title4)

	for i in range(len(c3)):
            if i == 7:
                z7=float(c3[i]) * (10**6)
                c3[i]=str(z7)
		if z7 <= 0.1:
                    file.write('<td bgcolor="#00FF00">' + c3[i] + '</td>')
                elif z7 > 0.1 and z7 <= 0.155:
                    file.write('<td bgcolor="#FFFB00">' + c3[i] + '</td>')
                elif z7 > 0.155 and z7 < 0.5:
                    file.write('<td bgcolor="#FFA500">' + c3[i] + '</td>')
                elif z7 >= 0.5:
                    file.write('<td bgcolor="#FF0000">' + c3[i] + '</td>')
        for i in range(len(c3)):
	    if i == 12:
		z12=float(c3[i]) * (10**-3)
		c3[i]=str(z12)
		file.write('<td>' + c3[i] + '</td>')
	for i in range(len(c3)):
	    if i == 2:
		file.write('<td>' + c3[i] + '</td>')
		seg.write(str(int(math.floor(float(c3[i])))) + '\t')
	for i in range(len(c3)):
	    if i == 3:
		file.write('<td>' + c3[i] + '</td>')
	for i in range(len(c3)):
	    if i == 5:
		R2_GPS = str(float(c3[i]) + 3600)
		file.write('<td>' + c3[i] + '</td>') 
		tfinal = str(int(math.ceil(float(c3[2]) + (2*(float(c3[i])-float(c3[2]))))))
                dur_veto = str(int(math.ceil(2*(float(c3[i])-float(c3[2])))))
                seg.write(tfinal + '\t' + dur_veto + '\n')

        file.write('</tr>')
        file.write('<tr>')
	for i in range(len(c4)):
            if i == 13:
                file.write('<td>' + c4[i] + '</td>')

        for i in range(len(c4)):
            if i == 2:
		CESTI_time1 = float(c4[i]) + 3600
                CESTI_time1 = int(CESTI_time1)
                Pisa_title1 = commands.getstatusoutput("lalapps_tconvert --local --zone=PDT -f%%H:%%M:%%S %d" % (CESTI_time1))
                P_title1 = str(Pisa_title1)
                pisa1 = P_title1.replace(P_title1[:5], '')
                pisa_title1 = pisa1.replace(pisa1[8:], '')
                file.write('<td> %s CET </td>' % pisa_title1)

        for i in range(len(c4)):
            if i == 3:
		CESTI_time2 = float(c4[i]) + 3600
                CESTI_time2 = int(CESTI_time2)
                Pisa_title2 = commands.getstatusoutput("lalapps_tconvert --local --zone=PDT -f%%H:%%M:%%S %d" % (CESTI_time2))
                P_title2 = str(Pisa_title2)
                pisa2 = P_title2.replace(P_title2[:5], '')
                pisa_title2 = pisa2.replace(pisa2[8:], '')
                file.write('<td> %s CET </td>' % pisa_title2)


        for i in range(len(c4)):
            if i == 5:
		CESTI_time4 = float(c4[i]) + 3600
                CESTI_time4 = int(CESTI_time4)
                Pisa_title4 = commands.getstatusoutput("lalapps_tconvert --local --zone=PDT -f%%H:%%M:%%S %d" % (CESTI_time4))
                P_title4 = str(Pisa_title4)
                pisa4 = P_title4.replace(P_title4[:5], '')
                pisa_title4 = pisa4.replace(pisa4[8:], '')
                file.write('<td><b> %s CET </b></td>' % pisa_title4)

	for i in range(len(c4)):
            if i == 7:
                h7=float(c4[i]) * (10**6)
                c4[i]=str(h7)
		if h7 <= 0.1:
                    file.write('<td bgcolor="#00FF00">' + c4[i] + '</td>')
                elif h7 > 0.1 and h7 <= 0.155:
                    file.write('<td bgcolor="#FFFB00">' + c4[i] + '</td>')
                elif h7 > 0.155 and h7 < 0.5:
                    file.write('<td bgcolor="#FFA500">' + c4[i] + '</td>')
                elif h7 >= 0.5:
                    file.write('<td bgcolor="#FF0000">' + c4[i] + '</td>')
        for i in range(len(c4)):
	    if i == 12:
		h12=float(c4[i]) * (10**-3)
		c4[i]=str(h12)
		file.write('<td>' + c4[i] + '</td>')
	for i in range(len(c4)):
	    if i == 2:
		file.write('<td>' + c4[i] + '</td>')
		seg.write(str(int(math.floor(float(c4[i])))) + '\t')
	for i in range(len(c4)):
	    if i == 3:
		file.write('<td>' + c4[i] + '</td>')
	for i in range(len(c4)):
	    if i == 5:
		R3_GPS = str(float(c4[i]) + 3600)
		file.write('<td>' + c4[i] + '</td>')
		tfinal = str(int(math.ceil(float(c4[2]) + (2*(float(c4[i])-float(c4[2]))))))
                dur_veto = str(int(math.ceil(2*(float(c4[i])-float(c4[2])))))
                seg.write(tfinal + '\t' + dur_veto + '\n\n')
 
        file.write('</tr>')
        file.write('</table>')



# Main function
def main():
    #Open veto segment file.
    segment = "/home/hunter.gabbard/public_html/earthquake_mon/veto_segments.txt" 
    # Get directory to process from user via command line argument
    if len(sys.argv) < 2:
        print 'Please provide a directory to process as a command line argument.'
        print 'Example: ./earthquakes2html.py 1109300301-1110423501'
        exit(1)
    main_dir = sys.argv[1] + '/earthquakes'

    # Get list of subdirectories in earthquakes directory
    # (using a list comprehension)
    sub_dirs = [ f for f in os.listdir(main_dir)
                 if os.path.isdir(os.path.join(main_dir, f)) ]
    sub_dirs.sort(reverse=True)
    # Start HTML file
    file = start_html_file(sys.argv[1],  "/home/hunter.gabbard/public_html/earthquake_mon/html_pages/earthquakes.html")
 
    # Iterate through subdirectories
    for dir in sub_dirs:
        # Process each subdirectory, looking for earthquakes.txt
        process_sub_dir(os.path.join(main_dir, dir), file)

    # End HTML file
    end_html_file(file)


if __name__ == "__main__":
   main() 
