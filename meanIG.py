#!/usr/bin/env python
#############################
#Funcion para calcular la media de un ensamble de n miembros
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
exp = args.Exp

if exp == 'GFS' or exp == 'GEFS':
	FCST =  '_' + args.FCST
else:
	FCST = '.' + args.FCST



path_upp = '/data/miglesias/verificacion_CE/variables_WRF_UPP_interpoladas'


exp =  '/' + args.Exp
path_salida = '/data/miglesias/verificacion_doc/MSPWRFupp' + exp 



d = datetime(Y,M,D,H)	# Listo, asi queda definida una fecha especifica

YY = str(d.year)
MM = str(d.month).zfill(2)
DD = str(d.day).zfill(2)
HH = str(d.hour).zfill(2)



MEM=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17', '18','19','20'] #vector numero de miembro de ensamble
# Ojo que M[1] = '02', acordate que python empieza a contar desde 0
m = 0 	# hay que inicializar la m aca adentro del loop de los dias, sino sigue contando y no encuentra



vertical_levels = [1000, 975, 925, 850, 800, 700, 600, 500, 400, 300, 250, 200] # en hPa
#Debo crear matrices con el tamano del numpy y 4ta dimiension el numero de miembro

	# ----------Variables a completar en cada hora para todos los miembros
geopt_M = np.ma.empty(( len(vertical_levels), 110, 160 , len(MEM) ))
tk_M = np.ma.empty(( len(vertical_levels), 110, 160 , len(MEM) ))
q_M = np.ma.empty(( len(vertical_levels), 110, 160 , len(MEM) ))
u_M = np.ma.empty(( len(vertical_levels), 110, 160 , len(MEM) ))
v_M = np.ma.empty(( len(vertical_levels), 110, 160 , len(MEM) ))
psfc_M = np.ma.empty(( 110, 160 , len(MEM) ))



day=datetime(2015,12,19,00)
delta = timedelta(hours=6)
i=0
f=17
while i <= f:
#cambiar los fcst como en la lectura inicial coregir. ver las dmas cosas

	while m < len(MEM):	# m < 20
		if exp == '/GFS':
			# ------Geopotencial------
			geopt_M[:,:,:,m] = np.ma.load(path_upp + '/geopt_GFS_20151219_00'  + FCST )	
			# ------Temperatura------
			tk_M[:,:,:,m]= np.ma.load(path_upp + '/tk_GFS_' + YY + MM + DD + HH + FCST )
			# ------Humedad especifica------
			q_M[:,:,:,m]= np.ma.load(path_upp + '/q_GFS_' + YY + MM + DD + HH + FCST )
			# ------Viento: componentes U y V------
			u_M[:,:,:,m]= np.ma.load(path_upp + '/u_GFS_' + YY + MM + DD + HH + FCST )
			v_M[:,:,:,m]= np.ma.load(path_upp + '/v_GFS_'+ YY + MM + DD + HH + FCST )
			# ------PSFC------
			psfc_M[:,:,m]= np.ma.load(path_upp + '/psfc_GFS_'+ YY + MM + DD + HH + FCST )
		elif exp == '/GEFS':
			# ------Geopotencial------	
			geopt_M[:,:,:,m] = np.ma.load(path_upp + '/' + MEM[m] + '/geopt_gefs_' + YY + MM + DD + HH + FCST )	
			# ------Temperatura------
			tk_M[:,:,:,m]= np.ma.load(path_upp + '/' + MEM[m] + '/tk_gefs_' + YY + MM + DD + HH + FCST )
			# ------Humedad especifica------
			q_M[:,:,:,m]= np.ma.load(path_upp + '/' + MEM[m] + '/q_gefs_' + YY + MM + DD + HH + FCST )
			# ------Viento: componentes U y V------
			u_M[:,:,:,m]= np.ma.load(path_upp + '/' + MEM[m] + '/u_gefs_' + YY + MM + DD + HH + FCST )
			v_M[:,:,:,m]= np.ma.load(path_upp + '/' + MEM[m] + '/v_gefs_'+ YY + MM + DD + HH + FCST )
			# ------PSFC------
			psfc_M[:,:,m]= np.ma.load(path_upp + '/' + MEM[m] + '/psfc_gefs_'+ YY + MM + DD + HH + FCST )
		else:
			# ------Geopotencial------	
			geopt_M[:,:,:,m] = np.ma.load(path_upp + '/' + MEM[m] + '/geopt_upp_' + YY + MM + DD + HH + FCST )	
			# ------Temperatura------
			tk_M[:,:,:,m]= np.ma.load(path_upp + '/' + MEM[m] + '/tk_upp_' + YY + MM + DD + HH + FCST )
			# ------Humedad especifica------
			q_M[:,:,:,m]= np.ma.load(path_upp + '/' + MEM[m] + '/q_upp_' + YY + MM + DD + HH + FCST )
			# ------Viento: componentes U y V------
			u_M[:,:,:,m]= np.ma.load(path_upp + '/' + MEM[m] + '/u_upp_' + YY + MM + DD + HH + FCST )
			v_M[:,:,:,m]= np.ma.load(path_upp + '/' + MEM[m] + '/v_upp_'+ YY + MM + DD + HH + FCST )
			# ------PSFC------
			psfc_M[:,:,m]= np.ma.load(path_upp + '/' + MEM[m] + '/psfc_upp_'+ YY + MM + DD + HH + FCST )
		m = m + 1	# Loop de los miembros
		day = day + delta



# quiero que solo me haga el mean punto a punto entre todos los miembros

geopt_mean= np.ma.mean(geopt_M,axis=3)
v_mean = np.ma.mean(v_M,axis=3)
u_mean = np.ma.mean(u_M,axis=3)
q_mean = np.ma.mean(q_M,axis=3)
tk_mean = np.ma.mean(tk_M,axis=3)
psfc_mean = np.ma.mean(psfc_M,axis=2) ## OJO QUE LA PSFC TIENE UNA DIMENSION MENOS, VA A SER AXIS=2

# Solo necesito una subseleccion de lat-lon que incluya la region, no me interesa el globo entero:
np.ma.dump(geopt_mean, path_salida  + '/geopt_mean_' + YY + MM + DD + HH + FCST )
np.ma.dump(tk_mean, path_salida  + '/tk_mean_'+ YY + MM + DD + HH + FCST )
np.ma.dump(q_mean, path_salida  + '/q_mean_' + YY + MM + DD + HH + FCST )
np.ma.dump(u_mean, path_salida  + '/u_mean_' + YY + MM + DD + HH + FCST)
np.ma.dump(v_mean, path_salida + '/v_mean_' + YY + MM + DD + HH + FCST )
np.ma.dump(psfc_mean, path_salida  + '/psfc_mean_' + YY + MM + DD + HH + FCST )
	
geopt_M = 0
v_M = 0
u_M = 0
q_M = 0
tk_M = 0
psfc_M = 0

gc.collect() # Saca la basura de la memoria






