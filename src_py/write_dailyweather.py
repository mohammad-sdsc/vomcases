import numpy as np
import os
import sys
import argparse
from netCDF4 import Dataset
import pandas as pd
import csv

#file to prepare meterological data from SILO
#and CO2 from Mauna Loa for applying it in
#the Vegetation Optimality Model (VOM)
#output: 
#dailyweather.prn: input file VOM
#written: June 2018, R.C. Nijzink


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-im", "--meteofile", help="inputfile with meteodata of Silo")
    parser.add_argument("-ic", "--co2file", help="inputfile with co2data of ManuaLoa")
    parser.add_argument("-p", "--interpolation", help="interpolation method for missing data",nargs='?',const='linear', default='linear')
    parser.add_argument("-o", "--outputfile", help="outputfile")
    args = parser.parse_args()



    ########################################################
    #settings

    #meteo file
    meteofile = args.meteofile

    #CO2 file
    co2file = args.co2file 

    #interpolation method for missing data
    interp = args.interpolation

    #output folder
    out_file = args.outputfile

    ####################################
    #read CO2 data
    co2data = pd.read_csv(co2file, skiprows = 44, na_values = "    NaN", header=None)

    #make a pandas datetime series
    pddatetime = pd.to_datetime(co2data[0])

    #make a pandas index
    index = pd.DatetimeIndex( pddatetime)	

    #replace index
    co2data.index = index

    #extract CO2 series
    co2mlo_pd = pd.Series(co2data[1], dtype = np.float64)

    #make daily series
    co2_daily = co2mlo_pd.resample('D')   # [ppm]

    #fill weekly values
    co2_daily = co2_daily.fillna(method = 'backfill')   # [ppm]


    ########################################################
    #read meteofile

    meteo_data = pd.read_csv(meteofile, skiprows = 43, delimiter=r"\s+", header=None )

    #make a pandas datetime series
    pddatetime = pd.to_datetime( meteo_data[2], format="%d-%m-%Y")

    #make a pandas index
    index = pd.DatetimeIndex( pddatetime)

    #replace index
    meteo_data.index = index

    #extract series

    tempmax_daily = meteo_data[:][3] #oC
    tempmin_daily = meteo_data[:][5] #oC
    prec_daily    = meteo_data[:][7] #mm/d
    vp_daily      = meteo_data[:][13]#hPa
    radn_daily    = meteo_data[:][11]#MJ/m2
    pres_daily    = meteo_data[:][26]#hPa

    day_daily     = index.day
    month_daily   = index.month
    year_daily    = index.year



    ##################################################
    #append to files

    #file for weather data, input VOM
    weatherfile = open(out_file, mode = 'w')

    #write header
    weatherfile.write("%8s%8s%8s%8s%8s%8s%8s%8s%8s%8s%8s\n" %
        ("Dcum","Day","Month", "Year", "T.Max", "T.Min", "Rain", "Radn", "VP", "Pres", "Ca" ))


    for i in range(0,len(day_daily)):
        weatherfile.write("%8.0f%8.0f%8.0f%8.0f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f\n" % ( i+1 , 
        day_daily[i] , 
        month_daily[i] ,
        year_daily[i] ,
        tempmax_daily[i] ,    
        tempmin_daily[i] ,    
        prec_daily[i] ,    
        radn_daily[i] ,    
        vp_daily[i] ,    
        pres_daily[i] ,    
        co2_daily[co2_daily.index== meteo_data.index[i] ] ))



    weatherfile.close()

    print("Script finished")

main()








