#!/bin/bash
#Script that produces earthquake arrival time information for the LIGO detectors.
#Author: Hunter Gabbard
#Date: 16/04/2015

#Calculating today's date...
rm -r /home/hunter.gabbard/public_html/earthquake_mon/most_recent_run
rm -r /home/hunter.gabbard/public_html/earthquake_mon/most_recent_iris
rm -r /home/hunter.gabbard/public_html/earthquake_mon/iris
rm -r /home/hunter.gabbard/public_html/earthquake_mon/recentSEISMONINFO

#source /home/hunter.gabbard/earthquake_mon/seismon/bin
time=$(lalapps_tconvert now)
#Below is where you can make changes to run over and archive a specific day.
#If you want a full day...use 86400 for both. This is just for a half day.
subtract_v=43200
let "start_time = $time - $subtract_v"
subtract_hour=43200
let "start_hour = $time - $subtract_hour"


#Copying relevant directories....
cp -r /home/mcoughlin/Seismon/publicdata /home/hunter.gabbard/Seismon_folders
cp -r /home/mcoughlin/Seismon/databasedata /home/hunter.gabbard/Seismon_folders
cp -r /home/mcoughlin/Seismon/velocity_maps /home/hunter.gabbard/Seismon_folders

. /home/hunter.gabbard/opt/gwpysoft/bin/activate
#Running earthquake monitoring code...
mkdir /home/hunter.gabbard/public_html/earthquake_mon/iris
mkdir /home/hunter.gabbard/public_html/earthquake_mon/public
python /home/hunter.gabbard/seismon/bin/seismon_traveltimes --paramsFile /home/hunter.gabbard/Seismon_folders/seismon/bin/seismon_params_traveltimes.txt --paramsFileCopy /home/hunter.gabbard/Seismon_folders/seismon/bin/seismon_params_traveltimes_copy.txt --doPrivate --doIRIS --publicFileType day -m 3.0 -s $start_time -e $time
#Making updated directory...
mkdir /home/hunter.gabbard/public_html/earthquake_mon/most_recent_run
mkdir /home/hunter.gabbard/public_html/earthquake_mon/run_$time
mv /home/hunter.gabbard/public_html/earthquake_mon/public /home/hunter.gabbard/public_html/earthquake_mon/old_runs/run_$time
cp -r /home/hunter.gabbard/public_html/earthquake_mon/old_runs/run_$time /home/hunter.gabbard/public_html/earthquake_mon/most_recent_run
rm -r /home/hunter.gabbard/public_html/earthquake_mon/run_$time

##########################################################################################################################################################################################

#Iris stuff...
mkdir /home/hunter.gabbard/public_html/earthquake_mon/most_recent_iris
mkdir /home/hunter.gabbard/public_html/earthquake_mon/iris_old/iris_$time
cp -r /home/hunter.gabbard/public_html/earthquake_mon/iris/*.xml /home/hunter.gabbard/public_html/earthquake_mon/iris_old/iris_$time
cp -r /home/hunter.gabbard/public_html/earthquake_mon/iris/*.xml /home/hunter.gabbard/Seismon_folders/eventfiles/iris
cp -r /home/hunter.gabbard/public_html/earthquake_mon/iris_old/iris_$time/*.xml /home/hunter.gabbard/public_html/earthquake_mon/most_recent_iris

###########################################################################################################################################################################################

#Running Seismon_info
#removed Seismon_folders/seismon
python /home/hunter.gabbard/seismon/bin/seismon_info -p /home/hunter.gabbard/Seismon_folders/seismon/bin/seismon_params_H1EQMon.txt --doEarthquakes --eventfilesType iris -s $start_hour -e $time

mkdir /home/hunter.gabbard/public_html/earthquake_mon/recentSEISMONINFO
mv /home/hunter.gabbard/Seismon_folders/all/H1EQMon/$start_hour-$time /home/hunter.gabbard/public_html/earthquake_mon/recentSEISMONINFO/$start_hour-$time
cp -r /home/hunter.gabbard/public_html/earthquake_mon/recentSEISMONINFO/$start_hour-$time /home/hunter.gabbard/public_html/earthquake_mon/past_seismon_info_run 

#####################################################################################################################################################################

#Running python html code...
rm -r /home/hunter.gabbard/public_html/earthquake_mon/html_pages
mkdir /home/hunter.gabbard/public_html/earthquake_mon/html_pages
python /home/hunter.gabbard/Seismon_folders/seismon/bin/earthquakes2html.py /home/hunter.gabbard/public_html/earthquake_mon/recentSEISMONINFO/$start_hour-$time

mv /home/hunter.gabbard/public_html/earthquake_mon/recentSEISMONINFO/$start_hour-$time/earthquakes/earthquakes.html /home/hunter.gabbard/public_html/earthquake_mon/recentSEISMONINFO

deactivate
