#!/usr/bin/env python3

###############################################################################
###############################################################################
##                                                                           ##
##     _    ___  ___   ___ ___ ___                                           ##
##    | |  | __ /   \ / __| _ | __|                                          ##
##    | |__| __| ( ) | (_ |  _|__ \                                          ##
##    |____|___ \___/ \___|_| \___/                                          ##
##                                    v 1.3 (Stable)                         ##
##                                                                           ##
##    This program is meant to be run as a subroutine in rinxtr.py. If       ##
##    Doppler observables D1/D2 are not found in the output of rinxtr.py,    ##
##    this program will estimate D1/D2 via polynomial interpolation of       ##
##    L1/L2 values, then  a first-order derivative of that polynomial.       ##
##                                                                           ##
##    Inputs: A dictionary of the RINEX observation data generated by        ##
##    rinxtr.rinxtr(). Only GPS observables (no multi-GNSS) are supported.   ##
##                                                                           ##
##    Output: RINEX observations WITH Doppler (pseudorange rate) estimates,  ##
##    saved as a dictionary of epochs, each epoch as a key with a sub-       ##
##    dictionary of GPS satellites based on SV IDs as values, each SV ID     ##
##    as a key with another sub-dictionary of observations. For example:     ## 
##                                                                           ##
##    Output = {epoch1 : {1 : {'L1':123, 'D1':123, ...                       ##
##                             'L4':321, 'flag':'none'} ...} ...             ##
##              epoch2 : {2 : {'L1':123, 'D1':123, ...                       ##
##                             'L4':321, 'flag':'slip'} ...} ...             ##
##                                                                           ##
##              ... ... ... ... ... ...                                      ##
##                                                                           ##
##              epochX : {1 : {'L1':123, 'D1':123, ...                       ##
##                             'L4':321, 'flag':'none'} ...}}                ##
##                                                                           ##
##    Written by Samuel Y. W. Low.                                           ##
##    Last modified 07-Jun-2021.                                             ##
##    Website: https://github.com/sammmlow/LEOGPS                            ##
##    Documentation: https://leogps.readthedocs.io/en/latest/                ##
##                                                                           ##
###############################################################################
###############################################################################

import copy
import numpy as np
import warnings

def dopest(rnxdata, goodsats, tstart, tstop, rnxstep, inps):
    '''Estimation of Doppler (carrier phase rates) using carrier phase.
    
    Parameters
    ----------
    rnxdata : dict
        A nested dictionary comprising code observations, carrier phase,
        but missing Doppler values (thus triggering this function).
    goodsats : list
        Sorted list of GPS satellites without outages by PRN IDs
    tstart : datetime.datetime
        Scenario start time for processing
    tstop : datetime.datetime
        Scenario stop time for processing
    rnxstep :datetime.timedelta
        Observed time step in RINEX file
    inps : dict
        A dictionary of inputs created by `inpxtr.inpxtr()`

    Returns
    -------
    rnxout : dict
        A nested dictionary comprising code observations, carrier phase,
        and non-zero doppler values, at data points where multiple carrier
        phase values are present in sequence.

    '''
    
    warnings.simplefilter('ignore', np.RankWarning) # Ignore polyfit warnings
    freqnum = inps['freq'] # Single frequency or dual frequency processing?
    rnxout = copy.deepcopy(rnxdata) # Copy the input RINEX dictionary
    dopp_condition = False # Condition for performing Doppler estimation.
    print('Estimating Doppler (carrier phase rate) values. \n')
    
    # For each frequency L1/L2...
    for f in range(1,1+freqnum):
        
        # For each GPS satellite...
        for p in goodsats:
            
            L = [] # Initialise the carrier phase array.
            
            # Across all time...
            for t in rnxout:
                
                # If we have at least two L values, we can estimate D values.
                # All observed satellites must have an assigned Doppler value.
                # Invalid Doppler values will be replaced with a 'NaN' string.
                
                if p in rnxout[t]:
                    
                    # Retrieve the flag marked by phasep.py
                    flag = rnxout[t][p]['flag']
                    
                    # We must isolate single L values from the observations.
                    # Because, single points cannot be interpolated.
                    if flag == 'solo' or flag == 'slip':
                        rnxout[t][p]['D'+str(f)] = 'NaN'
                        dopp_condition = False # Not ready yet
                        
                    # Then, we handle the other cases.
                    else:
                        
                        if flag == 'start':
                            L = [] # Reset the carrier phase array.
                            dopp_condition = False # Not ready yet
                        if flag == 'none':
                            dopp_condition = False # Not ready yet
                        if flag == 'end':
                            dopp_condition = True # Ready for processing!
                            
                        # Now, we append the carrier phase values.
                        if 'L'+str(f) in rnxout[t][p]:
                            L.append(rnxout[t][p]['L'+str(f)])
                            
                        else:
                            print('Error! Missing L'+str(f)+'value in epoch:')
                            print(str(t))
                            return False
                
                # Perform the Doppler estimation if L data is ready.
                if dopp_condition == True:
                    
                    # First, let's get the array for time, and phase.
                    L = np.array(L) # Numpy-rize the carrier phase values
                    N = np.linspace(0, len(L)-1, len(L)) # Normalised time
                                        
                    # We perform polynomial fitting of the carrier phase.
                    coeff = np.polyfit(N, L, 19) # Polynomial fit
                    
                    # Next, we get an array for an infinitesimal step of
                    # both time and phase (t + delta-t, and L + delta-L).
                    delta = 0.01 # Delta timestep
                    N_delta = N + delta # N + delta-N
                    L_delta = np.polyval(coeff, N_delta) # L + delta-L
                    
                    # Estimate Doppler with 1st order derivative of L
                    D = ((L-L_delta)/(delta*float(rnxstep.seconds))).tolist()
                    d = 0 # To be used as a counter later for indexing
                    
                    # Now, we want to plug these values back into rnxout.
                    for k in reversed(range(0,len(D))):
                        rnxout[t-(k*rnxstep)][p]['D'+str(f)] = D[d]
                        d += 1 # Update the count
                    
                    L = [] # Reset the carrier phase values array.
                    dopp_condition = False # Reset the condition.
    
    print('Doppler (pseudorange rate) estimation completed. \n')
    return rnxout