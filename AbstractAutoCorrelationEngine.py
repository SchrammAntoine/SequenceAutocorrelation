
from time import perf_counter
import logging


class AutoCorrelationEngine() :
	"""
	This class has been implemented in order to provide full function customization on the protocol for sequence repeat detection by autocorrelation.

	The protocol goes has follow :
		(1) for computation purpose, the sequence of interest in encoded into orthogonal vectors, each representing a letter in sequence
		(2) shifted versions of the sequence are generated for autocorrelation purpose
		(3) main sequence and its shifted version are then compared, following those steps :
			(a) Comparison  : direct comparison of the two arrays, leading to single array reporting a distance metric at each position
			(b) Convolution : the signal previously obtained goes throught convolution for accumulating signal in neighborhood
			(c) Scoring : the convoluted signal is then transformed to comprehensive scores in order to highlight the features of interest

	This class is an abstract protocol in which the full workflow is defined but functions for each step presented above are not implemented.
	Those functions must be programmatically set at initialization.
	Those functions are expected to take a specific amount of arguments. Consider using the functools.partial function to setup this object properly.
	"""

	def __init__( self, encoding_F, comparison_F, convolution_F, scoring_F, generator_F ) :
		"""

		encoding_F :
			-> Function used to encore the sequence ( example : SequenceEncoding.one_hot_encoding )
			-> Take one argument : sequence
			-> return an array of vectors 

		comparison_F :
			-> Function for sequence-sequence comparison ( example : SequenceOperations.compute_sequence_identity )
			-> Take two arguments : sequence_1 and sequence_2
			-> return an array of vectors 

		convolution_F :
			-> Function for array convolution ( example : SequenceOperations.convolve_sequence )
			-> Take one argument : array
			-> return an array of numbers (float)

		scoring_F :
			-> Function for array transformation to score ( example : SequenceOperations.transform_with_hill_sigmoid )
			-> Take one argument : array
			-> return an array of numbers (float)

		generator_F :
			-> Function for sequence-sequence generation ( example : SubSequenceGenerator.generate_shifted_sequences )
			-> Take one argument : array of vectors (representing a sequence)
			-> return two array of vectors (representing shifted version of a sequence)

		"""
		self.EncodeSequence = encoding_F
		self.CompareSequences = comparison_F
		self.ConvolveSequence = convolution_F
		self.ScoreSequence = scoring_F
		self.GenerateSequenceShift = generator_F

		self.execution_times = list()

	def process_sequence_pair( self, sequence_1, sequence_2 ) :
		identity  = self.CompareSequences( sequence_1, sequence_2 )
		convolved = self.ConvolveSequence( identity )
		scored    = self.ScoreSequence( convolved )
		return scored

	def process(self, sequence) :
		logging.info(f"starting autocorrelation protocol")
		start = perf_counter()

		sequence = self.EncodeSequence( sequence )
		output = [ 
			self.process_sequence_pair(sequence_1, sequence_2) 
			for sequence_1, sequence_2 in self.GenerateSequenceShift(sequence)
		]

		end = perf_counter()
		self.execution_times.append(end-start)
		logging.info(f"execution done in {end-start:<10.8f} seconds")
		return output


if __name__ == "__main__" :

	## THIS IS AN EXAMPLE OF AutoCorrelationEngine USAGE

	from functools import partial
	from matplotlib import pyplot as plt
	import sys
	from seq_io import yield_sequences


	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
		handlers=[
			logging.StreamHandler(sys.stdout)
		]
	)

	
	### FUNCTION OF INTEREST
	#
	# here we import the functions we want to work with from the dedicated modules
	from SequenceOperations   import compute_sequence_identity
	from SequenceOperations   import convolve_sequence
	from SequenceOperations   import transform_with_hill_sigmoid
	from SubSequenceGenerator import generate_shifted_sequences
	from SequenceEncoding     import one_hot_encoding
	#
	###########################################################################################


	### PARAMETERS ###
	#
	# some of the functions above require parametrization. Here some parameters that will be used below
	#
	min_shift = 1      # goes for generate_shifted_sequences
	max_shift = 40     # goes for generate_shifted_sequences
	kernel_size = 120  # goes for convolve_sequence
	mid_point = 0.5	   # goes for transform_with_hill_sigmoid
	steepness = 20     # goes for transform_with_hill_sigmoid
	#
	###########################################################################################


	### DEFINE FUNCTIONS FOR AUTOCOREL INIT
	#
	# below we wrap multiple arguments functions into simplified version that only required single arguments (others are fixed)
	# to achieved this, we use the partial function from functools module. We can also create our own wrapper if required
	#
	encodingF    = one_hot_encoding
	comparisonF  = compute_sequence_identity
	convolutionF = partial(convolve_sequence, kernel_size=kernel_size, convolution_mode="valid")
	scoringF     = partial(transform_with_hill_sigmoid, midpoint=mid_point, steepness=steepness )
	generatorF   = partial(generate_shifted_sequences, min_shift=min_shift, max_shift=max_shift)
	#
	###########################################################################################

	### AutoCorrelationEngine Setup
	#
	# here we bind all functions to the object for processing. This is done at initialization
	#
	auto_correlation_engine = AutoCorrelationEngine(
		encoding_F    = encodingF, 
		comparison_F  = comparisonF, 
		convolution_F = convolutionF, 
		scoring_F     = scoringF, 
		generator_F   = generatorF
	)
	#
	###########################################################################################


	### Then we can use our protocol as we want
	#
	file_name = "seq/unc13a_gene.fasta"
	for name, sequence in yield_sequences(file_name) :
		output = auto_correlation_engine.process(sequence)
		plt.matshow(output, aspect="auto")
		plt.show()
	#
	###########################################################################################
