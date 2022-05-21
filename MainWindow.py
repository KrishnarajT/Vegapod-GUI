# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Bose_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import sys, os
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import motor_control as mtcr
from PyQt5.QtCore import QThread, QObject, pyqtSignal
import time
import sensor_output as so
import socket
from datetime import datetime


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(list, list, float, int)
    gimme_values = pyqtSignal()

    def __init__(self, direction_text, step_val, end_val, interval_val):
        super().__init__()
        if direction_text == 'Forward':
            self.direction = 1
        else: self.direction = str(2)
        
        self.step_val = str(step_val)
        self.end_val = str(end_val)
        self.interval_val = str(interval_val)

    def run(self):
        print('motor code was invoked. ')
        
                
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.bind((socket.gethostname(), 1234))
        # s.listen(5)
        # clientsocket, address = s.accept()
        # print(f"connection from {address} has been established!")

        # clientsocket.send(bytes(self.direction, "utf-8"))
        # time.sleep(0.5)
        # clientsocket.send(bytes(self.end_val, "utf-8"))
        # time.sleep(0.5)
        # clientsocket.send(bytes(self.step_val, "utf-8"))
        # time.sleep(0.5)
        # clientsocket.send(bytes(self.interval_val, "utf-8"))
        # time.sleep(0.5)
            
        # s.close()
        # clientsocket.close
        # clientsocket.detach
        # time.sleep(1)        
        
        # #Connecting as client
        # a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # a.connect(('169.254.201.77', 1234))
        # print(f"connection from {address} has been established AGAIN as client !!!")

        # Take values for approx 20/25 seconds
        x = time.time()
        samay = 0
        while (samay < 7):
            b = time.time()
            samay = b - x
            print("inside recv loop")
            
            ### RECEIVING VALUES FROM PI and PARSING JSON

            # Taking data from the PI as a dict. 
            # raw_data = a.recv(1024)
            # if not raw_data:
            #     break;
            # raw_data = raw_data.decode("utf-8")

            # raw_data = json.loads(raw_data) # is now a dictionary. 

            # accel_data = raw_data['Acceleration']
            # gyro_data = raw_data['Gyroscope']
            # rpm_data = raw_data['RPM']
            # pressure_data = raw_data['Pressure']
            
            ### DUMMY VALUES  ###
            
            accel_data = [datetime.today().second * 2, datetime.today().second - 1, datetime.today().second]
            gyro_data = [datetime.today().second * 5, datetime.today().second, datetime.today().second * 7]
            rpm_data = 5000
            pressure_data = 100.00

            
            ### Sending values to GUI for updating ###
            
            self.progress.emit(accel_data, gyro_data, pressure_data, rpm_data)
            time.sleep(0.1)
            
            
            
        
        print("Session finished...")
                
        self.finished.emit()

    def stop_immediately(self):
        # Maybe ask the pi to break? 
        print('breaking. ')
        # self.maybeconnectionserver.close() and b4 that send break. 
        self.finished.emit()

class Ui_MainWindow(QMainWindow):
    stop_signal = pyqtSignal()  # make a stop signal to communicate with the worker in another thread

    def __init__(self):
        super().__init__()
        self.setObjectName("BOSE GUI")
        self.resize(720, 480)
        self.setupUi()

        # Defining basic values

        self.start_value = 1
        self.end_value = 20
        self.step_value = 5
        self.interval = 500
        
        
    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker(self.direction_combo_box.currentText(), int(self.step_value_line_edit.text()),\
            int(self.end_value_line_edit.text()), int(self.interval_line_edit.text()))
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        self.worker.gimme_values.connect(self.give_val)
        self.stop_signal.connect(self.worker.stop_immediately)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        # self.longRunningBtn.setEnabled(False)
        # self.thread.finished.connect(
        #     lambda: self.longRunningBtn.setEnabled(True)
        # )
        # self.thread.finished.connect(
        #     lambda: self.stepLabel.setText("Long-Running Step: 0")
        # )
        
    def stop_thread(self):
        self.stop_signal.emit()
    
    def give_val(self):
        return 1
        
    def start_pod(self):
        
        
        if 'Forward' == self.direction_combo_box.currentText():
            self.start_value = 1
        else: self.start_value = 2
        
        self.end_value = self.end_value_line_edit.text()
        self.step_value = self.step_value_line_edit.text()
        self.end_value = self.end_value_line_edit.text()
        self.interval = self.interval_line_edit.text()
        
        # Calling the function to run the motors. 
        mtcr.input_and_control(self.start_value, self.end_value, self.step_value, self.interval)

        # # switching tab to data tab
        # self.navigation_tab_widget.setCurrentIndex(2)
        
        
        # self.thread = QThread()
        # self.worker = Worker(parent=self)
        # self.worker.asx.connect(self.updateit)
        # # self.stop_signal.connect(self.worker.stop)  # connect stop signal to worker stop method
        # # self.worker.moveToThread(self.thread)

        # # self.thread.started.connect(lambda: self.worker.do_work(self.navigation_tab_widget, self.acc_x_value_lbl))
        # # self.worker.finished.connect(self.thread.quit)  # connect the workers finished signal to stop thread
        # # self.worker.finished.connect(self.worker.deleteLater)  # connect the workers finished signal to clean up worker
        # # self.thread.finished.connect(self.thread.deleteLater)  # connect threads finished signal to clean up thread

        # # self.thread.finished.connect(self.worker.stop)
        # self.thread.start()

      
    def stop_pod(self):
        self.stop_signal.emit()

    def reportProgress(self, n, b, p, r):
        self.navigation_tab_widget.setCurrentIndex(2)
        self.step_value_lbl.setText(f"Long-Running Step: {n[0]}")
        self.gyro_x_value_lbl.setText(str(round(n[0], 3)))
        self.gyro_y_value_lbl.setText(str(round(n[1], 3)))
        self.gyro_z_value_lbl.setText(str(round(n[2], 3)))        
        self.acc_x_value_lbl.setText(str(round(b[0], 3)))
        self.acc_y_value_lbl.setText(str(round(b[1], 3)))
        self.acc_z_value_lbl.setText(str(round(b[2], 3))) 
        self.pressure_value_lbl.setText(str(p))
        self.rpm_value_lbl.setText(str(r))


 
    def setupUi(self):

        
        # Setting Font
        font = QtGui.QFont()
        font.setFamily("Arvo")
        font.setPointSize(15)
        
        dir_ = QtCore.QDir("Roboto")
        QtGui.QFontDatabase.addApplicationFont("./design/JerseyM54-aLX9.ttf")
        
        number_font = QtGui.QFont()
        number_font.setFamily("Arvo")
        number_font.setPointSize(70)
        # Defining Basic Widgets
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.navigation_tab_widget = QtWidgets.QTabWidget(self.centralwidget)
        self.navigation_tab_widget.setGeometry(QtCore.QRect(0, 100, 720, 380))
        self.navigation_tab_widget.setStyleSheet("background-color: #DDDDDD")
        self.navigation_tab_widget.setObjectName("navigation_tab_widget")
        
        
        # Adding the Heading Image. 
        
        self.im = QPixmap(os.path.join(os.getcwd(), 'design', 'images', 'Heading.jpg'))
        self.heading_image_lbl = QtWidgets.QLabel(self.centralwidget)
        self.heading_image_lbl.setPixmap(self.im)
        self.heading_image_lbl.resize(self.im.width(), self.im.height())
        
        
        #############################################################################################
        #### Tab 1 - Input Tab ######        
        #############################################################################################
        
        
        self.inputs_tab = QtWidgets.QWidget()
        self.inputs_tab.setObjectName("inputs_tab")
        self.navigation_tab_widget.addTab(self.inputs_tab, "")

        
        self.direction_lbl = QtWidgets.QLabel(self.inputs_tab)
        self.direction_lbl.setGeometry(QtCore.QRect(140, 20, 231, 51))
        self.direction_lbl.setFont(font)
        self.direction_lbl.setStyleSheet("color:#06113C")
        self.direction_lbl.setObjectName("direction_lbl")
        
        
        # self.start_value_lbl = QtWidgets.QLabel(self.inputs_tab)
        # self.start_value_lbl.setGeometry(QtCore.QRect(140, 70, 231, 51))
        # self.start_value_lbl.setFont(font)
        # self.start_value_lbl.setStyleSheet("color:#06113C")
        # self.start_value_lbl.setObjectName("start_value_lbl")
        
        
        # self.start_value_line_edit = QtWidgets.QLineEdit(self.inputs_tab)
        # self.start_value_line_edit.setGeometry(QtCore.QRect(420, 80, 113, 34))
        # self.start_value_line_edit.setObjectName("start_value_line_edit")
        
        
        self.end_value_lbl = QtWidgets.QLabel(self.inputs_tab)
        self.end_value_lbl.setGeometry(QtCore.QRect(140, 110, 231, 51))
        self.end_value_lbl.setFont(font)
        self.end_value_lbl.setStyleSheet("color:#06113C")
        self.end_value_lbl.setObjectName("end_value_lbl")
        
        
        self.end_value_line_edit = QtWidgets.QLineEdit(self.inputs_tab)
        self.end_value_line_edit.setGeometry(QtCore.QRect(420, 120, 113, 34))
        self.end_value_line_edit.setObjectName("end_value_line_edit")
        
        self.step_value_lbl = QtWidgets.QLabel(self.inputs_tab)
        self.step_value_lbl.setGeometry(QtCore.QRect(140, 150, 231, 51))
        self.step_value_lbl.setFont(font)
        self.step_value_lbl.setStyleSheet("color:#06113C")
        self.step_value_lbl.setObjectName("step_value_lbl")
        
        
        self.step_value_line_edit = QtWidgets.QLineEdit(self.inputs_tab)
        self.step_value_line_edit.setGeometry(QtCore.QRect(420, 160, 113, 34))
        self.step_value_line_edit.setObjectName("step_value_line_edit")
        
        
        
        self.interval_value_lbl = QtWidgets.QLabel(self.inputs_tab)
        self.interval_value_lbl.setGeometry(QtCore.QRect(140, 190, 241, 71))
        self.interval_value_lbl.setFont(font)
        self.interval_value_lbl.setStyleSheet("color:#06113C")
        self.interval_value_lbl.setObjectName("interval_value_lbl")
        
        
        self.interval_line_edit = QtWidgets.QLineEdit(self.inputs_tab)
        self.interval_line_edit.setGeometry(QtCore.QRect(420, 200, 113, 34))
        self.interval_line_edit.setObjectName("interval_line_edit")
        
        
        self.start_btn = QtWidgets.QPushButton(self.inputs_tab)
        self.start_btn.setGeometry(QtCore.QRect(270, 270, 160, 34))
        self.start_btn.setObjectName("start_btn")
        self.start_btn.clicked.connect(self.runLongTask)
        
        self.direction_combo_box = QtWidgets.QComboBox(self.inputs_tab)
        self.direction_combo_box.setGeometry(QtCore.QRect(420, 30, 171, 34))
        self.direction_combo_box.setStyleSheet("color:#06113C")
        self.direction_combo_box.setObjectName("direction_combo_box")

        
        #############################################################################################
        #### Tab 2 - Dashboard Tab ######        
        #############################################################################################
        
        # We are supposed to make the dashboard in this tab, after calculating speed. 
        
        self.dashboard_tab = QtWidgets.QWidget()
        self.dashboard_tab.setObjectName("dashboard_tab")
        self.navigation_tab_widget.addTab(self.dashboard_tab, "")
        
        self.dashboard_tab.setStyleSheet('background-color:#06113C')
        
        self.speed_lbl = QtWidgets.QLabel(self.dashboard_tab)
        self.speed_lbl.setGeometry(QtCore.QRect(300, 100, 300, 100))
        self.speed_lbl.setFont(number_font)
        self.speed_lbl.setStyleSheet("color:#FF8C32")
        self.speed_lbl.setObjectName("interval_value_lbl")        
        
        
        
        
        
        
        
        #############################################################################################
        #### Tab 3 - Data Tab ######        
        #############################################################################################
        
        # This tab has all the raw data displayed. 
        
        self.data_tab = QtWidgets.QWidget()
        self.data_tab.setObjectName("data_tab")
        
        # On the top we have Temperature
        
        
        self.widget = QtWidgets.QWidget(self.data_tab)
        self.widget.setGeometry(QtCore.QRect(200, 10, 301, 51))
        self.widget.setObjectName("widget")
        
        self.temp_hori_layout = QtWidgets.QHBoxLayout(self.widget)
        self.temp_hori_layout.setContentsMargins(0, 0, 0, 0)
        self.temp_hori_layout.setObjectName("temp_hori_layout")
        
        
        self.temp_lbl = QtWidgets.QLabel(self.widget)
        self.temp_lbl.setFont(font)
        self.temp_lbl.setStyleSheet("color:#06113C")
        self.temp_lbl.setObjectName("temp_lbl")
        
        
        self.temp_hori_layout.addWidget(self.temp_lbl)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.temp_hori_layout.addItem(spacerItem)
        
        
        font.setPointSize(15)
        self.temp_value_lbl = QtWidgets.QLabel(self.widget)
        self.temp_value_lbl.setFont(font)
        self.temp_value_lbl.setStyleSheet("color:#06113C")
        self.temp_value_lbl.setObjectName("temp_value_lbl")
        
        
        self.temp_hori_layout.addWidget(self.temp_value_lbl) 


        self.pressure_lbl = QtWidgets.QLabel(self.data_tab)
        self.pressure_lbl.setGeometry(200, 50, 300, 50)
        self.pressure_lbl.setFont(font)
        self.pressure_lbl.setStyleSheet("color:#06113C")
        self.pressure_lbl.setObjectName("pressure_lbl")
        
   
        font.setPointSize(15)
        self.pressure_value_lbl = QtWidgets.QLabel(self.data_tab)
        self.pressure_value_lbl.setGeometry(400, 50, 50, 50)
        self.pressure_value_lbl.setFont(font)
        self.pressure_value_lbl.setStyleSheet("color:#06113C")
        self.pressure_value_lbl.setObjectName("pressure_value_lbl")
        
        
        self.rpm_lbl = QtWidgets.QLabel(self.data_tab)
        self.rpm_lbl.setGeometry(250, 90, 300, 50)
        self.rpm_lbl.setFont(font)
        self.rpm_lbl.setStyleSheet("color:#06113C")
        self.rpm_lbl.setObjectName("rpm_lbl")
        
   
        font.setPointSize(15)
        self.rpm_value_lbl = QtWidgets.QLabel(self.data_tab)
        self.rpm_value_lbl.setGeometry(400, 90, 50, 50)
        self.rpm_value_lbl.setFont(font)
        self.rpm_value_lbl.setStyleSheet("color:#06113C")
        self.rpm_value_lbl.setObjectName("rpm_value_lbl")
        
        
        # Then on the left we have Acceleration
        
        self.acceleration_lbl = QtWidgets.QLabel(self.data_tab)
        self.acceleration_lbl.setGeometry(QtCore.QRect(70, 90, 141, 41))
        self.acceleration_lbl.setFont(font)
        self.acceleration_lbl.setStyleSheet("color:#06113C")
        self.acceleration_lbl.setObjectName("acceleration_lbl")
        

        self.layoutWidget = QtWidgets.QWidget(self.data_tab)
        self.layoutWidget.setGeometry(QtCore.QRect(70, 190, 111, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        
        
        self.acc_y_hori_layout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.acc_y_hori_layout.setContentsMargins(0, 0, 0, 0)
        self.acc_y_hori_layout.setObjectName("acc_y_hori_layout")
        
        
        self.acc_y_lbl = QtWidgets.QLabel(self.layoutWidget)
        self.acc_y_lbl.setFont(font)
        self.acc_y_lbl.setStyleSheet("color:#06113C")
        self.acc_y_lbl.setObjectName("acc_y_lbl")
        
        
        self.acc_y_hori_layout.addWidget(self.acc_y_lbl)
        
        self.acc_y_value_lbl = QtWidgets.QLabel(self.layoutWidget)
        self.acc_y_value_lbl.setFont(font)
        self.acc_y_value_lbl.setStyleSheet("color:#06113C")
        self.acc_y_value_lbl.setObjectName("acc_y_value_lbl")
        
        self.acc_y_hori_layout.addWidget(self.acc_y_value_lbl)
        
        self.layoutWidget_2 = QtWidgets.QWidget(self.data_tab)
        self.layoutWidget_2.setGeometry(QtCore.QRect(70, 230, 111, 31))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        
        
        self.acc_z_hori_layout = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.acc_z_hori_layout.setContentsMargins(0, 0, 0, 0)
        self.acc_z_hori_layout.setObjectName("acc_z_hori_layout")
        
        self.acc_z_lbl = QtWidgets.QLabel(self.layoutWidget_2)
        self.acc_z_lbl.setFont(font)
        self.acc_z_lbl.setStyleSheet("color:#06113C")
        self.acc_z_lbl.setObjectName("acc_z_lbl")
        
        
        self.acc_z_hori_layout.addWidget(self.acc_z_lbl)
        
        self.acc_z_value_lbl = QtWidgets.QLabel(self.layoutWidget_2)
        self.acc_z_value_lbl.setFont(font)
        self.acc_z_value_lbl.setStyleSheet("color:#06113C")
        self.acc_z_value_lbl.setObjectName("acc_z_value_lbl")
        
        
        self.acc_z_hori_layout.addWidget(self.acc_z_value_lbl)
        
        
        # Then on the right we have the gyroscope Data
        
        
        self.layoutWidget_3 = QtWidgets.QWidget(self.data_tab)
        self.layoutWidget_3.setGeometry(QtCore.QRect(480, 190, 111, 31))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        
                
        self.gyroscope_lbl = QtWidgets.QLabel(self.data_tab)
        self.gyroscope_lbl.setGeometry(QtCore.QRect(490, 90, 141, 41))
        self.gyroscope_lbl.setFont(font)
        self.gyroscope_lbl.setStyleSheet("color:#06113C")
        self.gyroscope_lbl.setObjectName("gyroscope_lbl")
    
        
        self.gyro_y_hori_layout = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.gyro_y_hori_layout.setContentsMargins(0, 0, 0, 0)
        self.gyro_y_hori_layout.setObjectName("gyro_y_hori_layout")
        
        
        self.gyro_y_lbl = QtWidgets.QLabel(self.layoutWidget_3)
        self.gyro_y_lbl.setFont(font)
        self.gyro_y_lbl.setStyleSheet("color:#06113C")
        self.gyro_y_lbl.setObjectName("gyro_y_lbl")
        
        
        self.gyro_y_hori_layout.addWidget(self.gyro_y_lbl)
        self.gyro_y_value_lbl = QtWidgets.QLabel(self.layoutWidget_3)
        self.gyro_y_value_lbl.setFont(font)
        self.gyro_y_value_lbl.setStyleSheet("color:#06113C")
        self.gyro_y_value_lbl.setObjectName("gyro_y_value_lbl")
        
        
        self.gyro_y_hori_layout.addWidget(self.gyro_y_value_lbl)
        
        self.layoutWidget_4 = QtWidgets.QWidget(self.data_tab)
        self.layoutWidget_4.setGeometry(QtCore.QRect(480, 230, 111, 31))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        
        
        self.gyro_z_hori_layout = QtWidgets.QHBoxLayout(self.layoutWidget_4)
        self.gyro_z_hori_layout.setContentsMargins(0, 0, 0, 0)
        self.gyro_z_hori_layout.setObjectName("gyro_z_hori_layout")
        
        
        self.gyro_z_lbl = QtWidgets.QLabel(self.layoutWidget_4)
        self.gyro_z_lbl.setFont(font)
        self.gyro_z_lbl.setStyleSheet("color:#06113C")
        self.gyro_z_lbl.setObjectName("gyro_z_lbl")
        
        self.gyro_z_hori_layout.addWidget(self.gyro_z_lbl)

        self.gyro_z_value_lbl = QtWidgets.QLabel(self.layoutWidget_4)
        self.gyro_z_value_lbl.setFont(font)
        self.gyro_z_value_lbl.setStyleSheet("color:#06113C")
        self.gyro_z_value_lbl.setObjectName("gyro_z_value_lbl")
        
        
        self.gyro_z_hori_layout.addWidget(self.gyro_z_value_lbl)
        
        self.layoutWidget_5 = QtWidgets.QWidget(self.data_tab)
        self.layoutWidget_5.setGeometry(QtCore.QRect(480, 150, 111, 31))
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        
        self.gyro_x_hori_layout = QtWidgets.QHBoxLayout(self.layoutWidget_5)
        self.gyro_x_hori_layout.setContentsMargins(0, 0, 0, 0)
        self.gyro_x_hori_layout.setObjectName("gyro_x_hori_layout")
        
        
        self.gyro_x_lbl = QtWidgets.QLabel(self.layoutWidget_5)
        self.gyro_x_lbl.setFont(font)
        self.gyro_x_lbl.setStyleSheet("color:#06113C")
        self.gyro_x_lbl.setObjectName("gyro_x_lbl")
        
        
        self.gyro_x_hori_layout.addWidget(self.gyro_x_lbl)
        
        
        self.gyro_x_value_lbl = QtWidgets.QLabel(self.layoutWidget_5)
        self.gyro_x_value_lbl.setFont(font)
        self.gyro_x_value_lbl.setStyleSheet("color:#06113C")
        self.gyro_x_value_lbl.setObjectName("gyro_x_value_lbl")
        self.gyro_x_hori_layout.addWidget(self.gyro_x_value_lbl)
        
        
        self.widget1 = QtWidgets.QWidget(self.data_tab)
        self.widget1.setGeometry(QtCore.QRect(70, 150, 111, 31))
        self.widget1.setObjectName("widget1")
        
        
        self.acc_x_hori_layout = QtWidgets.QHBoxLayout(self.widget1)
        self.acc_x_hori_layout.setContentsMargins(0, 0, 0, 0)
        self.acc_x_hori_layout.setObjectName("acc_x_hori_layout")
        
        self.acc_x_lbl = QtWidgets.QLabel(self.widget1)
        self.acc_x_lbl.setFont(font)
        self.acc_x_lbl.setStyleSheet("color:#06113C")
        self.acc_x_lbl.setObjectName("acc_x_lbl")
        
        
        self.acc_x_hori_layout.addWidget(self.acc_x_lbl)
        self.acc_x_value_lbl = QtWidgets.QLabel(self.widget1)
        self.acc_x_value_lbl.setFont(font)
        self.acc_x_value_lbl.setStyleSheet("color:#06113C")
        self.acc_x_value_lbl.setObjectName("acc_x_value_lbl")
        self.acc_x_hori_layout.addWidget(self.acc_x_value_lbl)

        self.stop_btn = QtWidgets.QPushButton(self.data_tab)
        self.stop_btn.setGeometry(QtCore.QRect(260, 270, 160, 34))
        self.stop_btn.setObjectName("stop_btn")
        self.stop_btn.clicked.connect(self.stop_thread)


        
        
        self.navigation_tab_widget.addTab(self.data_tab, "")
        




        
        # Usual steps. 

        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        self.navigation_tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "BOSE POD GUI"))
        self.direction_lbl.setText(_translate("self", "Enter Direction of Pod"))
        # self.start_value_lbl.setText(_translate("self", "Enter Start Value"))
        self.step_value_lbl.setText(_translate("self", "Enter Step value"))
        self.end_value_lbl.setText(_translate("self", "Enter End Value"))
        self.interval_value_lbl.setText(_translate("self", "<html><head/><body><p>Enter Interval <br/>(in microseconds)</p></body></html>"))
        self.start_btn.setText(_translate("self", "Start Run"))
        self.stop_btn.setText(_translate("self", "Stop Run"))
        self.direction_combo_box.addItem("")
        self.direction_combo_box.addItem("")
        self.direction_combo_box.setItemText(0, _translate("self", "Forward"))
        self.direction_combo_box.setItemText(1, _translate("self", "Reverse"))
        self.navigation_tab_widget.setTabText(self.navigation_tab_widget.indexOf(self.inputs_tab), _translate("self", "Inputs"))
        self.navigation_tab_widget.setTabText(self.navigation_tab_widget.indexOf(self.dashboard_tab), _translate("self", "Dashboard"))
        self.acceleration_lbl.setText(_translate("self", "Acceleration"))
        self.gyroscope_lbl.setText(_translate("self", "Gyroscope"))
      
        self.gyro_y_lbl.setText(_translate("self", "Y:"))
        self.gyro_y_value_lbl.setText(_translate("self", "10"))
        self.gyro_z_lbl.setText(_translate("self", "Z:"))
        self.gyro_z_value_lbl.setText(_translate("self", "10"))
        self.gyro_x_lbl.setText(_translate("self", "X:"))
        self.gyro_x_value_lbl.setText(_translate("self", "10"))
        self.temp_lbl.setText(_translate("self", "Temperature (C) :"))
        self.temp_value_lbl.setText(_translate("self", "40 C"))
        self.pressure_lbl.setText(_translate("self", "Pressure (atm) :"))
        self.pressure_value_lbl.setText(_translate("self", "100"))
        self.rpm_lbl.setText(_translate("self", "rpm :"))
        self.rpm_value_lbl.setText(_translate("self", "100"))
        self.acc_x_lbl.setText(_translate("self", "X:"))
        self.acc_x_value_lbl.setText(_translate("self", "10"))
        self.acc_y_lbl.setText(_translate("self", "Y:"))
        self.acc_y_value_lbl.setText(_translate("self", "10"))
        self.acc_z_lbl.setText(_translate("self", "Z:"))
        self.acc_z_value_lbl.setText(_translate("self", "10"))
        self.navigation_tab_widget.setTabText(self.navigation_tab_widget.indexOf(self.data_tab), _translate("self", "Data"))
        self.speed_lbl.setText("24")

        # self.validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[0-9].+'))
        # self.curncy_1_line_edit.setValidator(self.validator)
        # self.curncy_1_line_edit.setText('1.000')
        # self.cur_1_value = 1.000
        # self.curncy_2_line_edit.setValidator(self.validator)

