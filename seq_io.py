
from Bio import SeqIO
import logging

def yield_sequences( file_name, file_format="fasta") :
	"""
	Read a sequence containing file and yields both name and sequence for each entry

	inputs :
		- file_name (str) path to sequence file
		- file_format (str) (default = fasta) see Biopython SeqIO parsing function.

	yields :
		- name (str) the name of the entry
		- sequence (str) the sequence of the entry
	
	returns :
		- None

	raises :
		- FileNotFoundError -> file_name doesn't corresponds to any file on the system
	"""
	logging.info(f"Attempting to read and parse {file_name} given {file_format} format")
	for record in SeqIO.parse(file_name, file_format):
		sequence = str(record.seq)
		name = str(record.id)
		logging.info(f"Yield {name} sequence containing {len(sequence)} letters")
		yield name, sequence
