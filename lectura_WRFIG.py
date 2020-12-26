# Modulos para obtener variables del WRF del tipo  wrfprs0( )_20151219_12.000
#
# Es una alternativa al pygrib.index, que para el GFS te tira un warning:
# has multi-field messages, keys inside multi-field messages will not be indexed correctly
#
# Sept 2016 - Maru Dillon, Maxi Sacco
# Modificado 2018 Martin Iglesias #Github SudestadaARG
# ------------------------------------------------- 

# ********* read_WRF ************

import pygrib
import numpy as np


def read_WRF01(wrf,var,lev):

	"""Funcion para leer un grib en grb2 de las variables de altura del la 		salida del WRF Funcion para leer un GFS en grb2
	y obtener numpy arrays de las variables

        Para usar esta funcion necesito abrir el grb2 antes, de la siguiente 		manera:
	   import pygrib
	   wrf=pygrib.open(file)

	Pedis especificamente la variable y el nivel
	Esta funcion se puede ampliar para todas las variables, para eso buscar 	los registros en wrf01[:]
	
	Keyword args:
	wrf -- se refiere al nombre que le asignas la apertura del archivo
	var -- 'u','v','rh','psfc' (vars de superficie) (psfc esta en Pa) 
	       'u','v','t','geopt','spfh' (vars de altura)
	lev -- 0 (para superficie); nivel de presion en hPa (para altura)
	Para WRF01 no se ve el nivel de superficie(lev--0), solo los de altura.
	Output:
	1 array con una sola variable y nivel
	(los numeros de registro se obtuvieron de usar wgrib en los datos del 		WRF tanto para superficie (02) como para niveles de presion (01)
	"""


	if lev == 1000:
                if var == "HGT":          #Geopotential height [gpm]
                        registro = 56
		elif var == "TMP":        #Temp. [K]
                        registro = 57
		elif var == "SPFH":       #Specific humidity [kg/kg]
                        registro = 58
		elif var == "UGRD":       #u wind [m/s]
                        registro = 59
		elif var == "VGRD":       #v wind [m/s]
                        registro = 60
        elif lev == 975:
                if var == "HGT":          #Geopotential height [gpm]
                        registro = 51
		elif var == "TMP":        #Temp. [K]
                        registro = 52
		elif var == "SPFH":       #Specific humidity [kg/kg]
                        registro = 53
		elif var == "UGRD":       #u wind [m/s]
                        registro = 54
		elif var == "VGRD":       #v wind [m/s]
                        registro = 55
        elif lev == 925:
                if var == "HGT":          #Geopotential height [gpm]
                        registro = 46
		elif var == "TMP":        #Temp. [K]
                        registro = 47
		elif var == "SPFH":       #Specific humidity [kg/kg]
                        registro = 48
		elif var == "UGRD":       #u wind [m/s]
                        registro = 49
		elif var == "VGRD":       #v wind [m/s]
                        registro = 50
        elif lev == 850:
                if var == "HGT":          #Geopotential height [gpm]
                        registro = 41
		elif var == "TMP":        #Temp. [K]
                        registro = 42
		elif var == "SPFH":       #Specific humidity [kg/kg]
                        registro = 43
		elif var == "UGRD":       #u wind [m/s]
                        registro = 44
		elif var == "VGRD":       #v wind [m/s]
                        registro = 45
        elif lev == 800:
                if var == "HGT":          #Geopotential height [gpm]
                        registro = 36
		elif var == "TMP":        #Temp. [K]
                        registro = 37
		elif var == "SPFH":       #Specific humidity [kg/kg]
                        registro = 38 
		elif var == "UGRD":       #u wind [m/s]
                        registro = 39
		elif var == "VGRD":       #v wind [m/s]
                        registro = 40
        elif lev == 700: 
                if var == "HGT":          #Geopotential height [gpm]
                        registro = 31
		elif var == "TMP":        #Temp. [K]
                        registro = 32
		elif var == "SPFH":       #Specific humidity [kg/kg]
                        registro = 33
		elif var == "UGRD":       #u wind [m/s]
                        registro = 34
		elif var == "VGRD":       #v wind [m/s]
                        registro = 35
        elif lev == 600:
                if var == "HGT":          #Geopotential height [gpm]
                        registro = 26
		elif var == "TMP":        #Temp. [K]
                        registro = 27
		elif var == "SPFH":       #Specific humidity [kg/kg]
                        registro = 28
		elif var == "UGRD":       #u wind [m/s]
                        registro = 29
		elif var == "VGRD":       #v wind [m/s]
                        registro = 30
        elif lev == 500:
                if var == "HGT":          #Geopotential height [gpm]
                        registro = 21
		elif var == "TMP":        #Temp. [K]
                        registro = 22 
		elif var == "SPFH":       #Specific humidity [kg/kg]
                        registro = 23
		elif var == "UGRD":       #u wind [m/s]
                        registro = 24
		elif var == "VGRD":       #v wind [m/s]
                        registro = 25
        elif lev == 400:
                if var == "HGT":          #Geopotential height [gpm]
                        registro = 16
		elif var == "TMP":        #Temp. [K]
                        registro = 17
		elif var == "SPFH":       #Specific humidity [kg/kg]
                        registro = 18
		elif var == "UGRD":       #u wind [m/s]
                        registro = 19
		elif var == "VGRD":       #v wind [m/s]
                        registro = 20
        elif lev == 300:
                if var == "HGT":          #Geopotential height [gpm]
                        registro = 11
		elif var == "TMP":        #Temp. [K]
                        registro = 12
		elif var == "SPFH":       #Specific humidity [kg/kg]
                        registro = 13
		elif var == "UGRD":       #u wind [m/s]
                        registro = 14
		elif var == "VGRD":       #v wind [m/s]
                        registro = 15

        elif lev == 250:
                if var == "HGT":          #Geopotential height [gpm]
                        registro = 6
		elif var == "TMP":        #Temp. [K]
                        registro = 7
		elif var == "SPFH":       #Specific humidity [kg/kg]
                        registro = 8 
		elif var == "UGRD":       #u wind [m/s]
                        registro = 9
		elif var == "VGRD":       #v wind [m/s]
                        registro = 10

        elif lev == 200:
                if var == "HGT":          #Geopotential height [gpm]
                        registro = 1
		elif var == "TMP":        #Temp. [K]
                        registro = 2
		elif var == "SPFH":       #Specific humidity [kg/kg]
                        registro = 3
		elif var == "UGRD":       #u wind [m/s]
                        registro = 4
		elif var == "VGRD":       #v wind [m/s]
                        registro = 5

	return wrf[registro]['values']



def read_WRF02(wrf,var,lev):

	""" Funcion para leer un grib en grb2 de las variables de superficie del la salida del WRF y obtener numpy arrays de las variables

        wrf=pygrib.open(file)

	Pedis especificamente la variable y el nivel
	Esta funcion se puede ampliar para todas las variables, para eso buscar los registros en wrf02[:]
	
	Keyword args:
	wrf -- se refiere al nombre que le asignas la apertura del archivo
	var -- 'u','v','spfh','psfc', 'APCP' (vars de superficie) (psfc esta en Pa) 
	       'u','v','t','geopt','spfh' (vars de altura)
	lev -- 0 (para superficie); nivel de presion en hPa (para altura)
	
	Output:
	1 array con una sola variable y nivel
	"""
	if lev == 0:
		if var == "UGRD":         #u wind 10[m/s]
			registro = 4				
		elif var == "VGRD":       #v wind 10[m/s]
			registro = 5
		elif var == "SPFH":       #Specific humidity [kg/kg]
			registro = 3
		elif var == "TMP":	  #Temp. 2m [K]
			registro = 2
		elif var == "PRES":	  #Pressure [Pa]
			registro = 1
        	elif var == "APCP":      #Total precipitation acumulada [kg/m^2]
			registro = 6
	return wrf[registro]['values']
