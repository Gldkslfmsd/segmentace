#!/bin/bash
if [ ! -z "$1" ]; then
	source ../p3/bin/activate
	cat demo | python3 triv-morph-split.py -m morfflex-cz.2016-11-15.utf8.lemmaID_suff-tag-form.tab.csv.xz -a czech-morfflex-pdt-161115/czech-morfflex-pdt-161115.tagger -s big_segmenter$1"".pickle -l big_segmenter$1"".pickle derinet-1-4.tsv.gz
else
	# 2: 128G
	# 3: 512G
	# 4: 256G
	qsubmit -jobname=$0""4 -mem=256G "bash triv.cmd 4"
fi
	
