#! /usr/bin/env python
# coding: utf-8
#########################################
#LIBRARIES
#########################################
"""
Get top node parameters from a bipartite graph
"""
import os
import sys
import optparse
import math
import numpy
from networkx import *
from decimal import *
from networkx.algorithms import bipartite
import pandas as pd

# Hypergeometric index implementation by Anibal Bueno and Elena Rojano
#########################################
#METHODS
#########################################

def productorio(mayor, menor):
    resultado = 1
    for i in xrange(mayor, menor, -1):
	resultado = resultado * i
    return resultado

def pcc_weight(G,u,v):
    ny = len(bottom_nodes)
    unbrs = set(G[u])
    vnbrs = set(G[v])
    return (float(len(unbrs & vnbrs)) * ny - (len(unbrs) * len(vnbrs))) / (math.sqrt((len(unbrs) * len(vnbrs)) * (ny - len(unbrs)) * (ny - len(vnbrs)))) 
    
def jaccard(G,u,v):
	unbrs = set(G[u])
	vnbrs = set(G[v])
	return float(len(unbrs & vnbrs)) / len(unbrs | vnbrs)

def hypergeometric(G,u,v):
    unbrs = set(G[u])
    vnbrs = set(G[v])
    init = len(unbrs & vnbrs)
    NA = len(unbrs)
    NB = len(vnbrs)
    end = min(NA,NB)
    output = 0
    ny = len(bottom_nodes)
    for i in xrange(init, end+1, 1):
	half = NA/2
	
	if(i > half):
	    new_NA=productorio(NA,i)
	    new_i=math.factorial(NA-i)
	else:
	    new_NA=productorio(NA,NA-i)
	    new_i=math.factorial(i)
	num1=new_NA/new_i

	up=ny-NA
	down=NB-i
	
	half2 = up/2
	
	if(down > half2):
	    new_up=productorio(up,down)
	    new_down=math.factorial(up-down)
	else:
	    new_up=productorio(up,up-down)
	    new_down=math.factorial(down)
	num2=new_up/new_down	

	half3 = ny/2

	if(NB > half3):
	    new_ny=productorio(ny,NB)
	    new_NB=math.factorial(ny-NB)
	else:
	    new_ny=productorio(ny,ny-NB)
	    new_NB=math.factorial(NB)
	den=new_ny/new_NB

	numerador=num1*num2
	resu = Decimal(numerador)/Decimal(den)
        output += resu
    if output < 9E-324:
    	output = 9E-324
    return -math.log10(output)


#########################################
#OPTPARSE
#########################################
parser = optparse.OptionParser()
parser.add_option('-i', '--input_file',
	dest = "input_filename",
	help = "Input file name",
	default = ""
	)

parser.add_option('-m', '--metric_type',
	dest = "metric",
	help = "Type of metric to use with input data (Jaccard, Hypergeometric, Simpson, PCC)",
	default = ""
	)
parser.add_option('-o', '--output_file',
	dest = "output_filename",
	help = "Output file name",
	default = ""
	)

options, remainder = parser.parse_args()


#########################################
#MAIN
#########################################                             
print "Reading bipartite graph"
print "-----------------------"
nodes = pd.read_csv(options.input_filename, sep='\t', header = None)

B = Graph()
for row in nodes.iterrows():
	B.add_node(row[1][0], bipartite=0)
	B.add_node(row[1][1], bipartite=1)
	B.add_edge(row[1][0], row[1][1])

top_nodes = set(n for n,d in B.nodes(data=True) if d['bipartite']==0)
bottom_nodes = set(B) - top_nodes

top=list(top_nodes)
bottom=list(bottom_nodes)

print "Generating network projection"

if options.metric == "hypergeometric":
	G = bipartite.generic_weighted_projected_graph(B, top_nodes, weight_function=hypergeometric) #HYPERGEOMETRIC
elif options.metric == "jaccard":
	G = bipartite.generic_weighted_projected_graph(B, top_nodes, weight_function=jaccard) #Jaccard
elif options.metric == "PCC":
	G = bipartite.generic_weighted_projected_graph(B, top_nodes, weight_function=pcc_weight) #PCC
elif options.metric == "simpson":
	G = bipartite.overlap_weighted_projected_graph(B, top_nodes, jaccard=False) #Simpson

write_weighted_edgelist(G, options.output_filename, delimiter="\t")
print "Execution finished"