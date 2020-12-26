#!/usr/bin/env python
#Martin Iglesias Github SudestadaARG
import numpy as np
import os
import argparse
import gc
from datetime import datetime
from datetime import timedelta
from grads import GrADS

from mpl_toolkits.basemap import interp
from lectura_gefs_ctl import read_ctl
ga = GrADS(Bin='grads',Echo=False,Port=True,Window=False)

path_in = '/data/miglesias/GEFS_FCST12/GEFS_prono12h'
path_out = '/data/miglesias/verificacion_doc/variables_GEFS/'

# Defino argumentos para indicarle la fecha y el miembro por linea de comando:
parser = argparse.ArgumentParser(description='Year Month Day Hour Member FCST')
parser.add_argument('Year',type=int)
parser.add_argument('Month',type=int)
parser.add_argument('Day',type=int)
parser.add_argument('Hour',type=int)
parser.add_argument('Member',type=int)
parser.add_argument('FCST',type=str)
args = parser.parse_args()

Y = args.Year
M = args.Month
D = args.Day
H = args.Hour
FCST = args.FCST
ME = args.Member
MEM = str(ME).zfill(2)

if FCST == '012':
	delta_fcst = timedelta(hours=12)
elif FCST == '006':
	delta_fcst = timedelta(hours=6)
elif FCST == '000':
	delta_fcst = timedelta(hours=0)
else:
	quit()


# Caracteristicas reticulas (hay que interpolar el GEFS al ERA por diferencia de resolucion)
# Ambas son cilindricas
# para usar interp no necesito la matriz 2d de lat lon del GEFS, solo los vectores
lon_gefs = np.load('/home/miglesias/originales/lectura_GFSGEFS/lon_gefs.npy')
lat_gefs = np.load('/home/miglesias/originales/lectura_GFSGEFS/lat_gefs.npy')

# Cargo las matrices de ERA dimension (361,720):
lat2d_era = np.load('/data/miglesias/verificacion_doc/lat2d_era.npy')
lon2d_era = np.load('/data/miglesias/verificacion_doc/lon2d_era.npy')

vertical_levels = [1000, 975, 925, 850, 800, 700, 600, 500, 400, 300, 250, 200] # en hPa

d = datetime(Y,M,D,H)	# Listo, asi queda definida una fecha especifica
YY = str(d.year)
MM = str(d.month).zfill(2)
DD = str(d.day).zfill(2)
HH = str(d.hour).zfill(2)

d_fcst = d + delta_fcst	
# Nombre de fecha para escribir:
Yfcst = str(d_fcst.year)
Mfcst = str(d_fcst.month).zfill(2)
Dfcst = str(d_fcst.day).zfill(2)
Hfcst = str(d_fcst.hour).zfill(2)

gefs_ctl = path_in +'/' + YY + MM + DD + '_' + HH  +'/'+ MEM +'/'+ 'gens_' + YY + MM + DD + '_' + HH + '00_'+ FCST + '_' + MEM + '.ctl'

CTL = ga.open(gefs_ctl)

# ------ PSFC -------

psfc_gefs = read_ctl(ga,'psfc',0)
psfc_gefs = psfc_gefs/100
psfc = interp(psfc_gefs,lon_gefs,lat_gefs,lon2d_era,lat2d_era,masked=True)


# Variables con niveles verticales:
geopt = np.ma.empty(( len(vertical_levels), np.shape(lat2d_era)[0], np.shape(lat2d_era)[1] ))
tk = np.ma.empty(( len(vertical_levels), np.shape(lat2d_era)[0], np.shape(lat2d_era)[1] ))
q = np.ma.empty(( len(vertical_levels), np.shape(lat2d_era)[0], np.shape(lat2d_era)[1] ))
u = np.ma.empty(( len(vertical_levels), np.shape(lat2d_era)[0], np.shape(lat2d_era)[1] ))
v = np.ma.empty(( len(vertical_levels), np.shape(lat2d_era)[0], np.shape(lat2d_era)[1] ))

for k,lev in np.ndenumerate(vertical_levels):

# ------Geopotencial------      
        geopt_gefs = read_ctl(ga,'hgtprs',lev)
        geopt2= interp(geopt_gefs,lon_gefs,lat_gefs,lon2d_era,lat2d_era,masked=True)
	geopt[k,:,:] = np.ma.masked_where(psfc-lev < 0, geopt2)	# Hay que usar la psfc interpolada

# ------Temperatura------
        tk_gefs = read_ctl(ga,'tmpprs',lev)
        tk2 = interp(tk_gefs,lon_gefs,lat_gefs,lon2d_era,lat2d_era,masked=True)
	tk[k,:,:] = np.ma.masked_where(psfc-lev < 0, tk2)

# ------Humedad especifica------
        q_gefs = read_ctl(ga,'spfhprs',lev)
        q2= interp(q_gefs,lon_gefs,lat_gefs,lon2d_era,lat2d_era,masked=True)
	q[k,:,:] = np.ma.masked_where(psfc-lev < 0, q2)

# ------Viento: componentes U y V------
        u_gefs = read_ctl(ga,'ugrdprs',lev)
        v_gefs = read_ctl(ga,'vgrdprs',lev)
        u2 = interp(u_gefs,lon_gefs,lat_gefs,lon2d_era,lat2d_era,masked=True)
	u[k,:,:] = np.ma.masked_where(psfc-lev < 0, u2)

        v2 = interp(v_gefs,lon_gefs,lat_gefs,lon2d_era,lat2d_era,masked=True)
	v[k,:,:] = np.ma.masked_where(psfc-lev < 0, v2)



# Guardamos un dominio:
np.ma.dump(psfc[190:300,519:679], path_out + MEM  + '/' + 'psfc_gefs_'+ str(Yfcst) + str(Mfcst) + str(Dfcst) + str(Hfcst) + '_' + FCST )
np.ma.dump(geopt[:,190:300,519:679], path_out + MEM  + '/' + 'geopt_gefs_'+ str(Yfcst) + str(Mfcst) + str(Dfcst) + str(Hfcst) + '_' + FCST  )
np.ma.dump(tk[:,190:300,519:679], path_out + MEM  + '/' + 'tk_gefs_'+ str(Yfcst) + str(Mfcst) + str(Dfcst) + str(Hfcst) + '_' + FCST  )
np.ma.dump(q[:,190:300,519:679], path_out + MEM  + '/' + 'q_gefs_'+ str(Yfcst) + str(Mfcst) + str(Dfcst) + str(Hfcst) + '_' + FCST )
np.ma.dump(u[:,190:300,519:679], path_out + MEM + '/' + '/' + 'u_gefs_'+ str(Yfcst) + str(Mfcst) + str(Dfcst) + str(Hfcst) + '_' + FCST )
np.ma.dump(v[:,190:300,519:679], path_out + MEM  + '/' + 'v_gefs_'+ str(Yfcst) + str(Mfcst) + str(Dfcst) + str(Hfcst) + '_' + FCST  )

ga.cmd('reinit') #cierra y reinicia



psfc_gefs = 0
psfc = 0
geopt_gefs =0
geopt2 =0
geopt = 0
tk_gefs = 0
tk2 = 0
tk = 0
q_gefs = 0
q2 = 0
q = 0
u_gefs = 0
u2 = 0
u = 0
v_gefs = 0
v2 = 0
v = 0
gc.collect()

