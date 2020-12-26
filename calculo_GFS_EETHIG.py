#!/usr/bin/env python
#Martin Iglesias Github SudestadaARG
# Programa para calcular el error total de energia humedad usando una funcion previamente definida
#
# Voy a necesitar:
#
# -- Las diferencias de las variables de sfc que fueron almacenadas asi:
#	np.ma.dump(dif_psfc[190:300,519:679], nombre)
#    o sea dimension (110,160)
#
# -- Las diferencias de las variables por niveles que fueron almacenadas asi:
#	np.ma.dump(dif_geopt[:,190:300,519:679], nombre)
#    o sea dimension (12,110,160) 
#

##hecho solo para el FCST de 12utc, falta revisar para los otros tiempos
import numpy as np
import os
from datetime import datetime
from datetime import timedelta
import argparse
import gc
from error_energiaIG import error_energia_total_humeda


parser = argparse.ArgumentParser(description='Year Month Day Hour FCST Exp')
parser.add_argument('Year',type=int)
parser.add_argument('Month',type=int)
parser.add_argument('Day',type=int)
parser.add_argument('Hour',type=int)
parser.add_argument('FCST',type=str)
parser.add_argument('Exp',type=str)
args = parser.parse_args()


Y = args.Year
M = args.Month
D = args.Day
H = args.Hour
EXP = args.Exp
###SETEO el FCST, los datos que se usen estan en la fecha correspondiente al fcst
FCST = '_' + args.FCST


if EXP == 'GFS':
	exp = '/GFS' 
	path_in = '/data/miglesias/verificacion_doc/dif_ERA_GEFS' + exp 
	path_out = '/data/miglesias/verificacion_doc/dif_ERA_GEFS/ErrorEnergiaTotalHumeda' + exp
else:
	quit()


d = datetime(Y,M,D,H)

# Nombre de fecha para abrir:
YY = str(d.year)
MM = str(d.month).zfill(2)
DD = str(d.day).zfill(2)
HH = str(d.hour).zfill(2)
		
udif = np.ma.load( path_in +  '/u_dif_era-gfs_' + YY + MM + DD + HH + FCST)
vdif = np.ma.load( path_in +  '/v_dif_era-gfs_' + YY + MM + DD + HH + FCST)
tdif = np.ma.load( path_in +  '/tk_dif_era-gfs_' + YY + MM + DD + HH + FCST)
pdif = np.ma.load( path_in +  '/psfc_dif_era-gfs_' + YY + MM + DD + HH + FCST)
qdif = np.ma.load( path_in +  '/q_dif_era-gfs_' + YY + MM + DD + HH + FCST)

(cinetica, temp, psup, humedad, EETH ) = error_energia_total_humeda(udif,vdif,tdif,pdif,qdif,1)
#	me devuelve todo esto y puedo llamarlo por separado despues

np.ma.dump(cinetica, path_out +  '/cinetica_GFS_'+ YY + MM + DD + HH + FCST)
np.ma.dump(temp, path_out +  '/temp_GFS_'+ YY + MM + DD + HH + FCST)
np.ma.dump(psup, path_out +  '/psup_GFS_'+ YY + MM + DD + HH + FCST)
np.ma.dump(humedad, path_out +  '/humedad_GFS_'+ YY + MM + DD + HH + FCST)
np.ma.dump(EETH, path_out +  '/EETH_GFS_'+ YY + MM + DD + HH +  FCST)
	

udif = 0
vdif = 0
tdif = 0
pdif = 0
qdif = 0
cinetica = 0
temp = 0
psup = 0
humedad = 0
EETH = 0
gc.collect() # Saca la basura de la memoria
