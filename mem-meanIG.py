#!/usr/bin/env python
#############################
#Funcion para calcular el spread y la medio de un ensamble de n miembros
##Martin Iglesias Github SudestadaARG
####################################

import numpy as np
import os
from datetime import datetime  
from datetime import timedelta
import argparse
import gc

# Defino argumentos para indicarle la fecha y el miembro por linea de comando:
parser = argparse.ArgumentParser(description='Year Month Day Hour FCST Exp Per')
parser.add_argument('Year',type=int)
parser.add_argument('Month',type=int)
parser.add_argument('Day',type=int)
parser.add_argument('Hour',type=int)
parser.add_argument('FCST',type=str)
parser.add_argument('Exp',type=str)

parser.add_argument('Per',type=str)
args = parser.parse_args()

periodo= args.Per

Y = args.Year
M = args.Month
D = args.Day
H = args.Hour
###SETEO el FCST, los datos que se usen estan en la fecha correspondiente al fcst

exp= args.Exp
if exp=='GFS' or exp=='GEFS':
	FCST =  '_' + args.FCST
else:
	FCST = '.' + args.FCST

# Caminos de los archivos:


if exp == 'connud':
	path_upp = '/data/miglesias/verificacion_doc/variables_WRF_UPP_interpoladas'	
	if periodo=='2meses':
		periodo='_'+periodo
	else:
		periodo=''
elif exp == 'sinnud':
	path_upp = '/data/miglesias/verificacion_doc/variables_WRF_UPP_interpoladas_sinnud'
	if periodo=='2meses':
		periodo='_'+periodo
	else:
		periodo=''
elif exp == 'spnud6h':
	path_upp = '/data/miglesias/verificacion_doc/variables_WRF_UPP_interpoladas_spnud6h'
	if periodo=='2meses':
		periodo='_'+periodo
	else:
		periodo=''
elif exp == 'spnudUV6h':
	path_upp = '/data/miglesias/verificacion_doc/variables_WRF_UPP_interpoladas_SPnudUV6h'
	if periodo=='2meses':
		periodo='_'+periodo
	else:
		periodo=''
elif exp == 'GEFS':
	path_upp = '/data/miglesias/verificacion_doc/variables_GEFS'
	if periodo=='2meses':
		periodo='_'+periodo
	else:
		periodo=''
elif exp == 'GFS':
	path_upp = '/data/miglesias/verificacion_doc/variables_GEFS/deterministico'
	if periodo=='2meses':
		periodo='_'+periodo
	else:
		periodo=''


exp=  '/' + args.Exp

path_in = '/data/miglesias/verificacion_doc/MSPWRFupp' + exp 
path_salida =  '/data/miglesias/verificacion_doc/MSPWRFupp/dif_mean_mem' + exp
 


d = datetime(Y,M,D,H)	# Listo, asi queda definida una fecha especifica

YY = str(d.year)
MM = str(d.month).zfill(2)
DD = str(d.day).zfill(2)
HH = str(d.hour).zfill(2)




if exp=='GFS':
	MEM=['01'] 
	m = 0
else:
	MEM=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17', '18','19','20'] #vector numero de miembro de ensamble
	# Ojo que M[1] = '02', acordate que python empieza a contar desde 0
	m = 0 	# hay que inicializar la m aca adentro del loop de los dias, sino sigue contando y no encuentra


vertical_levels = [1000, 975, 925, 850, 800, 700, 600, 500, 400, 300, 250, 200] # en hPa




#tomo la media del ensamble para hacer la diferencia con cada miembro
geopt_mean= np.ma.load(path_in  + '/geopt_mean_' + YY + MM + DD + HH +periodo+ FCST )	
v_mean = np.ma.load(path_in + '/v_mean_' + YY + MM + DD + HH +periodo+ FCST )	
u_mean = np.ma.load( path_in  + '/u_mean_' + YY + MM + DD + HH +periodo+ FCST)	
q_mean = np.ma.load(path_in  + '/q_mean_' + YY + MM + DD + HH +periodo+ FCST )	
tk_mean = np.ma.load(path_in  + '/tk_mean_'+ YY + MM + DD + HH +periodo+ FCST )	
psfc_mean = np.ma.load(path_in  + '/psfc_mean_' + YY + MM + DD + HH +periodo+ FCST)	

	# ----------Variables a completar en cada hora para todos los miembros

while m < len(MEM):	# m < 20
	# Nombre de fecha para abrir:
	YY = str(d.year)
	MM = str(d.month).zfill(2)
	DD = str(d.day).zfill(2)
	HH = str(d.hour).zfill(2)
	
	if exp=='/GFS':
		# ------Geopotencial------	
		geopt_M = np.ma.load(path_upp + '/geopt_GFS_' + YY + MM + DD + HH + FCST )	
		geopt_dif_mean_Mem= geopt_M - geopt_mean
		np.ma.dump(geopt_dif_mean_Mem, path_salida + '/dif_geoptMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)
	
		# ------Temperatura------
		tk_M= np.ma.load(path_upp + '/tk_GFS_' + YY + MM + DD + HH + FCST )
		tk_dif_mean_Mem= tk_M - tk_mean
		np.ma.dump(tk_dif_mean_Mem, path_salida + '/dif_tkMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)
		# ------Humedad especifica------
		q_M= np.ma.load(path_upp + '/q_GFS_' + YY + MM + DD + HH + FCST )
		q_dif_mean_Mem= q_M - q_mean
		np.ma.dump(q_dif_mean_Mem, path_salida + '/dif_qMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)
		# ------Viento: componentes U y V------
		u_M= np.ma.load(path_upp + '/u_GFS_' + YY + MM + DD + HH + FCST )
	 	u_dif_mean_Mem= u_M - u_mean
		np.ma.dump(u_dif_mean_Mem, path_salida + '/dif_uMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)
		v_M= np.ma.load(path_upp + '/v_GFS_'+ YY + MM + DD + HH + FCST )
		v_dif_mean_Mem= v_M - v_mean
		np.ma.dump(v_dif_mean_Mem, path_salida + '/dif_vMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)
		# ------PSFC------
		psfc_M= np.ma.load(path_upp + '/psfc_GFS_'+ YY + MM + DD + HH + FCST )
		psfc_dif_mean_Mem= psfc_M - psfc_mean
		np.ma.dump(psfc_dif_mean_Mem, path_salida + '/dif_psfcMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)

	elif exp=='/GEFS':
		# ------Geopotencial------	
		geopt_M = np.ma.load(path_upp + '/' + MEM[m] + '/geopt_gefs_' + YY + MM + DD + HH + FCST )	

		geopt_dif_mean_Mem= geopt_M - geopt_mean

		np.ma.dump(geopt_dif_mean_Mem, path_salida + '/' + MEM[m] + '/dif_geoptMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)
	
		# ------Temperatura------
		tk_M= np.ma.load(path_upp + '/' + MEM[m] + '/tk_gefs_' + YY + MM + DD + HH + FCST )
		tk_dif_mean_Mem= tk_M - tk_mean
		np.ma.dump(tk_dif_mean_Mem, path_salida + '/' + MEM[m] + '/dif_tkMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)
		# ------Humedad especifica------
		q_M= np.ma.load(path_upp + '/' + MEM[m] + '/q_gefs_' + YY + MM + DD + HH + FCST )
		q_dif_mean_Mem= q_M - q_mean
		np.ma.dump(q_dif_mean_Mem, path_salida + '/' + MEM[m] + '/dif_qMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)
		# ------Viento: componentes U y V------
		u_M= np.ma.load(path_upp + '/' + MEM[m] + '/u_gefs_' + YY + MM + DD + HH + FCST )
 		u_dif_mean_Mem= u_M - u_mean
		np.ma.dump(u_dif_mean_Mem, path_salida + '/' + MEM[m] + '/dif_uMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)
		v_M= np.ma.load(path_upp + '/' + MEM[m] + '/v_gefs_'+ YY + MM + DD + HH + FCST )
		v_dif_mean_Mem= v_M - v_mean
		np.ma.dump(v_dif_mean_Mem, path_salida + '/' + MEM[m] + '/dif_vMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)
		# ------PSFC------
		psfc_M= np.ma.load(path_upp + '/' + MEM[m] + '/psfc_gefs_'+ YY + MM + DD + HH + FCST )
		psfc_dif_mean_Mem= psfc_M - psfc_mean
		np.ma.dump(psfc_dif_mean_Mem, path_salida + '/' + MEM[m] + '/dif_psfcMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)

	else:
		# ------Geopotencial------	
		geopt_M = np.ma.load(path_upp + '/' + MEM[m] + '/geopt_upp_' + YY + MM + DD + HH + FCST )	

		geopt_dif_mean_Mem= geopt_M - geopt_mean

		np.ma.dump(geopt_dif_mean_Mem, path_salida + '/' + MEM[m] + '/dif_geoptMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)
	
		# ------Temperatura------
		tk_M= np.ma.load(path_upp + '/' + MEM[m] + '/tk_upp_' + YY + MM + DD + HH + FCST )
		tk_dif_mean_Mem= tk_M - tk_mean
		np.ma.dump(tk_dif_mean_Mem, path_salida + '/' + MEM[m] + '/dif_tkMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)
		# ------Humedad especifica------
		q_M= np.ma.load(path_upp + '/' + MEM[m] + '/q_upp_' + YY + MM + DD + HH + FCST )
		q_dif_mean_Mem= q_M - q_mean
		np.ma.dump(q_dif_mean_Mem, path_salida + '/' + MEM[m] + '/dif_qMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)
		# ------Viento: componentes U y V------
		u_M= np.ma.load(path_upp + '/' + MEM[m] + '/u_upp_' + YY + MM + DD + HH + FCST )
	 	u_dif_mean_Mem= u_M - u_mean
		np.ma.dump(u_dif_mean_Mem, path_salida + '/' + MEM[m] + '/dif_uMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)
		v_M= np.ma.load(path_upp + '/' + MEM[m] + '/v_upp_'+ YY + MM + DD + HH + FCST )
		v_dif_mean_Mem= v_M - v_mean
		np.ma.dump(v_dif_mean_Mem, path_salida + '/' + MEM[m] + '/dif_vMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)
		# ------PSFC------
		psfc_M= np.ma.load(path_upp + '/' + MEM[m] + '/psfc_upp_'+ YY + MM + DD + HH + FCST )
		psfc_dif_mean_Mem= psfc_M - psfc_mean
		np.ma.dump(psfc_dif_mean_Mem, path_salida + '/' + MEM[m] + '/dif_psfcMEM-mean_' + YY + MM + DD + HH +periodo+ FCST)

	geopt_M = 0
	v_M = 0
	u_M = 0
	q_M = 0
	tk_M = 0
	psfc_M = 0

	geopt_dif_mean_Mem = 0
	v_dif_mean_Mem = 0
	u_dif_mean_Mem = 0
	q_dif_mean_Mem = 0
	tk_dif_mean_Mem = 0
	psfc_dif_mean_Mem = 0



	gc.collect()	# Saca la basura de la memoria
	m = m + 1	# Loop de los miembros


