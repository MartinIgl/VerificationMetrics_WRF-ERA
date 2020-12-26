#!/usr/bin/env python
#Martin Iglesias Github SudestadaARG
# Programa para calcular los distintos promedios de los terminos de EETH  
# usando funciones previamente definidas
#
# Voy a necesitar:
#
# -- La EETH calculada con calculo_EETH.py, que fue almacenada asi:
#	np.ma.dump(EETH) con dimension (12,110,160)
#
# Voy a querer hacer los calculos solo con el dominio 296 a 310 lon -15 a -40 lat
# es decir [20:71,73:102] -> la dimension queda en (51,29)

import numpy as np
import os
from datetime import datetime
from datetime import timedelta

from error_energiaIG import M_EETH_horizontal
from error_energiaIG import M_EETH_temporal
from error_energiaIG import M_EETH_vertical
import argparse
import gc



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
diafin =  datetime(Y,M,D,H)
delta = timedelta(hours=6)

###SETEO el FCST, los datos que se usen estan en la fecha correspondiente al fcst
FCST = '_' + args.FCST



EXP = args.Exp

if EXP == 'GFS':
	exp= '/GFS'
	path_in = '/data/miglesias/verificacion_doc/dif_ERA_GEFS/ErrorEnergiaTotalHumeda'  + exp
	path_out = '/data/miglesias/verificacion_doc/dif_ERA_GEFS/ErrorEnergiaTotalHumeda' + exp
elif EXP == 'GEFS':
	exp= '/GEFS'
	path_in = '/data/miglesias/verificacion_doc/dif_ERA_GEFS/ErrorEnergiaTotalHumeda'  + exp
	path_out = '/data/miglesias/verificacion_doc/dif_ERA_GEFS/ErrorEnergiaTotalHumeda' + exp


else:
	quit()





M=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17', '18','19','20'] #vector numero de miembro de ensamble
#m=0	# Ojo que M[1] = '02', acordate que python empieza a contar desde 0


m = 0 	# hay que inicializar la m aca adentro del loop de los dias, sino sigue contando y no encuentra

while m < len(M):	# m < 20

	#dato inicial para los promedios, es el mismo para initial date setting
	Yo=2015
	Mo=12
	Do=01
	Ho=12
	d =datetime(Yo,Mo,Do,Ho)
	tiempos = 1 + timedelta.total_seconds(diafin-d)/21600

#Recorte de maru (doc)
	#totalcinetica = np.ma.empty(( tiempos, 12, 51, 29 ))
	#totaltemp = np.ma.empty(( tiempos, 12, 51, 29 ))
	#totalhumedad = np.ma.empty(( tiempos, 12, 51, 29 ))
	#totalpsup = np.ma.empty(( tiempos, 12, 51, 29 ))
#Recorte Nuevo
	totalcinetica = np.ma.empty(( tiempos, 12, 70, 35 ))
	totaltemp = np.ma.empty(( tiempos, 12, 70, 35 ))
	totalhumedad = np.ma.empty(( tiempos, 12, 70, 35 ))
	totalpsup = np.ma.empty(( tiempos, 12, 70, 35 ))

#dominio total
	#totalcinetica1 = np.ma.empty(( tiempos, 12, 110, 160 )) 
	#totaltemp1 = np.ma.empty(( tiempos,  12, 110, 160 ))
	#totalhumedad1 = np.ma.empty(( tiempos,  12, 110, 160 ))
	#totalpsup1 = np.ma.empty(( tiempos,  12, 110, 160 ))
#dominio grafico
	totalcinetica1 = np.ma.empty((tiempos, 12, 83, 91 )) 
	totaltemp1 = np.ma.empty(( tiempos, 12, 83, 91 ))
	totalhumedad1 = np.ma.empty(( tiempos, 12, 83, 91 ))
	totalpsup1 = np.ma.empty(( tiempos, 12, 83, 91 ))
	


	contador = -1



	while d <= diafin:


		contador = contador + 1

		# Nombre de fecha para abrir:
		YY = str(d.year)
		MM = str(d.month).zfill(2)
		DD = str(d.day).zfill(2)
		HH = str(d.hour).zfill(2)
		

		cinetica = np.ma.load( path_in +'/' + M[m] + '/cinetica_' + YY + MM + DD + HH + FCST)
		temp = np.ma.load( path_in +'/' + M[m] + '/temp_' + YY + MM + DD + HH + FCST)
		humedad = np.ma.load( path_in +'/' + M[m] + '/humedad_' + YY + MM + DD + HH + FCST)
		psup = np.ma.load( path_in +'/' + M[m] + '/psup_' + YY + MM + DD + HH + FCST)

#Recorte de maru (doc)
		#totalcinetica[contador,:,:,:] = cinetica[:,20:71,73:102]
       	 	#totaltemp[contador,:,:,:] = temp[:,20:71,73:102]
       		#totalhumedad[contador,:,:,:] = humedad[:,20:71,73:102]
       		#totalpsup[contador,:,:,:] = psup[:,20:71,73:102]


#Recorte Nuevo lvl, lat lon
		totalcinetica[contador,:,:,:] = cinetica[:,20:90,70:105]
       	 	totaltemp[contador,:,:,:] = temp[:,20:90,70:105]
       		totalhumedad[contador,:,:,:] = humedad[:,20:90,70:105]
       		totalpsup[contador,:,:,:] = psup[:,20:90,70:105]

#dominio total
		#totalcinetica1[contador,:,:,:] = cinetica[:,:,:] 
       	 	#totaltemp1[contador,:,:,:] = temp[:,:,:]
       		#totalhumedad1[contador,:,:,:] = humedad[:,:,:]
       		#totalpsup1[contador,:,:,:] = psup[:,:,:]

#dominio grafico
		totalcinetica1[contador,:,:,:] = cinetica[:,20:103,31:122] 
		totaltemp1[contador,:,:,:] = temp[:,20:103,31:122]
		totalhumedad1[contador,:,:,:] = humedad[:,20:103,31:122]
		totalpsup1[contador,:,:,:] = psup[:,20:103,31:122]

	
		d = d + delta
	# -------------------------------------------------------------
	# Considerando todos los niveles: calculo promedios de cada termino de EETH
	#M_cin_T_recortado = M_EETH_temporal(totalcinetica)
	#M_cin_H_recortado = M_EETH_horizontal(totalcinetica) 
	#M_cin_V_recortado = M_EETH_vertical(totalcinetica)

	#np.ma.dump(M_cin_T_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_cinetica_temporal_recortado' + FCST)
	#np.ma.dump(M_cin_H_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_cinetica_horizontal_recortado' + FCST)
	#np.ma.dump(M_cin_V_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_cinetica_vertical_recortado' + FCST)

	#
	#M_tem_T_recortado = M_EETH_temporal(totaltemp)
	#M_tem_H_recortado = M_EETH_horizontal(totaltemp)
	#M_tem_V_recortado = M_EETH_vertical(totaltemp)

	#np.ma.dump(M_tem_T_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_temp_temporal_recortado' + FCST)
	#np.ma.dump(M_tem_H_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_temp_horizontal_recortado' + FCST)
	#np.ma.dump(M_tem_V_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_temp_vertical_recortado' + FCST)

	#
	#M_hum_T_recortado = M_EETH_temporal(totalhumedad)
	#M_hum_H_recortado = M_EETH_horizontal(totalhumedad)
	#M_hum_V_recortado = M_EETH_vertical(totalhumedad)

	#np.ma.dump(M_hum_T_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_humedad_temporal_recortado' + FCST)
	#np.ma.dump(M_hum_H_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_humedad_horizontal_recortado' + FCST)
	#np.ma.dump(M_hum_V_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_humedad_vertical_recortado' + FCST)

	#
	#M_p_T_recortado = M_EETH_temporal(totalpsup)
	#M_p_H_recortado = M_EETH_horizontal(totalpsup)
	#M_p_V_recortado = M_EETH_vertical(totalpsup)

	#np.ma.dump(M_p_T_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_psup_temporal_recortado' + FCST)
	#np.ma.dump(M_p_H_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_psup_horizontal_recortado' + FCST)
	#np.ma.dump(M_p_V_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_psup_vertical_recortado' + FCST)
	if EXP == 'GEFS':
		#dominio entero
		M_cin_T = M_EETH_temporal(totalcinetica1)
		M_cin_H = M_EETH_horizontal(totalcinetica1) 
		M_cin_V = M_EETH_vertical(totalcinetica1)

		np.ma.dump(M_cin_T, path_out + '/meanterm' + '/' + M[m] + '/M_cinetica_temporal_'+periodo + FCST)
		np.ma.dump(M_cin_H, path_out + '/meanterm' + '/' + M[m] + '/M_cinetica_horizontal_'+periodo + FCST)
		np.ma.dump(M_cin_V, path_out + '/meanterm' + '/' + M[m] + '/M_cinetica_vertical_'+periodo + FCST)

		#
		M_tem_T = M_EETH_temporal(totaltemp1)
		M_tem_H = M_EETH_horizontal(totaltemp1)
		M_tem_V = M_EETH_vertical(totaltemp1)

		np.ma.dump(M_tem_T, path_out + '/meanterm' + '/' + M[m] + '/M_temp_temporal_'+periodo + FCST)
		np.ma.dump(M_tem_H, path_out + '/meanterm' + '/' + M[m] + '/M_temp_horizontal_'+periodo + FCST)
		np.ma.dump(M_tem_V, path_out + '/meanterm' + '/' + M[m] + '/M_temp_vertical_'+periodo + FCST)

		#
		M_hum_T = M_EETH_temporal(totalhumedad1)
		M_hum_H = M_EETH_horizontal(totalhumedad1)
		M_hum_V = M_EETH_vertical(totalhumedad1)
	
		np.ma.dump(M_hum_T, path_out + '/meanterm' + '/' + M[m] + '/M_humedad_temporal_'+periodo + FCST)
		np.ma.dump(M_hum_H, path_out + '/meanterm' + '/' + M[m] + '/M_humedad_horizontal_'+periodo + FCST)
		np.ma.dump(M_hum_V, path_out + '/meanterm' + '/' + M[m] + '/M_humedad_vertical_'+periodo + FCST)

		#
		M_p_T = M_EETH_temporal(totalpsup1)
		M_p_H = M_EETH_horizontal(totalpsup1)
		M_p_V = M_EETH_vertical(totalpsup1)

		np.ma.dump(M_p_T, path_out + '/meanterm' + '/' + M[m] + '/M_psup_temporal_'+periodo + FCST)
		np.ma.dump(M_p_H, path_out + '/meanterm' + '/' + M[m] + '/M_psup_horizontal_'+periodo + FCST)
		np.ma.dump(M_p_V, path_out + '/meanterm' + '/' + M[m] + '/M_psup_vertical_'+periodo + FCST)
		m = m + 1	# Loop de los miembros
	elif EXP == 'GFS':
		#dominio entero
		M_cin_T = M_EETH_temporal(totalcinetica1)
		M_cin_H = M_EETH_horizontal(totalcinetica1) 
		M_cin_V = M_EETH_vertical(totalcinetica1)

		np.ma.dump(M_cin_T, path_out + '/meanterm' + '/M_cinetica_temporal_'+periodo + FCST)
		np.ma.dump(M_cin_H, path_out + '/meanterm' +'/M_cinetica_horizontal_'+periodo + FCST)
		np.ma.dump(M_cin_V, path_out + '/meanterm' +'/M_cinetica_vertical_'+periodo + FCST)

		#
		M_tem_T = M_EETH_temporal(totaltemp1)
		M_tem_H = M_EETH_horizontal(totaltemp1)
		M_tem_V = M_EETH_vertical(totaltemp1)
	
		np.ma.dump(M_tem_T, path_out + '/meanterm' +'/M_temp_temporal_'+periodo + FCST)
		np.ma.dump(M_tem_H, path_out + '/meanterm' +'/M_temp_horizontal_'+periodo + FCST)
		np.ma.dump(M_tem_V, path_out + '/meanterm' +'/M_temp_vertical_'+periodo + FCST)

	#
		M_hum_T = M_EETH_temporal(totalhumedad1)
		M_hum_H = M_EETH_horizontal(totalhumedad1)
		M_hum_V = M_EETH_vertical(totalhumedad1)

		np.ma.dump(M_hum_T, path_out + '/meanterm' +'/M_humedad_temporal_'+periodo + FCST)	
		np.ma.dump(M_hum_H, path_out + '/meanterm' +'/M_humedad_horizontal_'+periodo + FCST)
		np.ma.dump(M_hum_V, path_out + '/meanterm' +'/M_humedad_vertical_'+periodo + FCST)

		#
		M_p_T = M_EETH_temporal(totalpsup1)
		M_p_H = M_EETH_horizontal(totalpsup1)
		M_p_V = M_EETH_vertical(totalpsup1)
	
		np.ma.dump(M_p_T, path_out + '/meanterm' +'/M_psup_temporal_'+periodo + FCST)
		np.ma.dump(M_p_H, path_out + '/meanterm' +'/M_psup_horizontal_'+periodo + FCST)
		np.ma.dump(M_p_V, path_out + '/meanterm' +'/M_psup_vertical_'+periodo + FCST)
		m = m + 1	# Loop de los miembros



gc.collect()

