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


parser = argparse.ArgumentParser(description='Exp')
parser.add_argument('Exp',type=str)
args = parser.parse_args()



exp = args.Exp


path_in = '/data/miglesias/verificacion_CE/dif_ERA_WRFupp/' + exp 
path_out = '/data/miglesias/verificacion_CE/dif_ERA_WRFupp/ErrorEnergiaTotalHumeda/' + exp



M=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17', '18','19','20'] #vector numero de miembro de ensamble
#m=0	# Ojo que M[1] = '02', acordate que python empieza a contar desde 0

m = 0 	# hay que inicializar la m aca adentro del loop de los dias, sino sigue contando y no encuentra

day=datetime(2015,12,19,00)
delta = timedelta(hours=6)
i=0
f=17
while i <= f:
	m = 0
	# Nombre de fecha para abrir:
	YY = str(day.year)
	MM = str(day.month).zfill(2)
	DD = str(day.day).zfill(2)
	HH = str(day.hour).zfill(2)
		
	while m < len(M):	# m < 20
		udif = np.ma.load( path_in + '/' + M[m] +  '/u_dif_era-upp_' + YY + MM + DD + HH )
		vdif = np.ma.load( path_in + '/' + M[m] +  '/v_dif_era-upp_' + YY + MM + DD + HH )
		tdif = np.ma.load( path_in + '/' + M[m] +  '/tk_dif_era-upp_' + YY + MM + DD + HH )
		pdif = np.ma.load( path_in + '/' + M[m] +  '/psfc_dif_era-upp_' + YY + MM + DD + HH)
		qdif = np.ma.load( path_in + '/' + M[m] +  '/q_dif_era-upp_'  + YY + MM + DD + HH )

		(cinetica, temp, psup, humedad, EETH ) = error_energia_total_humeda(udif,vdif,tdif,pdif,qdif,1)
#	me devuelve todo esto y puedo llamarlo por separado despues

		np.ma.dump(cinetica, path_out + '/' + M[m] + '/CE_cinetica_'+ YY + MM + DD + HH)
		np.ma.dump(temp, path_out + '/' + M[m] + '/CE_temp_'+ YY + MM + DD + HH)
		np.ma.dump(psup, path_out + '/' + M[m] + '/CE_psup_'+ YY + MM + DD + HH)
		np.ma.dump(humedad, path_out + '/' + M[m] + '/CE_humedad_'+ YY + MM + DD + HH)
		np.ma.dump(EETH, path_out + '/' + M[m] + '/CE_EETH_'+ YY + MM + DD + HH )
		
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
		m = m + 1	# Loop de los miembros


	day = day + delta
	i=i+1
