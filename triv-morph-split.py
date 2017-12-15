#!/usr/bin/env python3

import sys
import unittest
import argparse
import logging
import pickle
import os

from lexeme import Lexeme
from segmentshandler import SegmentedLoader, SegmentedStorer
from segmentace_triv import Segmentace


def parse_args():
	parser = argparse.ArgumentParser(description="Extract possible segmentations from dictionaries of derivations and inflections and segment corpora from STDIN.", epilog="By default, only lemmas from DeriNet are loaded. Since segmentation of lemmas only is too limited for most applications, you can optionally enable support for segmenting inflected forms by using the --analyzer or --morfflex options. Loading MorfFlex produces the most detailed segmentation, but it is very memory intensive. Using the MorphoDiTa analyzer is cheaper, but requires you to install the 'ufal.morphodita' package prom PyPI and doesn't segment all forms reliably.")
	
	parser.add_argument("derinet", metavar="DERINET.tsv.gz", help="a path to the compressed DeriNet dictionary.")
	#parser.add_argument("morfflex", metavar="MORFFLEX.tab.csv.xz", help="a path to the compressed MorfFlex dictionary.")
	parser.add_argument("-a", "--analyzer", metavar="DICTIONARY.tagger", help="a path to the MorphoDiTa tagger data. When used, will lemmatize the input data before segmenting, thus supporting segmentation of inflected forms.")
	parser.add_argument("-m", "--morfflex", metavar="MORFFLEX.tab.csv.xz", help="a path to the compressed MorfFlex dictionary. When used, will enrich the dictionary with forms in addition to lemmas, thus supporting segmentation of inflected forms. Beware, this makes the program very memory intensive.")
	parser.add_argument("-f", "--from", metavar="FORMAT", dest="from_format", help="the format to read. Available: vbpe, hbpe, spl, hmorph. Default: spl.", default="spl", choices=["vbpe", "hbpe", "spl", "hmorph"])
	parser.add_argument("-t", "--to", metavar="FORMAT", dest="to_format", help="the format to write. Available: vbpe, hbpe, spl, hmorph. Default: vbpe.", default="vbpe", choices=["vbpe", "hbpe", "spl", "hmorph"])
	#parser.add_argument("morpho", metavar="MORPHO", help="a path to the MorphoDiTa morphological resource.")

	default_save = "segmenter.pickle"
	parser.add_argument("-s", "--save-pickled-segmenter", default=default_save, dest="save", help="save pickled segmenter file to SAVE. Default: %s" % default_save)

	parser.add_argument("-l", "--load-pickled-segmenter", default=default_save, dest="load", help="load pickled segmenter file from SAVE. Default: %s" % default_save)
	
	args = parser.parse_args()
	return args

def set_up_logging():
	# Create a 'root' logger.
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)

	# Create a console handler and set its level to debug.
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)

	# Create a formatter
	formatter = logging.Formatter("%(levelname)s from %(name)s at %(asctime)s: %(message)s")

	# Add the formatter to the handler.
	ch.setFormatter(formatter)

	# Add the handler to the root logger.
	logger.addHandler(ch)


def process_input(loader, storer, segmenter):
	for input_sentence in loader:
		output_sentence = segmenter.segment_sentence(input_sentence)
		storer.print_sentence(output_sentence)


if __name__ == '__main__':
	#unittest.main()
	set_up_logging()
	logger = logging.getLogger(__name__)
	
	logger.info("Started.")
	
	args = parse_args()

#	print(args)
#	sys.exit()
	if not os.path.exists(args.load):
		logger.info("pickled segmenter file %s doesn't exist, loading a new one from source files" % args.load)
		
		derinet_file_name = args.derinet
		morfflex_file_name = args.morfflex
		morpho_file_name = args.analyzer
		
		segmenter = Segmentace(derinet_file_name, morfflex_file_name, morpho_file_name)

		logger.info("saving segmenter to pickle file %s" % args.save)
		with open(args.save, "wb") as f:
			pickle.dump(segmenter, f)
		logger.info("pickled segmenter saved")
	else:
		logger.info("pickled segmenter file %s found, stored segmenter will be used" % args.load)
		with open(args.load, "rb") as f:
			segmenter = pickle.load(f)
	segmenter.load_morpho_file()
	
	logger.info("Ready to split STDIN.")
	
	loader = SegmentedLoader(args.from_format, filehandle=sys.stdin)
	storer = SegmentedStorer(args.to_format, filehandle=sys.stdout)
	
	process_input(loader, storer, segmenter)
	
	logger.info("Finished.")
