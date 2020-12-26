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


parser = argparse.ArgumentParser(description='Year Month Day Hour Exp')
parser.add_argument('Year',type=int)
parser.add_argument('Month',type=int)
parser.add_argument('Day',type=int)
parser.add_argument('Hour',type=int)
parser.add_argument('Exp',type=str)
args = parser.parse_args()


Y = args.Year
M = args.Month
D = args.Day
H = args.Hour
EXP = args.Exp
###SETEO el FCST, los datos que se usen estan en la fecha correspondiente al fcst
ANA = '.000'


if EXP == 'connud':
	exp = '/connud'
	path_in = '/data/miglesias/verificacion_doc/dif_ERA_WRFupp' + exp 
	path_out = '/data/miglesias/verificacion_doc/dif_ERA_WRFupp/ErrorEnergiaTotalHumeda' + exp
elif EXP == 'sinnud':
	exp = '/sinnud'
	path_in = '/data/miglesias/verificacion_doc/dif_ERA_WRFupp' + exp 
	path_out = '/data/miglesias/verificacion_doc/dif_ERA_WRFupp/ErrorEnergiaTotalHumeda' + exp
elif EXP == 'spnud6h':
	exp = '/spnud6h'
	path_in = '/data/miglesias/verificacion_doc/dif_ERA_WRFupp' + exp 
	path_out = '/data/miglesias/verificacion_doc/dif_ERA_WRFupp/ErrorEnergiaTotalHumeda' + exp
elif EXP == 'spnudUV6h':
	exp = '/spnudUV6h'
	path_in = '/data/miglesias/verificacion_doc/dif_ERA_WRFupp' + exp 
	path_out = '/data/miglesias/verificacion_doc/dif_ERA_WRFupp/ErrorEnergiaTotalHumeda' + exp
else:
	quit()


d = datetime(Y,M,D,H)

M=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17', '18','19','20'] #vector numero de miembro de ensamble
#m=0	# Ojo que M[1] = '02', acordate que python empieza a contar desde 0

m = 0 	# hay que inicializar la m aca adentro del loop de los dias, sino sigue contando y no encuentra

while m < len(M):	# m < 20
	
	# Nombre de fecha para abrir:
	YY = str(d.year)
	MM = str(d.month).zfill(2)
	DD = str(d.day).zfill(2)
	HH = str(d.hour).zfill(2)
		

	udif = np.ma.load( path_in + '/' + M[m] + '/u_dif_era-upp_' + YY + MM + DD + HH + '_ana' + ANA )
	vdif = np.ma.load( path_in + '/' + M[m] +  '/v_dif_era-upp_' + YY + MM + DD + HH + '_ana' + ANA )
	tdif = np.ma.load( path_in + '/' + M[m] +  '/tk_dif_era-upp_' + YY + MM + DD + HH + '_ana' + ANA )
	pdif = np.ma.load( path_in + '/' + M[m] +  '/psfc_dif_era-upp_' + YY + MM + DD + HH + '_ana' + ANA )
	qdif = np.ma.load( path_in + '/' + M[m] +  '/q_dif_era-upp_'  + YY + MM + DD + HH + '_ana' + ANA )

	(cinetica, temp, psup, humedad, EETH ) = error_energia_total_humeda(udif,vdif,tdif,pdif,qdif,1)
#	me devuelve todo esto y puedo llamarlo por separado despues

	np.ma.dump(cinetica, path_out + '/' + M[m] + '/cinetica_'+ YY + MM + DD + HH + '_ana' + ANA )
	np.ma.dump(temp, path_out + '/' + M[m] + '/temp_'+ YY + MM + DD + HH + '_ana' + ANA )
	np.ma.dump(psup, path_out + '/' + M[m] + '/psup_'+ YY + MM + DD + HH + '_ana' + ANA )
	np.ma.dump(humedad, path_out + '/' + M[m] + '/humedad_'+ YY + MM + DD + HH + '_ana' + ANA )
	np.ma.dump(EETH, path_out + '/' + M[m] + '/EETH_'+ YY + MM + DD + HH + '_ana' + ANA )
		

	m = m + 1	# Loop de los miembros

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


