#!/usr/bin/env python
#Martin Iglesias Github SudestadaARG
############################# es para crear la matriz para hacer la correlacion spread vs rmse

import numpy as np
import os
from datetime import datetime  
from datetime import timedelta
import argparse
import gc

# Defino argumentos para indicarle la fecha y el miembro por linea de comando:
parser = argparse.ArgumentParser(description='Exp EY EM ED EH NoDD')
parser.add_argument('Exp',type=str)
parser.add_argument('EY',type=int)
parser.add_argument('EM',type=int)
parser.add_argument('ED',type=int)
parser.add_argument('EH',type=int)
parser.add_argument('NoDD',type=int)
args = parser.parse_args()



###SETEO el '_ana' +ANA, los datos que se usen estan en la fecha correspondiente al '_ana' +ANA
ANA = '.000'



exp = '/' + args.Exp

path_inre =  '/data/miglesias/verificacion_doc/MSPWRFupp/RMSEns' + exp
path_insp =  '/data/miglesias/verificacion_doc/MSPWRFupp/spread' + exp
path_salida =  '/data/miglesias/verificacion_doc/MSPWRFupp/'


vertical_levels = [1000, 975, 925, 850, 800, 700, 600, 500, 400, 300, 250, 200] # en hPa

Y = 2015
M = 12
D = 01
H = 12
delta = timedelta(hours=6)
Ye=args.EY
Me=args.EM
De=args.ED
He=args.EH
diafin = datetime(Ye,Me,De,He)
d = datetime(Y,M,D,H)

NoDD= args.NoDD #(hasta el 9 18z)
#NoDD=62 #(numero de dias periodo completo)

if NoDD==62:
	periodo='_2meses'
elif NoDD==10:
	periodo=''

contador = 0
while d <= diafin:
	contador = contador+1
	d= d + delta

NoDDh=contador



#####Genero la matriz Spread


geopt_MSp = np.ma.empty(( len(vertical_levels), NoDDh ))
tk_MSp = np.ma.empty(( len(vertical_levels), NoDDh ))
q_MSp = np.ma.empty(( len(vertical_levels), NoDDh ))
u_MSp = np.ma.empty(( len(vertical_levels), NoDDh ))
v_MSp = np.ma.empty(( len(vertical_levels), NoDDh ))
psfc_MSp = np.ma.empty(( 1 , NoDDh ))

n=0
d = datetime(Y,M,D,H)

while d <= diafin:

	# hay que inicializar la m aca adentro del loop de los dias, sino sigue contando y no encuentra
	YY = str(d.year)
	MM = str(d.month).zfill(2)
	DD = str(d.day).zfill(2)
	HH = str(d.hour).zfill(2)

	geopt_MSp[:,n]=np.ma.load(path_insp + '/geopt_spread_' + YY + MM + DD + HH + '_ana' +ANA)
	tk_MSp[:,n]=np.ma.load(path_insp + '/tk_spread_' + YY + MM + DD + HH + '_ana' +ANA)
	q_MSp[:,n]=np.ma.load(path_insp + '/q_spread_' + YY + MM + DD + HH + '_ana' +ANA)
	u_MSp[:,n]=np.ma.load(path_insp + '/u_spread_' + YY + MM + DD + HH + '_ana' +ANA)
	v_MSp[:,n]=np.ma.load(path_insp + '/v_spread_' + YY + MM + DD + HH + '_ana' +ANA)
	psfc_MSp[0,n]=np.ma.load(path_insp + '/psfc_spread_' + YY + MM + DD + HH + '_ana' +ANA)

	n=n+1
	d = d + delta	# Loop de la fecha

np.ma.dump(geopt_MSp, path_salida  + 'spread/' + exp + '/geopt_spread_'+ str(NoDD) + 'Days'  +periodo+ '_ana' +ANA  )
np.ma.dump(tk_MSp, path_salida + 'spread/' + exp + '/tk_spread_' + str(NoDD) + 'Days' +periodo+ '_ana' +ANA  )
np.ma.dump(q_MSp, path_salida  + 'spread/' + exp + '/q_spread_' + str(NoDD) + 'Days'  +periodo+ '_ana' +ANA )
np.ma.dump(u_MSp, path_salida   + 'spread/' + exp + '/u_spread_' + str(NoDD) + 'Days' +periodo+ '_ana' +ANA  )
np.ma.dump(v_MSp, path_salida  + 'spread/' + exp + '/v_spread_' + str(NoDD) + 'Days'  +periodo+ '_ana' +ANA  )
np.ma.dump(psfc_MSp, path_salida   + 'spread/' + exp + '/psfc_spread_' + str(NoDD) + 'Days' +periodo+ '_ana' +ANA )



geopt_MSp = 0
v_MSp = 0
u_MSp = 0
q_MSp = 0
tk_MSp= 0
psfc_MSp = 0


####genero la matriz de RMSE


geopt_MRe = np.ma.empty(( len(vertical_levels), NoDDh ))
tk_MRe = np.ma.empty(( len(vertical_levels), NoDDh ))
q_MRe = np.ma.empty(( len(vertical_levels), NoDDh ))
u_MRe = np.ma.empty(( len(vertical_levels), NoDDh ))
v_MRe = np.ma.empty(( len(vertical_levels), NoDDh ))
psfc_MRe = np.ma.empty(( 1 , NoDDh ))


d = datetime(Y,M,D,H)
n=0
while d <= diafin:

	# hay que inicializar la m aca adentro del loop de los dias, sino sigue contando y no encuentra
	YY = str(d.year)
	MM = str(d.month).zfill(2)
	DD = str(d.day).zfill(2)
	HH = str(d.hour).zfill(2)

	geopt_MRe[:,n]=np.ma.load(path_inre + '/rmsdMean_geopt_' + YY + MM + DD + HH + '_ana' +ANA)
	tk_MRe[:,n]=np.ma.load(path_inre + '/rmsdMean_tk_' + YY + MM + DD + HH + '_ana' +ANA)
	q_MRe[:,n]=np.ma.load(path_inre + '/rmsdMean_q_' + YY + MM + DD + HH + '_ana' +ANA)
	u_MRe[:,n]=np.ma.load(path_inre + '/rmsdMean_u_' + YY + MM + DD + HH + '_ana' +ANA)
	v_MRe[:,n]=np.ma.load(path_inre + '/rmsdMean_v_' + YY + MM + DD + HH + '_ana' +ANA)
	psfc_MRe[0,n]=np.ma.load(path_inre + '/rmsdMean_psfc_' + YY + MM + DD + HH + '_ana' +ANA)

	n=n+1
	d = d + delta	# Loop de la fecha

np.ma.dump(geopt_MRe, path_salida  + 'RMSEns/' + exp + '/geopt_rmsdMean_'+ str(NoDD) + 'Days'  +periodo+ '_ana' +ANA  )
np.ma.dump(tk_MRe, path_salida  + 'RMSEns/' + exp + '/tk_rmsdMean_' + str(NoDD) + 'Days' +periodo+ '_ana' +ANA  )
np.ma.dump(q_MRe, path_salida   + 'RMSEns/' + exp + '/q_rmsdMean_' + str(NoDD) + 'Days'  +periodo+ '_ana' +ANA )
np.ma.dump(u_MRe, path_salida   + 'RMSEns/' + exp + '/u_rmsdMean_' + str(NoDD) + 'Days' +periodo+ '_ana' +ANA  )
np.ma.dump(v_MRe, path_salida  + 'RMSEns/' + exp + '/v_rmsdMean_' + str(NoDD) + 'Days'  +periodo+ '_ana' +ANA  )
np.ma.dump(psfc_MRe, path_salida   + 'RMSEns/' + exp + '/psfc_rmsdMean_' + str(NoDD) + 'Days' +periodo+ '_ana' +ANA )


geopt_MRe = 0
v_MRe = 0
u_MRe = 0
q_MRe = 0
tk_MRe= 0
psfc_MRe = 0

gc.collect()	# Saca la basura de la memoria








