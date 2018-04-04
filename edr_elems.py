# -*- coding: utf-8 -*-

import pandas as pd
import datetime as dt

class EDRElems:
    def __init__(self,array,time,amountofelem):
        self._amountofelem=amountofelem
        self._array=array
        self.time=time
    def to_df(self):
        pass
    def _correcttime(self):
        time = self.time
        amount = self._amountofelem
        timedelta = dt.timedelta(milliseconds = (60000/amount))
        correcttime = []
        for i in time:
            correcttime.append(i)
            temptime = i
            for k in range(amount-1):
                temptime += timedelta
                correcttime.append(temptime)                
        return  correcttime
  
        
class Ephemeris(EDRElems):
    def __init__(self,array,time):
        super().__init__(array,time,3)
        self.time = self._correcttime()
        temp = [ ]
        for i in self._array:
            temp.extend(i)
        self.Geographic_latitude = temp[::6]
        self.Geographic_longitude = temp[1::6]
        self.Apex_latitude = temp[2::6]
        self.Apex_longitude = temp[3::6]
        self.Apex_local_time = temp[4::6]
        self.Satellite_altitude = temp[5::6] 

    def to_df(self):
        d = {'Geographic_latitude':pd.Series(self.Geographic_latitude,index=self.time),
             'Geographic_longitude':pd.Series(self.Geographic_longitude,index=self.time),
             'Apex_latitude':pd.Series(self.Apex_latitude,index=self.time),
             'Apex_longitude':pd.Series(self.Apex_longitude,index=self.time),
             'Apex_local_time':pd.Series(self.Apex_local_time,index=self.time),
             'Satellite_altitude':pd.Series(self.Satellite_altitude,index=self.time)}
        return pd.DataFrame(d)

        
class SatellitePotential(EDRElems):
    def __init__(self,array,time):
        super().__init__(array,time,15)
        self.time = self._correcttime()
        temp = array
        self.Satellite_potential = []
        self.source = temp[0][-1]
        for i in range(len(temp)):
            del temp[i][-1]
            self.Satellite_potential.extend(temp[i]) 
  
    def to_df(self):
        return pd.DataFrame(self.Satellite_potential,index = self.time,
                            columns=["Satellite_Potential"])

        
class PrimaryPlasmaDensity(EDRElems):
    def __init__(self,array,time):
        super().__init__(array,time,60)
        self.time = self._correcttime()
        temp = self._array
        self.source = temp[0][-1]
        self.Primary_plasma_density = []
        for i in range(len(self._array)): 
            del temp[i][-1]
            self.Primary_plasma_density.extend(self._array[i])

    def to_df(self):
       return pd.DataFrame(self.Primary_plasma_density,index=self.time,
                           columns=['Primary_plasma_density'])

       
class VerticalIonDriftVelocity(EDRElems):
    def __init__(self,array,time):
        super().__init__(array,time,60)
        self.time = self._correcttime()
        temp = self._array
        self.Vertical_ion_drift_velocity = []
        for i in range(len(temp)):        
            self.Vertical_ion_drift_velocity.extend(temp[i])

    def to_df(self):
        return pd.DataFrame(self.Vertical_ion_drift_velocity,index=self.time,
                            columns=['Vertical_ion_drift_velocity'])
       
         
class HorizontalIonDriftVelocity(EDRElems):
    def __init__(self,array,time):
        super().__init__(array,time,60)
        self.time = self._correcttime()
        temp = self._array
        self.Horizontal_ion_drift_velocity = []
        for i in range(len(temp)):        
            self.Horizontal_ion_drift_velocity.extend(temp[i])   
        
    def to_df(self):
        return pd.DataFrame(self.Horizontal_ion_drift_velocity,index=self.time,
                            columns=['Horizontal_ion_drift_velocity'])   

        
class Engineering_data(EDRElems):
    def __init__(self,array,time):
        super().__init__(array,time,1)
        temp = []
        for i in self._array:
            temp.extend(i)
        self.ADC_temperature = temp[1::7] 
        self.SEP_temperature = temp[2::7]
        self.RPA_plasma_plate_potential = temp[3::7]
        self.DM_mode = temp[4::7]
        self.EP_mode = temp[5::7]
        self.VIP_at_edr_start = temp[6::7]
    def to_df(self):
        d = {'ADC_temperature':pd.Series(self.ADC_temperature,index=self.time),
             'SEP_temperature':pd.Series(self.SEP_temperature,index=self.time),
             'RPA_plasma_plate_potential':pd.Series(self.RPA_plasma_plate_potential,index=self.time),
             'DM_model':pd.Series(self.DM_mode,index=self.time),
             'EP_mode':pd.Series(self.EP_mode,index=self.time),
             'VIP_at_edr_start':pd.Series(self.VIP_at_edr_start,index=self.time)}
        return pd.DataFrame(d)

    
class DMIonDensity(EDRElems):
    def __init__(self,array,time):
        super().__init__(array,time,60)
        self.time = self._correcttime()
        temp = self._array
        self.DM_ion_density = []
        for i in range(len(temp)):        
            self.DM_ion_density.extend(temp[i])  
         
    def to_df(self):
        return pd.DataFrame(self.DM_ion_density,index=self.time,
                            columns=['DM_ion_density'])         

        
class EpSweepAnalysesSets(EDRElems):
    def __init__(self,array,time):
        super().__init__(array,time,15)
        self.time = self._correcttime()
        temp = []
        for i in self._array:
            temp.extend(i)
        self.Sweep_center_time = temp[::6]
        self.Electron_density = temp[1::6]
        self.Electron_temperature = temp[2::6]
        self.Satellite_potential = temp[3::6]
        self.Analysis_qualifier = temp[4::6]
        self.EP_photoelectron_surrogate_value = temp[5::6] 

    def to_df(self):
        d = {'Sweep_center_time':pd.Series(self.Sweep_center_time,index=self.time),
             'Electron_density':pd.Series(self.Electron_density,index=self.time),
             'Electron_temperature':pd.Series(self.Electron_temperature,index=self.time),
             'Satellite_potential':pd.Series(self.Satellite_potential,index=self.time),
             'Analysis_qualifier':pd.Series(self.Analysis_qualifier,index=self.time),
             'EP_photo-electron_surrogate_value':pd.Series(self.EP_photoelectron_surrogate_value,
                                                           index=self.time)}
        return pd.DataFrame(d) 

        
class RPASweepAnalyses(EDRElems):
    def __init__(self,array,time):
        super().__init__(array,time,15)
        self.time = self._correcttime()
        self.source = self._array[0][-1]
        temp = [] 
        for i in range(len(self._array)):        
            del self._array[i][-1]    
            temp.extend(self._array[i])
        self.Sweep_center_time = temp[::8]
        self.O_plus_density = temp[1::8]
        self.Total_density = temp[2::8]
        self.Light_ion_flag = temp[3::8]
        self.Ion_temperature = temp[4::8]
        self.Ram_ion_drift_velocity = temp[5::8] 
        self.Analysis_qualifier = temp[6::8] 
        self.RPA_derived_total_ion_density = temp[7::8] 

    def to_df(self):
        d = {'Sweep_center_time':pd.Series(self.Sweep_center_time,index=self.time),
             'O_plus_density':pd.Series(self.O_plus_density,index=self.time),
             'Total_density':pd.Series(self.Total_density,index=self.time),
             'Light_ion_flag':pd.Series(self.Light_ion_flag,index=self.time),
             'Ion_temperature':pd.Series(self.Ion_temperature,index=self.time),
             'Ram_ion_drift_velocity':pd.Series(self.Ram_ion_drift_velocity,index=self.time),
             'Analysis_qualifier':pd.Series(self.Analysis_qualifier,index=self.time),
             'RPA_derived_total_ion_density':pd.Series(self.RPA_derived_total_ion_density,
                                                       index=self.time)}
        return pd.DataFrame(d) 
        
       
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
        
        
        