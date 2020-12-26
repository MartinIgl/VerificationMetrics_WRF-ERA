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
import argparse
import gc
from error_energiaIG import M_EETH_horizontal
from error_energiaIG import M_EETH_temporal
from error_energiaIG import M_EETH_vertical


parser = argparse.ArgumentParser(description='Exp')
parser.add_argument('Exp',type=str)
args = parser.parse_args()
exp = args.Exp



exp = args.Exp
path_in = '/data/miglesias/verificacion_CE/dif_ERA_WRFupp/ErrorEnergiaTotalHumeda/' + exp
path_out = '/data/miglesias/verificacion_CE/dif_ERA_WRFupp/ErrorEnergiaTotalHumeda/' + exp


M=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17', '18','19','20'] #vector numero de miembro de ensamble
#m=0	# Ojo que M[1] = '02', acordate que python empieza a contar desde 0

day=datetime(2015,12,19,00)
delta = timedelta(hours=6)
dayfin=datetime(2015,12,23,00)
m = 0
while m < len(M):	# m < 20

	tiempos = 1 + timedelta.total_seconds(dayfin-day)/21600


#Recorte de maru (doc)
	#totalcinetica = np.ma.empty(( tiempos, 12, 51, 29 ))
	#totaltemp = np.ma.empty(( tiempos, 12, 51, 29 ))
	#totalhumedad = np.ma.empty(( tiempos, 12, 51, 29 ))
	#totalpsup = np.ma.empty(( tiempos, 12, 51, 29 ))
#Recorte Nuevo
#	totalcinetica = np.ma.empty(( tiempos, 12, 70, 35 ))
#	totaltemp = np.ma.empty(( tiempos, 12, 70, 35 ))
#	totalhumedad = np.ma.empty(( tiempos, 12, 70, 35 ))
#	totalpsup = np.ma.empty(( tiempos, 12, 70, 35 ))

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



	while day <= dayfin:


		contador = contador + 1

		# Nombre de fecha para abrir:
		YY = str(day.year)
		MM = str(day.month).zfill(2)
		DD = str(day.day).zfill(2)
		HH = str(day.hour).zfill(2)
		

		cinetica = np.ma.load( path_in + '/' + M[m] + '/CE_cinetica_' + YY + MM + DD + HH )
		temp = np.ma.load( path_in + '/' + M[m] + '/CE_temp_' + YY + MM + DD + HH )
		humedad = np.ma.load( path_in + '/' + M[m] + '/CE_humedad_' + YY + MM + DD + HH )
		psup = np.ma.load( path_in + '/' + M[m] + '/CE_psup_' + YY + MM + DD + HH)

#Recorte de maru (doc)
		#totalcinetica[contador,:,:,:] = cinetica[:,20:71,73:102]
       	 	#totaltemp[contador,:,:,:] = temp[:,20:71,73:102]
       		#totalhumedad[contador,:,:,:] = humedad[:,20:71,73:102]
       		#totalpsup[contador,:,:,:] = psup[:,20:71,73:102]


#Recorte Nuevo lvl, lat lon
#		totalcinetica[contador,:,:,:] = cinetica[:,20:90,70:105]
#      	 	totaltemp[contador,:,:,:] = temp[:,20:90,70:105]
#      		totalhumedad[contador,:,:,:] = humedad[:,20:90,70:105]
#      		totalpsup[contador,:,:,:] = psup[:,20:90,70:105]

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

	
		day = day + delta
	# -------------------------------------------------------------
	# Considerando todos los niveles: calculo promedios de cada termino de EETH
	#M_cin_T_recortado = M_EETH_temporal(totalcinetica)
	#M_cin_H_recortado = M_EETH_horizontal(totalcinetica) 
	#M_cin_V_recortado = M_EETH_vertical(totalcinetica)

	#np.ma.dump(M_cin_T_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_cinetica_temporal_recortado_2meses' + FCST)
	#np.ma.dump(M_cin_H_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_cinetica_horizontal_recortado_2meses' + FCST)
	#np.ma.dump(M_cin_V_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_cinetica_vertical_recortado_2meses' + FCST)

	#
	#M_tem_T_recortado = M_EETH_temporal(totaltemp)
	#M_tem_H_recortado = M_EETH_horizontal(totaltemp)
	#M_tem_V_recortado = M_EETH_vertical(totaltemp)

	#np.ma.dump(M_tem_T_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_temp_temporal_recortado_2meses' + FCST)
	#np.ma.dump(M_tem_H_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_temp_horizontal_recortado_2meses' + FCST)
	#np.ma.dump(M_tem_V_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_temp_vertical_recortado_2meses' + FCST)

	#
	#M_hum_T_recortado = M_EETH_temporal(totalhumedad)
	#M_hum_H_recortado = M_EETH_horizontal(totalhumedad)
	#M_hum_V_recortado = M_EETH_vertical(totalhumedad)

	#np.ma.dump(M_hum_T_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_humedad_temporal_recortado_2meses' + FCST)
	#np.ma.dump(M_hum_H_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_humedad_horizontal_recortado_2meses' + FCST)
	#np.ma.dump(M_hum_V_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_humedad_vertical_recortado_2meses' + FCST)

	#
	#M_p_T_recortado = M_EETH_temporal(totalpsup)
	#M_p_H_recortado = M_EETH_horizontal(totalpsup)
	#M_p_V_recortado = M_EETH_vertical(totalpsup)

	#np.ma.dump(M_p_T_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_psup_temporal_recortado_2meses' + FCST)
	#np.ma.dump(M_p_H_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_psup_horizontal_recortado_2meses' + FCST)
	#np.ma.dump(M_p_V_recortado, path_out + '/meanterm' + '/' + M[m] + '/M_psup_vertical_recortado_2meses' + FCST)

#########dominio entero
	M_cin_T = M_EETH_temporal(totalcinetica1)
	M_cin_H = M_EETH_horizontal(totalcinetica1) 
	M_cin_V = M_EETH_vertical(totalcinetica1)

	np.ma.dump(M_cin_T, path_out + '/meanterm' + '/' + M[m] + '/M_cinetica_temporal_Casodeestudio_19-23' )
	np.ma.dump(M_cin_H, path_out + '/meanterm' + '/' + M[m] + '/M_cinetica_horizontal_Casodeestudio_19-23')
	np.ma.dump(M_cin_V, path_out + '/meanterm' + '/' + M[m] + '/M_cinetica_vertical_Casodeestudio_19-23')

	#
	M_tem_T = M_EETH_temporal(totaltemp1)
	M_tem_H = M_EETH_horizontal(totaltemp1)
	M_tem_V = M_EETH_vertical(totaltemp1)

	np.ma.dump(M_tem_T, path_out + '/meanterm' + '/' + M[m] + '/M_temp_temporal_Casodeestudio_19-23')
	np.ma.dump(M_tem_H, path_out + '/meanterm' + '/' + M[m] + '/M_temp_horizontal_Casodeestudio_19-23')
	np.ma.dump(M_tem_V, path_out + '/meanterm' + '/' + M[m] + '/M_temp_vertical_Casodeestudio_19-23')

	#
	M_hum_T = M_EETH_temporal(totalhumedad1)
	M_hum_H = M_EETH_horizontal(totalhumedad1)
	M_hum_V = M_EETH_vertical(totalhumedad1)

	np.ma.dump(M_hum_T, path_out + '/meanterm' + '/' + M[m] + '/M_humedad_temporal_Casodeestudio_19-23')
	np.ma.dump(M_hum_H, path_out + '/meanterm' + '/' + M[m] + '/M_humedad_horizontal_Casodeestudio_19-23')
	np.ma.dump(M_hum_V, path_out + '/meanterm' + '/' + M[m] + '/M_humedad_vertical_Casodeestudio_19-23')

	#
	M_p_T = M_EETH_temporal(totalpsup1)
	M_p_H = M_EETH_horizontal(totalpsup1)
	M_p_V = M_EETH_vertical(totalpsup1)

	np.ma.dump(M_p_T, path_out + '/meanterm' + '/' + M[m] + '/M_psup_temporal_Casodeestudio_19-23')
	np.ma.dump(M_p_H, path_out + '/meanterm' + '/' + M[m] + '/M_psup_horizontal_Casodeestudio_19-23')
	np.ma.dump(M_p_V, path_out + '/meanterm' + '/' + M[m] + '/M_psup_vertical_Casodeestudio_19-23')
	m = m + 1	# Loop de los miembros



M_EETH_T_recortado = 0
M_EETH_H_recortado = 0
M_EETH_V_recortado = 0
M_EETH_T = 0
M_EETH_H = 0
M_EETH_V = 0
gc.collect() # Saca la basura de la memoria
