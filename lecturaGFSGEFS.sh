#!/bin/bash

################falta un dia del GFS!!!!!!! *falta un dato 2016 01 xx 18utc

# Corro el arwpost
# a partir de los wrfout prono a 24hs

### initial date setting ............................
IY=2015
IM=12
ID=20
IH=12
IMN=00
### final date setting ..............................
EY=2016
EM=01
ED=02
EH=12
EMN=00

FCST=006
#012,006, 000

dir_input1=/data/miglesias/GEFS_FCST12/GEFS_prono12h
#dir_input2=/data/miglesias/GFS_FCST12/


source /home/miglesias/originales/lectura_GFSGEFS/util.sh
#source /data/miglesias/GEFS_FCST12/lectura_GEFS/envvars.sh

while test $IY$IM$ID$IH -le $EY$EM$ED$EH
do


for MEM in $(seq -f "%02g" 1 20)
do

cd $dir_input1/${IY}${IM}${ID}_${IH}/${MEM}

/home/miglesias/originales/lectura_GFSGEFS/obtengo_variables_GEFS.py ${IY} ${IM} ${ID} ${IH} ${MEM} ${FCST}

done

#cd $dir_input1/

#/home/miglesias/originales/lectura_GFSGEFS/gfs_obtengo_variables.py ${IY} ${IM} ${ID} ${IH} ${FCST}




# Listo! Paso al dia siguiente:
date_edit $IY $IM $ID $IH 00 360 > next_time.txt
read NY NM ND NH NMN < next_time.txt
 IY=$NY
 IM=$NM
 ID=$ND
 IH=$NH
 IMN=$NMN

done






