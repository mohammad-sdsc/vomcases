#!/usr/bin/env python
# coding: utf-8

# # Does maximisation of net carbon profit explain vegetation behaviour in savanna sites along a precipitation gradient?
# 
# It was shown by Whitley et al. (2016) that six models that expliticly included land surface exchange and vegetation dynamics (i.e. terrestial biosphere models, TBM's) were not able to represent, especially, the wet season dynamics in savanna regions. This reflects generally the simplicity used in the current generation TBM's with regard to modelling vegetation, which becomes especially apparent in the more complex ecosystems of savannas. The understanding of these more complex interactions between vegetation, water and climate in savanna-sites is therefore crucial in order to improve modelling with TBM's. 
# Similar to the model inter-comparison presented by Whitley et al. (2016), in this study a coupled water-vegetation model (VOM, Schymanski et al. 2009) is applied in several savanna sites. In this case, vegetation properties are optimized for net carbon profit, instead of prescribing these.
# 
# The hypotheses tested are:
# 
# - Observed vegetation dynamics in tropical savanna sites can be explained by the maximization of Net Carbon Profit. 
# 
# - Optimization of vegetation properties for the Net Carbon Profit leads to reduced data requirements for Land Surface Models
# 
# - Carbon cost functions for roots, water transport system and foliage are valid along a precipitation gradient
# 
# 
# 

# # Results



import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta, date
from matplotlib.pyplot import imread
import matplotlib.cbook as cbook
from netCDF4 import Dataset
import argparse

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--outfile", help="outputfile with plot")
    parser.add_argument("--vom", help="VOM results", nargs='+')
    parser.add_argument("--vom_pc", help="VOM results", nargs='+')
    parser.add_argument("--vom_pc2", help="VOM results", nargs='+')
    parser.add_argument("--vom_zr", help="VOM results", nargs='+')

    parser.add_argument("--vom_evap_stats", help="vom statistics evaporation", nargs='+')
    parser.add_argument("--vom_gpp_stats", help="vom statistics evaporation", nargs='+')

    parser.add_argument("--vom_pc_evap_stats", help="vom statistics evaporation", nargs='+')
    parser.add_argument("--vom_pc_gpp_stats", help="vom statistics evaporation", nargs='+')

    parser.add_argument("--vom_pc2_evap_stats", help="vom statistics evaporation", nargs='+')
    parser.add_argument("--vom_pc2_gpp_stats", help="vom statistics evaporation", nargs='+')

    parser.add_argument("--vom_zr_evap_stats", help="vom statistics evaporation", nargs='+')
    parser.add_argument("--vom_zr_gpp_stats", help="vom statistics evaporation", nargs='+')

    parser.add_argument("--bess", help="bess input files", nargs='+')
    parser.add_argument("--bios2", help="bios2 input files", nargs='+')
    parser.add_argument("--lpjguess", help="lpj-guess input files, first all files with et, second gpp", nargs='+')
    parser.add_argument("--maespa", help="maespa input files", nargs='+')
    parser.add_argument("--spa", help="spa input files", nargs='+')
    parser.add_argument("--cable", help="cable input files", nargs='+')

    parser.add_argument("--bess_evap_stats", help="bess statistics evaporation", nargs='+')
    parser.add_argument("--bios2_evap_stats", help="bios2 statistics evaporation", nargs='+')
    parser.add_argument("--lpjguess_evap_stats", help="lpj-guess statistics evaporation", nargs='+')
    parser.add_argument("--maespa_evap_stats", help="maespa statistics evaporation", nargs='+')
    parser.add_argument("--spa_evap_stats", help="spa statistics evaporation", nargs='+')
    parser.add_argument("--cable_evap_stats", help="cable statistics evaporation", nargs='+')

    parser.add_argument("--bess_gpp_stats", help="bess statistics assimilation", nargs='+')
    parser.add_argument("--bios2_gpp_stats", help="bios2 statistics assimilation", nargs='+')
    parser.add_argument("--lpjguess_gpp_stats", help="lpj-guess statistics assimilation", nargs='+')
    parser.add_argument("--maespa_gpp_stats", help="maespa statistics assimilation", nargs='+')
    parser.add_argument("--spa_gpp_stats", help="spa statistics assimilation", nargs='+')
    parser.add_argument("--cable_gpp_stats", help="cable statistics assimilation", nargs='+')

    parser.add_argument("--startyear", help="startyears for BESS modelruns", nargs='+')

    parser.add_argument("--sites", help="study sites, should correspond to the number and order of inputfiles", nargs='+')
    parser.add_argument("--whitley_sites", help="mask the study sites that are also used in Whitley et al.",nargs='+', type=int )
    parser.add_argument("--dingo_et", help="DINGO files evaporation", nargs='+')
    parser.add_argument("--dingo_gpp", help="DINGO files assimilation", nargs='+')
    parser.add_argument("--i2015", help="results_daily AoB2015 ")
    parser.add_argument("--figsize", help="figure size", nargs='+', type=float, default = [18,18] )
    parser.add_argument("--fig_lab", dest="fig_lab", action='store_true', help="plot labels of subplots")
    parser.add_argument("--no_fig_lab", dest="fig_lab", action='store_false', help="do not plot labels of subplots")
    parser.add_argument("--sharex", help="share x-axis", dest="sharex", action='store_true' )
    parser.add_argument("--no_sharex", help="share x-axis", dest="sharex", action='store_false')
    parser.set_defaults(fig_lab=True, sharex = True)

    args = parser.parse_args()

    ###################################
    #some constants for conversions
    lat_heat_vapor = 2.26   #[MJ/kg]
    rho_w = 997             #[kg/m3]

    ###################################
    #read in data from Whitley et al. 
    whitley_sites = np.array(args.sites)[np.array(args.whitley_sites)==1]

    bess_assma = dict()
    bess_ema = dict()
    bess_evap_stats = dict()
    bess_ass_stats = dict()

    bios2_assma = dict()
    bios2_ema = dict()
    bios2_evap_stats = dict()
    bios2_ass_stats = dict()

    lpjguess_assma = dict()
    lpjguess_ema = dict()
    lpjguess_evap_stats = dict()
    lpjguess_ass_stats = dict()

    maespa_assma = dict()
    maespa_ema = dict()
    maespa_evap_stats = dict()
    maespa_ass_stats = dict()

    spa_assma = dict()
    spa_ema = dict()
    spa_evap_stats = dict()
    spa_ass_stats = dict()

    cable_assma = dict()
    cable_ema = dict()
    cable_evap_stats = dict()
    cable_ass_stats = dict()

    for i in range(0, len(whitley_sites)):
        #read in data from BESS
        evap_tmp, ass_tmp = read_bess(args.bess[i], args.startyear[i])

        bess_ema[whitley_sites[i]] = np.mean( evap_tmp.resample("A").sum() )
        bess_assma[whitley_sites[i]] = np.mean( ass_tmp.resample("A").sum() )
        bess_evap_stats[whitley_sites[i]] = np.genfromtxt( args.bess_evap_stats[i]  )
        bess_ass_stats[whitley_sites[i]] = np.genfromtxt( args.bess_gpp_stats[i]  )

        #read in data from BIOS2
        evap_tmp, ass_tmp = read_bios2(args.bios2[i])

        bios2_ema[whitley_sites[i]] = np.mean( evap_tmp.resample("A").sum() )
        bios2_assma[whitley_sites[i]] = np.mean( ass_tmp.resample("A").sum() )
        bios2_evap_stats[whitley_sites[i]] = np.genfromtxt( args.bios2_evap_stats[i]  )
        bios2_ass_stats[whitley_sites[i]] = np.genfromtxt( args.bios2_gpp_stats[i]  )

        #read in data from LPJ-GUESS, ET in W/m2, GPP in umol/m2/s
        evap_tmp, ass_tmp = read_lpjguess(args.lpjguess[i], args.lpjguess[i+len(whitley_sites)])
        lpjguess_ema[whitley_sites[i]] = np.mean( evap_tmp.resample("A").sum() )
        lpjguess_assma[whitley_sites[i]] = np.mean( ass_tmp.resample("A").sum() )
        lpjguess_evap_stats[whitley_sites[i]] = np.genfromtxt( args.lpjguess_evap_stats[i]  )
        lpjguess_ass_stats[whitley_sites[i]] = np.genfromtxt( args.lpjguess_gpp_stats[i]  )

        #read in data from MAESPA, ET in W m-2, GPP in umol m-2 s-1
        evap_tmp, ass_tmp = read_maespa(args.maespa[i])
        maespa_ema[whitley_sites[i]] = np.mean( evap_tmp.resample("A").sum() )
        maespa_assma[whitley_sites[i]] = np.mean( ass_tmp.resample("A").sum() )
        maespa_evap_stats[whitley_sites[i]] = np.genfromtxt( args.maespa_evap_stats[i]  )
        maespa_ass_stats[whitley_sites[i]] = np.genfromtxt( args.maespa_gpp_stats[i]  )

        #read in data from SPA, ET in W m-2, GPP in mmol m-2 s-1
        evap_tmp, ass_tmp = read_spa(args.spa[i])
        spa_ema[whitley_sites[i]] = np.mean( evap_tmp.resample("A").sum() )
        spa_assma[whitley_sites[i]] = np.mean( ass_tmp.resample("A").sum() )
        spa_evap_stats[whitley_sites[i]] = np.genfromtxt( args.spa_evap_stats[i]  )
        spa_ass_stats[whitley_sites[i]] = np.genfromtxt( args.spa_gpp_stats[i]  )

        #read in data from CABLE, ET in kg/m^2/s, GPP in umol/m^2/s
        evap_tmp, ass_tmp = read_cable(args.cable[i])
        cable_ema[whitley_sites[i]] = np.mean( evap_tmp.resample("A").sum() )
        cable_assma[whitley_sites[i]] = np.mean( ass_tmp.resample("A").sum() )
        cable_evap_stats[whitley_sites[i]] = np.genfromtxt( args.cable_evap_stats[i]  )
        cable_ass_stats[whitley_sites[i]] = np.genfromtxt( args.cable_gpp_stats[i]  )

    ####################################################
    #load other data 

    dingo_evap = dict()
    dingo_gpp = dict()
    vom_evap = dict()
    vom_pc_evap = dict()
    vom_pc2_evap = dict()
    vom_zr_evap = dict()
    vom_evap_stats = dict()
    vom_pc_evap_stats = dict()
    vom_pc2_evap_stats = dict()
    vom_zr_evap_stats = dict()
    vom_gpp = dict()
    vom_pc_gpp = dict()
    vom_pc2_gpp = dict()
    vom_zr_gpp = dict()
    vom_gpp_stats = dict()
    vom_pc_gpp_stats = dict()
    vom_pc2_gpp_stats = dict()
    vom_zr_gpp_stats = dict()

    for i in range(0, len(args.sites)):
        ea_tmp = np.loadtxt(args.dingo_et[i], usecols=2) #mm/d
        le_tmp = ea_tmp *  lat_heat_vapor * rho_w * 1000/(3600*24) 
        le_time =  np.genfromtxt(args.dingo_et[i],usecols=0, dtype=np.str )#mm/d
        le_time = pd.date_range(le_time[0], le_time[-1], freq='D')   
        e_pd = pd.Series(ea_tmp, index = le_time)         

        gpp_tmp = np.loadtxt(args.dingo_gpp[i], usecols=2) #mm/d
        gpp_obs = -1000000*gpp_tmp/ (3600*24)
        gpp_time =  np.genfromtxt(args.dingo_gpp[i],usecols=0, dtype=np.str )#mm/d
        gpp_time= pd.date_range(gpp_time[0], gpp_time[-1], freq='D')  
        gpp_pd = pd.Series(-gpp_tmp, index = gpp_time)         

        dingo_evap[args.sites[i]] = np.mean( e_pd.resample("A").sum() )
        dingo_gpp[args.sites[i]] = np.mean( gpp_pd.resample("A").sum() )

        vom_tmp = np.genfromtxt(args.vom[i], names=True)
        etot = (vom_tmp["esoil"] + vom_tmp["etmt"] + vom_tmp["etmg"])*1000
        letot= etot[-3650:]* lat_heat_vapor * rho_w * 1000 * 1000/(3600*24)
        gpptot = vom_tmp["assg"] + vom_tmp["asst"]

        vom_pc = np.genfromtxt(args.vom_pc[i], names=True)
        etot_pc = (vom_pc["esoil"] + vom_pc["etmt"] + vom_pc["etmg"])*1000
        letot_pc = etot_pc[-3650:]* lat_heat_vapor * rho_w * 1000 * 1000/(3600*24)
        gpptot_pc = vom_pc["assg"] + vom_pc["asst"]

        vom_pc2 = np.genfromtxt(args.vom_pc2[i], names=True)
        etot_pc2 = (vom_pc2["esoil"] + vom_pc2["etmt"] + vom_pc2["etmg"])*1000
        letot_pc2 = etot_pc2[-3650:]* lat_heat_vapor * rho_w * 1000 * 1000/(3600*24)
        gpptot_pc2 = vom_pc2["assg"] + vom_pc2["asst"]

        vom_zr = np.genfromtxt(args.vom_zr[i], names=True)
        etot_zr = (vom_zr["esoil"] + vom_zr["etmt"] + vom_zr["etmg"])*1000
        letot_zr = etot_zr[-3650:]* lat_heat_vapor * rho_w * 1000 * 1000/(3600*24)
        gpptot_zr = vom_zr["assg"] + vom_zr["asst"]

        time = pd.date_range(datetime(int(vom_tmp["fyear"][3]),int(vom_tmp["fmonth"][0]),int(vom_tmp["fday"][0])), 
              datetime(int(vom_tmp["fyear"][-1]),int(vom_tmp["fmonth"][-1]),int(vom_tmp["fday"][-1])), 
              freq='D')


        emod_pd = pd.Series(etot[-3650:], index = time[-3650:] )
        assmod_pd = pd.Series(gpptot[-3650:], index = time[-3650:] )

        emod_pc_pd = pd.Series(etot_pc[-3650:], index = time[-3650:] )
        assmod_pc_pd = pd.Series(gpptot_pc[-3650:], index = time[-3650:] )

        emod_pc2_pd = pd.Series(etot_pc2[-3650:], index = time[-3650:] )
        assmod_pc2_pd = pd.Series(gpptot_pc2[-3650:], index = time[-3650:] )

        emod_zr_pd = pd.Series(etot_zr[-3650:], index = time[-3650:] )
        assmod_zr_pd = pd.Series(gpptot_zr[-3650:], index = time[-3650:] )

        vom_evap[args.sites[i]] = np.mean( emod_pd.resample("A").sum() )
        vom_gpp[args.sites[i]] = np.mean( assmod_pd.resample("A").sum() )
    
        vom_pc_evap[args.sites[i]] = np.mean( emod_pc_pd.resample("A").sum() )
        vom_pc_gpp[args.sites[i]] = np.mean( assmod_pc_pd.resample("A").sum() )

        vom_pc2_evap[args.sites[i]] = np.mean( emod_pc2_pd.resample("A").sum() )
        vom_pc2_gpp[args.sites[i]] = np.mean( assmod_pc2_pd.resample("A").sum() )

        vom_zr_evap[args.sites[i]] = np.mean( emod_zr_pd.resample("A").sum() )
        vom_zr_gpp[args.sites[i]] = np.mean( assmod_zr_pd.resample("A").sum() )

        vom_evap_stats[args.sites[i]] = np.genfromtxt( args.vom_evap_stats[i]  )
        vom_gpp_stats[args.sites[i]] = np.genfromtxt( args.vom_gpp_stats[i]  )

        vom_pc_evap_stats[args.sites[i]] = np.genfromtxt( args.vom_pc_evap_stats[i]  )
        vom_pc_gpp_stats[args.sites[i]] = np.genfromtxt( args.vom_pc_gpp_stats[i]  )

        vom_pc2_evap_stats[args.sites[i]] = np.genfromtxt( args.vom_pc2_evap_stats[i]  )
        vom_pc2_gpp_stats[args.sites[i]] = np.genfromtxt( args.vom_pc2_gpp_stats[i]  )

        vom_zr_evap_stats[args.sites[i]] = np.genfromtxt( args.vom_zr_evap_stats[i]  )
        vom_zr_gpp_stats[args.sites[i]] = np.genfromtxt( args.vom_zr_gpp_stats[i]  )

    ####################################################
    #start plotting

    #parameters for plotting
    if args.fig_lab is True:
        plot_label = [ "a)","b)","c)","d)","e)","f)", "g)", "h)" ]
    else: 
        plot_label = [ " "," "," "," "," "," ", " ", " " ]

    loc = np.arange(5,65,10) 
    loc_vom =  np.arange(0.5, 60.5, 10)  
    loc_vom2 =  np.arange(1.5, 61.5, 10)  
    loc_vom3 =  np.arange(2.5, 62.5, 10)  
    loc_vom4 =  np.arange(3.5, 63.5, 10)  

    loc_bess = np.arange(4.5, 64.5, 10)
    loc_bios2 = np.arange(5.5, 65.5, 10)
    loc_cable = np.arange(6.5, 66.5, 10)
    loc_lpjguess = np.arange(7.5, 67.5, 10)
    loc_maespa = np.arange(8.5, 68.5, 10)
    loc_spa = np.arange(9.5, 69.5, 10)


    ylabels = [ r"Evaporation [mm/year]",
                r'Assimilation [mol/m$^2$/year]',
                "Rel.Err. evaporation [-]",  
                "Rel.Err. assimilation [-]", 
                "Rel.Err. amplitude evaporation[-]", 
                "Rel.Err. amplitude assimilation[-]", 
                "Err. Min. Annual [-]", 
                "Err. Min. Annual [-]", 
                "Mean Wet Season Rel. Err. [-]", 
                "Mean Wet Season Rel. Err. [-]", 
              ]


    maxy= [1500, 200, 1,1, 1.0, 1.0, 1.0 , 2.0, 1.5,1.5]
    miny= [0, 0 , -1,-1, -1.0,-1.0, -1.5,-2.5, -1.5,-1.5]

    stats_order = [ 1,5]
    iplot = 0

    #start plotting
    fig, axes   = plt.subplots(nrows=3, ncols=2, figsize=(args.figsize[0], args.figsize[1]), sharex=args.sharex) 
    ax = axes.flat

    ax[0].set_axisbelow(True)
    ax[0].grid(color='gray', linestyle='dashed', axis="y")
    for i in range(0,len(vom_evap_stats)):    
        ax[0].plot( [loc_vom[i]-0.5, loc_vom[i]-0.5],[-9999,9999], "--", c="gray") 

    ax[1].set_axisbelow(True)
    ax[1].grid(color='gray', linestyle='dashed', axis="y")
    for i in range(0,len(vom_evap_stats)):    
        ax[1].plot( [loc_vom[i]-0.5, loc_vom[i]-0.5],[-9999,9999], "--", c="gray") 


    ax[0].plot(loc, pd.Series(vom_evap),  "--", color="darkgreen" , zorder=1)
    ax[0].plot(loc, pd.Series(vom_pc_evap),  "--", color="darkgreen" , zorder=1)
    ax[0].plot(loc, pd.Series(vom_pc2_evap),  "--", color="darkgreen" , zorder=1)
    ax[0].plot(loc, pd.Series(vom_zr_evap),  "--", color="darkgreen" , zorder=1)

    ax[0].plot(loc, pd.Series(dingo_evap),"--", color="black" , lw=3, zorder=1)

    ax[0].plot(np.delete(loc,1), pd.Series(bess_ema), "--", color="purple", zorder=1)
    ax[0].plot(np.delete(loc,1), pd.Series(bios2_ema), "--", color="lightgreen", zorder=1)
    ax[0].plot(np.delete(loc,1), pd.Series(cable_ema), "--", color="red", zorder=1)
    ax[0].plot(np.delete(loc,1), pd.Series(maespa_ema), "--", color="gold", zorder=1)
    ax[0].plot(np.delete(loc,1), pd.Series(spa_ema), "--", color="pink", zorder=1)
    ax[0].plot(np.delete(loc,1), pd.Series(lpjguess_ema), "--", color="blue", zorder=1)

    ax[1].plot(loc, pd.Series(vom_gpp),  "--", color="darkgreen", zorder=1 )
    ax[1].plot(loc, pd.Series(vom_pc_gpp),  "--", color="darkgreen", zorder=1 )
    ax[1].plot(loc, pd.Series(vom_pc2_gpp),  "--", color="darkgreen", zorder=1 )
    ax[1].plot(loc, pd.Series(vom_zr_gpp),  "--", color="darkgreen", zorder=1 )

    ax[1].plot(loc, pd.Series(dingo_gpp),"--", color="black", lw=3, zorder=1)

    ax[1].plot(np.delete(loc,1), pd.Series(bess_assma), "--", color="purple", zorder=1)
    ax[1].plot(np.delete(loc,1), pd.Series(bios2_assma), "--", color="lightgreen", zorder=1)
    ax[1].plot(np.delete(loc,1), pd.Series(cable_assma), "--", color="red", zorder=1)
    ax[1].plot(np.delete(loc,1), pd.Series(maespa_assma), "--", color="gold", zorder=1)
    ax[1].plot(np.delete(loc,1), pd.Series(spa_assma), "--", color="pink", zorder=1)
    ax[1].plot(np.delete(loc,1), pd.Series(lpjguess_assma), "--", color="blue", zorder=1)

    iplot = 0
    #loop over study sites
    for isite in range(0, len(args.sites)): 

        #ensemble years from Whitley
        try:
            ax[0].scatter(loc[isite], bess_ema[args.sites[isite]],color="purple", s=100, zorder=2)
            ax[0].scatter(loc[isite], bios2_ema[args.sites[isite]],color="lightgreen", s=100, zorder=2)
            ax[0].scatter(loc[isite], cable_ema[args.sites[isite]],color="red", s=100, zorder=2)
            ax[0].scatter(loc[isite], maespa_ema[args.sites[isite]],color="gold", s=100, zorder=2)
            ax[0].scatter(loc[isite], spa_ema[args.sites[isite]],color="pink", s=100, zorder=2)
            ax[0].scatter(loc[isite], lpjguess_ema[args.sites[isite]],color="blue", s=100, zorder=2)

            if( isite == 0):
                ax[1].scatter(loc[isite], bess_assma[args.sites[isite]],color="purple", label = "BESS", s=100, zorder=2)
                ax[1].scatter(loc[isite], bios2_assma[args.sites[isite]],color="lightgreen", label = "BIOS2", s=100, zorder=2)
                ax[1].scatter(loc[isite], cable_assma[args.sites[isite]],color="red", label = "CABLE", s=100, zorder=2)
                ax[1].scatter(loc[isite], maespa_assma[args.sites[isite]],color="gold", label = "MAESPA", s=100, zorder=2)
                ax[1].scatter(loc[isite], spa_assma[args.sites[isite]],color="pink", label = "SPA", s=100, zorder=2)
                ax[1].scatter(loc[isite], lpjguess_assma[args.sites[isite]],color="blue", label = "LPJ-GUESS", s=100, zorder=2)
            else:
                ax[1].scatter(loc[isite], bess_assma[args.sites[isite]],color="purple", s=100, zorder=2)
                ax[1].scatter(loc[isite], bios2_assma[args.sites[isite]],color="lightgreen", s=100, zorder=2)
                ax[1].scatter(loc[isite], cable_assma[args.sites[isite]],color="red", s=100, zorder=2)
                ax[1].scatter(loc[isite], maespa_assma[args.sites[isite]],color="gold", s=100, zorder=2)
                ax[1].scatter(loc[isite], spa_assma[args.sites[isite]],color="pink", s=100, zorder=2)
                ax[1].scatter(loc[isite], lpjguess_assma[args.sites[isite]],color="blue", s=100, zorder=2)
            
        except KeyError:
            print("Litchfield")


        if( isite == 0):
            ax[0].scatter(loc[isite], vom_evap[args.sites[isite]], color="darkgreen", s=130, marker= "s", zorder=2 )
            ax[0].scatter(loc[isite], vom_pc_evap[args.sites[isite]], color="darkgreen", s=130, marker= "v", zorder=2 )
            ax[0].scatter(loc[isite], vom_pc2_evap[args.sites[isite]], color="darkgreen", s=130, marker= "*", zorder=2 )
            ax[0].scatter(loc[isite], vom_zr_evap[args.sites[isite]], color="darkgreen", s=130, marker= "X", zorder=2 )

            ax[0].scatter(loc[isite], dingo_evap[args.sites[isite]],color="black", s=175, marker= "*", zorder=2 )

            ax[1].scatter(loc[isite], vom_gpp[args.sites[isite]], color="darkgreen", s=130, marker= "s", zorder=2 )
            ax[1].scatter(loc[isite], vom_pc_gpp[args.sites[isite]], color="darkgreen", s=130, marker= "v", zorder=2 )
            ax[1].scatter(loc[isite], vom_pc2_gpp[args.sites[isite]], color="darkgreen", s=130, marker= "*", zorder=2 )
            ax[1].scatter(loc[isite], vom_zr_gpp[args.sites[isite]], color="darkgreen", s=130, marker= "X", zorder=2 )

            ax[1].scatter(loc[isite], dingo_gpp[args.sites[isite]],color="black", s=130, marker= "*", label = "Obs.", zorder=2 )
        else:
            ax[0].scatter(loc[isite], vom_evap[args.sites[isite]], color="darkgreen", s=130, marker= "s", zorder=2)
            ax[0].scatter(loc[isite], vom_pc_evap[args.sites[isite]], color="darkgreen", s=130, marker= "v", zorder=2 )
            ax[0].scatter(loc[isite], vom_pc2_evap[args.sites[isite]], color="darkgreen", s=130, marker= "*", zorder=2 )
            ax[0].scatter(loc[isite], vom_zr_evap[args.sites[isite]], color="darkgreen", s=130, marker= "X", zorder=2 )

            ax[0].scatter(loc[isite], dingo_evap[args.sites[isite]],color="black", s=175, marker= "*", zorder=2 )

            ax[1].scatter(loc[isite], vom_gpp[args.sites[isite]], color="darkgreen", s=130, marker= "s", zorder=2 )
            ax[1].scatter(loc[isite], vom_pc_gpp[args.sites[isite]], color="darkgreen", s=130, marker= "v", zorder=2 )
            ax[1].scatter(loc[isite], vom_pc2_gpp[args.sites[isite]], color="darkgreen", s=130, marker= "*", zorder=2 )
            ax[1].scatter(loc[isite], vom_zr_gpp[args.sites[isite]], color="darkgreen", s=130, marker= "X", zorder=2 )

            ax[1].scatter(loc[isite], dingo_gpp[args.sites[isite]],color="black", s=130, marker= "*", zorder=2 )


    ax[0].set_xlim([0,60])
    ax[0].set_ylim([ miny[0], maxy[0]])
    ax[0].set_xticks( np.arange(5,65,10)  )
    ax[0].set_xticklabels( args.sites, rotation=90, fontsize=20  ) 
    ax[0].set_ylabel( ylabels[0], fontsize=20   )
    ax[0].text(-0.15, 1.04, plot_label[0], transform=ax[0].transAxes,  size=20, weight='bold')
    for tick in ax[0].yaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    ax[1].set_xlim([0,60])
    ax[1].set_ylim([ miny[1], maxy[1]])
    ax[1].set_xticks( np.arange(5,65,10)  )
    ax[1].set_xticklabels( args.sites, rotation=90, fontsize=20  ) 
    ax[1].set_ylabel( ylabels[1], fontsize=20   )    
    ax[1].text(-0.15, 1.04, plot_label[1], transform=ax[1].transAxes,  size=20, weight='bold')
    for tick in ax[1].yaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    #plot statistics
    iplot = 2

    for i_stat in stats_order:
        
        #Evap
        ax[iplot].grid(color='gray', linestyle='dashed', axis="y")

        for i in range(0,len(vom_evap_stats)):    
            ax[iplot].plot( [loc_vom[i]-0.5, loc_vom[i]-0.5],[-9999,9999], "--", c="gray")    


        for isite in range(0, len(args.sites)): 
            try:
                ax[iplot].scatter( loc_vom[isite], vom_evap_stats[args.sites[isite]][i_stat], c="darkgreen", s=130, marker="s"   )
                ax[iplot].scatter( loc_vom2[isite], vom_pc_evap_stats[args.sites[isite]][i_stat], c="green", s=100, marker="v"   )
                ax[iplot].scatter( loc_vom3[isite], vom_pc2_evap_stats[args.sites[isite]][i_stat], c="green",s=100, marker="*"  )
                ax[iplot].scatter( loc_vom4[isite], vom_zr_evap_stats[args.sites[isite]][i_stat], c="green", s=100,marker="X"   )

                ax[iplot].scatter( loc_bess[isite], bess_evap_stats[args.sites[isite]][i_stat] ,c = "purple",s=100 )
                ax[iplot].scatter( loc_bios2[isite], bios2_evap_stats[args.sites[isite]][i_stat], c = "lightgreen",s=100   )
                ax[iplot].scatter( loc_cable[isite], cable_evap_stats[args.sites[isite]][i_stat], c = "red", s=100  )
                ax[iplot].scatter( loc_lpjguess[isite], lpjguess_evap_stats[args.sites[isite]][i_stat], c = "blue",s=100   )
                ax[iplot].scatter( loc_maespa[isite], maespa_evap_stats[args.sites[isite]][i_stat], c = "gold", s=100  )
                ax[iplot].scatter( loc_spa[isite], spa_evap_stats[args.sites[isite]][i_stat], c = "pink", s=100  )
            except KeyError:
               print("Litchfield")

        ax[iplot].grid(color='gray', linestyle='--', linewidth=1, alpha=0.5, axis="y")
        ax[iplot].set_ylim([ miny[iplot], maxy[iplot]])
        ax[iplot].set_xlim([0,60])
        ax[iplot].set_xticks( np.arange(5,65,10)  )
        ax[iplot].set_xticklabels( args.sites, rotation=90, fontsize=20  )        
        ax[iplot].set_ylabel( ylabels[iplot], fontsize=20  )    
        ax[iplot].text(-0.15, 1.04, plot_label[iplot], transform=ax[iplot].transAxes,  size=20, weight='bold')
        for tick in ax[iplot].yaxis.get_major_ticks():
            tick.label.set_fontsize(16)

        #GPP
        iplot = iplot + 1
        ax[iplot].grid(color='gray', linestyle='dashed', axis="y")

        for i in range(0,len(vom_evap_stats)):    
            ax[iplot].plot( [loc_vom[i]-0.5, loc_vom[i]-0.5],[-9999,9999], "--", c="gray")   
 
        for isite in range(0, len(args.sites)): 
            try:
                if( (isite == 0) & (i_stat == stats_order[0]) ):
                    ax[iplot].scatter( loc_vom[isite], vom_gpp_stats[args.sites[isite]][i_stat], c="darkgreen", s=130, marker="s", label = "VOM"    )
                    ax[iplot].scatter( loc_vom2[isite], vom_pc_gpp_stats[args.sites[isite]][i_stat], c="green", s=100,marker="v", label = "VOM - prescribed cover"    )
                    ax[iplot].scatter( loc_vom3[isite], vom_pc2_gpp_stats[args.sites[isite]][i_stat], c="green",s=100, marker="*", label = "VOM - prescribed cover (mean monthly)"    )
                    ax[iplot].scatter( loc_vom4[isite], vom_zr_gpp_stats[args.sites[isite]][i_stat], c="green", s=100,marker="X", label = "VOM - prescribed roots"    )

                    ax[iplot].scatter( loc_bess[isite], bess_ass_stats[args.sites[isite]][i_stat] ,c = "purple", s=100 )
                    ax[iplot].scatter( loc_bios2[isite], bios2_ass_stats[args.sites[isite]][i_stat], c = "lightgreen",s=100  )
                    ax[iplot].scatter( loc_cable[isite], cable_ass_stats[args.sites[isite]][i_stat], c = "red",s=100  )
                    ax[iplot].scatter( loc_lpjguess[isite], lpjguess_ass_stats[args.sites[isite]][i_stat], c = "blue",s=100  )
                    ax[iplot].scatter( loc_maespa[isite], maespa_ass_stats[args.sites[isite]][i_stat], c = "gold",s=100  )
                    ax[iplot].scatter( loc_spa[isite], spa_ass_stats[args.sites[isite]][i_stat], c = "pink", s=100 )
                else:
                    ax[iplot].scatter( loc_vom[isite], vom_gpp_stats[args.sites[isite]][i_stat], c="green",s=130, marker="s"  )
                    ax[iplot].scatter( loc_vom2[isite], vom_pc_gpp_stats[args.sites[isite]][i_stat], c="green", s=100,marker="v"   )
                    ax[iplot].scatter( loc_vom3[isite], vom_pc2_gpp_stats[args.sites[isite]][i_stat], c="green",s=100, marker="*"   )
                    ax[iplot].scatter( loc_vom4[isite], vom_zr_gpp_stats[args.sites[isite]][i_stat], c="green", s=100,marker="X"   )

                    ax[iplot].scatter( loc_bess[isite], bess_ass_stats[args.sites[isite]][i_stat] ,c = "purple", s=100 )
                    ax[iplot].scatter( loc_bios2[isite], bios2_ass_stats[args.sites[isite]][i_stat], c = "lightgreen",s=100  )
                    ax[iplot].scatter( loc_cable[isite], cable_ass_stats[args.sites[isite]][i_stat], c = "red" ,s=100 )
                    ax[iplot].scatter( loc_lpjguess[isite], lpjguess_ass_stats[args.sites[isite]][i_stat], c = "blue",s=100  )
                    ax[iplot].scatter( loc_maespa[isite], maespa_ass_stats[args.sites[isite]][i_stat], c = "gold",s=100  )
                    ax[iplot].scatter( loc_spa[isite], spa_ass_stats[args.sites[isite]][i_stat], c = "pink" ,s=100)

            except KeyError:
               print("Litchfield")


        ax[iplot].grid(color='gray', linestyle='--', linewidth=1, alpha=0.5, axis="y")
        ax[iplot].set_ylim([ miny[iplot], maxy[iplot]])
        ax[iplot].set_xlim([0,60])
        ax[iplot].set_xticks( np.arange(5,65,10)  )
        ax[iplot].set_xticklabels( args.sites, rotation=90, fontsize=20  ) 
        ax[iplot].set_ylabel( ylabels[iplot], fontsize=20   )    
        ax[iplot].text(-0.15, 1.04, plot_label[iplot], transform=ax[iplot].transAxes,  size=20, weight='bold')
        for tick in ax[iplot].yaxis.get_major_ticks():
            tick.label.set_fontsize(16)
        
        iplot = iplot + 1


    lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

    ax[5].legend(lines, labels, bbox_to_anchor=(1.0, 1.0), fontsize=14)

    plt.tight_layout()

    if args.outfile is not None:
        plt.savefig(args.outfile, bbox_inches = "tight")
    else:
        plt.show()

def read_bess(infile, startyear):

    lat_heat_vapor = 2.26   #[MJ/kg]
    rho_w = 1000             #[kg/m3]

    data = np.loadtxt(infile, delimiter=",") 
    time = pd.date_range("01-01-" + startyear, periods = len(data[:,0]), freq='D')

    tmp = 24*60*60*data[:,0] /( lat_heat_vapor * rho_w * 1000 )

    #make pandas series and return daily values
    evap_pd = pd.Series(tmp, index = time ) #mm/day
    ass_pd = pd.Series(data[:,1]*24*60*60*10**-6, index = time ) #mol/m2/d

    return evap_pd, ass_pd

def read_bios2(infile):

    lat_heat_vapor = 2.26   #[MJ/kg]
    rho_w = 1000             #[kg/m3]

    data = np.loadtxt(infile, delimiter=",") 
    time = pd.date_range(datetime(int(data[0,0]),int(data[0,1]),int(data[0,2])), 
              datetime(int(data[-1,0]),int(data[-1,1]),int(data[-1,2])),freq='D')

    tmp = 24*60*60*data[:,3] /( lat_heat_vapor * rho_w * 1000 )

    #make pandas series and return daily values
    ass_pd = pd.Series(data[:,4]*24*60*60*10**-6, index = time ) #mol/m2/d
    evap_pd = pd.Series(tmp, index = time ) 

    return evap_pd, ass_pd

def read_lpjguess(infile_et, infile_gpp):

    lat_heat_vapor = 2.26   #[MJ/kg]
    rho_w = 1000             #[kg/m3]

    data_et = np.loadtxt(infile_et, skiprows=1, usecols=3)
    data_gpp = np.loadtxt(infile_gpp, skiprows=1, usecols=3)
    time_tmp = np.loadtxt(infile_gpp, skiprows=1)
    time = pd.date_range(datetime(int(time_tmp[0,0]),int(time_tmp[0,1]),int(time_tmp[0,2])), 
              datetime(int(time_tmp[-1,0]),int(time_tmp[-1,1]),int(time_tmp[-1,2])),freq='D')

    tmp = 24*60*60*data_et /( lat_heat_vapor * rho_w * 1000 )

    #make pandas series and return daily values
    evap_pd = pd.Series(tmp, index = time ) #mm/day
    ass_pd = pd.Series(data_gpp*24*60*60*10**-6, index = time ) 

    return evap_pd, ass_pd

def read_maespa(infile):

    lat_heat_vapor = 2.26   #[MJ/kg]
    rho_w = 1000             #[kg/m3]

    data = np.loadtxt(infile, delimiter=",", skiprows=3, usecols=(3,6))
    data[data == -9999.9] = np.nan
    data[data == -999] = np.nan
    time_tmp = np.loadtxt(infile, delimiter=",", dtype=np.str, skiprows=3, usecols=0)
    time = pd.date_range(time_tmp[0], time_tmp[-1],freq='30min')

    tmp = 30*60*data[:,1] /( lat_heat_vapor * rho_w * 1000 )

    evap_pd = pd.Series(tmp, index = time ) #mm/30min
    ass_pd = pd.Series(data[:,0]*30*60*10**-6, index = time ) 

    return evap_pd, ass_pd

def read_spa(infile):

    lat_heat_vapor = 2.26   #[MJ/kg]
    rho_w = 1000             #[kg/m3]

    data = np.loadtxt(infile, delimiter=",", skiprows=1, usecols=(1,3))
    time_tmp = np.loadtxt(infile, delimiter=",", dtype=np.str, skiprows=1, usecols=0)
    time = pd.date_range(time_tmp[0], time_tmp[-1],freq='30min')

    tmp = 30*60*data[:,1] /( lat_heat_vapor * rho_w * 1000 )

    evap_pd = pd.Series(tmp, index = time ) #mm/30min
    ass_pd = pd.Series(-1.0*data[:,0]*30*60*10**-6, index = time ) #mol/m2/s

    return evap_pd, ass_pd

def read_cable(infile):

    lat_heat_vapor = 2.26   #[MJ/kg]
    rho_w = 1000             #[kg/m3]

    ncfile = Dataset(infile)
    data_gpp = np.squeeze(ncfile.variables["GPP"]) # extract variable
    data_et = np.squeeze(ncfile.variables["Evap"]) # extract variable
    time_tmp = np.squeeze(ncfile.variables["time"]) # extract variable
    time_tmp = [pd.to_datetime("2007-01-01 00:01:00") + pd.Timedelta(seconds=i) for i in time_tmp]
    time = pd.date_range(time_tmp[0], time_tmp[-1],freq='30min')

    ass_pd = pd.Series(data_gpp*30*60*10**-6, index = time ) 
    evap_pd = 30*60*pd.Series(data_et, index = time )  #mm/30min

    return evap_pd, ass_pd


main()
