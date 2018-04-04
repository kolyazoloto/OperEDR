# -*- coding: utf-8 -*-
import pandas as pd
import datetime as dt
import edr_elems
import os

class OpenEDR:
    def __init__(self,filename):            
        temp = open(filename, 'r')
        self._data = temp.readlines()
        temp.close()
        self._examples=pd.Series([1, 3, 2, 11, 10, 10, 19, 15, 16, 10, 1, 1],
                                    index=[ "RECORD",
                                            "EPHEMERIS",
                                            "SATELLITE POTENTIAL",
                                            "PRIMARY PLASMA DENSITY",
                                            "HORIZONTAL ION DRIFT VELOCS",
                                            "VERTICAL ION DRIFT VELOCS",
                                            "CKL ANALYSES",
                                            "EP SWEEP ANALYSES SETS",
                                            "RPA SWEEP ANALYSES SETS",
                                            "DM ION DENSITY",
                                            "ENGINEERING DATA",
                                            "FILLER"
                                ])
        self._time = self._inittime()
    
    def _inittime(self):
        time = []
        systype = self._examples.index[0]
        data = self._data
        for i in range(len(data)):
            if systype in data[i]:
                temp = data[i+1].split()
                currenttime = temp[-2]+temp[-1]
                datetime = dt.datetime.strptime(currenttime,"%Y%m%d%H%M")
                time.append(datetime)  
        return time
    
    def _initarray(self,index):
        array = []
        arraytype = self._examples.index[index]
        linesnumber = self._examples[index]
        data = self._data
        for i in range(len(data)):
            if arraytype  in data[i]:
                temp = ' '.join(data[i+1:i+linesnumber+1])
                array.append([float(i) for i in temp.split()])
        return array
        
    def ephemeris(self):
        array = self._initarray(1)
        return edr_elems.Ephemeris(array, self._time).to_df()
        
    def satellite_potential(self):
        array = self._initarray(2)
        return edr_elems.SatellitePotential(array, self._time).to_df()
        
    def primary_plasma_density(self):
        array = self._initarray(3)
        return edr_elems.PrimaryPlasmaDensity(array, self._time).to_df()
        
    def horizontal_ion_drift_velocity(self):
        array = self._initarray(4)
        return edr_elems.HorizontalIonDriftVelocity(array, self._time).to_df()
        
    def vertical_ion_drift_velocity(self):
        array = self._initarray(5)
        return edr_elems.VerticalIonDriftVelocity(array, self._time).to_df()
        
    def ep_sweep_analyses_sets(self):
        array = self._initarray(7)
        return edr_elems.EpSweepAnalysesSets(array, self._time).to_df()
        
    def rpa_sweep_analyses(self):
        array = self._initarray(8)
        return edr_elems.RPASweepAnalyses(array, self._time).to_df()
        
    def dm_ion_density(self):
        array = self._initarray(9)
        return edr_elems.DMIonDensity(array, self._time).to_df() 
        
    '''def engineering_data(self):
        array = self._initarray(10)
        return edr_elems.Engineering_data(array,self._time).to_df()'''
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    