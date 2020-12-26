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

parser = argparse.ArgumentParser(description='Exp')
parser.add_argument('Exp',type=str)
args = parser.parse_args()
exp = args.Exp

path_upp = '/data/miglesias/verificacion_CE/variables_WRF_UPP_interpoladas/CE_' + exp
path_salida = '/data/miglesias/verificacion_CE/dif_ERA_WRFupp/' + exp

path_eralvl = '/data/miglesias/verificacion_CE/variables_ERA/dic2015/plvl'
path_erasfc = '/data/miglesias/verificacion_CE/variables_ERA/dic2015/sfc'

M=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20']
d=6
Fcst=0
i=0
f=17
day=datetime(2015,12,19,00)
delta = timedelta(hours=6)

while i <= f:
	m=0
	# Nombre de fecha para abrir:
	YY = str(day.year)
	MM = str(day.month).zfill(2)
	DD = str(day.day).zfill(2)
	HH = str(day.hour).zfill(2)
	FCST = '.' + str(Fcst).zfill(3)
	while m < len(M):
		# GEOPOTENCIAL
		geopt_upp = np.ma.load(path_upp + '/' + M[m] + '/geopt_upp_20151219_00' + FCST)
		geopt_era = np.load(path_eralvl + '/geopt_era_' + YY + MM + DD + HH + '.npy')
		dif_geopt = geopt_era - geopt_upp

		# Temperatura
		tk_upp = np.ma.load(path_upp + '/' + M[m] + '/tk_upp_20151219_00' + FCST)
		tk_era = np.load(path_eralvl + '/tk_era_' + YY + MM + DD + HH + '.npy')
		dif_tk = tk_era - tk_upp

		# Humedad Especifica
		q_upp = np.ma.load(path_upp + '/' + M[m] + '/q_upp_20151219_00' + FCST)
		q_era = np.load(path_eralvl + '/q_era_' + YY + MM + DD + HH + '.npy')
		dif_q = q_era - q_upp
		# Viento U y V
		v_upp = np.ma.load(path_upp + '/' + M[m] + '/v_upp_20151219_00' + FCST)
		v_era = np.load(path_eralvl + '/v_era_' + YY + MM + DD + HH + '.npy')
		dif_v = v_era - v_upp

		u_upp = np.ma.load(path_upp + '/' + M[m] + '/u_upp_20151219_00' + FCST)
		u_era = np.load(path_eralvl + '/u_era_' + YY + MM + DD + HH + '.npy')
		dif_u = u_era - u_upp
		#PSFC
		psfc_upp = np.ma.load(path_upp + '/' + M[m] + '/psfc_upp_20151219_00' + FCST)
		psfc_era = np.load(path_erasfc + '/psfc_era_' + YY + MM + DD + HH + '.npy')
		psfc_era = psfc_era/100
		dif_psfc = psfc_era - psfc_upp
		
		#Guardo la subseleccion de lat-lon que incluya la region
		np.ma.dump(dif_geopt, path_salida + '/' + M[m] + '/geopt_dif_era-upp_'+ YY + MM + DD + HH )
		np.ma.dump(dif_tk, path_salida + '/' + M[m] + '/tk_dif_era-upp_'+ YY + MM + DD + HH )
		np.ma.dump(dif_q, path_salida + '/' + M[m] + '/q_dif_era-upp_'+ YY + MM + DD + HH )
		np.ma.dump(dif_u, path_salida + '/' + M[m] + '/u_dif_era-upp_'+ YY + MM + DD + HH )
		np.ma.dump(dif_v, path_salida + '/' + M[m] + '/v_dif_era-upp_'+ YY + MM + DD + HH )
		np.ma.dump(dif_psfc, path_salida + '/' + M[m] + '/psfc_dif_era-upp_'+ YY + MM + DD + HH )
		
		geopt_upp = 0
		geopt_era = 0
		dif_geopt = 0
		tk_upp = 0
		tk_era = 0
		dif_tk = 0
		q_upp = 0
		q_era = 0
		dif_q = 0
		u_upp = 0
		u_era = 0
		dif_u = 0
		v_upp = 0
		v_era = 0
		dif_v = 0
		psfc_upp = 0
		psfc_era = 0
		dif_psfc = 0
		
		gc.collect()
		m = m + 1
	day = day + delta
	Fcst = Fcst + d
	i=i+1
