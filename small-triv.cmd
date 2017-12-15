source ../p3/bin/activate
cat demo | python3 triv-morph-split.py -m demo-morfflex.lemmaID_suff-tag-form.tab.csv.xz -a czech-morfflex-pdt-161115/czech-morfflex-pdt-161115.tagger demo-derinet-1-4.tsv.gz
