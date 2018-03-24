#SetupSignalProcNodes.py
#This script sets up signal processing nodes, especially for getting the transfer function between Mirnov coils and the antenna drive.  It sets up a signal node to hold the Hilbert transform of a parent node, and then a toolbox of TDI expressions that may be used as functions to do calculation of the transfer function (time-domain) locally.
#Ted Golfinopoulos, 23 Feb 2012

from MDSplus import *
import sys

if (len(sys.argv)>1) : #If shot number is provided, use it.
	s=int(sys.argv[1]) #0th argument is script name; first argument is shot number.  Parse integer.
else :
	s=-1 #Otherwise, use model tree as default.

tree = Tree('magnetics',s,'edit')

#Make node for holding signal processing toolbox.
tree.setDefault(tree.getNode('shoelace'))

def addHilbert(parentNode) :
	#hilbert transform of drive signal
	parentNode.addNode('hilbert','signal') #This node will get data from a post-processing routine.


addHilbert(tree.getNode('ant_v'))
addHilbert(tree.getNode('ant_i'))

tree.addNode('toolbox','structure')
toolboxNode=tree.getNode('toolbox')

#signal processing toolbox:
#Here, TDI expressions are put into text nodes.  These may be compiled with arguments in other expressions - a poor-man's function call.
tree.setDefault(toolboxNode)
#ifft(Y) - inverse fast Fourier transform
tree.addNode('ifft','text')
tree.getNode('ifft').putData('CONJG(fft(CONJG($1)) / size($1,1)')

#lp(y,flow) - low-pass filter
tree.addNode('lp','text')
tree.getNode('lp').putData( '_y=$1, _flow=$2, _YY = fft(_y,1), _tt = dim_of(_y), _ff = build_range(0.,1.,1./(size(y,1)-1.))/(_tt[1]-_tt[0]), N=size(_YY), for( _i=0; _i < floor(N/2)+1; _i++ ) { 	if( _ff[_i]>_flow, _YY[_i]=0 ); 	if( _i>0, _YY[ N-_i ] = CONJG(_YY[_i]) ); }, compile( shoelace:toolbox.ifft, _YY )' )

#hp(y,fhigh) - high-pass filter
tree.addNode('hp','text')
tree.getNode('hp').putData( '_y=$1, _fhigh=$2, _YY = fft(_y,1), _tt = dim_of(_y), _ff = build_range(0.,1.,1./(size(y,1)-1.))/(_tt[1]-_tt[0]), for( _i=0; _i < floor(size(_ff,1)/2)+1; _i++ ) { if( _ff[_i]<_fhigh, _YY[_i]=0 ); if( _i>0, _YY[ N-_i ] = CONJG(_YY[_i]) ); }, compile( shoelace:toolbox.ifft, _YY)' )

#bp(y,flow,fhigh) - band-pass filter
tree.addNode('bp', 'text')
tree.getNode('bp').putData('_y=$1, _flow=$2, _fhigh=$3, _YY = fft(_y,1), _tt = dim_of(_y), _ff = build_range(0.,1.,1./(size(y,1)-1.))/(_tt[1]-_tt[0]), for( _i=0; _i < floor(size(_ff,1)/2)+1; _i++ ) { if( _ff[_i]<_flow || _ff[_i]>_fhigh, _YY[_i]=0 ); if( _i>0, _YY[ N-_i ] = CONJG(_YY[_i]) ); }, compile( shoelace:toolbox.ifft, _YY )')

#getTransSyncDetect(y,yrefHilb,flow,fhigh,fdc_cutoff)
tree.addNode('syncDetect','text') 
tree.getNode('syncDetect').putData( '_ysig=$1, _yrefHilb=$2, _flow = $3, _fhigh = $4, _fdcLine = $5, _ysigbp = compile( BP, _ysig, _flow, _fhigh ), _yrefbp = compile( BP, _yrefhilb, _flow, _fhigh ), _H=compile( LP,  _ysigbp*_yrefbp, _fdcLine ) / compile( LP, _yrefbp*_yrefbp, _fdcLine ), /* Transfer function */ _N=size(_H), _tt = dim_of(_ysig), _newNumberSamples=_fdcLine * 4. * (_tt[size(_tt)-1]-_tt[0]), _numSamplesToSkip = _N / _newNumberSamples, /* Downsample transfer function. */ _H=_H[ 0 : N-1 : _numSamplesToSkip ], _ttLow=_tt[ 0 : N-1 : _numSamplesToSkip ], build_signal( _H, *, _ttLow ) /*Return down-sampled transfer function with timebase.*/' )
	
tree.addNode('comment', 'text')
tree.getNode('comment').putData('This structure subtree holds text nodes which define TDI functions.  To call a function, reference   compile( \magnetics::shoelace.toolbox.fun, arg1, arg2, ... ).  Functions: ifft(Y) = inverse fast fourier transform, lp(y,fLowCutoff) = low-pass filter, hp(y,fHighCutoff)=high-pass filter, bp(y,fLowCutoff,fHighCutoff)=band-pass filter, syncDetect(y,yref,fLowCutoff,fHighCutoff,fdcCutoff)=gives (down-sampled) transfer function, y/yref, with yref the hilbert transform of the reference signal (real part of signal + j*90-deg rotation of real part), fLowCutoff/fHighCutoff=low/high frequencies [Hz] inside of which signals are band-pass-filtered, fdcCutoff = cutoff frequency under which multiplied signals are finally low-pass-filtered to give slowly-varying transfer function [Hz].')
#Write changes to tree
tree.write()
