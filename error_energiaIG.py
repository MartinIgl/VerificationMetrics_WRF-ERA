# Modulos para calcular el error de la energia
# basandome en: 
# Saucedo (2016)
# Tan etal (2004)
# Ehrendorfer etal (1999)
# Ota etal (2013)
#Martin Iglesias Github SudestadaARG
import numpy as np

def error_energia_seca(rho,udif,vdif,tdif,pdif):

	"""
	Funcion para calcular el error de energia seca (EES) para todo i,j,k
	pesado por la densidad
	El calculo corresponde a la ecuac (2.46) de la tesis de Saucedo (2016)
	
	Keyword args:
	rho -- densidad del estado de referencia
	udif -- diferencia de la componente u, entre el estado que se evalua y el estado de referencia
	vdif -- diferencia de la componente v, entre el estado que se evalua y el estado de referencia
	tdif -- diferencia de la temperatura, entre el estado que se avalua y el estado de referencia
	pdif -- diferencia de la PSFC, entre el estado que se evalua y el estado de referencia

	rho, udif, vdif, tdif : dimension k,i,j
	pdif : dimension i,j

	Output:
	1 array con la EES [kg m-1 s-2]
	"""

	Cpd = 1004.	# Calor especifico a presion cte del aire seco [J/KgK]
	Rd = 287.05	# Constante del aire seco [J/KgK]
	Tr = 287.	# Temperatura de referencia [K] 
	Pref = 100000.	# Presion de superficie de referencia [Pa]

	# Constantes auxiliares:
	A = Cpd/Tr
	B = Rd*Tr/(Pref*Pref)

	# para facilitar las cuentas, armo un array repitiendo en todos los niveles la pdif:
	pdif_niv=np.ma.empty((np.shape(rho)[0],np.shape(pdif)[0],np.shape(pdif)[1]))
	for k in np.arange(np.shape(pdif_niv)[0]):
		pdif_niv[k,:,:] = pdif

	EES = 0.5 * rho * ( udif*udif + vdif*vdif + A*(tdif*tdif) + B*(pdif_niv*pdif_niv) )

	return EES


def EES_total_temporal(rho,EEST):

	"""
	Funcion para calcular la integracion temporal del error de energia seca (EES) 
        pesado por la masa total. 
	Para cada tiempo obtengo un solo valor, porque promedio en i,j,k
        El calculo corresponde a la ecuac (2.47) de la tesis de Saucedo (2016)

	Keyword args:
	rho -- densidad del estado de referencia 
	EEST -- error de energia seca para varios tiempos. Dimension t,k,i,j

	Output:
	1 array con la EES_TT, dimension axis 0 [m2 s-2]
	"""

	EES_TT = np.ma.sum(EEST, axis = (1,2,3)) / np.sum(rho, axis = (1,2,3))

	return EES_TT


def EES_total_vertical(rho,EEST):

        """
        Funcion para calcular la integracion vertical del error de energia seca (EES) 
        pesado por la masa total. 
        Para cada nivel obtengo un solo valor, porque promedio en i,j,t
        El calculo corresponde a la ecuac (2.47) de la tesis de Saucedo (2016)

        Keyword args:
	rho -- densidad del estado de referencia
        EEST -- error de energia seca para varios tiempos. Dimension t,k,i,j

        Output:
        1 array con la EES_TV, dimension axis 1 [m2 s-2]
        """

	EES_TV = np.ma.sum(EEST, axis = (0,2,3)) / np.sum(rho, axis = (0,2,3))

        return EES_TV


def EES_total_horizontal(rho,EEST):

        """
        Funcion para calcular la integracion horizontal del error de energia seca (EES) 
        pesado por la masa total. 
        Para cada i,j obtengo un solo valor, porque promedio en k,t
        El calculo corresponde a la ecuac (2.47) de la tesis de Saucedo (2016)

        Keyword args:
	rho -- densidad del estado de referencia
        EEST -- error de energia seca para varios tiempos. Dimension t,k,i,j

        Output:
        1 array con la EES_TH, dimension axis 2,3 [m2 s-2]
        """

	EES_TH = np.ma.sum(EEST, axis = (0,1)) / np.sum(rho, axis = (0,1))

        return EES_TH


def DTE(udif,vdif,tdif):

        """
        Funcion para calcular el error de energia DTE i,j,k
        El calculo corresponde a la ecuac (1) de Tan y otros (2004)
        
        Keyword args:
        udif -- diferencia de la componente u, entre el estado que se evalua y el estado de referencia
        vdif -- diferencia de la componente v, entre el estado que se evalua y el estado de referencia
        tdif -- diferencia de la temperatura, entre el estado que se avalua y el estado de referencia

        udif, vdif, tdif : dimension k,i,j
        
        Output:
        1 array con la DTE [m2 s-2]
        """
 
	Cpd = 1004.     # Calor especifico a presion cte del aire seco [J/KgK]
        Tr = 287.       # Temperatura de referencia [K] 

	# Constantes auxiliares:
        A = Cpd/Tr

	DTE = 0.5 * ( udif*udif + vdif*vdif + A*(tdif*tdif) )

        return DTE


def RM_DTE_horizontal(DTE):

        """
        Funcion para calcular la raiz de la media horizontal de DTE 
        Para cada i,j obtengo un solo valor, porque promedio en k,t

        Keyword args:
        DTE -- error de energia seca para varios tiempos. Dimension t,k,i,j

        Output:
        1 array con la RM_DTE_H, dimension axis 2,3 [m s-1]
        """

        RM_DTE_H = np.ma.sqrt( np.ma.mean( np.ma.mean(DTE, axis = 0), axis = 0 ) )

        return RM_DTE_H


def RM_DTE_vertical(DTE):

        """
        Funcion para calcular la raiz de la media vertical de DTE 
        Para cada k obtengo un solo valor, porque promedio en t,i,j

        Keyword args:
        DTE -- error de energia seca para varios tiempos. Dimension t,k,i,j

        Output:
        1 array con la RM_DTE_V, dimension axis 1 [m s-1]
        """

        RM_DTE_V = np.ma.sqrt( np.ma.mean( np.ma.mean( np.ma.mean(DTE, axis = 0), axis = 1 ), axis=1 ) )

        return RM_DTE_V


def RM_DTE_temporal(DTE):

        """
        Funcion para calcular la raiz de la media temporal de DTE 
        Para cada t obtengo un solo valor, porque promedio en k,i,j

        Keyword args:
        DTE -- error de energia seca para varios tiempos. Dimension t,k,i,j

        Output:
        1 array con la RM_DTE_T, dimension axis 0 [m s-1]
        """

        RM_DTE_T = np.ma.sqrt( np.ma.mean( np.ma.mean( np.ma.mean(DTE, axis = 1), axis = 1 ), axis=1 ) )

        return RM_DTE_T



# Se usa este por ahora 
def error_energia_total_humeda(udif,vdif,tdif,pdif,qdif,wq):

        """
        Funcion para calcular el error de energia total humeda (EETH) para todo i,j,k
        El calculo corresponde a la ecuac (2.2) de Ehrendorfer etal (1999), pero utilizando
	el valor de Tr de Ota etal (2013)
	Se la llama TE o Moist Total Energy
        
        Keyword args:
        udif -- diferencia de la componente u, entre el estado que se evalua y el estado de referencia
        vdif -- diferencia de la componente v, entre el estado que se evalua y el estado de referencia
        tdif -- diferencia de la temperatura, entre el estado que se evalua y el estado de referencia
        pdif -- diferencia de la PSFC, entre el estado que se evalua y el estado de referencia
        qdif -- diferencia de la humedad especifica, entre el estado que se evalua y el estado de referencia
	wq -- parametro adimensional que se utiliza para prener o apagar el termino de humedad. Si es 1 se incluye, si es 0 se descarta

        udif, vdif, tdif, qdif : dimension k,i,j
        pdif : dimension i,j

        Output:
        1 array con la EETH [J Kg-1]
        """

        Cp = 1005.7     # Calor especifico a presion cte [J/KgK]
        Rd = 287.04     # Constante del aire seco [J/KgK]
	L = 2510400	# Calor latente de condensacion por unidad de masa [J/Kg]
        Tr = 280.       # Temperatura de referencia [K] 
        Pref = 1000.  # Presion de superficie de referencia [hPa]

        # Constantes auxiliares:
        A = Cp/Tr
        B = Rd*Tr/(Pref*Pref)
	C = wq*L*L/(Cp*Tr)

        # para facilitar las cuentas, armo un array repitiendo en todos los niveles la pdif:
        pdif_niv=np.ma.empty((np.shape(udif)[0],np.shape(pdif)[0],np.shape(pdif)[1]))
        for k in np.arange(np.shape(pdif_niv)[0]):
                pdif_niv[k,:,:] = pdif

#	pdif_niv=np.ma.zeros((np.shape(udif)[0],np.shape(pdif)[0],np.shape(pdif)[1]))
#	pdif_niv[0,:,:] = pdif

	cinetica = 0.5 * ( udif*udif + vdif*vdif )
	temp = 0.5 * A * (tdif*tdif)
	psup = 0.5 * B * (pdif_niv*pdif_niv)
	humedad = 0.5 * C * (qdif*qdif) 
        EETH = cinetica + temp + psup + humedad

        return (cinetica, temp, psup, humedad, EETH )


def M_EETH_horizontal(EETH):

        """
        Funcion para calcular la media horizontal de EETH (o alguno de sus terminos) 
        Para cada i,j obtengo un solo valor, porque promedio en k,t

        Keyword args:
        EETH -- error de energia total humeda para varios tiempos. Dimension t,k,i,j
		tambien se puede usar para sus terminos por separado:
		cinetica, temp, psup, humedad

        Output:
        1 array con la M_EETH_H, dimension axis 2,3 [J Kg-1]
        """

        M_EETH_H = np.ma.mean( np.ma.mean(EETH, axis = 0), axis = 0 ) 

        return M_EETH_H


def M_EETH_vertical(EETH):

        """
        Funcion para calcular la media vertical de EETH (o alguno de sus terminos) 
        Para cada k obtengo un solo valor, porque promedio en t,i,j

        Keyword args:
        EETH -- error de energia total humeda para varios tiempos. Dimension t,k,i,j
                tambien se puede usar para sus terminos por separado:
                cinetica, temp, psup, humedad

        Output:
        1 array con la M_EETH_V, dimension axis 1 [J Kg-1]
        """

        M_EETH_V = np.ma.mean( np.ma.mean( np.ma.mean(EETH, axis = 0), axis = 1 ), axis=1 )

        return M_EETH_V


def M_EETH_temporal(EETH):

        """
        Funcion para calcular la media temporal de EETH (o alguno de sus terminos) 
        Para cada t obtengo un solo valor, porque promedio en k,i,j

        Keyword args:
        EETH -- error de energia total humeda para varios tiempos. Dimension t,k,i,j
                tambien se puede usar para sus terminos por separado:
                cinetica, temp, psup, humedad

        Output:
        1 array con la M_EETH_T, dimension axis 0 [J Kg-1]
        """

        M_EETH_T = np.ma.mean( np.ma.mean( np.ma.mean(EETH, axis = 1), axis = 1 ), axis=1 )

        return M_EETH_T


