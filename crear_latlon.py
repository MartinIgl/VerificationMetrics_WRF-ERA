#!/usr/bin/env python
#Martin Iglesias Github SudestadaARG
import numpy as np
import pygrib

idx=pygrib.index('gfs_4_20151201_0000_000.grb2','name','typeOfLevel','level')
t = idx.select(name="Temperature",typeOfLevel="isobaricInhPa",level='500')
lat, lon = t[0].latlons()

np.save('lon2d_gfs05.npy',lon)
np.save('lat2d_gfs05.npy',lat)



