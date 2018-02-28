import numpy as np
from matplotlib import pyplot as plt
import tifffile as tif
import time
print 'importing arcpy...'
import arcpy
print 'done'

# f, axarr = plt.subplots(3)
# axarr[0].plot(x, y)
# axarr[0].set_title('Sharing X axis')
# axarr[1].scatter(x, y)

npyPath = r'D:\VATtest\dataCube.npy'
make_datacube = 0
layers = 11

dem = r"Q:\CHII\0_GIS\CHII_Exports\TEST_LH_DEMB_m534_1m.tif"
inRas = arcpy.Raster(dem)
lowerLeft = arcpy.Point(inRas.extent.XMin,inRas.extent.YMin)
cellSize = inRas.meanCellWidth

if make_datacube:
	# dem = r'Q:\CHII\0_GIS\CHII_Exports\LP_DEMB_m534_1m.tif'
	dem = r"Q:\CHII\0_GIS\CHII_Exports\TEST_LH_DEMB_m534_1m.tif"
	# dem = r"Q:\CHII\4_GRID\20140924_152843\t300_s000_m534\DEMB\20140924_152843__s000_m534_4534944_DEMB.tif"
	ws = r'Q:\CHII\0_GIS\CHII_Exports\LP_WATR_m534_1m.tif'

	# t0 = time.time()
	# a = tif.imread(dem)
	# print a.shape
	# print time.time() - t0, 'tifffile'
	
	# plt.imshow(a)
	# plt.show()
	
	t0 = time.time()
	inRas = arcpy.Raster(dem)
	lowerLeft = arcpy.Point(inRas.extent.XMin,inRas.extent.YMin)
	cellSize = inRas.meanCellWidth
	a = arcpy.RasterToNumPyArray(inRas,nodata_to_value=np.nan)
	print a.shape
	print time.time() - t0, 'arcpy'
	
	# plt.imshow(a)
	# plt.show()
	
	# raw_input('continue')



	b = np.zeros((a.shape[0],a.shape[1],layers))
	for i in range(0,layers):
		b[:,:,i]=a

	np.save(npyPath,b)
	
else:
	t0 = time.time()
	b = np.load(npyPath)

print b.shape
shape = b.shape

weights = np.random.rand(b.shape[2])
weights/=weights.sum() #normalizes to total 1

#loop select, 22.5 seconds
# for i in range(0,layers):
	# condlist = [b[:,:,i]>25, b[:,:,i]>20, b[:,:,i]>10, b[:,:,i]>5, b[:,:,i]>0, b[:,:,i]>-5, b[:,:,i]>-10, b[:,:,i]>-20]
	# choicelist = np.arange(len(condlist))*weights[i]
	# choicelist = choicelist.tolist()#should be specified
	# b[:,:,i] = np.select(condlist, choicelist, default=np.nan)
	
#digitize, 10.7 seconds breaks nan
# print ("Numpy version",np.__version__)
for i in range(0,layers):
	bins = np.array([-20,0,5.0, 10.0, 15.0, 20.0]) # requires breakpoints be monotonic
	b[:,:,i] = np.reshape(np.digitize(b[:,:,i].flatten(),bins),(shape[0],shape[1]))*weights[i] # in numper vesion 1.10+ this can be 2d arrays
	


c = np.sum(b, axis=2).astype(int)


vatTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
outTif = r'Q:/test/VATtest/VATtest_fromNUMPY1'+vatTime+'.tif'

newRaster = arcpy.NumPyArrayToRaster(c,lowerLeft,cellSize,
                                     value_to_nodata=0)
newRaster.save(outTif)

print time.time() - t0, 'redone'

plt.imshow(c)
plt.show()


# print a.shape
raw_input('test')

# plt.imshow(a)
# plt.show()

# map = np.random.randint(5, size=(500, 500,11))
# table = np.random.randint(5, size=(5, 3)).astype('float')
# table[:,2]/=5.0




# axarr[0].imshow(table, interpolation='none')
# axarr[1].imshow(map[:,:,2], interpolation='none')
# axarr[2].imshow(map[:,:,1], interpolation='none')
# axarr[1].imshow(table, interpolation='none', vmin=0, vmax=1000)

plt.show()
