# -*- coding: utf-8 -*-
import EDRread
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os 
import pickle as pkl
import matplotlib as mpl

def make_ion_density(filename,start='000000',end='235959', graph_num=1, save=0):
    #Открываем требуемый файл
    edr = EDRread.OpenEDR(filename)
    # Достаем необходимые данные из файла
    satelite_model = edr.satelite_model
    temp = edr.rpa_sweep_analyses()['RPA_derived_total_ion_density']
    ion_density = temp.where(temp != -1.000000e+37)
    
    ephemeris = edr.ephemeris()
    lat = ephemeris.columns[3]
    lon = ephemeris.columns[4]

    latitude = ephemeris[lat]
    longitude = ephemeris[lon]
    
    #Формируем датафрейм без колонок с общим временем
    starttime = ephemeris.index[0]
    time_range = pd.date_range(start = starttime, periods = 86400/4, freq = "4s")
    data_frame = pd.DataFrame(index = time_range)
    
    #Совмещаем все данные в data_frame
    data_frame[lon] = longitude
    data_frame[lat] = latitude
        ##
    #Корректируем интерполяцию и интерполируем
    correct_interpol = np.where(data_frame[lon]<10)
    for i in correct_interpol[0]:
        if data_frame[lon][i+5] < 10:
            continue
        else:
            data_frame[lon][i+1] = 360    
    data_frame = data_frame.interpolate()
    #Добавим плотность ионов и мереведем в метр на метр в квадрате
    data_frame['Ion_density'] = ion_density[:]*1000000
    #Отрегулируем значения долготы
    data_frame[lon][data_frame[lon]>180] -= 360 
    
    #Берем в необходимых пределах     
    date = data_frame.index[0].date()
    time = lambda x : dt.time(hour=int(x[0:2]),
                              minute=int(x[2:4]),
                              second=int(x[4:]))
    starttime = dt.datetime.combine(date, time(start))
    endtime = dt.datetime.combine(date, time(end))
    
    #---------------------------------------------------------
    #С каким периодом строить графики
    graph_delta = (endtime - starttime)/graph_num
    start_graph_time = starttime
    end_graph_time = start_graph_time + graph_delta
    
    for i in range(graph_num):
        period_frame = data_frame.loc[start_graph_time:end_graph_time]
        #Строим график
        figure = plt.figure()
        axes = figure.add_subplot(1, 1, 1)
        world_map = pkl.load(open('wm.pkl','rb'))
        plt.plot(world_map[:, 0],world_map[:, 1],
                 c='gray',
                 zorder=0,
                 figure=figure)
        
        #Нормируем cbar
        normalize = mpl.colors.Normalize(vmax=10e10)
        #
        plt.scatter(x=period_frame[lon],
                    y=period_frame[lat],
                    c=period_frame['Ion_density'],
                    cmap='nipy_spectral',
                    linewidth=0,
                    figure=figure,
                    norm=normalize)
        plt.xlim(-180,180)
        #plt.ylim(-70,-20)
        #plt.xlim(-20,80)
        
        #Ставим верные метки на осях
        locator = mpl.ticker.MultipleLocator(base=60)
        axes.xaxis.set_major_locator(locator)
        locator = mpl.ticker.MultipleLocator(base=30)
        axes.yaxis.set_major_locator(locator)
        
        #Приводим рисунок к хорошему виду
        plt.grid()
        #Название
        plt.title('F'+satelite_model+' '*60+'\n'+
                  date.strftime('%Y-%m-%d')+' '*16+
                  str(start_graph_time.time())[:8]+
                  ' -- '+
                  str(end_graph_time.time())[:8])
             
        #colorbar
        cbar = plt.colorbar()
        cbar.set_label(r'$\mathrm{Ion\ density,\ Ion/m^3}$',fontsize=14)
        #Подпищем оси
        plt.xlabel(r'$\mathrm{Longitude, E^\circ}$', fontsize=14)
        plt.ylabel(r'$\mathrm{Latitude,\ N^\circ}$', fontsize=14)
        
        
        #Cохраняем изображение
        root_dir = os.getcwd()
        date_str = date.strftime('%Y-%m-%d')
        if save == 1:
            name = lambda : ('F'+satelite_model+'  '+
                             start_graph_time.strftime('%H%M%S')+
                             '--'+
                             end_graph_time.strftime('%H%M%S'))
            os.chdir(root_dir+'\\pictures')
            if date_str not in os.listdir():
                os.mkdir(os.getcwd()+'\\'+date_str)
            os.chdir(os.getcwd()+'\\'+date_str)                                                                                        
            plt.savefig(name(), dpi=1000)
            os.chdir(root_dir)
        #-------------------------------------------------
        #Обновим период постройки графика
        start_graph_time = end_graph_time
        end_graph_time = start_graph_time + graph_delta
        
        



        

make_ion_density('F1520150815.EDR','130000','140000',graph_num=1, save=1)

