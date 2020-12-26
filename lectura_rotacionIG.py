# Modulos para leer/transformar salidas de ARWpost
# Sept 2016 - Maru Dillon, Maxi Sacco
# Modificacion de lectura ctl para usar la rotacion Martin Iglesias 2018 #Github SudestadaARG
# ------------------------------------------------- 

# ********* rotate_uv ************
import numpy as np
import numpy.matlib

def rotate_uv(u,v,truelat1,stand_lon,lon2d,lat2d):

	"""
	Para aplicar a u,v en coordenadas x-y de proyeccion Lambert, y rotarlas  
	a coordenadas de la Tierra W-E,N-S, es decir a las coordenadas posta de U y V
	que son las coordenadas de la proyeccion cilindrica equidistante (o sea lat-lon)
	basado en module_calc_uvmet.f90 del src del ARWpost

	Asumo que truelat1=truelat2 (sino hay que hacer otra cuenta para el cone)
	
	Keywords args:
	u,v -- vientos coord x-y 
	truelat1, stand_lon -- valores del namelist.wps
	lon2d, lat2d -- array de 2 dimensiones de longitudes y latitudes armado con el meshgrid
	
	Output: 
	(urot,vrot) 2 array separados 
	"""

	RAD_PER_DEG = np.pi/180
        cone = np.sin(np.abs(truelat1)*RAD_PER_DEG)

        diff = lon2d - stand_lon

	for i,val in np.ndenumerate(diff):
            if val > 180 :
               diff[i] = val - 360
            if val < -180 :
               diff[i] = val + 360

        alpha = np.zeros(np.shape(lat2d))

	for i,val in np.ndenumerate(lat2d):
    	    if val < 0 :
               alpha[i] = -diff[i] * cone * RAD_PER_DEG
            else:
               alpha[i] = diff[i] * cone * RAD_PER_DEG

        urot = v * np.sin(alpha) + u * np.cos(alpha)
        vrot = v * np.cos(alpha) - u * np.sin(alpha)

	return (urot, vrot) 

# ********* rotate_uv_masked ************
import numpy as np
import numpy.matlib

def rotate_uv_ma(u,v,truelat1,stand_lon,lon2d,lat2d):

	"""
	Para aplicar a u,v en coordenadas x-y de proyeccion Lambert, y rotarlas  
	a coordenadas de la Tierra W-E,N-S, es decir a las coordenadas posta de U y V
	que son las coordenadas de la proyeccion cilindrica equidistante (o sea lat-lon)
	basado en module_calc_uvmet.f90 del src del ARWpost

	Asumo que truelat1=truelat2 (sino hay que hacer otra cuenta para el cone)
	
	Keywords args:
	u,v -- vientos coord x-y 
	truelat1, stand_lon -- valores del namelist.wps
	lon2d, lat2d -- array de 2 dimensiones de longitudes y latitudes armado con el meshgrid
	
	Output: 
	(urot,vrot) 2 array separados 
	"""

	RAD_PER_DEG = np.pi/180
        cone = np.ma.sin(np.ma.abs(truelat1)*RAD_PER_DEG)

        diff = lon2d - stand_lon

	for i,val in np.ndenumerate(diff):
            if val > 180 :
               diff[i] = val - 360
            if val < -180 :
               diff[i] = val + 360

        alpha = np.ma.zeros(np.shape(lat2d))

	for i,val in np.ndenumerate(lat2d):
    	    if val < 0 :
               alpha[i] = -diff[i] * cone * RAD_PER_DEG
            else:
               alpha[i] = diff[i] * cone * RAD_PER_DEG

        urot = v * np.ma.sin(alpha) + u * np.ma.cos(alpha)
        vrot = v * np.ma.cos(alpha) - u * np.ma.sin(alpha)

	return (urot, vrot) 









