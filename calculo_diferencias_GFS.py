#!/usr/bin/env python
#Martin Iglesias Github SudestadaARG
# Programa para calcular diferencias entre distintas variables del ARW y el ERA-Interim
# La idea es guardar las diferencias como numpy array, para despues usarlas en el calculo de las medidas de error

# Previamente arme los array de cada variable de ambos modelos, de la siguiente manera:
# (no se usa) ARW:  np.ma.dump(geopt[:,190:300,519:679], path_salida + '/geopt_arw_'+ str(YY) + str(MM) + str(DD) + str(HH) )
# WRF UPP:  np.ma.dump(geopt[:,190:300,519:679], path_salida + '/geopt_arw_'+ str(YY) + str(MM) + str(DD) + str(HH) )

# ERA:  np.save(path_salida + '/geopt_era_'+ str(YY) + str(MM) + str(DD) + str(HH) + '.npy', geopt[:,190:300,519:679] )
# O sea que ya tengo el dominio de 110x160
# porque el WRF UPP ya esta interpolado

import numpy as np
import os
from datetime import datetime  
from datetime import timedelta
import argparse
import gc


parser = argparse.ArgumentParser(description='Year Month Day Hour FCST Exp')
parser.add_argument('Year',type=int)
parser.add_argument('Month',type=int)
parser.add_argument('Day',type=int)
parser.add_argument('Hour',type=int)
parser.add_argument('FCST',type=str)
parser.add_argument('Exp',type=str)
args = parser.parse_args()


Y = args.Year
M = args.Month
D = args.Day
H = args.Hour
EXP = args.Exp
###SETEO el FCST, los datos que se usen estan en la fecha correspondiente al fcst
FCST = '_' + args.FCST


# Caminos de los archivos:
if EXP == 'GFS':
	exp = '/GFS' 
	path_gfs = '/data/miglesias/verificacion_doc/variables_GEFS/deterministico'  
else:
 	quit()


path_salida = '/data/miglesias/verificacion_doc/dif_ERA_GEFS' + exp 


if Y == 2015:
	path_eralvl ='/data/miglesias/verificacion_doc/variables_ERA/dic2015/plvl'
	path_erasfc ='/data/miglesias/verificacion_doc/variables_ERA/dic2015/sfc'
elif Y == 2016:
	path_eralvl ='/data/miglesias/verificacion_doc/variables_ERA/ene2016/plvl'
	path_erasfc ='/data/miglesias/verificacion_doc/variables_ERA/ene2016/sfc'


d = datetime(Y,M,D,H)
YY = str(d.year)
MM = str(d.month).zfill(2)
DD = str(d.day).zfill(2)
HH = str(d.hour).zfill(2)




# ------Geopotencial------	
geopt_gfs = np.ma.load(path_gfs + '/geopt_GFS_' + YY + MM + DD + HH + FCST )
geopt_era = np.load(path_eralvl + '/geopt_era_' + YY + MM + DD + HH + '.npy')
dif_geopt = geopt_era - geopt_gfs

# ------Temperatura------
tk_gfs = np.ma.load(path_gfs + '/tk_GFS_' + YY + MM + DD + HH + FCST )
tk_era = np.load(path_eralvl + '/tk_era_' + YY + MM + DD + HH + '.npy')
dif_tk = tk_era - tk_gfs
# ------Humedad especifica------
q_gfs = np.ma.load(path_gfs + '/q_GFS_' + YY + MM + DD + HH + FCST )
q_era = np.load(path_eralvl + '/q_era_' + YY + MM + DD + HH + '.npy')
dif_q = q_era - q_gfs
# ------Viento: componentes U y V------
u_gfs = np.ma.load(path_gfs + '/u_GFS_' + YY + MM + DD + HH + FCST )
u_era = np.load(path_eralvl + '/u_era_' + YY + MM + DD + HH + '.npy')
dif_u = u_era - u_gfs
v_gfs = np.ma.load(path_gfs +'/v_GFS_'+ YY + MM + DD + HH + FCST )
v_era = np.load(path_eralvl + '/v_era_' + YY + MM + DD + HH + '.npy')
dif_v = v_era - v_gfs
# ------PSFC------
psfc_gfs = np.ma.load(path_gfs + '/psfc_GFS_'+ YY + MM + DD + HH + FCST )
psfc_era = np.load(path_erasfc + '/psfc_era_'+ YY + MM + DD + HH + '.npy')
psfc_era = psfc_era/100 #esta variable esta en pa, la del WRF en hpa
dif_psfc = psfc_era - psfc_gfs

# Solo necesito una subseleccion de lat-lon que incluya la region, no me interesa el globo entero:
np.ma.dump(dif_geopt, path_salida + '/geopt_dif_era-gfs_' + YY + MM + DD + HH + FCST )
np.ma.dump(dif_tk, path_salida  + '/tk_dif_era-gfs_'+ YY + MM + DD + HH + FCST )
np.ma.dump(dif_q, path_salida  + '/q_dif_era-gfs_' + YY + MM + DD + HH + FCST )
np.ma.dump(dif_u, path_salida  + '/u_dif_era-gfs_' + YY + MM + DD + HH + FCST)
np.ma.dump(dif_v, path_salida  + '/v_dif_era-gfs_' + YY + MM + DD + HH + FCST )
np.ma.dump(dif_psfc, path_salida  + '/psfc_dif_era-gfs_' + YY + MM + DD + HH + FCST )

geopt_gfs = 0
geopt_era = 0
dif_geopt = 0
tk_gfs = 0
tk_era = 0
dif_tk = 0
q_gfs = 0
q_era = 0
dif_q = 0
u_gfs = 0
u_era = 0
dif_u =0
v_gfs = 0
v_era = 0
dif_v = 0
psfc_gfs = 0
psfc_era = 0
dif_psfc = 0
gc.collect() # Saca la basura de la memoria

	
	

