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
##    This module holds various functions that publish and plot the results  ##
##    of either the GPS interpolated ephemeris and clock data, or results    ##
##    from the formation satellites' positioning and baseline estimation.    ##
##                                                                           ##
##    Written by Samuel Y. W. Low.                                           ##
##    Last modified 08-Aug-2021.                                             ##
##    Website: https://github.com/sammmlow/LEOGPS                            ##
##    Documentation: https://leogps.readthedocs.io/en/latest/                ##
##                                                                           ##
###############################################################################
###############################################################################

# Import global libraries
import datetime
import matplotlib.pyplot as plt
from decimal import Decimal
import os
def gps_report(gpsdata, goodsats, inps):
    '''Generates an ASCII text report of GPS position, velocity, and clock
    bias (ITRF). Report will be saved in the `output/gps_report` folder.
    
    Parameters
    ----------
    gpsdata : dict
        Nested dictionary of GPS ephemeris and clock data generated by
        `gpsxtr.gpsxtr()`.
    goodsats : list
        Sorted list of GPS satellites without outages by PRN IDs
    inps : dict
        A dictionary of inputs created by `inpxtr.inpxtr()`

    Returns
    -------
    None.

    '''
    
    cwd = inps['cwd'] # Get current main working directory
    
    file_path = open(cwd+ os.sep + 'output' + os.sep + 'gps_report' +  os.sep +'GPS_Report.txt', 'w')
    
    line = 'G         '
    line += 'Pos_X (km)       '
    line += 'Pos_Y (km)       '
    line += 'Pos_Z (km)     '
    line += 'Vel_X (km/s)     '
    line += 'Vel_Y (km/s)     '
    line += 'Vel_Z (km/s)     '
    line += '    Clk_Bias \n'
    file_path.write(line)
    
    # It's all string formatting from here... nothing scientific.
    for t in gpsdata:
        
        line = '\n'
        line += '*  '
        line += str(t.year) + ' '
        line += str(t.month) + ' '
        line += str(t.day) + ' '
        line += str(t.hour) + ' '
        line += str(t.minute) + ' '
        line += str(t.second) + '\n'
        file_path.write(line)

        for p in goodsats:
            
            if p < 10:
                pstr = '0' + str(p)
            else:
                pstr = str(p)
                
            # Write in position information
            line = 'G' + pstr + ' '
            
            for coord in ['x','y','z']:
                pos = str(gpsdata[t][p]['p' + coord])
                dot = pos.index('.')
                if len(pos[dot:]) > 7:
                    pos = pos[:dot+7]
                while len(pos[dot:]) < 7:
                    pos = pos + '0'
                while len(pos[:dot]) < 9:
                    pos = ' ' + pos
                    dot = pos.index('.')
                pos = pos + ' '
                line += pos
                            
            for coord in ['x','y','z']:
                vel = str(gpsdata[t][p]['v' + coord])
                dot = vel.index('.')
                if len(vel[dot:]) > 7:
                    vel = vel[:dot+7]
                while len(vel[dot:]) < 7:
                    vel = vel + '0'
                while len(vel[:dot]) < 9:
                    vel = ' ' + vel
                    dot = vel.index('.')
                vel = vel + ' '
                line += vel
            
            b = '%.9E' % Decimal(str(gpsdata[t][p]['clkb']))
            dot = b.index('.')
            while len(b[:dot]) < 2:
                b = ' ' + b
                dot = b.index('.')
                
            line += str(b)
            line += ' \n'
            file_path.write(line)
            
    file_path.close()
    return None

def gps_graphs(SV, t_usr_dt, t_usr_ss, gpsdata, inps):
    '''Generates a plot of the GPS position, velocity, and clock bias (ITRF).
    Plots will be saved in the `output/gps_plots` folder.

    Parameters
    ----------
    SV : int
        Space vehicle number (1 to 32)
    t_usr_dt : list
        List of `datetime.datetime` objects
    t_usr_ss : list
        List of integer time units in seconds 
    gpsdata : dict
        Nested dictionary of GPS ephemeris and clock data generated by
        `gpsxtr.gpsxtr()`.
    inps : dict
        A dictionary of inputs created by `inpxtr.inpxtr()`

    Returns
    -------
    None.

    '''
    cwd = inps['cwd'] # Get current main working directory
    
    # Turn off interactive plotting
    plt.ioff()
    
    # Initialise the 1x3 subplot for PVT data.
    fig, (ax1, ax2, ax3) = plt.subplots(3,1,figsize=(12,8))
        
    # Get the positions, velocities, and clock biases.
    px = [gpsdata[t][SV]['px'] for t in t_usr_dt]
    py = [gpsdata[t][SV]['py'] for t in t_usr_dt]
    pz = [gpsdata[t][SV]['pz'] for t in t_usr_dt]
    vx = [gpsdata[t][SV]['vx'] for t in t_usr_dt]
    vy = [gpsdata[t][SV]['vy'] for t in t_usr_dt]
    vz = [gpsdata[t][SV]['vz'] for t in t_usr_dt]
    clkb = [gpsdata[t][SV]['clkb'] for t in t_usr_dt]
    
    # Position plots
    ax1.set_title('SV ' + str(SV) + ' Position (km)')
    ax1.plot(t_usr_ss, px, c = 'r', label='X')
    ax1.plot(t_usr_ss, py, c = 'g', label='Y')
    ax1.plot(t_usr_ss, pz, c = 'b', label='Z')
    ax1.legend(loc='lower right')
    
    # Velocity plots
    ax2.set_title('SV ' + str(SV) + ' Velocity (km/s)')
    ax2.plot(t_usr_ss, vx, c = 'r', label='X')
    ax2.plot(t_usr_ss, vy, c = 'g', label='Y')
    ax2.plot(t_usr_ss, vz, c = 'b', label='Z')
    ax2.legend(loc='lower right')
    
    # Clock bias plots
    ax3.set_title('SV ' + str(SV) + ' Clock bias (s)')
    ax3.plot(t_usr_ss, clkb, c = 'k', label='Bias')
    ax3.legend(loc="right")
    
    # Tight-spaced plot
    plt.tight_layout()
    plt.savefig(cwd + os.sep + 'output' + os.sep + 'gps_plots' + os.sep + 'GPS_SV' + str(SV) + '_PVT.png')
    
    # Close this figure
    plt.close(fig)
    
    return None

def leo_results(results, inps):
    '''Generates the final report comprising the solutions to single-point
    positions and velocities of LEO-A and LEO-B, the dilution of precisions,
    the receiver clock bias values, and the precise relative baseline vectors.
    This report is saved in the `output` folder.
    
    Parameters
    ----------
    results : dict
        This is a Python dictionary, with each key being a datetime.datetime
        object, with values as a list of the NumPy arrays as elements:
        [pos1 (1x3), vel1 (1x3), dop1 (1x3), cb1 (1x1), pos2 (1x3), vel2 (1x3),
        dop2 (1x3), cb2 (1x1), baseline (1x3)]
    inps : dict
        A dictionary of inputs created by `inpxtr.inpxtr()`
    
    Returns
    -------
    None.

    '''
    
    print('Saving final report on both LEOs and their baselines \n')
    
    cwd = inps['cwd'] # Get current main working directory
    
    # Get the desired reference coordinate frames.
    frameOrb = inps['frameOrb']
    frameForm = inps['frameForm']
    
    file_path = open(cwd+ os.sep + 'output' + os.sep + 'LEOGPS_Results.txt', 'w')
    
    line  = 'Date       '
    line += 'Time      '
    
    # Headers for LEO 1
    line += inps['name1'] + '_PX_' + frameOrb + '  '
    line += inps['name1'] + '_PY_' + frameOrb + '  '
    line += inps['name1'] + '_PZ_' + frameOrb + '  '
    line += inps['name1'] + '_VX_' + frameOrb + '  '
    line += inps['name1'] + '_VY_' + frameOrb + '  '
    line += inps['name1'] + '_VZ_' + frameOrb + '     '
    line += inps['name1'] + '_GDOP     '
    line += inps['name1'] + '_PDOP     '
    line += inps['name1'] + '_TDOP         '
    line += inps['name1'] + '_ClkB  '
    
    # Headers for LEO 2
    line += inps['name2'] + '_PX_' + frameOrb + '  '
    line += inps['name2'] + '_PY_' + frameOrb + '  '
    line += inps['name2'] + '_PZ_' + frameOrb + '  '
    line += inps['name2'] + '_VX_' + frameOrb + '  '
    line += inps['name2'] + '_VY_' + frameOrb + '  '
    line += inps['name2'] + '_VZ_' + frameOrb + '     '
    line += inps['name2'] + '_GDOP     '
    line += inps['name2'] + '_PDOP     '
    line += inps['name2'] + '_TDOP         '
    line += inps['name2'] + '_ClkB   '
    
    # Headers for baseline information
    line += 'Rel_PX_' + frameForm + '   '
    line += 'Rel_PY_' + frameForm + '   '
    line += 'Rel_PZ_' + frameForm + '   '
    line += '\n'
    file_path.write(line)
    
    # Initialise the array of time steps used in the processing.
    time = sorted( list( results.keys() ) )
    
    # It's all string formatting from here... nothing scientific.
    for t in time:
        
        line  = str(t) # Date-time string (dictionary key)
        
        # Within each vector...
        for vector in results[t]:
            
            # Check if the vector is a 1x3 POS/VEL/DOP
            if len(vector) >= 3:
                for value in vector[:3]:
                    svalue = str(value)
                    dot = svalue.index('.')
                    if len(svalue[dot:]) > 4:
                        svalue = svalue[:dot+4]
                    while len(svalue[dot:]) < 4:
                        svalue = svalue + '0'
                    while len(svalue[:dot]) < 10:
                        svalue = ' ' + svalue
                        dot = svalue.index('.')
                    line += svalue
                    
            # Or the clock bias entry (1x1)
            else:
                for value in vector[:1]:
                    svalue = str(value/299792458.0)
                    dot = svalue.index('.')
                    
                    # Check if clock bias is in standard notation
                    if 'e' in svalue:
                        edot = svalue.index('e')
                        svalue1 = svalue[:dot]
                        svalue2 = svalue[dot:edot]
                        if len(svalue2) > 7:
                            svalue2 = svalue2[:7]
                        svalue3 = svalue[edot:]
                        svalue = svalue1 + svalue2 + svalue3
                    
                    # Else, if it is in decimal...
                    else:
                        if len(svalue[dot:]) > 11:
                            svalue = svalue[:dot+11]
                        while len(svalue[dot:]) < 11:
                            svalue = svalue + '0'
                    
                    while len(svalue[:dot]) < 7:
                        svalue = ' ' + svalue
                        dot = svalue.index('.')
                    line += svalue
                
        line += ' \n'
        file_path.write(line)
    
    file_path.close()
    
    print('Completed processing in LEOGPS! Output file stored:')
    print(cwd + os.sep + 'output'+ os.sep + 'LEOGPS_Results.txt \n')
    
    return None