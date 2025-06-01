import numpy as np
import logging

def one_hot_encoding( sequence ) :
	"""
	One-Hot Sequence Encoding transform a sequence of letters into a sequence of vectors.

	One-Hot represents each letter with a n dimentional vector where n corresponds to 
	the number of different letters that are present in the sequence of interest.
	Vectors representing different letters are orthogonals.
	Each vector used for encoding a letter is a unit vector of length 1.

	This function assumes that each letter represent a different object, meaning that this function 
	isn't optimized for working with regular expression that includes letters representing group of 
	other letter (like N = A,T,C or G).
	The length of vectors used for encoding is automatcally determined based on letter usage in sequence.
	
	** Warning 1 : If you use a nucleic acid sequence that combines both U and T (for whatever reasons...), this
	function will consider U and T as different letters and thus will be encoded differently. Make sure the
	sequence you provide in input is cleaned.

	** Warning 2 : This function is case-sensitive, meaning that letters a and A are considered different
	letters. Make sure you know what your sequence looks like prior injecting inputs to this function.

	inputs :
		- sequence (str) : the sequence to encode with One-Hot

	returns :
		- vectorized_sequence (array[array]) : the vectorized sequence

	logging :
		- info > prior encoding, indicates the sequence length and the number of different letters in it
		- info > prior returns, indicates the shape of the output vectorized sequence

	raises :
		- No exception handling implemented
	"""


	# Compute basic stuff to prepare the number of dimensions needed for encoding
	letters = set(sequence)
	dimensions = len(letters)
	logging.info(f"Attempting to encode a sequence with One-Hot. Sequence length is {len(sequence)} and contains the following letters {letters}")

	# Build the unit vectors library for easy encoding based on dictionnary accession
	unit_vectors = dict()
	for i, letter in enumerate(letters) :
		vector = np.zeros( dimensions )
		vector[i] += 1
		unit_vectors[letter] = vector

	# Perform letter encoding
	sequence_vectorized = np.array( [ unit_vectors[letter] for letter in sequence ] )
	logging.info(f"Sequence successfully encoded, new shape -> {sequence_vectorized.shape}")
	return sequence_vectorized