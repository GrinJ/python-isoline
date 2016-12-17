#More info:
#https://www.easycoding.org/2016/12/17/postroenie-izolinij-na-karte-mira-pri-pomoshhi-python-basemap.html

# 'values' is of the format [(lat, lon, val), (lat, lon, val), ..., (lat, lon, val)]
def show_map(values, maxvalue):

    #Import libraries
    from mpl_toolkits.basemap import Basemap, maskoceans
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.interpolate import griddata as gd

    #Create a new figure
    fig = plt.figure()

    #Read the data and convert into numpy array
    lats = np.array([x[0] for x in values])
    lons = np.array([x[1] for x in values])
    data = np.array([x[2] if x[2] <= maxvalue else maxvalue for x in values])

    #Size of the grid
    numcols, numrows = 500, 500

    #Create the grid
    xi = np.linspace(np.min(lons), np.max(lons), numcols)
    yi = np.linspace(np.min(lats), np.max(lats), numrows)

    #Create matrix
    xi, yi = np.meshgrid(xi, yi)

    #Interpolate the data values into our grid
    zi = gd((lons, lats), data, (xi, yi), method='linear')

    #Values of min/max longitude and latitude to display for Europe
    MinLat = 30.0
    MinLon = 0
    MaxLat = 60
    MaxLon = 50

    #Central lat/lon coordinates
    centerLat = 0.5 * (MinLat + MaxLat)
    centerLon = 0.5 * (MinLon + MaxLon)

    #Setup the Basemap with Lambert Conformal Projection
    m = Basemap(llcrnrlon=MinLon, llcrnrlat=MinLat,
                urcrnrlon=MaxLon, urcrnrlat=MaxLat,
                rsphere=(6378137.00, 6356752.3142), \
                resolution='l', area_thresh=1000., projection='lcc', \
                lat_1=45, lat_2=55,
                lat_0=centerLat, lon_0=centerLon)

    #Setup the Basemap with Robinson Projection
    #m = Basemap(projection='robin',lon_0=0,resolution='c')

    #Setup the Basemap with Mercator Projection
    """m = Basemap(
        projection='merc',
        llcrnrlon=MinLon, llcrnrlat=MinLat,
        urcrnrlon=MaxLon, urcrnrlat=MaxLat,
        rsphere=6371200., resolution='l', area_thresh=10000)"""

    #You can see all available projections at:
    # http://matplotlib.org/basemap/users/mapsetup.html

    #Fill the map
    m.drawmapboundary(fill_color='w')
    m.drawcoastlines(color='b')
    m.drawstates(color="w")
    m.drawcountries(color='w', linewidth=1.3)

    #Draw the lats and lons lines
    parallels = np.arange(-90, 90, 10.)
    m.drawparallels(parallels, labels=[True,True,False,False], fontsize=10)
    meridians = np.arange(-180, 180, 15.)
    m.drawmeridians(meridians, labels=[False,False,False,True], fontsize=10)

    #Create contour levels
    clevs = np.linspace(0, maxvalue, 20)

    #Remove the lakes and oceans
    data = maskoceans(xi, yi, zi)

    #Draw the contour
    #m.contour(xi, yi, data, 15, linewidths=0.5, colors='k', latlon=True)

    #Draw filled contour
    cf = m.contourf(xi, yi, data, clevs, cmap=plt.cm.jet, extend='both', latlon=True)

    #Draw colorbar
    cbar = m.colorbar(cf, location='bottom', pad="5%")
    cbar.set_label('Title of colorbar', y=1.2)

    #Draw title
    plt.title("Title of the plot")

    #If you want to save as a picture
    #fig.set_size_inches(12.5, 10.0, forward=True)
    #fig.savefig('result.png', dpi=250, bbox_inches='tight')

    #If you want to print on the display
    plt.show()


#Example call of function
show_map([(46.443673, 8.089143, 10), (55.505339, 25.491487, 15), (40.699175, 21.975862, 18), (37.270531, 14.241487, 1)], 20)