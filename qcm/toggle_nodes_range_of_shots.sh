#! /bin/sh
#Go through range of shots, toggling shoelace:ant_v, ant_i, src_v, and src_i nodes (i.e. when antenna is changing from pickup to active mode)
#Usage: toggle_nodes_range_of_shots startShot endShot
#startShot = integer argument - shot num
#endShot = integer argument - shot num
#Ted Golfinopoulos, 23 Apr 2012

#Loop through shots in each range
#Toggle nodes for shot range
python toggleAntPowerNodes.py $1 $2

