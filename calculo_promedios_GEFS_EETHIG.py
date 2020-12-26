#!/usr/bin/env python
#Martin Iglesias Github SudestadaARG
# Programa para calcular los distintos promedios del EETH  
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
Yo=2015
Mo=12
Do=01
Ho=12
d =datetime(Yo,Mo,Do,Ho)

###SETEO el FCST, los datos que se usen estan en la fecha correspondiente al fcst
FCST = '_' + args.FCST


EXP = args.Exp
# Caminos de los archivos:
if EXP == 'GEFS':
	exp= '/GEFS' 
	path_in = '/data/miglesias/verificacion_doc/dif_ERA_GEFS/ErrorEnergiaTotalHumeda'  + exp
	path_out = '/data/miglesias/verificacion_doc/dif_ERA_GEFS/ErrorEnergiaTotalHumeda' + exp
else:
	quit()


M=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17', '18','19','20'] #vector numero de miembro de ensamble
#m=0	# Ojo que M[1] = '02', acordate que python empieza a contar desde 0


# Calculo cuantos registros de tiempo voy a tener, para poder definir la dimension del array:
# Ojo si cambio esto, cambiar el nombre del archivo para guardar
tiempos = 1 + timedelta.total_seconds(diafin-d)/21600#Recorte de maru (doc)
	#totalcinetica = np.ma.empty(( tiempos, 12, 51, 29 ))

#totaleeth = np.ma.empty(( tiempos, 12, 51, 29 ))
#totaleeth1 = np.ma.empty(( tiempos, 12, 110, 160 )) 

  #sirve para generar un array de los promedios todos juntos
m = 0 	# hay que inicializar la m aca adentro del loop de los dias, sino sigue contando y no encuentra

while m < len(M):	# m < 20
	#dato inicial para los promedios, es el mismo para initial date setting
	Yo=2015
	Mo=12
	Do=01
	Ho=12
	d =datetime(Yo,Mo,Do,Ho)
	tiempos = 1 + timedelta.total_seconds(diafin-d)/21600
	
	contador = -1
#Recorte de maru (doc)
	#totaleeth = np.ma.empty(( tiempos, 12, 51, 29 ))

#dominio recortado nuevo
#	totaleeth = np.ma.empty(( tiempos, 12, 70, 35 )) 

#dominio total 
	#totaleeth1 = np.ma.empty(( tiempos, 12, 110, 160 )) 

#dominio de grafico
	totaleeth1 = np.ma.empty(( tiempos, 12, 83, 91 )) 
	
	

	while d <= diafin:

		contador = contador + 1
		# Nombre de fecha para abrir:
		YY = str(d.year)
		MM = str(d.month).zfill(2)
		DD = str(d.day).zfill(2)
		HH = str(d.hour).zfill(2)
	

		eeth = np.ma.load( path_in +'/' + M[m] +   '/EETH_' + YY + MM + DD + HH + FCST)

	#Recorte de maru (doc)
		#totaleeth[contador,:,:,:] = eeth[:,20:71,73:102]
	#dominio recortado nuevo
#		totaleeth[contador,:,:,:] = eeth[:,20:90,70:105] 
	#dominio total 	
		#totaleeth1[contador,:,:,:] = eeth[:,:,:] 
	#dominio de grafico	
		totaleeth1[contador,:,:,:] = eeth[:,20:103,31:122]

		d = d + delta
	# -------------------------------------------------------------
	# Considerando todos los niveles: calculo el promedio de EETH
		
#	M_EETH_T_recortado = M_EETH_temporal(totaleeth)
#	M_EETH_H_recortado = M_EETH_horizontal(totaleeth) 
#	M_EETH_V_recortado = M_EETH_vertical(totaleeth)

	M_EETH_T = M_EETH_temporal(totaleeth1)
	M_EETH_H = M_EETH_horizontal(totaleeth1) 
	M_EETH_V = M_EETH_vertical(totaleeth1)


#	np.ma.dump(M_EETH_T_recortado, path_out +'/meantot'+ '/' + M[m] + '/M_EETH_temporal_recortado' + FCST)
#	np.ma.dump(M_EETH_H_recortado, path_out +'/meantot'+ '/' + M[m] + '/M_EETH_horizontal_recortado' + FCST)
#	np.ma.dump(M_EETH_V_recortado, path_out +'/meantot'+ '/' + M[m] + '/M_EETH_vertical_recortado' + FCST)

	#dominio entero
	np.ma.dump(M_EETH_T, path_out +'/meantot'+ '/' + M[m] + '/M_EETH_temporal_'+periodo + FCST)
	np.ma.dump(M_EETH_H, path_out +'/meantot'+ '/' + M[m] + '/M_EETH_horizontal_'+periodo + FCST)
	np.ma.dump(M_EETH_V, path_out +'/meantot'+ '/' + M[m] + '/M_EETH_vertical_'+periodo + FCST)
	m = m + 1	# Loop de los miembros
	

#M_EETH_T_recortado = 0
#M_EETH_H_recortado = 0
#M_EETH_V_recortado = 0
M_EETH_T = 0
M_EETH_H = 0
M_EETH_V = 0
gc.collect() # Saca la basura de la memoria



