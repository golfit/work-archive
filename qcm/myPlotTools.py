#This module holds functions convenient for plotting in Python.
#Ted Golfinopoulos, 18 Aug 2012

def myImshow(X, Y, Z, cmap=None, norm=None, aspect=None, interpolation=None, alpha=1.0, vmin=None, vmax=None, origin=None, extent=None, shape=None, filternorm=1, filterrad=4.0, imlim=None, resample=None, url=None, hold=None, **kwargs) :
	"""
	Wrapper for matplotlib.imshow which takes X and Y vectors to use for the axes, rather than the pixel number.

	USAGE:
		myImshow(X,Y,Z,...[as in imshow, where Z replaces X])

	See also: matplotlib.imshow(), matplotlib.pcolor()

	Ted Golfinopoulos, 16 Aug 2012
	"""
	imOut=plt.imshow(Z, cmap, norm, aspect, interpolation, alpha, vmin, vmax, origin, extent, shape, filternorm, filterrad, imlim, resample, url, hold, **kwargs)

	#Rescale labels for axes
	xlocs,xlabels=plt.xticks() #Grab current location and label values for x-axis tick marks.
	ylocs,ylabels=plt.yticks() #Grab current location and label values for y-axis tick marks.

	xlocs=xlocs[1:-2]
	ylocs=ylocs[1:-2]

	print(xlocs)
	#Pixel numbers map to axis indices
	#interpObj=interp1d(range(0,len(X)),X,'linear',bounds_error=False)
	newXLabels=["{0:4.3f}".format(X[i]) for i in xlocs]
	#newXLabels=[interpObj(xlocs[0]), newXLabels[:], interpObj(xlocs[-1])]

	#interpObj=interp1d(range(0,len(Y)),Y,'linear',bounds_error=False)
	newYLabels=["{0:4.3f}".format(Y[i]) for i in ylocs]
	#newYLabels=[interpObj(ylocs[0]), newYLabels[:], interpObj(ylocs[-1])]

	plt.xticks(xlocs,newXLabels)
	plt.yticks(ylocs,newYLabels)

	return imOut
	

