# network_association

This code has been developed for the manuscript: "Phenotype-loci associations in networks of patients with rare disorders: application to assist in the diagnosis of novel clinical cases. Anibal Bueno, Rocío Rodríguez-López, Armando Reyes-Palomares, Elena Rojano, Manuel Corpas, Julián Nevado, Pablo Lapunzina, Francisca Sánchez-Jiménez & Juan A.G. Ranea, European Journal of Human Genetics (2018), submitted."
This code has been created by Anibal Bueno and modified by Elena Rojano.

Tested in Python 2.7.10.
pip version: 8.1.2.

The following modules are required: os, sys, optparse, math, numpy, networkx, decimal, pandas.

The python code can be executed using the following structure:

python network_metrics.py -i --input_file -m --metric_type -o -output_file

Metric type can be one of the following:
	"hypergeometric",
	"jaccard",
	"PCC" or 
	"simpson".

Example:
python network_metrics.py -i example.txt -m hypergeometric -o example_output.txt

There is also provided an example network on which to apply the method, and the result after applying it (using Hypergeometric index):
"example.txt" and 
"example_output.txt" files.

The input file shuold be a tabulated file, without headers, in UNICODE LF format, containing two columns, representing relationships betweed phenotypes and patients and between loci and patients. The first column corresponds to both phenotpyes (represented by letters in the example) and loci (represented by numbers in the example) indiscriminately and the second one only to patients (represented by "P"+number in the example).

The output file will be also a tabulated file, without headers, containing three columns: the first two correspond to phenotypes and loci indiscriminately and the third one to the HyI value obtained for each couple.

* Note that the results may contain three types of relationships: phenotype-phenotype, locus-locus and phenotype-locus; as the system projects these nodes of the network into the Patient's layer in order to estabilsh the relationships and their significance. In this study, we only take into account, for our purposes, the relationships between phenotypes and loci.

** See Material and Methods section, Supplementary Material and the References for more information about the algorithm.