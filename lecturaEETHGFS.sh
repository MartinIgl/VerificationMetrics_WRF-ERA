#!/bin/bash

### initial date setting ............................
IY=2015
IM=12
ID=01
IH=12
IMN=00

### final date setting ..............................
EY=2016
EM=01
ED=31
EH=18
EMN=00
Per="2meses"
FCST=000
#012,006, 000 (aca se activan los scripts de Ana)

#spnudUV6h, sinnud , spnud6h, spnudUV6h  cuando cambies de experimento luego de hacer los tres FCST comenta los GEFS y GFS para no hacerlos de nuevo!!!!!!!!!!!!!!!!!!!


source /home/miglesias/originales/lectura_GFSGEFS/util.sh
while test $IY$IM$ID$IH -le $EY$EM$ED$EH
do

###Calculo diferencias Exp-ERA
/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_diferencias_GFS.py ${IY} ${IM} ${ID} ${IH} ${FCST} GFS

#/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_diferencias_GEFS.py ${IY} ${IM} ${ID} ${IH} ${FCST} GEFS

#########Calculo EETH Exp

#/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_GEFS_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GEFS
/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_GFS_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GFS



if [[ $IY$IM$ID$IH == $EY$EM$ED$EH ]] 
then 
#########Calculo promedio de EETH EXp
#/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_promedios_GEFS_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GEFS ${Per}

/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_promedios_GFS_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GFS ${Per}

###########Calculo el promedio de los terminos de EETH EXP
#/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_promedios_GEFS_terminos_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GEFS ${Per}

/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_promedios_GFS_terminos_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GFS ${Per}



fi
# Listo! Paso al dia siguiente:
date_edit $IY $IM $ID $IH 00 360 > next_time.txt
read NY NM ND NH NMN < next_time.txt
 IY=$NY
 IM=$NM
 ID=$ND
 IH=$NH
 IMN=$NMN

done



##############################


### initial date setting ............................
IY=2015
IM=12
ID=01
IH=12
IMN=00

### final date setting ..............................
EY=2016
EM=01
ED=31
EH=18
EMN=00
Per="2meses"
FCST=006
#012,006, 000 (aca se activan los scripts de Ana)

#spnudUV6h, sinnud , spnud6h, spnudUV6h  cuando cambies de experimento luego de hacer los tres FCST comenta los GEFS y GFS para no hacerlos de nuevo!!!!!!!!!!!!!!!!!!!


source /home/miglesias/originales/lectura_GFSGEFS/util.sh
while test $IY$IM$ID$IH -le $EY$EM$ED$EH
do

###Calculo diferencias Exp-ERA
/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_diferencias_GFS.py ${IY} ${IM} ${ID} ${IH} ${FCST} GFS

#/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_diferencias_GEFS.py ${IY} ${IM} ${ID} ${IH} ${FCST} GEFS

#########Calculo EETH Exp

#/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_GEFS_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GEFS

/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_GFS_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GFS



if [[ $IY$IM$ID$IH == $EY$EM$ED$EH ]] 
then 
#########Calculo promedio de EETH EXp
#/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_promedios_GEFS_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GEFS ${Per}

/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_promedios_GFS_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GFS ${Per}


###########Calculo el promedio de los terminos de EETH EXP

#/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_promedios_GEFS_terminos_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GEFS ${Per}

/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_promedios_GFS_terminos_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GFS ${Per}


fi
# Listo! Paso al dia siguiente:
date_edit $IY $IM $ID $IH 00 360 > next_time.txt
read NY NM ND NH NMN < next_time.txt
 IY=$NY
 IM=$NM
 ID=$ND
 IH=$NH
 IMN=$NMN

done

###########################
### initial date setting ............................
IY=2015
IM=12
ID=01
IH=12
IMN=00

### final date setting ..............................
EY=2016
EM=01
ED=31
EH=18
EMN=00
Per="2meses"

FCST=012
#012,006, 000 (aca se activan los scripts de Ana)

#spnudUV6h, sinnud , spnud6h, spnudUV6h  cuando cambies de experimento luego de hacer los tres FCST comenta los GEFS y GFS para no hacerlos de nuevo!!!!!!!!!!!!!!!!!!!


source /home/miglesias/originales/lectura_GFSGEFS/util.sh
while test $IY$IM$ID$IH -le $EY$EM$ED$EH
do

###Calculo diferencias Exp-ERA
/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_diferencias_GFS.py ${IY} ${IM} ${ID} ${IH} ${FCST} GFS

#/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_diferencias_GEFS.py ${IY} ${IM} ${ID} ${IH} ${FCST} GEFS

#########Calculo EETH Exp

#/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_GEFS_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GEFS

/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_GFS_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GFS



if [[ $IY$IM$ID$IH == $EY$EM$ED$EH ]] 
then 
#########Calculo promedio de EETH EXp
#/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_promedios_GEFS_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GEFS ${Per}

/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_promedios_GFS_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GFS ${Per}


###########Calculo el promedio de los terminos de EETH EXP
#/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_promedios_GEFS_terminos_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GEFS ${Per}

/home/miglesias/originales/Calculoestadisticos/calculoenergia/calculo_promedios_GFS_terminos_EETHIG.py ${IY} ${IM} ${ID} ${IH} ${FCST} GFS ${Per}

fi
# Listo! Paso al dia siguiente:
date_edit $IY $IM $ID $IH 00 360 > next_time.txt
read NY NM ND NH NMN < next_time.txt
 IY=$NY
 IM=$NM
 ID=$ND
 IH=$NH
 IMN=$NMN

done

