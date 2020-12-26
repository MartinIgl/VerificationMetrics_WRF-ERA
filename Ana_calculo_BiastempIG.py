#!/usr/bin/env python
#Martin Iglesias Github SudestadaARG
# Programa para calcular el Bias, usando matrices diferencia hechas previamente

# Voy a necesitar:
#
# -- Las diferencias de las variables de sfc que fueron almacenadas asi:
#       np.ma.dump(dif_psfc[190:300,519:679], nombre)
#    o sea dimension (110,160)
#
# -- Las diferencias de las variables por niveles que fueron almacenadas asi:
#       np.ma.dump(dif_geoptc[:,20:103,31:122], nombre)
#    o sea dimension (12,110,160) 


import numpy as np
import os
from datetime import datetime
from datetime import timedelta

import argparse
import gc


# Defino argumentos para indicarle la fecha y el miembro por linea de comando:
parser = argparse.ArgumentParser(description='Year Month Day Hour Exp Per')
parser.add_argument('Year',type=int)
parser.add_argument('Month',type=int)
parser.add_argument('Day',type=int)
parser.add_argument('Hour',type=int)
parser.add_argument('Exp',type=str)
parser.add_argument('Per',type=str)
args = parser.parse_args()
periodo=args.Per
Y = args.Year
Mo = args.Month
D = args.Day
H = args.Hour

d = datetime(Y,Mo,D,H)
delta = timedelta(hours=24)
if periodo=='10dias':
	diafin = datetime(2015,12,10,00)
elif periodo=='2meses':
	diafin = datetime(2016,01,31,18)

###SETEO el ANA, los datos que se usen estan en la fecha correspondiente al ANA

exp =  '/' + args.Exp #'/sinnud' #'/spnudUV6h'#'/spnud6h'

date = str(args.Hour).zfill(2) + 'z' #'06Z' '12Z' '18Z''00Z'

# Caminos de los archivos:
if exp == '/GFS' or exp == '/GEFS':
	path_in = '/data/miglesias/verificacion_doc/dif_ERA_GEFS' + exp 
	path_out = '/data/miglesias/verificacion_doc/dif_ERA_GEFS/BIAS'+ exp
	ANA =  '_000'
else:
	path_in = '/data/miglesias/verificacion_doc/dif_ERA_WRFupp' + exp 
	path_out = '/data/miglesias/verificacion_doc/dif_ERA_WRFupp/BIAS'+ exp
	ANA =  '.000'


M=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17', '18','19','20'] #vector numero de miembro de ensamble
#m=0	# Ojo que M[1] = '02', acordate que python empieza a contar desde 0



#Entonces wrfprs01_20151219_12.000 verifica con miembro YY el 2015121912 hora XX de analisis y pronostico 0XX

# Calculo cuantos registros de tiempo voy a tener, para poder definir la dimension del array:
# Ojo si cambio esto, cambiar el nombre del archivo para guardar
#tiempos = 1 + timedelta.total_seconds(diafin-d)/21600		# timedelta 6h
tiempos = 1 + timedelta.total_seconds(diafin-d)/86400		# timedelta 24h

m = 0 	# hay que inicializar la m aca adentro del loop de los dias, sino sigue contando y no encuentra
	

contador = 0
while m < len(M):

	
	geo_total = np.ma.empty(( tiempos, 12, 83, 91 )) #dominio de grafico
	u_total = np.ma.empty(( tiempos, 12, 83, 91 ))
	v_total = np.ma.empty(( tiempos, 12, 83, 91 ))
	t_total = np.ma.empty(( tiempos, 12, 83, 91 ))
	q_total = np.ma.empty(( tiempos, 12, 83, 91 ))
	psfc_total = np.ma.empty(( tiempos, 12, 83, 91 ))
	contador = -1
	d = datetime(Y,Mo,D,H)
	while d <= diafin:	
		contador = contador + 1
		# Nombre de fecha para abrir:
		YY = str(d.year)
		MM = str(d.month).zfill(2)
		DD = str(d.day).zfill(2)
		HH = str(d.hour).zfill(2)
		
		if exp == '/GEFS':
			udif = np.ma.load( path_in + '/' + M[m] + '/u_dif_era-gefs_' + YY + MM + DD + HH + '_ana' + ANA)
			vdif = np.ma.load( path_in + '/' + M[m] +  '/v_dif_era-gefs_' + YY + MM + DD + HH + '_ana' + ANA)
			tdif = np.ma.load( path_in + '/' + M[m] +  '/tk_dif_era-gefs_' + YY + MM + DD + HH + '_ana' + ANA)
			pdif = np.ma.load( path_in + '/' + M[m] +  '/psfc_dif_era-gefs_' + YY + MM + DD + HH + '_ana' + ANA)
			qdif = np.ma.load( path_in + '/' + M[m] +  '/q_dif_era-gefs_'  + YY + MM + DD + HH + '_ana' + ANA)
			geodif = np.ma.load( path_in + '/' + M[m] + '/geopt_dif_era-gefs_' + YY + MM + DD + HH + '_ana' + ANA)
		elif exp == '/GFS':
			udif = np.ma.load( path_in + '/' + M[m] + '/u_dif_era-gfs_' + YY + MM + DD + HH + '_ana' + ANA)
			vdif = np.ma.load( path_in + '/' + M[m] +  '/v_dif_era-gfs_' + YY + MM + DD + HH + '_ana' + ANA)
			tdif = np.ma.load( path_in + '/' + M[m] +  '/tk_dif_era-gfs_' + YY + MM + DD + HH + '_ana' + ANA)
			pdif = np.ma.load( path_in + '/' + M[m] +  '/psfc_dif_era-gfs_' + YY + MM + DD + HH + '_ana' + ANA)
			qdif = np.ma.load( path_in + '/' + M[m] +  '/q_dif_era-gfs_'  + YY + MM + DD + HH + '_ana' + ANA)
			geodif = np.ma.load( path_in + '/' + M[m] + '/geopt_dif_era-gfs_' + YY + MM + DD + HH + '_ana' + ANA)
		else:
			udif = np.ma.load( path_in + '/' + M[m] + '/u_dif_era-upp_' + YY + MM + DD + HH + '_ana' + ANA)
			vdif = np.ma.load( path_in + '/' + M[m] +  '/v_dif_era-upp_' + YY + MM + DD + HH + '_ana' + ANA)
			tdif = np.ma.load( path_in + '/' + M[m] +  '/tk_dif_era-upp_' + YY + MM + DD + HH + '_ana' + ANA)
			pdif = np.ma.load( path_in + '/' + M[m] +  '/psfc_dif_era-upp_' + YY + MM + DD + HH + '_ana' + ANA)
			qdif = np.ma.load( path_in + '/' + M[m] +  '/q_dif_era-upp_'  + YY + MM + DD + HH + '_ana' + ANA)
			geodif = np.ma.load( path_in + '/' + M[m] + '/geopt_dif_era-upp_' + YY + MM + DD + HH + '_ana' + ANA)


        	geo_total[contador,:,:,:] = geodif[:,20:103,31:122]
        	u_total[contador,:,:,:] = udif[:,20:103,31:122]
		v_total[contador,:,:,:] = vdif[:,20:103,31:122]
        	t_total[contador,:,:,:] = tdif[:,20:103,31:122]
		q_total[contador,:,:,:] = qdif[:,20:103,31:122]
		psfc_total[contador,:,:] = pdif[20:103,31:122]

		d = d + delta
	# ----------------------------------------------------------
	# Considerando todos los niveles: calculo el promedio del BIAS
	bias_geo = np.ma.mean(geo_total, axis = (0))
	bias_u = np.ma.mean(u_total, axis = (0))
	bias_v = np.ma.mean(v_total, axis = (0))
	bias_t = np.ma.mean(t_total, axis = (0))
	bias_q = np.ma.mean(q_total, axis = (0))
	bias_psfc = np.ma.mean(psfc_total, axis = (0))


	if exp == '/GEFS':
		np.ma.dump(bias_geo, path_out+ '/' + M[m] + '/bias_geo_' + date + '_M'+ M[m]+'_'+periodo + '_ana' +  ANA)
		np.ma.dump(bias_u, path_out + '/' + M[m] + '/bias_u_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_v, path_out + '/' + M[m] + '/bias_v_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_t, path_out + '/' + M[m] + '/bias_t_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_q, path_out + '/' + M[m] + '/bias_q_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_psfc, path_out + '/' + M[m] +  '/bias_psfc_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
	elif exp == '/GFS':
		np.ma.dump(bias_geo, path_out + '/bias_geo_' + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_u, path_out + '/bias_u_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_v, path_out + '/bias_v_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_t, path_out + '/bias_t_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_q, path_out + '/bias_q_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_psfc, path_out + '/bias_psfc_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
	else:
		np.ma.dump(bias_geo, path_out + '/' + M[m] + '/bias_geo_' + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_u, path_out + '/' + M[m] + '/bias_u_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_v, path_out + '/' + M[m] + '/bias_v_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_t, path_out + '/' + M[m] + '/bias_t_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_q, path_out + '/' + M[m] + '/bias_q_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_psfc, path_out + '/' + M[m] + '/bias_psfc_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)

#promedio total vertical yhorizontal cada delta t
	bias_geotot = np.ma.mean(np.ma.mean(np.ma.mean(bias_geo, axis = (0)), axis = (0)), axis = (0))
	bias_utot = np.ma.mean(np.ma.mean(np.ma.mean(bias_u, axis = (0)), axis = (0)), axis = (0))
	bias_vtot = np.ma.mean(np.ma.mean(np.ma.mean(bias_v, axis = (0)), axis = (0)), axis = (0))
	bias_ttot = np.ma.mean(np.ma.mean(np.ma.mean(bias_t, axis = (0)), axis = (0)), axis = (0))
	bias_qtot = np.ma.mean(np.ma.mean(np.ma.mean(bias_q, axis = (0)), axis = (0)), axis = (0))
	bias_psfctot = np.ma.mean(np.ma.mean(np.ma.mean(bias_psfc, axis = (0)), axis = (0)), axis = (0))

	if exp == '/GEFS':
		np.ma.dump(bias_geotot, path_out + '/' + M[m] + '/bias_geotot_' + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_utot, path_out + '/' + M[m] + '/bias_utot_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_vtot, path_out + '/' + M[m] + '/bias_vtot_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_ttot, path_out + '/' + M[m] + '/bias_ttot_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_qtot, path_out + '/' + M[m] + '/bias_qtot_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_psfctot, path_out + '/' + M[m] + '/bias_psfctot_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
	elif exp == '/GFS':
		np.ma.dump(bias_geotot, path_out + '/bias_geotot_' + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_utot, path_out + '/bias_utot_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_vtot, path_out + '/bias_vtot_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_ttot, path_out + '/bias_ttot_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_qtot, path_out + '/bias_qtot_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_psfctot, path_out + '/bias_psfctot_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
	else:
		np.ma.dump(bias_geotot, path_out + '/' + M[m] + '/bias_geotot_' + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_utot, path_out + '/' + M[m] + '/bias_utot_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_vtot, path_out + '/' + M[m] + '/bias_vtot_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_ttot, path_out + '/' + M[m] + '/bias_ttot_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_qtot, path_out + '/' + M[m] + '/bias_qtot_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_psfctot, path_out + '/' + M[m] + '/bias_psfctot_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)

#promedio total vertical y temporal para cada delta t

	bias_geoH = np.ma.mean(bias_geo, axis = (0))
	bias_uH =  np.ma.mean(bias_u, axis = (0))
	bias_vH =  np.ma.mean(bias_v, axis = (0))
	bias_tH =  np.ma.mean(bias_t, axis = (0))
	bias_qH =  np.ma.mean(bias_q, axis = (0))
	bias_psfcH =  np.ma.mean(bias_psfc, axis = (0))

	if exp == '/GEFS':
		np.ma.dump(bias_geoH, path_out + '/' + M[m] + '/bias_geoH_' + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_uH, path_out + '/' + M[m] + '/bias_uH_'  + date + '_M'+ M[m] + '_ana' +'_'+periodo +   ANA)
		np.ma.dump(bias_vH, path_out + '/' + M[m] + '/bias_vH_'  + date + '_M'+ M[m] + '_ana' +'_'+periodo +   ANA)
		np.ma.dump(bias_tH, path_out + '/' + M[m] + '/bias_tH_'  + date + '_M'+ M[m] + '_ana' +'_'+periodo +   ANA)
		np.ma.dump(bias_qH, path_out + '/' + M[m] + '/bias_qH_'  + date + '_M'+ M[m] + '_ana' +'_'+periodo +   ANA)
		np.ma.dump(bias_psfcH, path_out + '/' + M[m] + '/bias_psfcH_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
	elif exp == '/GFS':
		np.ma.dump(bias_geoH, path_out + '/bias_geoH_' + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_uH, path_out + '/bias_uH_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_vH, path_out + '/bias_vH_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_tH, path_out + '/bias_tH_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_qH, path_out + '/bias_qH_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_psfcH, path_out + '/bias_psfcH_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
	else:
		np.ma.dump(bias_geoH, path_out + '/' + M[m] + '/bias_geoH_' + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_uH, path_out + '/' + M[m] + '/bias_uH_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_vH, path_out + '/' + M[m] + '/bias_vH_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_tH, path_out + '/' + M[m] + '/bias_tH_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_qH, path_out + '/' + M[m] + '/bias_qH_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)
		np.ma.dump(bias_psfcH, path_out + '/' + M[m] + '/bias_psfcH_'  + date + '_M'+ M[m] +'_'+periodo +  '_ana' +  ANA)


	bias_geoH = 0
	bias_uH = 0
	bias_vH = 0
	bias_tH = 0
	bias_qH = 0
	bias_psfcH = 0


	bias_geo = 0
	bias_u = 0
	bias_v = 0
	bias_t = 0
	bias_q = 0
	bias_psfc = 0
	bias_geotot = 0
	bias_utot = 0
	bias_vtot = 0
	bias_ttot = 0
	bias_qtot = 0
	bias_psfctot = 0
	



	m = m + 1	# Loop de los miembros
gc.collect()	# Saca la basura de la memoria
	



