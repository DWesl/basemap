# make shaded relief plot of etopo bathymetry/topography data on
# lambert conformal conic map projection.

# the data is interpolated to the native projection grid.

from mpl_toolkits.basemap import Basemap, shiftgrid
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.colors import lightsource

# read in topo data (on a regular lat/lon grid)
# longitudes go from 20 to 380.
topoin = mlab.load('etopo20data.gz')
lons = mlab.load('etopo20lons.gz')
lats = mlab.load('etopo20lats.gz')
# shift data so lons go from -180 to 180 instead of 20 to 380.
topoin,lons = shiftgrid(180.,topoin,lons,start=False)

# setup of basemap ('lcc' = lambert conformal conic).
# use major and minor sphere radii from WGS84 ellipsoid.
m = Basemap(llcrnrlon=-145.5,llcrnrlat=1.,urcrnrlon=-2.566,urcrnrlat=46.352,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',area_thresh=1000.,projection='lcc',\
            lat_1=50.,lon_0=-107.)
# transform to nx x ny regularly spaced native projection grid
nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1
topodat,x,y = m.transform_scalar(topoin,lons,lats,nx,ny,returnxy=True)
ls = lightsource(azdeg = 90, altdeg = 20)
print topodat.shape
rgb = ls.shade(topodat, plt.cm.jet)
# create the figure.
fig=plt.figure(figsize=(8,8))
# plot image over map with imshow.
im = m.imshow(rgb)
# draw coastlines and political boundaries.
m.drawcoastlines()
m.drawcountries()
# draw parallels and meridians.
# label on left, right and bottom of map.
parallels = np.arange(0.,80,20.)
m.drawparallels(parallels,labels=[1,1,0,1])
meridians = np.arange(10.,360.,30.)
m.drawmeridians(meridians,labels=[1,1,0,1])
# set title.
plt.title('ETOPO Shaded Relief - Lambert Conformal Conic')
#plt.savefig('plotmap.pdf')
plt.show()