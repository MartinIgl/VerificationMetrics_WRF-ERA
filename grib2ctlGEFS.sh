#!/bin/bash

# Corro el arwpost
# a partir de los wrfout prono a 24hs

### initial date setting ............................
IY=2015
IM=12
ID=20
IH=00
IMN=00
### final date setting ..............................
EY=2016
EM=01
ED=05
EH=18
EMN=00
FCST=006


dir_input=/data/miglesias/GEFS_FCST12/GEFS_prono12h


#dir_execute=/home/dillon/WRFmerge

source /home/miglesias/originales/lectura_GFSGEFS/util.sh
#source /data/miglesias/GEFS_FCST12/lectura_GEFS/envvars.sh

while test $IY$IM$ID$IH -le $EY$EM$ED$EH
do


for MEM in $(seq -f "%02g" 1 20)
do
echo ${MEM}

cd $dir_input/${IY}${IM}${ID}_${IH}/${MEM}


/home/miglesias/originales/lectura_GFSGEFS/g2ctl.pl  gens_${IY}${IM}${ID}_${IH}${IMN}_${FCST}_${MEM}.grb2 > gens_${IY}${IM}${ID}_${IH}${IMN}_${FCST}_${MEM}.ctl

/usr/local/bin/gribmap -i gens_${IY}${IM}${ID}_${IH}${IMN}_${FCST}_${MEM}.ctl


done

# Listo! Paso al dia siguiente:
date_edit $IY $IM $ID $IH 00 360 > next_time.txt
read NY NM ND NH NMN < next_time.txt
 IY=$NY
 IM=$NM
 ID=$ND
 IH=$NH
 IMN=$NMN

done






