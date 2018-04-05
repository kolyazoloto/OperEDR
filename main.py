# -*- coding: utf-8 -*-
import EDRread
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os 
import pickle as pkl
import matplotlib as mpl

def make_ion_density(filename,start='000000',end='235959', save=0):
    #Открываем требуемый файл
    edr = EDRread.OpenEDR(filename)
    # Достаем необходимые данные из файла
    temp = edr.dm_ion_density()
    ion_density = temp.where(temp != -1.000000e+37)
    
    ephemeris = edr.ephemeris()
    lat = ephemeris.columns[3]
    lon = ephemeris.columns[4]

    latitude = ephemeris[lat]
    longitude = ephemeris[lon]
    #Формируем датафрейм без колонок с общим временем
    starttime = ephemeris.index[0]
    time_range = pd.date_range(start = starttime, periods = 86400, freq = "s")
    data_frame = pd.DataFrame(index = time_range)
    #Совмещаем все данные в data_frame
    data_frame[lon] = longitude
    data_frame[lat] = latitude
    #Добавим плотность ионов и мереведем в метр на метр в квадрате
    data_frame['Ion_density'] = ion_density[:]*1000000
    ##
    # Исправляем ошибку интерполяции и интерполируем
    correct_interpol = np.where(data_frame[lon]<10)
    for i in correct_interpol[0]:
        if data_frame[lon][i+20] < 10:
            continue
        else:
            data_frame[lon][i+1] = 360    
    data_frame = data_frame.interpolate()
    #Для нормирования колорбара возмем максимальное значение)
    vmax_cbar = data_frame['Ion_density'].max()
    vmin_cbar = data_frame['Ion_density'].min()
    #Отрегулируем значения долготы
    data_frame[lon][data_frame[lon]>180] -= 360 
    #Берем в необходимых пределах     
    date = data_frame.index[0].date()
    time = lambda x : dt.time(hour=int(x[0:2]),
                              minute=int(x[2:4]),
                              second=int(x[4:]))
    starttime = dt.datetime.combine(date, time(start))
    endtime = dt.datetime.combine(date, time(end))
    data_frame = data_frame.loc[starttime:endtime]
    #Строим график
    figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    world_map = pkl.load(open('wm.pkl','rb'))
    plt.plot(world_map[:, 0],world_map[:, 1],
             c='gray',
             zorder=0,
             figure=figure)
    #Нормируем cbar
    #normalize = mpl.colors.Normalize(vmin=1e10, vmax=vmax_cbar)
    #
    plt.scatter(x=data_frame[lon],
                y=data_frame[lat],
                c=data_frame['Ion_density'],
                cmap='inferno',
                linewidth=0,
                figure=figure)
                #norm=normalize)
    plt.xlim(-180,180)
    #Ставим верные метки на осях
    locator = mpl.ticker.MultipleLocator(base=60)
    axes.xaxis.set_major_locator(locator)
    locator = mpl.ticker.MultipleLocator(base=30)
    axes.yaxis.set_major_locator(locator)
    
    #Приводим рисунок к хорошему виду
    plt.grid()
    #Сдесь я беру время ,переделываю его в кортеж,где отдельно время дата и тд
    format_date = lambda x:'%3s:%s:%s' % tuple([x[i:i+2] for i in range(6)[::2]])
    plt.title(date.strftime('%Y-%m-%d')+'              '+
              format_date(start)+' --'+format_date(end))
    #colorbar
    cbar = plt.colorbar()
    cbar.set_label(r'$\mathrm{Ion\ density,\ Ion/m^3}$',fontsize=14)
    #Подпищем оси
    plt.xlabel(r'$\mathrm{Longitude, E^\circ}$', fontsize=14)
    plt.ylabel(r'$\mathrm{Latitude,\ N^\circ}$', fontsize=14)
    #Поменяем размерность
    
    #Cохраняем изображение
    root_dir = os.getcwd()
    date_str = date.strftime('%Y-%m-%d')
    if save == 1:
        name = lambda : start+'--'+end
        os.chdir(root_dir+'\\pictures')
        if date_str not in os.listdir():
            os.mkdir(os.getcwd()+'\\'+date_str)
        os.chdir(os.getcwd()+'\\'+date_str)                                                                                        
        plt.savefig(name(), dpi=1000)
        os.chdir(root_dir)
        
#Цикл для вызова функции за весь цепь с периодом 2 часа  
def corr_len(time):
    if len(time) != 6: 
        time = '0' * (6-len(time)) + time
    return time
      

        
make_ion_density('20150815.EDR','000000','020000',save=1)
'''make_ion_density('20150815.EDR','020000','040000',save=1)
make_ion_density('20150815.EDR','040000','060000',save=1)
make_ion_density('20150815.EDR','060000','080000',save=1)
make_ion_density('20150815.EDR','080000','100000',save=1)
make_ion_density('20150815.EDR','100000','120000',save=1)
make_ion_density('20150815.EDR','120000','140000',save=1)
make_ion_density('20150815.EDR','140000','160000',save=1)
make_ion_density('20150815.EDR','160000','180000',save=1)
make_ion_density('20150815.EDR','180000','200000',save=1)
make_ion_density('20150815.EDR','200000','220000',save=1)
make_ion_density('20150815.EDR','220000','235959',save=1)'''












