#!/usr/bin/env python
#Martin Iglesias Github SudestadaARG
# Programa para calcular el perfil vertical (promediado en el tiempo y horizontal) de RMSD, usando matrices RMSD hechas previamente

# Voy a necesitar:
#
#	matrices de RMSD en 3D que fueron almacenadas en: calculo_rmsdtempIG.py
#	

import numpy as np
import os
import argparse
import gc


# Defino argumentos para indicarle la fecha y el miembro por linea de comando:
parser = argparse.ArgumentParser(description='Hour Exp Per')
parser.add_argument('Hour',type=int)
parser.add_argument('Exp',type=str)
parser.add_argument('Per',type=str)
args = parser.parse_args()

periodo= args.Per

exp =  '/' + args.Exp #'/sinnud' #'/spnudUV6h'#'/spnud6h'

#se indica que conjunto de datos se usan y que horas del dia que se uso
temp= str(args.Hour).zfill(2) + 'z'#'06Z' '12Z' '18Z''00Z' es la fecha de inicio que usan los calculos de rmsdtemp



if exp=='/GFS' or exp=='/GEFS':
	path_in = '/data/miglesias/verificacion_doc/dif_ERA_GEFS/RMSD' + exp + '/'
	path_out = '/data/miglesias/verificacion_doc/dif_ERA_GEFS/RMSD' + exp + '/perfilvertical'
	ANA =  '_000'
if periodo=='2meses':
		periodo='_'+periodo
	else:
		periodo=''
	FCST = '_'+ args.FCST
else:
	path_in = '/data/miglesias/verificacion_doc/dif_ERA_WRFupp/RMSD' + exp + '/'  
	path_out = '/data/miglesias/verificacion_doc/dif_ERA_WRFupp/RMSD' + exp + '/perfilvertical'
	ANA =  '.000'
	if periodo=='2meses':
		periodo='_'+periodo
	else:
		periodo=''
	FCST = '.'+ args.FCST


M=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17', '18','19','20'] #vector numero de miembro de ensamble
#m=0	# Ojo que M[1] = '02', acordate que python empieza a contar desde 0

m = 0 	# hay que inicializar la m aca adentro del loop de los dias, sino sigue contando y no encuentra




while m < len(M):
	if exp=='/GFS':
		rmsd_geo = np.ma.load( path_in + 'rmsd_geo_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA )
		rmsd_u = np.ma.load( path_in + 'rmsd_u_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA)
		rmsd_v = np.ma.load( path_in + 'rmsd_v_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA)
		rmsd_t = np.ma.load( path_in + 'rmsd_t_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA)
		rmsd_q = np.ma.load( path_in + 'rmsd_q_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA)

	else:
		rmsd_geo = np.ma.load( path_in + M[m] + '/rmsd_geo_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA )
		rmsd_u = np.ma.load( path_in + M[m] + '/rmsd_u_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA)
		rmsd_v = np.ma.load( path_in + M[m] + '/rmsd_v_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA)
		rmsd_t = np.ma.load( path_in + M[m] + '/rmsd_t_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA)
		rmsd_q = np.ma.load( path_in + M[m] + '/rmsd_q_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA)


	rmsd_geo_vert = np.ma.mean(np.ma.mean(rmsd_geo, axis = (1)),axis=(1))
	rmsd_u_vert = np.ma.mean(np.ma.mean(rmsd_u, axis = (1)),axis=(1))
	rmsd_v_vert = np.ma.mean(np.ma.mean(rmsd_v, axis = (1)),axis=(1))
	rmsd_t_vert = np.ma.mean(np.ma.mean(rmsd_t, axis = (1)),axis=(1))
	rmsd_q_vert = np.ma.mean(np.ma.mean(rmsd_q, axis = (1)),axis=(1))


	if exp=='/GFS':
		np.ma.dump(rmsd_geo_vert, path_out + '/rmsd_geo_vert_' + temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
		np.ma.dump(rmsd_u_vert, path_out + '/rmsd_u_vert_' + temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
		np.ma.dump(rmsd_v_vert, path_out + '/rmsd_v_vert_' + temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
		np.ma.dump(rmsd_t_vert, path_out + '/rmsd_t_vert_' + temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
		np.ma.dump(rmsd_q_vert, path_out + '/rmsd_q_vert_' + temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
	else:
		np.ma.dump(rmsd_geo_vert, path_out + '/'  + M[m] + '/rmsd_geo_vert_' + temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
		np.ma.dump(rmsd_u_vert, path_out + '/'  + M[m] + '/rmsd_u_vert_' + temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
		np.ma.dump(rmsd_v_vert, path_out + '/'  + M[m] + '/rmsd_v_vert_' + temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
		np.ma.dump(rmsd_t_vert, path_out + '/'  + M[m] + '/rmsd_t_vert_' + temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
		np.ma.dump(rmsd_q_vert, path_out + '/'  + M[m] + '/rmsd_q_vert_' + temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)

	rmsd_geo = 0
	rmsd_geo_vert = 0 
	rmsd_u = 0
	rmsd_u_vert = 0
	rmsd_v = 0
	rmsd_v_vert = 0
	rmsd_t = 0
	rmsd_t_vert = 0
	rmsd_q = 0
	rmsd_q_vert = 0

	m = m + 1	# Loop de los miembros



gc.collect()	# Saca la basura de la memoria
	

