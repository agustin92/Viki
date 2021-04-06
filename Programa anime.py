# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 19:21:39 2021

@author: MSI

Programa animes viki
"""


from PyQt5 import QtWidgets, Qt, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import time 
import os
import vlc 

import sys

from Programa_anime_GUI import Ui_MainWindow

player = vlc.MediaPlayer("C:/Users/MSI/Documents/Zoom/2020-06-30 19.36.44 Agustin Lopez Pedroso's Personal Meeting Room 2221026514/zoom_0.mp4")
player.video_set_key_input(True)
player.video_set_mouse_input(True)
player.play()
player.toggle_fullscreen()
player.pause()
player.get_state()
player.set_time(80000)
player.stop()
player = vlc.MediaPlayer("E:\Videos\Anime\Dr. Stone\Doctor de piedra 02.mp4")

folders = os.listdir("E:\Videos\Anime")

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    Supported signals are:
    finished
        No data    
  
    result
        `object` data returned from processing, anything

    '''
    finished = pyqtSignal()
    result = pyqtSignal(object)
    
class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    '''

    def __init__(self, parameters):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.parameters = parameters
        self.signals = WorkerSignals()
        self.results_inst = [0.0,0.0,0.0,0,0.0]
        self.running = True
        self.res = kd.K6221()
        self.temp = te.Ls331()
        if parameters['field_on']:
            self.campo = cc.FieldControl()

        # Add the callback to our kwargs
            
    
    @pyqtSlot()
    def run(self):
        '''
        results_inst[0] = Temperature_a
        results_inst[1] = Temperature_b
        results_inst[2] = Resistance
        results_inst[3] = Heater output
        results_inst[3] = Time
        '''
        
        self.res.reset()
        time.sleep(2)
        self.res.delta_mode(self.parameters['current_mA']/1000.0)
        time.sleep(1)
        self.temp.change_temp(self.parameters['temperature'],self.parameters['rate'],
                              self.parameters['heater'])
        time.sleep(5)
        
        ti = time.time()
        
        try:
            while True and self.running:
                time_aux = time.time() - ti             
                self.results_inst[:4] = self.measure()
                self.results_inst[4] = time_aux
                result = self.results_inst
                self.signals.result.emit(result)
                time.sleep(self.parameters['sleep_time'])
       
#                self.res.stop_meas()
#                
#                
#            if not self.running:
#                self.res.stop_meas()
#                self.campo.set_voltage_steps(0.0)
#                time.sleep(5)
#                print('pare la medicion')
            
            if not self.running:
                self.res.stop_meas()
                if not self.parameters['temp_check']:
                    self.temp.set_range()
                print('pare la medicion')
                pass    
            
        except not self.running:
            self.res.stop_meas()
            if not self.parameters['temp_check']:
                self.temp.set_range()
            print('pare la medicion')
            pass

        finally:
            self.signals.finished.emit()  # Done


class mywindow(QtWidgets.QMainWindow):
 
    def __init__(self):
 
        super(mywindow, self).__init__()
 
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.pushButton.clicked.connect(self.open_dialog_box)
        
        self.ui.pushButton_11.clicked.connect(self.start)
        self.vistos = []
        
        # self.ui.checkBox.stateChanged.connect(self.field_check)
        # self.field_on = False

        # self.ui.checkBox_2.stateChanged.connect(self.save_check)
        # self.save = False
        
        # self.ui.checkBox_3.stateChanged.connect(self.temp_check)
        # self.temp_c = False
        
        # self.curve = self.ui.graphWidget.plot(pen=(200,200,200), symbolBrush=(255,0,0), symbolPen='w')
        # self.ui.graphWidget.setLabel('left', "Resistencia", units='Ohm')
        # self.ui.graphWidget.setLabel('bottom', "Temperature_A", units='K')
        
        # self.curve2 = self.ui.graphWidget_2.plot(pen=(200,200,200), symbolBrush=(255,0,0), symbolPen='w')
        # self.ui.graphWidget_2.setLabel('left', "Temperature_A", units='K')
        # self.ui.graphWidget_2.setLabel('bottom', "Time", units='seg')
                
        # self.curve3 = self.ui.graphWidget_3.plot(pen=(200,200,200), symbolBrush=(255,0,0), symbolPen='w')
        # self.ui.graphWidget_3.setLabel('left', "Temperature_B", units='K')
        # self.ui.graphWidget_3.setLabel('bottom', "Time", units='seg')        
        
        # self.ui.pushButton.pressed.connect(self.start)
        # self.running_state = False
        # self.ui.pushButton_2.pressed.connect(self.stop)
        

        
        # self.ui.pushButton_4.clicked.connect(self.plot_temp)
        # self.plot_temp_b = True
        
        # self.ui.progressBar.setRange(0, 100)
        # self.ui.progressBar.setValue(0)        
        
        self.show()
        self.threadpool = QThreadPool()
        self._translate = QtCore.QCoreApplication.translate
        # self.heater = 0

    def open_dialog_box(self):
        file = ''
        file = QFileDialog.getExistingDirectory()
        self.folder = file
        self.folders = os.listdir(self.folder)
        self.number_elements = len(self.folders)
        self.capitulos = []
        for element in self.folders:
            self.capitulos.append(self.contar_cap("{}/{}".format(self.folder,element)))
        total_cap = np.sum(np.array(self.capitulos))
        self.weights = np.array(self.capitulos)/total_cap
        
            
        
    def contar_cap(self,carpeta):
        sub_folders = os.listdir(carpeta)
        number_cap = 0
        print(sub_folders)
        for element in sub_folders:
            number_cap += len(os.listdir("{}/{}".format(carpeta,element)))
        return number_cap
            
    
    def random_weight(self,number_folder,weights):
        aux = np.linspace(0, number_folder-1,num=number_folder-1)
        result = np.random.choice(aux,p=weights)
        return result
    
    def random(self,number_folder):
        result = int(np.random.random()*number_folder)
        return result

        
    def update(self,data):
        self.temperature_a.append(data[0])
        self.temperature_b.append(data[1])
        self.resistance.append(data[2])
        self.time.append(data[4])
        
        self.ui.lineEdit_11.setText(self._translate("MainWindow", "{}".format(str(self.resistance[-1]))))
        self.ui.lineEdit_12.setText(self._translate("MainWindow", "{}".format(str(self.temperature_a[-1]))))
        self.ui.lineEdit_13.setText(self._translate("MainWindow", "{}".format(str(self.temperature_b[-1]))))
        
        if self.plot_temp_b:
            self.curve.setData(self.temperature_b,self.resistance)
        else:
            self.curve.setData(self.temperature_a,self.resistance)
            
        self.curve2.setData(self.time,self.temperature_a)
        self.curve3.setData(self.time,self.temperature_b)
        self.ui.progressBar.setValue(data[3])
        if self.param['save'] and self.running_state:
            self.f.write('{},{},{},{}\n'.format(self.time[-1],self.temperature_a[-1],
                                                self.temperature_b[-1],self.resistance[-1]))

            
        
    def stop(self):
        self.worker.stop()
        print('Pare el thread')
        if self.param['save']:
            self.f.close()
        self.ui.lineEdit_14.setText(self._translate("MainWindow", "User stop"))
        
        self.running_state = False
        
    def end(self):
        if self.param['save']:
            self.f.close()
        self.ui.lineEdit_14.setText(self._translate("MainWindow", "Finished"))
        print('Medicion finalizada')
        self.running_state = False
            
        
    def start(self):
        self.ui.pushButton_11.setEnabled(False)
        serie = None
        if len(self.vistos) ==0:
            serie = self.random_weight(self.number_elements,self.weights)
        else:
            serie_aux = self.random_weight(self.number_elements,self.weights)
            while serie_aux in self.vistos:
                serie_aux = self.random_weight(self.number_elements,self.weights)
            serie = serie_aux
        
        video_path = "{}/{}".format(self.folder,self.folders[serie])
        self.worker = self.Worker(video_path,self.ui.lineEdit.text())
        
        
        if not self.running_state:
    #        self.curve.setData([1,2,3],[4,3,2])
            self.running_state = True
            
            self.temperature_a = []
            self.temperature_b = []
            self.resistance = []
            self.time = []
            
            self.heater_state()
            
            self.param = {'current_mA': float(self.ui.lineEdit.text()),
                          'samples': int(self.ui.lineEdit_2.text()),
                          'field_on' : self.field_on,
                          'field' : float(self.ui.lineEdit_6.text()),
                          'temperature' : float(self.ui.lineEdit_7.text()),
                          'rate': float(self.ui.lineEdit_8.text()),
                          'heater' : self.heater,
                          'sleep_time' : float(self.ui.lineEdit_9.text()),
                          'save' : self.save,
                          'name' : str(self.ui.lineEdit_10.text()),
                          'temp_check' : self.temp_c
                         }        
            
    
            tiempo_aux_ini = time.time()
            tiempo_aux = tiempo_aux_ini
            while (tiempo_aux - tiempo_aux_ini) < 2:
                tiempo_aux = time.time()
            
            if self.param['save']:
                self.f = open(self.path + '/{}'.format(self.param['name']),'w')
                self.f.write('Time(s),Temperature_a(K),Temperature_b(K),Resistance(Ohm)\n')
                
                    
            self.worker = Worker(self.param)
            self.worker.signals.result.connect(self.update)
            self.worker.signals.finished.connect(self.end)
            self.threadpool.start(self.worker) 
            self.ui.lineEdit_14.setText(self._translate("MainWindow", "Running"))

            
#        self.ui.pushButton.clicked.connect(self.btnClicked) # connecting the clicked signal with btnClicked slot
# 
#    def btnClicked(self):
# 
#        self.ui.label.setText("Button Clicked")
 
 
#app = QtWidgets.QApplication([])
# 
#application = mywindow()
# 
#application.show()
#app.exec_()
#sys.exit(app.exec())
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = mywindow()
    application.show()
    sys.exit(app.exec_())