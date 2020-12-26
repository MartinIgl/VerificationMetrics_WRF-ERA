#!/usr/bin/env python
#############################
#Funcion para calcular el spread y la medio de un ensamble de n miembros
##Martin Iglesias Github SudestadaARG
####################################

import numpy as np
import os
from datetime import datetime  
from datetime import timedelta
import argparse
import gc


# Defino argumentos para indicarle la fecha y el miembro por linea de comando:
parser = argparse.ArgumentParser(description='Year Month Day Hour  Exp Per')
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

###SETEO el  '_ana' + ANA, los datos que se usen estan en la fecha correspondiente al  '_ana' + ANA
exp=  '/' + args.Exp

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
path_in = '/data/miglesias/verificacion_doc/MSPWRFupp/dif_mean_mem' + exp 
path_salida =  '/data/miglesias/verificacion_doc/MSPWRFupp/spread' + exp
 



d = datetime(Y,M,D,H)	# Listo, asi queda definida una fecha especifica

YY = str(d.year)
MM = str(d.month).zfill(2)
DD = str(d.day).zfill(2)
HH = str(d.hour).zfill(2)



if exp=='/GFS':
	MEM=['01'] 
	m = 0
else:
	MEM=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17', '18','19','20'] #vector numero de miembro de ensamble
#m=0	# Ojo que M[1] = '02', acordate que python empieza a contar desde 0
	m = 0 	# hay que inicializar la m aca adentro del loop de los dias, sino sigue contando y no encuentra

vertical_levels = [1000, 975, 925, 850, 800, 700, 600, 500, 400, 300, 250, 200] # en hPa



	# ----------Variables a completar en cada hora para todos los miembros
geopt_difMEM2 = np.ma.empty(( len(vertical_levels), 110, 160, len(MEM) ))
tk_difMEM2 = np.ma.empty(( len(vertical_levels), 110, 160, len(MEM) ))
q_difMEM2 = np.ma.empty(( len(vertical_levels), 110, 160, len(MEM) ))
u_difMEM2 = np.ma.empty(( len(vertical_levels), 110, 160, len(MEM) ))
v_difMEM2 = np.ma.empty(( len(vertical_levels), 110, 160, len(MEM) ))
psfc_difMEM2 = np.ma.empty((110, 160, len(MEM) ))

while m < len(MEM):	# m < 20
	# Nombre de fecha para abrir:
	YY = str(d.year)
	MM = str(d.month).zfill(2)
	DD = str(d.day).zfill(2)
	HH = str(d.hour).zfill(2)
	if exp=='/GFS':
		# ------Geopotencial------	
		geopt_difMEM = np.ma.load(path_in + '/dif_geoptMEM-mean_' + YY + MM + DD + HH + periodo +'_ana' + ANA )	
		geopt_difMEM2[:,:,:,m]= geopt_difMEM*geopt_difMEM
		# ------Temperatura------
		tk_difMEM= np.ma.load(path_in + '/dif_tkMEM-mean_' + YY + MM + DD + HH + periodo +'_ana' + ANA )

		tk_difMEM2[:,:,:,m]= tk_difMEM*tk_difMEM
		# ------Humedad especifica------
		q_difMEM= np.ma.load(path_in + '/dif_qMEM-mean_' + YY + MM + DD + HH +  periodo +'_ana' + ANA )

		q_difMEM2[:,:,:,m]= q_difMEM*q_difMEM
		# ------Viento: componentes U y V------
		u_difMEM= np.ma.load(path_in + '/dif_uMEM-mean_' + YY + MM + DD + HH +  periodo +'_ana' + ANA )

	 	u_difMEM2[:,:,:,m]= u_difMEM*u_difMEM

		v_difMEM= np.ma.load(path_in + '/dif_vMEM-mean_'+ YY + MM + DD + HH +  periodo +'_ana' + ANA )

		v_difMEM2[:,:,:,m]= v_difMEM*v_difMEM
		# ------PSFC------
		psfc_difMEM= np.ma.load(path_in + '/dif_psfcMEM-mean_'+ YY + MM + DD + HH +  periodo +'_ana' + ANA )

		psfc_difMEM2[:,:,m]= psfc_difMEM*psfc_difMEM

	else:
		# ------Geopotencial------	
		geopt_difMEM = np.ma.load(path_in + '/' + MEM[m] + '/dif_geoptMEM-mean_' + YY + MM + DD + HH +  periodo +'_ana' + ANA )	
		
		geopt_difMEM2[:,:,:,m]= geopt_difMEM*geopt_difMEM
		# ------Temperatura------
		tk_difMEM= np.ma.load(path_in + '/' + MEM[m] + '/dif_tkMEM-mean_' + YY + MM + DD + HH + periodo +'_ana' + ANA )
	
		tk_difMEM2[:,:,:,m]= tk_difMEM*tk_difMEM
		# ------Humedad especifica------
		q_difMEM= np.ma.load(path_in + '/' + MEM[m] + '/dif_qMEM-mean_' + YY + MM + DD + HH + periodo +'_ana' + ANA )
	
		q_difMEM2[:,:,:,m]= q_difMEM*q_difMEM
		# ------Viento: componentes U y V------
		u_difMEM= np.ma.load(path_in + '/' + MEM[m] + '/dif_uMEM-mean_' + YY + MM + DD + HH +  periodo +'_ana' + ANA  )
	
 		u_difMEM2[:,:,:,m]= u_difMEM*u_difMEM
		
		v_difMEM= np.ma.load(path_in + '/' + MEM[m] + '/dif_vMEM-mean_'+ YY + MM + DD + HH +  periodo +'_ana' + ANA  )
	
		v_difMEM2[:,:,:,m]= v_difMEM*v_difMEM
		# ------PSFC------
		psfc_difMEM= np.ma.load(path_in + '/' + MEM[m] + '/dif_psfcMEM-mean_'+ YY + MM + DD + HH +  periodo +'_ana' + ANA  )
	
		psfc_difMEM2[:,:,m]= psfc_difMEM*psfc_difMEM

	m = m + 1	# Loop de los miembros
	

geopt_difMEM = 0
v_difMEM = 0
u_difMEM = 0
q_difMEM = 0
tk_difMEM = 0
psfc_difMEM = 0

if exp=='/GFS':
	#realizo la suma en los miembros primero, luego en lat y luego lon. 
	geopt_sumdif2= np.ma.sum((np.ma.sum((np.ma.sum(geopt_difMEM2, axis=3) / (len(MEM))),axis=2)/160), axis=1)/110
	tk_sumdif2= np.ma.sum((np.ma.sum((np.ma.sum(tk_difMEM2, axis=3) / (len(MEM))),axis=2)/160), axis=1)/110
	q_sumdif2= np.ma.sum((np.ma.sum((np.ma.sum(q_difMEM2, axis=3) / (len(MEM))),axis=2)/160), axis=1)/110
	u_sumdif2= np.ma.sum((np.ma.sum((np.ma.sum(u_difMEM2, axis=3) / (len(MEM))),axis=2)/160), axis=1)/110
	v_sumdif2= np.ma.sum((np.ma.sum((np.ma.sum(v_difMEM2, axis=3) / (len(MEM))),axis=2)/160), axis=1)/110
	psfc_sumdif2= np.ma.sum((np.ma.sum((np.ma.sum(psfc_difMEM2, axis=2) / (len(MEM))),axis=1)/160), axis=0)/110

else:
	#realizo la suma en los miembros primero, luego en lat y luego lon. 
	geopt_sumdif2= np.ma.sum((np.ma.sum((np.ma.sum(geopt_difMEM2, axis=3) / (len(MEM)-1)),axis=2)/160), axis=1)/110
	tk_sumdif2= np.ma.sum((np.ma.sum((np.ma.sum(tk_difMEM2, axis=3) / (len(MEM)-1)),axis=2)/160), axis=1)/110
	q_sumdif2= np.ma.sum((np.ma.sum((np.ma.sum(q_difMEM2, axis=3) / (len(MEM)-1)),axis=2)/160), axis=1)/110
	u_sumdif2= np.ma.sum((np.ma.sum((np.ma.sum(u_difMEM2, axis=3) / (len(MEM)-1)),axis=2)/160), axis=1)/110
	v_sumdif2= np.ma.sum((np.ma.sum((np.ma.sum(v_difMEM2, axis=3) / (len(MEM)-1)),axis=2)/160), axis=1)/110
	psfc_sumdif2= np.ma.sum((np.ma.sum((np.ma.sum(psfc_difMEM2, axis=2) / (len(MEM)-1)),axis=1)/160), axis=0)/110

geopt_difMEM2 = 0
v_difMEM2 = 0
u_difMEM2 = 0
q_difMEM2 = 0
tk_difMEM2 = 0
psfc_difMEM2 = 0


geopt_spread=np.ma.sqrt(geopt_sumdif2)
tk_spread=np.ma.sqrt(tk_sumdif2)
q_spread=np.ma.sqrt(q_sumdif2)
u_spread=np.ma.sqrt(u_sumdif2)
v_spread=np.ma.sqrt(v_sumdif2)
psfc_spread=np.ma.sqrt(psfc_sumdif2)

geopt_sumdif2 = 0
tk_sumdif2 = 0
q_sumdif2 = 0
u_sumdif2 = 0
v_sumdif2 = 0
psfc_sumdif2 = 0

# Solo necesito una subseleccion de lat-lon que incluya la region, no me interesa el globo entero:
np.ma.dump(geopt_spread, path_salida  + '/geopt_spread_' + YY + MM + DD + HH +  periodo +'_ana' + ANA  )
np.ma.dump(tk_spread, path_salida  + '/tk_spread_' + YY + MM + DD + HH +  periodo +'_ana' + ANA  )
np.ma.dump(q_spread, path_salida  + '/q_spread_' + YY + MM + DD + HH +  periodo +'_ana' + ANA  )
np.ma.dump(u_spread, path_salida  + '/u_spread_' + YY + MM + DD + HH +  periodo +'_ana' + ANA )
np.ma.dump(v_spread, path_salida + '/v_spread_' + YY + MM + DD + HH + periodo +'_ana'+ ANA  )
np.ma.dump(psfc_spread, path_salida  + '/psfc_spread_' + YY + MM + DD + HH +periodo +'_ana'+ ANA  )
	
geopt_spread = 0
v_spread = 0
u_spread = 0
q_spread = 0
tk_spread= 0
psfc_spread = 0


gc.collect()	# Saca la basura de la memoria
	
