#! /bin/sh
#Calibrate voltages from custom probe boxes for range of shots - all shots in range will be used as input to the CalibrateBoxVoltages.py script.
#Usage: process_range_of_shots startShot endShot
#startShot = integer argument - shot num
#endShot = integer argument - shot num
#Ted Golfinopoulos, 23 Apr 2012

#Loop through shots in each range
#for ((s=${shotRangeStart[i]}; s<=${shotRangeStop[i]}; s++))
for ((s=$1; s<=$2; s++))
do
	#Setup necessary nodes for shot.
	#python SetupCalibrationNodes.py $s
	#Call process_shoelace script on shot.
	python CalibrateBoxVoltages.py $s
done

