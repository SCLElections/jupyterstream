import numpy as np
import os
import sys
#============= Update details ========================================
program = 'python runipy_wrapper.py'

list_vals= ['AK', 'AR', 'AZ', 'CO', 'CT', 'DC', 'DE', 'FL', 'IA', 'ID', 'KS', 'KY', 'LA', 'MA', 'ME', 'MD', 'NC', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OK', 'OR', 'PA', 'RI', 'SD', 'UT', 'WV', 'WY']

myvar_str = "state_abrv"
#=====================================================================

run = False
max_parallel = 1                                                                                                                    
for iarg, arg in enumerate(sys.argv[1:]):
    if "-run" == arg: run = True
    if "-parallel" == arg: max_parallel = np.int(sys.argv[iarg + 2])                                                                
nvals = len(list_vals)
print "Number of {} values: {}".format(myvar_str, nvals)
list_vals_str = " ".join(list_vals)
nparallel_str = str( min([max_parallel, nvals]) ) 

if run:
    program += ' -run'
    
command = 'parallel -j {} {} '.format(nparallel_str, program)
command += '-{} '.format(myvar_str)
command += '{1}'
command += ' ::: {}'.format(list_vals_str)

print "=================================================="
print command
print "=================================================="

if run:
    os.system(command)
else:
     print "(The above is the parallel call, but it did not run.) To execute, add the flag: -run "