#! /bin/sh
#Process timebase error information after shot

firstShot=$1
expectedArgs=2

if [ $# = $expectedArgs ]; then
	lastShot=$2
else
	lastShot=$1
fi

for ((s=firstShot; s<=lastShot; s++))
do
	#Process corrected timebase for magnetics and PCI
	python /home/golfit/python/versionControlled/trunk/magnetics/timebase_store_mag.py $s
	python /home/golfit/python/versionControlled/trunk/magnetics/timebase_store_pci.py $s

	#Extract timebase information from timebases and store in timebaseErrorSurvey.txt.
	python /home/golfit/python/versionControlled/trunk/qcm/getTimebaseData.py $s
done

