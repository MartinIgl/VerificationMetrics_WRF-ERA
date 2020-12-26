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
if EXP == 'GEFS':
	exp = '/GEFS' 
	path_gefs = '/data/miglesias/verificacion_doc/variables_GEFS' 
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


M=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17', '18','19','20'] #vector numero de miembro de ensamble
#m=0	# Ojo que M[1] = '02', acordate que python empieza a contar desde 0

m = 0 	# hay que inicializar la m aca adentro del loop de los dias, sino sigue contando y no encuentra

while m < len(M):	# m < 20


	# Nombre de fecha para abrir:
	YY = str(d.year)
	MM = str(d.month).zfill(2)
	DD = str(d.day).zfill(2)
	HH = str(d.hour).zfill(2)
		
	# ------Geopotencial------	
	geopt_gefs = np.ma.load(path_gefs + '/' + M[m] + '/geopt_gefs_' + YY + MM + DD + HH + FCST )
	geopt_era = np.load(path_eralvl + '/geopt_era_' + YY + MM + DD + HH + '.npy')
	dif_geopt = geopt_era - geopt_gefs

	# ------Temperatura------
        tk_gefs = np.ma.load(path_gefs + '/' + M[m] + '/tk_gefs_' + YY + MM + DD + HH + FCST )
        tk_era = np.load(path_eralvl + '/tk_era_' + YY + MM + DD + HH + '.npy')
        dif_tk = tk_era - tk_gefs
	# ------Humedad especifica------
        q_gefs = np.ma.load(path_gefs + '/' + M[m] + '/q_gefs_' + YY + MM + DD + HH + FCST )
        q_era = np.load(path_eralvl + '/q_era_' + YY + MM + DD + HH + '.npy')
        dif_q = q_era - q_gefs
	# ------Viento: componentes U y V------
        u_gefs = np.ma.load(path_gefs + '/' + M[m] + '/u_gefs_' + YY + MM + DD + HH + FCST )
        u_era = np.load(path_eralvl + '/u_era_' + YY + MM + DD + HH + '.npy')
        dif_u = u_era - u_gefs

        v_gefs = np.ma.load(path_gefs + '/' + M[m] + '/v_gefs_'+ YY + MM + DD + HH + FCST )
        v_era = np.load(path_eralvl + '/v_era_' + YY + MM + DD + HH + '.npy')
        dif_v = v_era - v_gefs
	# ------PSFC------
	psfc_gefs = np.ma.load(path_gefs + '/' + M[m] + '/psfc_gefs_'+ YY + MM + DD + HH + FCST )
        psfc_era = np.load(path_erasfc + '/psfc_era_'+ YY + MM + DD + HH + '.npy')
	psfc_era = psfc_era/100 #esta variable esta en pa, la del WRF en hpa
        dif_psfc = psfc_era - psfc_gefs
	
	# Solo necesito una subseleccion de lat-lon que incluya la region, no me interesa el globo entero:

        np.ma.dump(dif_geopt, path_salida + '/' + M[m] + '/geopt_dif_era-gefs_' + YY + MM + DD + HH + FCST )
	np.ma.dump(dif_tk, path_salida + '/' + M[m] + '/tk_dif_era-gefs_'+ YY + MM + DD + HH + FCST )
        np.ma.dump(dif_q, path_salida + '/' + M[m] + '/q_dif_era-gefs_' + YY + MM + DD + HH + FCST )
        np.ma.dump(dif_u, path_salida + '/' + M[m] + '/u_dif_era-gefs_' + YY + MM + DD + HH + FCST)
        np.ma.dump(dif_v, path_salida + '/' + M[m] + '/v_dif_era-gefs_' + YY + MM + DD + HH + FCST )
        np.ma.dump(dif_psfc, path_salida + '/' + M[m] + '/psfc_dif_era-gefs_' + YY + MM + DD + HH + FCST )
	
	
	
	m = m + 1	# Loop de los miembros
geopt_gefs = 0
geopt_era = 0
dif_geopt = 0
tk_gefs = 0
tk_era = 0
dif_tk = 0
q_gefs = 0
q_era = 0
dif_q = 0
u_gefs = 0
u_era = 0
dif_u =0
v_gefs = 0
v_era = 0
dif_v = 0
psfc_gefs = 0
psfc_era = 0
dif_psfc = 0
gc.collect() # Saca la basura de la memoria


