# para generar las matrices de GEFS de lat lon segui los siguientes pasos en ipython:
#Martin Iglesias Github SudestadaARG
import numpy as np
from grads import GrADS

ga = GrADS(Bin='grads',Echo=False,Port=True,Window=False)

CTL = ga.open('gens_20151201_0000_012_01.ctl')

ga('set lev 1000')
t=ga.exp('TMPPRS')

lats = t.grid.lat[:]	# (181,)
lons = t.grid.lon[:]	# (361,)

np.save('lon_gefs.npy',lons)
np.save('lat_gefs.npy',lats)

# Para generar las 2D con dimension (181,361):
lat2d = np.empty((181,361))
for i in range(0,361):
	lat2d[:,i]=lats

lon2d = np.empty((181,361))
for i in range(0,181):
        lon2d[i,:]=lons

np.save('lon2d_gefs.npy',lon2d)
np.save('lat2d_gefs.npy',lat2d)




