#!/usr/bin/env python
#Martin Iglesias Github SudestadaARG
# Programa para obtener distintas variables de la salida de UPP (postprocessing de WRF)
# e interpolarlas al ERA-Interim
# La idea es guardarlas como numpy array

# Previamente arme los array de lat-lon de ambos modelos, de la siguiente manera:
# UPP:  wrf_idx=pygrib.index('wrfprs01_20151201_00.000','name','typeOfLevel','level')
#	t = wrf_idx.select(name="Temperature",typeOfLevel="isobaricInhPa",level='500')
#	lat_wrf, lon_wrf = t[0].latlons()       # dimension (269, 279)
#	np.save('lon2d_upp.npy',lon_wrf)
#	np.save('lat2d_upp.npy',lat_wrf)
# ERA:  psfc_era = era_sfc_idx.select(name="Surface pressure",typeOfLevel="surface",level=0)
#	lat_era, lon_era = psfc_era[0].latlons()
#	np.save('lon2d_era.npy',lon_era)
#	np.save('lat2d_era.npy',lat_era)

import numpy as np
import os
import pygrib
import gc
from datetime import datetime  
from datetime import timedelta
from matplotlib.mlab import griddata  


from lectura_WRFIG import read_WRF01   
from lectura_WRFIG import read_WRF02
from lectura_rotacionIG import rotate_uv  #se incorporan las nuevas funciones para lectura y rotacion

import argparse
parser = argparse.ArgumentParser(description='Exp')
parser.add_argument('Exp',type=str)
args = parser.parse_args()
Exp=args.Exp

#agregar arpase exp para hacer lectura por experimento

# Caminos de los archivos:
path_upp = '/data/miglesias/CASO_DE_ESTUDIO/CE_'+Exp+'/FCST/2015121900'
path_salida = '/data/miglesias/verificacion_CE/variables_WRF_UPP_interpoladas/CE_'+Exp

# Caracteristicas reticulas:
# Cargo matrices del WRF UPP dimension (269,279):
lat2d_upp = np.load('lat2d_upp.npy')   
lon2d_upp = np.load('lon2d_upp.npy') 

lon2d_upp360 = lon2d_upp + 360   

lon2d_upp360_rav = np.ravel(lon2d_upp360)	# Necesito 0-360 para ser consistente con ERA en la interpolacion
lat2d_upp_rav = np.ravel(lat2d_upp)

# Cargo las matrices de ERA dimension (361,720):
lat2d_era = np.load('/data/miglesias/verificacion_doc/lat2d_era.npy')
lon2d_era = np.load('/data/miglesias/verificacion_doc/lon2d_era.npy')

truelat1 = -34                	#son los puntos en donde la proyeccion Lambert interseca la esfera
stand_lon = -60

vertical_levels = [1000, 975, 925, 850, 800, 700, 600, 500, 400, 300, 250, 200] # en hPa



M=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17', '18','19','20'] #vector numero de miembro de ensamble
#m=0	# Ojo que M[1] = '02', acordate que python empieza a contar desde 0

d=6
Fcst=0
i=0
f=16
while i <= f:
	m = 0
	while m < len(M):	# m < 20

                FCST ='.'+ str(Fcst).zfill(3)

		arch_WRF01 = path_upp + '/' + M[m] + '/wrfprs01_20151219_00'+ FCST 
		arch_WRF02 = path_upp + '/' + M[m] + '/wrfprs02_20151219_00'+ FCST	

		# ------ PSFC -------
		wrf02= pygrib.open(arch_WRF02)
		psfc_upp = read_WRF02(wrf02,'PRES',0)
	        psfc_upp = psfc_upp/100                #viene en Pascales (se pasa a hpa)
		#------PP acumulada----
		#PPacu_upp =read_WRF02(wrf02,'APCP',0)
		#ppacu_rav = np.ma.ravel(PPacu_upp)
		#ppacu_up = griddata(lon2d_upp360_rav, lat2d_upp_rav, geopt_rav, lon2d_era, lat2d_era, interp='linear')
		#np.ma.dump(ppacu_up[190:300,519:679], path_salida + '/' + M[m] + '/pp_acu_upp_20151219_00'+ FCST)
		#PPacu_upp = 0



		# Interpolacion de reticula Lambert a reticula cilindrica del ERA
		# uso griddata y para eso hay que convertir las matrices 2d en 1d con np.ravel:
	        psfc_rav = np.ravel(psfc_upp)
		psfc = griddata(lon2d_upp360_rav, lat2d_upp_rav, psfc_rav, lon2d_era, lat2d_era, interp='linear') 
                 
		# ---------- Variables con niveles verticales -------------
		geopt = np.ma.empty(( len(vertical_levels), np.shape(lat2d_era)[0], np.shape(lat2d_era)[1] )) 
		tk = np.ma.empty(( len(vertical_levels), np.shape(lat2d_era)[0], np.shape(lat2d_era)[1] ))
		q = np.ma.empty(( len(vertical_levels), np.shape(lat2d_era)[0], np.shape(lat2d_era)[1] ))
		u = np.ma.empty(( len(vertical_levels), np.shape(lat2d_era)[0], np.shape(lat2d_era)[1] ))
		v = np.ma.empty(( len(vertical_levels), np.shape(lat2d_era)[0], np.shape(lat2d_era)[1] ))
		
		# Interpolacion de reticula Lambert a reticula cilindrica del ERA
		# uso griddata y para eso hay que convertir las matrices 2d en 1d con np.ravel:
		# OJO: griddata tiene problemas si le das un np enmascarado de input		

		wrf01= pygrib.open(arch_WRF01)

		for k,lev in np.ndenumerate(vertical_levels):
			# ------Geopotencial------	
			geopt_upp = read_WRF01(wrf01,'HGT',lev)
			geopt_upp = geopt_upp * 9.8	
			geopt_rav = np.ma.ravel(geopt_upp)
			geopt_up = griddata(lon2d_upp360_rav, lat2d_upp_rav, geopt_rav, lon2d_era, lat2d_era, interp='linear')

			geopt[k,:,:] = np.ma.masked_where(psfc-lev < 0, geopt_up)	# Hay que usar la psfc interpolada

		np.ma.dump(geopt[:,190:300,519:679], path_salida + '/' + M[m] + '/geopt_upp_20151219_00'+ FCST)
		# Libero memoria:
		geopt = 0
		geopt_up = 0
		geopt_rav = 0
		geopt_upp = 0

		for k,lev in np.ndenumerate(vertical_levels):
			# ------Temperatura------
  	     		tk_upp = read_WRF01(wrf01,'TMP',lev)
			tk_rav = np.ma.ravel(tk_upp)
	       		tk_up = griddata(lon2d_upp360_rav, lat2d_upp_rav, tk_rav, lon2d_era, lat2d_era, interp='linear')
		
			tk[k,:,:] = np.ma.masked_where(psfc-lev < 0, tk_up)

		np.ma.dump(tk[:,190:300,519:679], path_salida + '/' + M[m] + '/tk_upp_20151219_00'+ FCST)
		tk = 0
		tk_up = 0
		tk_rav = 0
		tk_upp = 0

		for k,lev in np.ndenumerate(vertical_levels):
			#------Humedad especifica------
			q_upp = read_WRF01(wrf01,'SPFH',lev)
			q_rav = np.ma.ravel(q_upp)	       	
 	      		q_up = griddata(lon2d_upp360_rav, lat2d_upp_rav, q_rav, lon2d_era, lat2d_era, interp='linear')
		
			q[k,:,:] = np.ma.masked_where(psfc-lev < 0, q_up)

		np.ma.dump(q[:,190:300,519:679], path_salida + '/' + M[m] + '/q_upp_20151219_00'+ FCST)
		q = 0
		q_up = 0
		q_rav = 0
		q_upp = 0

		for k,lev in np.ndenumerate(vertical_levels):	
			# ------Viento: componentes U y V------
			u_upp = read_WRF01(wrf01,'UGRD',lev)
			v_upp = read_WRF01(wrf01,'VGRD',lev)

   	    		# antes de interpolar, hay que rotar los vientos:
			(urot,vrot) = rotate_uv(u_upp, v_upp, truelat1, stand_lon, lon2d_upp, lat2d_upp)

			urot_rav = np.ma.ravel(urot) 
			vrot_rav = np.ma.ravel(vrot)
	    	        u_up = griddata(lon2d_upp360_rav, lat2d_upp_rav, urot_rav, lon2d_era, lat2d_era, interp='linear')
        	        v_up = griddata(lon2d_upp360_rav, lat2d_upp_rav, vrot_rav, lon2d_era, lat2d_era, interp='linear')

			u[k,:,:] = np.ma.masked_where(psfc-lev < 0, u_up)
			v[k,:,:] = np.ma.masked_where(psfc-lev < 0, v_up)

		np.ma.dump(u[:,190:300,519:679], path_salida + '/' + M[m] + '/u_upp_20151219_00'+ FCST)
		u = 0
		u_up = 0
		urot_rav = 0
		urot = 0
		u_upp = 0

		np.ma.dump(v[:,190:300,519:679], path_salida + '/' + M[m] + '/v_upp_20151219_00'+ FCST)
		v = 0
                v_up = 0
                vrot_rav = 0
                vrot = 0
                v_upp = 0

		np.ma.dump(psfc[190:300,519:679], path_salida + '/' + M[m] + '/psfc_upp_20151219_00'+ FCST)
		psfc = 0

		# Cierro ambos grib antes de pasar al miembro siguiente: 
		wrf01.close()
		wrf02.close()

		gc.collect()	# Saca la basura de la memoria
		m = m + 1	# Loop de los miembros


	gc.collect()
	Fcst = Fcst + d
	i=i+1


