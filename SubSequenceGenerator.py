

def generate_shifted_sequences( sequence, min_shift, max_shift ) :
	"""
	generated sequences derived from input sequence by shifting it.
	ensure all sequences generated have the same length (between iterations)
	
	inputs : 
		- sequence (array) : input sequence used as template for shifted version generation
		- min_shift (int)  : minimal shift value to start generation with
		- max_shift (int)  : maximal shift value to end generation with

	yields :
		- sequence_shifted : a shifted version of input sequence
		- sequence_cropped : a cropped version of input sequence with length matching the shifted version

	"""
	sequence_length = len(sequence)
	max_sequence_length = sequence_length - max_shift

	for shift in range( min_shift, max_shift ) :
		sequence_shifted = sequence[shift:]
		sequence_shifted = sequence_shifted[:max_sequence_length]
		sequence_cropped = sequence[:max_sequence_length]
		yield sequence_shifted, sequence_cropped


def generate_shifted_sequences_varLen( sequence, min_shift, max_shift ) :
	"""
	generated sequences derived from input sequence by shifting it.
	Sequences generated have variable decreasing length (between iterations)

	inputs : 
		- sequence (array) : input sequence used as template for shifted version generation
		- min_shift (int)  : minimal shift value to start generation with
		- max_shift (int)  : maximal shift value to end generation with

	yields :
		- sequence_shifted : a shifted version of input sequence
		- sequence_cropped : a cropped version of input sequence with length matching the shifted version

	"""

	sequence_length = len(sequence)
	for shift in range( min_shift, max_shift ) :
		max_sequence_length = sequence_length - shift
		sequence_shifted = sequence[shift:]
		sequence_shifted = sequence_shifted[:max_sequence_length]
		sequence_cropped = sequence[:max_sequence_length]
		yield sequence_shifted, sequence_cropped