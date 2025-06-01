
## Common
import sys
from functools import partial
import numpy as np
import argparse
import logging

## CustomLib ##
from seq_io import yield_sequences

from SequenceOperations import compute_sequence_identity, convolve_sequence, transform_with_hill_sigmoid
from SubSequenceGenerator import generate_shifted_sequences, generate_shifted_sequences_varLen
from SequenceEncoding import one_hot_encoding

## CORE ##
from AbstractAutoCorrelationEngine import AutoCorrelationEngine

## GUI
from matplotlib import pyplot as plt


def GetPlottingFunction( plot_scoring_function, min_shift, max_shift, figure_size, midpoint, steepness ) :

	def wrapper_1(autocorrelation_matrix, name) :
		row_length = len(autocorrelation_matrix[0])
		autocorrelation_matrix_filled = [ np.append(row, np.nan*np.ones(row_length-len(row)) ) for row in autocorrelation_matrix ]
		fig, axs = plt.subplots(figsize=figure_size)
		axs.matshow(autocorrelation_matrix_filled, aspect="auto")
		axs.set_yticks( np.arange(0,max_shift-min_shift,2),np.arange(min_shift, max_shift,2) )
		fig.suptitle(name)
		plt.tight_layout()
		plt.show()	

	def wrapper_2(autocorrelation_matrix, name) :
		row_length = len(autocorrelation_matrix[0])
		autocorrelation_matrix_filled = [ np.append(row, np.nan*np.ones(row_length-len(row)) ) for row in autocorrelation_matrix ]

		fig, axs = plt.subplots(2,1, figsize=figure_size)
		axs[0].matshow(autocorrelation_matrix_filled, aspect="auto")
		axs[0].set_yticks( np.arange(0,max_shift-min_shift,2),np.arange(min_shift, max_shift,2) )
		x = np.linspace(0,1,100)
		axs[1].plot(x, transform_with_hill_sigmoid(x,midpoint,steepness))
		axs[1].set_xlabel("% identity")
		axs[1].set_ylabel("score")
		fig.suptitle(name)
		plt.tight_layout()
		plt.show()

	if plot_scoring_function : return wrapper_2
	return wrapper_1

def parse_commandline_arguments() :
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-f","--file",
		required=True,
		type=str,
		help="path to sequence file"
	)
	parser.add_argument(
		"-ff","--file_format",
		default="fasta",
		type=str,
		help="format for parsing sequence file"
	)
	parser.add_argument(
		"-ls","--lower_shift",
		default=1,
		type=int,
		help="minimum shift value to start with for auto-correlation (default=1)"
	)
	parser.add_argument(
		"-hs","--higher_shift",
		default=40,
		type=int,
		help="maximum shift value to end with for auto-correlation (default=40)"
	)
	parser.add_argument(
		"-k","--kernel_size",
		default=120,
		type=int,
		help="length of sequence motifs to use for auto-correlation motif-motif comparison (default=120)"
	)
	parser.add_argument(
		"-mp","--midpoint",
		default=0.5,
		type=float,
		help="for scoring, indicates the sigmoidal filter midpoint (default=0.5)"
	)
	parser.add_argument(
		"-sp","--steepness",
		default=20.0,
		type=float,
		help="for scoring, indicates the sigmoidal steepness (default=20.0)"
	)
	parser.add_argument(
		"-ps","--plot_sigmoid",
		action="store_true",
		help="plot the sigmoidal scoring function"
	)
	parser.add_argument(
		"-fs","--fig_size",
		nargs=2,
		type=float,
		default = (10,4),
		help="plot height/width"
	)
	args = parser.parse_args()
	return args

def main( file_path, file_format, min_shift=1, max_shift=40, kernel_size=120, midpoint=0.5, steepness=20 ) :

	auto_corr_worker = AutoCorrelationEngine(
		encoding_F    = one_hot_encoding,
		comparison_F  = compute_sequence_identity,
		convolution_F = partial(convolve_sequence, kernel_size=kernel_size, convolution_mode="valid"),
		scoring_F     = partial(transform_with_hill_sigmoid, midpoint=midpoint, steepness=steepness ),
		generator_F   = partial(generate_shifted_sequences, min_shift=min_shift, max_shift=max_shift)
	)

	for name, sequence in yield_sequences( file_path, file_format) :
		logging.info(f"Running AutoCorrelation on {name}")
		auto_corr_matrix = auto_corr_worker.process(sequence)
		plot_results(auto_corr_matrix, name)

def InitLog(args) :
	logging.info("Sequence AutoCorrelation Pipeline")
	logging.info("Author : Antoine Schramm")

	logging.info(f"sequences will be analyzed from {args.file} given {args.file_format} format")
	logging.info(f"autocorrelation will study sequence shifts from {args.lower_shift} to {args.higher_shift}")
	logging.info(f"signal convolution by windowing over {args.kernel_size} positions")
	logging.info(f"scoring using sigmoidal transformation with midpoint at {args.midpoint} and steepness of {args.steepness}")

	logging.info(f"will plot scoring function : {args.plot_sigmoid}")
	logging.info(f"figure size set to {args.fig_size}")


if __name__ == "__main__" :

	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
		handlers=[
			logging.StreamHandler(sys.stdout)
		]
	)

	args = parse_commandline_arguments()
	InitLog(args)


	plot_results = GetPlottingFunction(
		plot_scoring_function = args.plot_sigmoid,
		min_shift	=  args.lower_shift,
		max_shift	=  args.higher_shift,
		figure_size = args.fig_size,
		midpoint = args.midpoint,
		steepness = args.steepness
	)

	main(
		file_path	=  args.file,
		file_format	=  args.file_format,
		min_shift	=  args.lower_shift,
		max_shift	=  args.higher_shift,
		kernel_size	=  args.kernel_size,
		midpoint    =  args.midpoint,
		steepness   =  args.steepness,
	)
