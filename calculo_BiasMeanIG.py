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

exp =  '/' + args.Exp
if Y==2015:
	expera='/dic2015'
elif Y==2016:
	expera='/ene2016'

if exp=='/GFS' or exp=='/GEFS':
	FCST =  '_' + args.FCST
	if periodo=='2meses':
		periodo='_'+periodo
	else:
		periodo=''
else:
	FCST =  '.' + args.FCST
	if periodo=='2meses':
		periodo='_'+periodo
	else:
		periodo=''


# Caminos de los archivos:
path_in = '/data/miglesias/verificacion_doc/MSPWRFupp' + exp 
path_salida = '/data/miglesias/verificacion_doc/MSPWRFupp/BIASEns' + exp 
path_era ='/data/miglesias/verificacion_doc/variables_ERA'


d = datetime(Y,M,D,H)	# Listo, asi queda definida una fecha especifica

YY = str(d.year)
MM = str(d.month).zfill(2)
DD = str(d.day).zfill(2)
HH = str(d.hour).zfill(2)

#tomo la media del ensamble para hacer la diferencia con cada miembro
geopt_mean= np.ma.load(path_in  + '/geopt_mean_' + YY + MM + DD + HH +periodo+ FCST )	
v_mean = np.ma.load(path_in + '/v_mean_' + YY + MM + DD + HH +periodo+ FCST )	
u_mean = np.ma.load( path_in  + '/u_mean_' + YY + MM + DD + HH +periodo+ FCST)	
q_mean = np.ma.load(path_in  + '/q_mean_' + YY + MM + DD + HH +periodo+ FCST )	
tk_mean = np.ma.load(path_in  + '/tk_mean_'+ YY + MM + DD + HH +periodo+ FCST )	
psfc_mean = np.ma.load(path_in  + '/psfc_mean_' + YY + MM + DD + HH +periodo+ FCST)	
# ----------Variables a completar en cada hora para todos los miembros


#direfencia era-mean
u_era = np.load(path_era + expera + '/plvl/u_era_' + YY + MM + DD + HH + '.npy')
v_era = np.load(path_era + expera + '/plvl/v_era_' + YY + MM + DD + HH + '.npy')
tk_era = np.load(path_era + expera + '/plvl/tk_era_' + YY + MM + DD + HH + '.npy')
q_era = np.load(path_era + expera + '/plvl/q_era_' + YY + MM + DD + HH + '.npy')
geo_era = np.load(path_era + expera + '/plvl/geopt_era_' + YY + MM + DD + HH + '.npy')
psfc_era = np.load(path_era + expera + '/sfc/psfc_era_' + YY + MM + DD + HH + '.npy')


geopt_dif_mean_ERA= geo_era - geopt_mean
u_dif_mean_ERA= u_era - u_mean
v_dif_mean_ERA= v_era - v_mean
tk_dif_mean_ERA= tk_era - tk_mean
q_dif_mean_ERA= q_era - q_mean
psfc_dif_mean_ERA= psfc_era - psfc_mean
		



#voy a hacer el promedio horizontal del bias para todas las alturas. tiempo a tiempo (en los miembros hice el rmsd y bias  para todo el espacio promediado en el tiempo)

geopt_bias_eramean= np.ma.sum((np.ma.sum(geopt_dif_mean_ERA,axis=2)/160), axis=1)/110
tk_bias_eramean=np.ma.sum((np.ma.sum(tk_dif_mean_ERA,axis=2)/160), axis=1)/110
q_bias_eramean= np.ma.sum((np.ma.sum(q_dif_mean_ERA,axis=2)/160), axis=1)/110
u_bias_eramean= np.ma.sum((np.ma.sum(u_dif_mean_ERA,axis=2)/160), axis=1)/110
v_bias_eramean= np.ma.sum((np.ma.sum(v_dif_mean_ERA,axis=2)/160), axis=1)/110
psfc_bias_eramean= np.ma.sum((np.ma.sum(psfc_dif_mean_ERA ,axis=1)/160), axis=0)/110

geopt_dif_mean_ERA = 0
u_dif_mean_ERA = 0
v_dif_mean_ERA = 0
tk_dif_mean_ERA = 0
q_dif_mean_ERA = 0
psfc_dif_mean_ERA = 0



# Bias  DE LA MEDIA DEL ENSAMBLE
np.ma.dump(geopt_bias_eramean, path_salida + '/biasMean_geopt_'+ YY + MM + DD + HH +periodo+ FCST)
np.ma.dump(u_bias_eramean, path_salida +  '/biasMean_u_'  + YY + MM + DD + HH +periodo+ FCST)
np.ma.dump(v_bias_eramean, path_salida +  '/biasMean_v_'  + YY + MM + DD + HH +periodo+ FCST)
np.ma.dump(tk_bias_eramean, path_salida +  '/biasMean_tk_' + YY + MM + DD + HH +periodo+ FCST)
np.ma.dump(q_bias_eramean, path_salida + '/biasMean_q_' + YY + MM + DD + HH +periodo+ FCST)
np.ma.dump(psfc_bias_eramean, path_salida + '/biasMean_psfc_'  + YY + MM + DD + HH +periodo+ FCST)

geo_bias_eramean = 0
u_bias_eramean = 0
v_bias_eramean = 0
tk_bias_eramean = 0
q_bias_eramean = 0
psfc_bias_eramean = 0

gc.collect()	# Saca la basura de la memoria
	


