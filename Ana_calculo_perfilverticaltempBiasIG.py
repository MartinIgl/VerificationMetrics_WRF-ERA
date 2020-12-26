#!/usr/bin/env python
#Martin Iglesias Github SudestadaARG
# Programa para calcular el perfile vertical de Bias, usando matrices Bias hechas previamente

# Voy a necesitar:
#
#	matrices de Bias en 3D que fueron almacenadas asi:
#	np.ma.dump(bias_u, path_out + '/bias_u_' + exp + '_ANA12h')

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
ANA =  '.000'
#se indica que conjunto de datos se usan y que horas del dia que se uso
temp= str(args.Hour).zfill(2) + 'z'#'06Z' '12Z' '18Z''00Z' es la fecha de inicio que usan los calculos de biastemp



if exp=='/GFS' or exp=='/GEFS':
	path_in = '/data/miglesias/verificacion_doc/dif_ERA_GEFS/BIAS' + exp + '/' 
	path_out = '/data/miglesias/verificacion_doc/dif_ERA_GEFS/BIAS' + exp + '/perfilvertical'
	ANA =  '_000'
else:
	path_in = '/data/miglesias/verificacion_doc/dif_ERA_WRFupp/BIAS' + exp  + '/'
	path_out = '/data/miglesias/verificacion_doc/dif_ERA_WRFupp/BIAS' + exp + '/perfilvertical'
	ANA =  '.000'



M=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17', '18','19','20'] #vector numero de miembro de ensamble
#m=0	# Ojo que M[1] = '02', acordate que python empieza a contar desde 0

m = 0 	# hay que inicializar la m aca adentro del loop de los dias, sino sigue contando y no encuentra




while m < len(M):
	if exp == '/GFS':
		bias_geo = np.ma.load( path_in + 'bias_geo_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA )
		bias_u = np.ma.load( path_in + 'bias_u_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA)
		bias_v = np.ma.load( path_in + 'bias_v_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA)
		bias_t = np.ma.load( path_in + 'bias_t_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA)
		bias_q = np.ma.load( path_in + 'bias_q_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA)

	else:

		bias_geo = np.ma.load( path_in + M[m] + '/bias_geo_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA )
		bias_u = np.ma.load( path_in + M[m] + '/bias_u_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA)
		bias_v = np.ma.load( path_in + M[m] + '/bias_v_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA)
		bias_t = np.ma.load( path_in + M[m] + '/bias_t_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA)
		bias_q = np.ma.load( path_in + M[m] + '/bias_q_' + temp + '_M'+ M[m]+'_'+periodo+'_ana' + ANA)


	bias_geo_vert = np.ma.mean(np.ma.mean(bias_geo, axis = (1)),axis=(1))
	bias_u_vert = np.ma.mean(np.ma.mean(bias_u, axis = (1)),axis=(1))
	bias_v_vert = np.ma.mean(np.ma.mean(bias_v, axis = (1)),axis=(1))
	bias_t_vert = np.ma.mean(np.ma.mean(bias_t, axis = (1)),axis=(1))
	bias_q_vert = np.ma.mean(np.ma.mean(bias_q, axis = (1)),axis=(1))

	if exp == '/GFS':
		np.ma.dump(bias_geo_vert, path_out + '/bias_geo_vert_' + temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
		np.ma.dump(bias_u_vert, path_out + '/bias_u_vert_'+ temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
		np.ma.dump(bias_v_vert, path_out + '/bias_v_vert_'+ temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
		np.ma.dump(bias_t_vert, path_out + '/bias_t_vert_'+ temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
		np.ma.dump(bias_q_vert, path_out + '/bias_q_vert_'+ temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)

	else:
		np.ma.dump(bias_geo_vert, path_out + '/'  + M[m] + '/bias_geo_vert_' + temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
		np.ma.dump(bias_u_vert, path_out  + '/' + M[m] + '/bias_u_vert_'+ temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
		np.ma.dump(bias_v_vert, path_out  + '/' + M[m] + '/bias_v_vert_'+ temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
		np.ma.dump(bias_t_vert, path_out  + '/' + M[m] + '/bias_t_vert_'+ temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)
		np.ma.dump(bias_q_vert, path_out + '/' + M[m]  + '/bias_q_vert_'+ temp + '_M'+ M[m] +'_'+periodo+'_ana' + ANA)



	bias_geo = 0
	bias_geo_vert = 0 
	bias_u = 0
	bias_u_vert = 0
	bias_v = 0
	bias_v_vert = 0
	bias_t = 0
	bias_t_vert = 0
	bias_q = 0
	bias_q_vert = 0

	m = m + 1	# Loop de los miembros



gc.collect()	# Saca la basura de la memoria
	

