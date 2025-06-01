
import numpy as np
from scipy.signal import fftconvolve, convolve
import logging

### SEQUENCE OPERATIONS ###

def compute_sequence_identity(sequence_1, sequence_2) :
	"""
	Given two one-hot encoded sequences.
	sequence identity is computed by multiplication of the two arrays followed by summation.

	illustration :
		A x A -> [1,0] * [1,0] = [1,0] -> sum = 1
		A x B -> [1,0] * [0,1] = [0,0] -> sum = 0
		
		AAA X ABA 
			-> [ [1,0],[1,0],[1,0] ] * [ [1,0],[0,1],[1,0] ] = [ [1,0],[0,0],[1,0] ]
			-> sum( [ [1,0],[0,0],[1,0] ] ) = [1,0,1] # positions 0 and 2 and identical, position 1 has missmatch

	This function has been implemented under one-hot sequence enconding consideration.
	However, it works with all kind of sequence encoding.
	But, the output of this function may not correspond to sequence identity computing while using a different sequence encoding protocol.
	Thus, make sure you know what you're doing if you don't use one-hot sequence encoding.

	inputs :
		- sequence_1 ( vector encoded sequences ) 
		- sequence_2 ( vector encoded sequences ) 

	returns :
		- sequence ( array )

	"""
	return np.sum( sequence_1 * sequence_2, axis=1 )


def convolve_sequence( sequence, kernel_size=120, convolution_mode="valid" ) :
	"""
	Given an array repporting a single value measurement per position,
	compute a convoluted version of this array using a mobile average strategy.
	the mobile average is carried out using a gliding window.

	** Warning : This function rely on the scipy.signal.convolve function
	if you want to use the fft accelerated version, see convolve_sequence_fft below
	However, unless you're using a crazy big window, this function run faster than fft acceleration
	Benchmark shows better performances while kernel_size approximately under 200.
	Above 200, consider using convolve_sequence_fft instead. But who on earth would use such big window ?
	"""
	kernel = np.ones(kernel_size)/kernel_size
	convolved  = convolve( sequence, kernel, mode=convolution_mode, method="direct")
	return convolved


def convolve_sequence_fft( sequence, kernel_size=120, convolution_mode="valid" ) :
	"""
	Similar to convolve_sequence above.
	This function rely on the fft acceleration procedure. 
	However, in the case of convolution procedure for the computation of a mobile average,
	this method isn't garanteed to be faster than the direct method.
	Benchmarks show faster results using fft for averaging on kernel_size above 200 which is already very big.
	"""
	kernel = np.ones(kernel_size)/kernel_size
	convolved  = convolve( sequence, kernel, mode=convolution_mode, method="fft")
	return convolved


def transform_with_hill_sigmoid( sequence, midpoint=0.5, steepness=10) :
	"""
	apply a sigmoidal filter onto an array of floats

	This function has been implemented with array of identity percent in mind as input sequence.

	The rational behind applying a sigmoidal filter onto identity percent comes with the idea that 
	the extreme low identity percent region carry the same information and the extreme high identity
	percent carry the same information, meaning that whatever the exact identity value is within those chunks,
	the sequences that are compared can be considered as different and similar respectively. The sigmoidal
	filter rescale the identity percent so that the result give a value with better meaning where the region
	of low identities is flatten down to ~0 and the region of high identities is flatten up to ~1.

	The midpoint input argument control which identity value leads to a value of 0.5. In other words, this
	parameter control the position of the sigmoid curve along the x axis.

	The steepness parameter controls how fast the sigmoid curve transit from 0 to one passing throught the
	midpoint. Higher the steepness value, higher the slope at inflexion point.

	Below some rescaling key values for various steepness inputs, assuming midpoint=0.5

	                         Steepness
	 i  |     5     10    15    20    30    40   50    100
	----+---------------------------------------------------
	0.1 |   0.12  0.02  0.00  0.00  0.00  0.00  0.00  0.00
	0.2 |   0.18  0.05  0.01  0.00  0.00  0.00  0.00  0.00
	0.3 |   0.27  0.12  0.05  0.02  0.00  0.00  0.00  0.00
	0.4 |   0.38  0.27  0.18  0.12  0.05  0.02  0.01  0.00
	----+-------------------------------------------------
	0.5 |   0.50  0.50  0.50  0.50  0.50  0.50  0.50  0.50
	----+-------------------------------------------------
	0.6 |   0.62  0.73  0.82  0.88  0.95  0.98  0.99  1.00
	0.7 |   0.73  0.88  0.95  0.98  1.00  1.00  1.00  1.00
	0.8 |   0.82  0.95  0.99  1.00  1.00  1.00  1.00  1.00
	0.9 |   0.88  0.98  1.00  1.00  1.00  1.00  1.00  1.00

	"""
	return 1 / ( 1 + np.exp(-steepness * (sequence-midpoint)) )

