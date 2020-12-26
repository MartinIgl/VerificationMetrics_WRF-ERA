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

Y = args.Year
M = args.Month
D = args.Day
H = args.Hour
periodo=args.Per

###SETEO el FCST, los datos que se usen estan en la fecha correspondiente al fcst
ANA =  '.000'

if Y==2015:
	expera='/dic2015'
elif Y==2016:
	expera='/ene2016'

exp =  '/' + args.Exp
if exp=='/GFS' or exp=='/GEFS':
	ANA =  '.000'
	if periodo=='2meses':
		periodo='_'+periodo
	else:
		periodo=''
else:
	ANA =  '.000'
	if periodo=='2meses':
		periodo='_'+periodo
	else:
		periodo=''


# Caminos de los archivos:
path_in = '/data/miglesias/verificacion_doc/MSPWRFupp' + exp 
path_salida = '/data/miglesias/verificacion_doc/MSPWRFupp/RMSEns' + exp 
path_era ='/data/miglesias/verificacion_doc/variables_ERA'

d = datetime(Y,M,D,H)	# Listo, asi queda definida una fecha especifica

YY = str(d.year)
MM = str(d.month).zfill(2)
DD = str(d.day).zfill(2)
HH = str(d.hour).zfill(2)

#tomo la media del ensamble para hacer la diferencia con cada miembro
geopt_mean= np.ma.load(path_in  + '/geopt_mean_' + YY + MM + DD + HH + periodo +'_ana' + ANA  )
v_mean = np.ma.load(path_in + '/v_mean_' + YY + MM + DD + HH + periodo +'_ana' + ANA  )
u_mean = np.ma.load( path_in  + '/u_mean_' + YY + MM + DD + HH + periodo +'_ana' + ANA )
q_mean = np.ma.load(path_in  + '/q_mean_' + YY + MM + DD + HH + periodo +'_ana' + ANA  )
tk_mean = np.ma.load(path_in  + '/tk_mean_'+ YY + MM + DD + HH + periodo +'_ana' + ANA  )
psfc_mean = np.ma.load(path_in  + '/psfc_mean_' + YY + MM + DD + HH + periodo +'_ana'  + ANA )

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

# Me voy quedando con la diferencia al cuadrado	
geopt_total = geopt_dif_mean_ERA*geopt_dif_mean_ERA
u_total = u_dif_mean_ERA*u_dif_mean_ERA
v_total = v_dif_mean_ERA*v_dif_mean_ERA
tk_total= tk_dif_mean_ERA*tk_dif_mean_ERA
q_total = q_dif_mean_ERA*q_dif_mean_ERA
psfc_total = psfc_dif_mean_ERA*psfc_dif_mean_ERA


geopt_dif_mean_ERA = 0
u_dif_mean_ERA = 0
v_dif_mean_ERA = 0
tk_dif_mean_ERA = 0
q_dif_mean_ERA = 0
psfc_dif_mean_ERA = 0

#realizo la suma en los miembros primero, luego en lat y luego lon. 

geopt_sumdif2= np.ma.sum((np.ma.sum(geopt_total,axis=2)/160), axis=1 )/110
tk_sumdif2= np.ma.sum((np.ma.sum(tk_total,axis=2)/160), axis=1)/110
q_sumdif2= np.ma.sum((np.ma.sum(q_total,axis=2)/160), axis=1)/110
u_sumdif2= np.ma.sum((np.ma.sum(u_total,axis=2)/160), axis=1)/110
v_sumdif2= np.ma.sum((np.ma.sum(v_total,axis=2)/160), axis=1)/110
psfc_sumdif2= np.ma.sum((np.ma.sum(psfc_total ,axis=1)/160), axis=0)/110


geopt_total = 0
u_total = 0
v_total = 0
q_total = 0
tk_total = 0
psfc_total = 0


rmsd_geopt = np.ma.sqrt( geopt_sumdif2 )
rmsd_u = np.ma.sqrt( u_sumdif2)
rmsd_v = np.ma.sqrt( v_sumdif2 )
rmsd_tk = np.ma.sqrt( tk_sumdif2 )
rmsd_q = np.ma.sqrt( q_sumdif2)
rmsd_psfc = np.ma.sqrt( psfc_sumdif2)


geopt_sumdif2 = 0
u_sumdif2 = 0
v_sumdif2 = 0
q_sumdif2 = 0
tk_sumdif2 = 0
psfc_sumdif2 = 0



np.ma.dump(rmsd_geopt, path_salida + '/rmsdMean_geopt_' + YY + MM + DD + HH + periodo +'_ana' + ANA )
np.ma.dump(rmsd_u, path_salida + '/rmsdMean_u_'   + YY + MM + DD + HH + periodo +'_ana' + ANA )
np.ma.dump(rmsd_v, path_salida + '/rmsdMean_v_'   + YY + MM + DD + HH + periodo +'_ana' + ANA )
np.ma.dump(rmsd_tk, path_salida + '/rmsdMean_tk_'   + YY + MM + DD + HH + periodo +'_ana' + ANA )
np.ma.dump(rmsd_q, path_salida + '/rmsdMean_q_'   + YY + MM + DD + HH + periodo +'_ana' + ANA )
np.ma.dump(rmsd_psfc, path_salida +  '/rmsdMean_psfc_' + YY + MM + DD + HH + periodo +'_ana' + ANA )

rmsd_geopt = 0
rmsd_u = 0
rmsd_v = 0
rmsd_tk = 0
rmsd_q = 0
rmsd_psfc = 0

gc.collect()	# Saca la basura de la memoria
	


