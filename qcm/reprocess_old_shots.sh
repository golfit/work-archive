#! /bin/sh
#This script contains a list of shots to re-process - it runs the process_shoelace.sh script on those shots.
#The shots are specified in start/stop ranges, and the process_range_of_shots.sh script is used.
#Usage:
#reprocess_old_shots.sh
#No arguments
#Ted Golfinopoulos, 21 Feb 2012

#Ranges of shots for which shoelace antenna is run
shotRangeStart=(1120105011 1120211900 1120212903 1120213014 1120213800 1120214027)
shotRangeStop=(1120105020 1120211902 1120212918 1120213018 1120213803 1120214032)

for ((i=0; i<${#shotRangeStart[*]}; i++))
do
	bash process_range_of_shots.sh ${shotRangeStart[i]} ${shotRangeStop[i]}
done

