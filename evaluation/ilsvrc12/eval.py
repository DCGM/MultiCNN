import sys
import numpy as np

usage="""Usage:
eval.py validation_data result_data [top X=5]
top X: search in first X results, default is 5"""

len_argv = len(sys.argv)
if(len_argv < 3):
	print(usage)
	exit()

VALDATA = sys.argv[1]
RESULTDATA= sys.argv[2]
TOPX=int(5)
if(len_argv > 3):
	TOPX= int(sys.argv[3]) if sys.argv[3] > 0 else 5

data = dict()
val = dict()

with open(RESULTDATA,"r") as f:
	data.update({member[0][9:]:tuple([float(float_member) for float_member in member[1:]]) for member in [line.strip().split(",") for line in f]})
#       add to dict| key:val                                                                 | member in list from line in file  

true = 0.
false = 0.

with open(VALDATA, "r") as f:
	#val.update({key:int(val) for key,val in [line.split() for line in f]})
	for key,val in [line.split() for line in f]:
		sorted_indices = np.array(data[key]).argsort()[-TOPX:]
		if int(val) in sorted_indices:
			true += 1.
		else:
			false +=1. 

print "True: "+str(true)
print "False: "+str(false)
print "Accuracy: "+str(true/(true+false))
