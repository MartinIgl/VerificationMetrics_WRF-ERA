#!/usr/bin/env python
#Martin Iglesias Github SudestadaARG
# Programa para calcular el RMSD, usando matrices diferencia hechas previamente

# Voy a necesitar:
#
# -- Las diferencias de las variables de sfc que fueron almacenadas asi:
#       np.ma.dump(dif_psfc[190:300,519:679], nombre)
#    o sea dimension (110,160)
#
# -- Las diferencias de las variables por niveles que fueron almacenadas asi:
#       np.ma.dump(dif_geopt[:,190:300,519:679], nombre)
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
###SETEO el , los datos que se usen estan en la fecha correspondiente al 

exp =  '/' + args.Exp #'/sinnud' #'/spnudUV6h'#'/spnud6h'

date = str(args.Hour).zfill(2) + 'z'  #'06Z' '12Z' '18Z''00Z'

# Caminos de los archivos:
if exp == '/GFS' or exp == '/GEFS':
	path_in = '/data/miglesias/verificacion_doc/dif_ERA_GEFS' + exp 
	path_out = '/data/miglesias/verificacion_doc/dif_ERA_GEFS/RMSD'+ exp
	ANA =  '_000'
else:
	path_in = '/data/miglesias/verificacion_doc/dif_ERA_WRFupp' + exp 
	path_out = '/data/miglesias/verificacion_doc/dif_ERA_WRFupp/RMSD'+ exp
	ANA =  '.000'




M=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17', '18','19','20'] #vector numero de miembro de ensamble
#m=0	# Ojo que M[1] = '02', acordate que python empieza a contar desde 0



#Entonces wrfprs01_20151219_12.000 verifica con miembro YY el 2015121912 hora XX de analisis y pronostico 0XX

# Calculo cuantos registros de tiempo voy a tener, para poder definir la dimension del array:
# Ojo si cambio esto, cambiar el nombre del archivo para guardar
#tiempos = 1 + timedelta.total_seconds(diafin-d)/21600		# timedelta 6h
tiempos = 1 + timedelta.total_seconds(diafin-d)/86400           # timedelta 24h

m = 0 	# hay que inicializar la m aca adentro del loop de los dias, sino sigue contando y no encuentra
	
contador = 0
while m < len(M):

	
	geo_total = np.ma.empty(( tiempos, 12, 83, 91 ))#dominio de grafico
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
			udif = np.ma.load( path_in + '/' + M[m] + '/u_dif_era-gefs_' + YY + MM + DD + HH + '_ana' + ANA )
			vdif = np.ma.load( path_in + '/' + M[m] +  '/v_dif_era-gefs_' + YY + MM + DD + HH + '_ana' + ANA )
			tdif = np.ma.load( path_in + '/' + M[m] +  '/tk_dif_era-gefs_' + YY + MM + DD + HH + '_ana' + ANA )
			pdif = np.ma.load( path_in + '/' + M[m] +  '/psfc_dif_era-gefs_' + YY + MM + DD + HH + '_ana' + ANA )
			qdif = np.ma.load( path_in + '/' + M[m] +  '/q_dif_era-gefs_'  + YY + MM + DD + HH + '_ana' + ANA )
			geodif = np.ma.load( path_in + '/' + M[m] + '/geopt_dif_era-gefs_' + YY + MM + DD + HH + '_ana' + ANA )
		elif exp == '/GFS':
			udif = np.ma.load( path_in + '/' + M[m] + '/u_dif_era-gfs_' + YY + MM + DD + HH + '_ana' + ANA )
			vdif = np.ma.load( path_in + '/' + M[m] +  '/v_dif_era-gfs_' + YY + MM + DD + HH + '_ana' + ANA )
			tdif = np.ma.load( path_in + '/' + M[m] +  '/tk_dif_era-gfs_' + YY + MM + DD + HH + '_ana' + ANA )
			pdif = np.ma.load( path_in + '/' + M[m] +  '/psfc_dif_era-gfs_' + YY + MM + DD + HH + '_ana' + ANA )
			qdif = np.ma.load( path_in + '/' + M[m] +  '/q_dif_era-gfs_'  + YY + MM + DD + HH + '_ana' + ANA )
			geodif = np.ma.load( path_in + '/' + M[m] + '/geopt_dif_era-gfs_' + YY + MM + DD + HH + '_ana' + ANA )
		else:
			udif = np.ma.load( path_in + '/' + M[m] + '/u_dif_era-upp_' + YY + MM + DD + HH + '_ana' + ANA )
			vdif = np.ma.load( path_in + '/' + M[m] +  '/v_dif_era-upp_' + YY + MM + DD + HH + '_ana' + ANA )
			tdif = np.ma.load( path_in + '/' + M[m] +  '/tk_dif_era-upp_' + YY + MM + DD + HH + '_ana' + ANA )
			pdif = np.ma.load( path_in + '/' + M[m] +  '/psfc_dif_era-upp_' + YY + MM + DD + HH + '_ana' + ANA )
			qdif = np.ma.load( path_in + '/' + M[m] +  '/q_dif_era-upp_'  + YY + MM + DD + HH + '_ana' + ANA )
			geodif = np.ma.load( path_in + '/' + M[m] + '/geopt_dif_era-upp_' + YY + MM + DD + HH + '_ana' + ANA )


		# Me voy quedando con la diferencia al cuadrado	
        	geo_total[contador,:,:,:] = geodif[:,20:103,31:122]*geodif[:,20:103,31:122]
        	u_total[contador,:,:,:] = udif[:,20:103,31:122]*udif[:,20:103,31:122]
		v_total[contador,:,:,:] = vdif[:,20:103,31:122]*vdif[:,20:103,31:122]
        	t_total[contador,:,:,:] = tdif[:,20:103,31:122]*tdif[:,20:103,31:122]
		q_total[contador,:,:,:] = qdif[:,20:103,31:122]*qdif[:,20:103,31:122]
		psfc_total[contador,:,:] = pdif[20:103,31:122]*pdif[20:103,31:122]

        	d = d + delta

	# Hago la sumatoria en todos los tiempos, o sea que queda rmsd con dimension 
	rmsd_geo = np.ma.sqrt( np.ma.mean(geo_total, axis = (0)) )
	rmsd_u = np.ma.sqrt( np.ma.mean(u_total, axis = (0)) )
	rmsd_v = np.ma.sqrt( np.ma.mean(v_total, axis = (0)) )
	rmsd_t = np.ma.sqrt( np.ma.mean(t_total, axis = (0)) )
	rmsd_q = np.ma.sqrt( np.ma.mean(q_total, axis = (0)) )
	rmsd_psfc = np.ma.sqrt( np.ma.mean(psfc_total, axis = (0)) )

	if exp == '/GFS':
		np.ma.dump(rmsd_geo, path_out + '/rmsd_geo_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_u, path_out + '/rmsd_u_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_v, path_out + '/rmsd_v_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_t, path_out + '/rmsd_t_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_q, path_out + '/rmsd_q_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_psfc, path_out + '/rmsd_psfc_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
	else:
		np.ma.dump(rmsd_geo, path_out + '/' + M[m] + '/rmsd_geo_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_u, path_out + '/' + M[m] + '/rmsd_u_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_v, path_out + '/' + M[m] + '/rmsd_v_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_t, path_out + '/' + M[m] + '/rmsd_t_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_q, path_out + '/' + M[m] + '/rmsd_q_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_psfc, path_out + '/' + M[m] + '/rmsd_psfc_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)

	#promedio total vertical,horizontal y temporal cada delta t
	rmsd_geotot = np.ma.sqrt( np.ma.mean(geo_total) )
	rmsd_utot = np.ma.sqrt(np.ma.mean(u_total))
	rmsd_vtot = np.ma.sqrt(np.ma.mean(v_total))
	rmsd_ttot = np.ma.sqrt(np.ma.mean(t_total))
	rmsd_qtot = np.ma.sqrt(np.ma.mean(q_total))
	rmsd_psfctot = np.ma.sqrt(np.ma.mean(psfc_total))

	if exp == '/GFS': 
		np.ma.dump(rmsd_geotot, path_out + '/rmsd_geotot_' + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_utot, path_out + '/rmsd_utot_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_vtot, path_out + '/rmsd_vtot_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_ttot, path_out + '/rmsd_ttot_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_qtot, path_out + '/rmsd_qtot_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_psfctot, path_out + '/rmsd_psfctot_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
	else:
		np.ma.dump(rmsd_geotot, path_out + '/' + M[m] + '/rmsd_geotot_' + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_utot, path_out + '/' + M[m] + '/rmsd_utot_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_vtot, path_out + '/' + M[m] + '/rmsd_vtot_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_ttot, path_out + '/' + M[m] + '/rmsd_ttot_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_qtot, path_out + '/' + M[m] + '/rmsd_qtot_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_psfctot, path_out + '/' + M[m] + '/rmsd_psfctot_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)

	rmsd_geo = 0
	rmsd_u = 0
	rmsd_v = 0
	rmsd_t = 0
	rmsd_q = 0
	rmsd_psfc = 0
	rmsd_geotot = 0
	rmsd_utot = 0
	rmsd_vtot = 0
	rmsd_ttot = 0
	rmsd_qtot = 0
	rmsd_psfctot = 0



#promedio total vertical y temporal cada delta t 

	rmsd_geoH = np.ma.sqrt(np.ma.mean(np.ma.mean(geo_total, axis = (0)), axis = (0)))
	rmsd_uH =  np.ma.sqrt(np.ma.mean(np.ma.mean(u_total, axis = (0)), axis = (0)))
	rmsd_vH =  np.ma.sqrt(np.ma.mean(np.ma.mean(v_total, axis = (0)), axis = (0)))
	rmsd_tH =  np.ma.sqrt(np.ma.mean(np.ma.mean(t_total, axis = (0)), axis = (0)))
	rmsd_qH =  np.ma.sqrt(np.ma.mean(np.ma.mean(q_total, axis = (0)), axis = (0)))
	rmsd_psfcH =  np.ma.sqrt(np.ma.mean(np.ma.mean(psfc_total, axis = (0)), axis = (0)))

	if exp == '/GFS':
		np.ma.dump(rmsd_geoH, path_out + '/rmsd_geoH_' + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_uH, path_out + '/rmsd_uH_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_vH, path_out + '/rmsd_vH_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_tH, path_out + '/rmsd_tH_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_qH, path_out + '/rmsd_qH_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_psfcH, path_out + '/rmsd_psfcH_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
	else:
		np.ma.dump(rmsd_geoH, path_out + '/' + M[m] + '/rmsd_geoH_' + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_uH, path_out + '/' + M[m] + '/rmsd_uH_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_vH, path_out + '/' + M[m] + '/rmsd_vH_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_tH, path_out + '/' + M[m] + '/rmsd_tH_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_qH, path_out + '/' + M[m] + '/rmsd_qH_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)
		np.ma.dump(rmsd_psfcH, path_out + '/' + M[m] + '/rmsd_psfcH_'  + date + '_M'+ M[m] +'_'+periodo + '_ana' + ANA)

	rmsd_geo = 0
	rmsd_u = 0
	rmsd_v = 0
	rmsd_t = 0
	rmsd_q = 0
	rmsd_psfc = 0
	rmsd_geotot = 0
	rmsd_utot = 0
	rmsd_vtot = 0
	rmsd_ttot = 0
	rmsd_qtot = 0
	rmsd_psfctot = 0
	rmsd_geoH = 0
	rmsd_uH = 0
	rmsd_vH = 0
	rmsd_tH = 0
	rmsd_qH = 0
	rmsd_psfcH = 0




	m = m + 1	# Loop de los miembros


gc.collect()	# Saca la basura de la memoria
	



