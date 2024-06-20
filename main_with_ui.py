# Version: 1.0
"""
This file contains the implementation of the main program with user interface (UI).
It imports necessary modules and defines functions for PLC connection, fuzzy matching, and loading AI module.
It also includes a custom model class for displaying data in a PyQt5 table view.

Functions:
- plc_connect(ip_address, connect_type): Establishes a connection to a PLC using the specified IP address and connection type.
- fuzzy_match(ocr_fpc_list, ocr_batch_list, conf_level): Performs fuzzy matching on OCR results to determine the FPC batch.
- load_ai_module(path, bath_size, anchor_sizes, anchor_ratios, num_classes, accept_score): Loads an AI module from the specified path with the given parameters.

Variables:
- df_user_congfigure: DataFrame containing user configuration data.
- df1_ocr_sort_info: DataFrame containing OCR and sorting information.
- df2_fpc_batch_summary: DataFrame containing FPC batch summary information.
- df3_sorter_output_status: DataFrame containing sorter output status information.
"""

# Rest of the code...
# -*- coding: utf-8 -*-

"""
This file contains the implementation of the main program with user interface (UI).
"""
import sys
sys.path.append('/home/psic02/.local/lib/python3.10/site-packages/')

from PyQt5 import QtCore, QtGui, QtWidgets
import datetime,traceback,sys,cv2,time,logging,re,random
from math import isnan
from Modules import plc as plc
import pandas as pd
import numpy as np
from Modules import basler_camera as camera
from Modules import ocrModule as ocr_ai
from Modules.thread3_calculate_sorter_output import calculate_sorter_output
from Modules.thread5_accumulated_cnt_and_sorter_release import accumulated_cnt_and_sorter_release
from UI_MainWindow import Ui_MainWindow
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

df_user_congfigure = pd.DataFrame(columns = ['user','password','user_level'],data =[['admin','admin',1],['test_user_1','admin',2] ,['test_user_2','admin',2]])

df1_ocr_sort_info = pd.DataFrame(columns=['serial_num', 'sensor_on_tm','sensor_off_tm','image_capture_tm', 'ocr_finish_tm','img',

                                         'fpc_batch','ocr_result', 'sorter_output',

                                         'backup_output', 'sorter_enter_tm',

                                         'sorter_success_enter', 'success_sort'])

df1_ocr_sort_info['img'] = df1_ocr_sort_info['img'].astype('object')

thread3_ocr_ai_thread_id = 0
#df1_ocr_sort_info.set_index('serial_num', inplace=True)  # make the type as index, then easy to retrieve the data

df2_fpc_batch_summary  = pd.DataFrame(columns=['fpc_batch', 'target_qty', 'actual_qty','completion', 'last_enter_tm', 'waited_tm', 'sorter_output'])

#df2_fpc_batch_summary.set_index('fpc_batch', inplace=True)  # make the type as index, then easy to retrieve the data

df3_sorter_output_status = pd.DataFrame(columns=['sorter_output', 'logic_available', 'physical_available',

                                                'previous_fpc', 'output_available'])

df3_sorter_output_status['sorter_output'] = ['1','2','3','4','5','6','7']

df3_sorter_output_status['logic_available'] = [False, True,True,False,False,False,True]

df3_sorter_output_status['physical_available'] = [True, True,True,True,True,True,True]

df3_sorter_output_status['output_available'] = [False, True,True,True,True,True,True]

#df_sorter_output_status.set_index('sorter_output', inplace=True)  # make the type as index, then easy to retrieve the data

def plc_connect(ip_address, connect_type):
    """
    Connects to a Siemens PLC using the specified IP address and connection type.

    Args:
        ip_address (str): The IP address of the PLC.
        connect_type (str): The type of connection to establish.

    Returns:
        siemens_plc: The connected Siemens PLC object.
        False: If an exception occurs during the connection process.
    """
    try:
        siemens_plc = plc.plc_connect(ip_address, connect_type)

        return siemens_plc

    except Exception:
        print(traceback.print_exc())

        return False

def fuzzy_match(ocr_fpc_list, ocr_batch_list,conf_level=0.7) -> (str, str): # type: ignore
    global df2_fpc_batch_summary
    
    df2_copy = df2_fpc_batch_summary.iloc[:-1,:]

    dict_similar_char = pd.read_csv('similar_char.csv',sep='\t',converters={'RegionChar':str,'MaybeChar': eval}).set_index('RegionChar')['MaybeChar'].to_dict()

    def longest_common_subsequence(s1: str, s2: str):

        """
        Calculates the length of the longest common subsequence between two strings.

        Args:
            s1 (str): The first string.
            s2 (str): The second string.

        Returns:
            int: The length of the longest common subsequence.
        """
        m = len(s1)
        n = len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # dict_similar_char = {'B':['8','3'],
        #                      'D':['0'£¬'1'],
        #                      '8':['3'],
        #                      'G':['6','8','0'],
        #                      '4':['A'],
        #                      '2':['Z'],
        #                      'L':['1'],
        #                      '1':['T'],
        #                      'C':['0','6'],
        #                      '0':['Q'],
        #                      '5':['S']
        #                      }



        for i in range(1, m + 1):
            for j in range(1, n + 1):

                # ÌØÊâ×Ö·ûÆ¥Åä¹ØÏµ

                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:   
                    for key,values in dict_similar_char.items():

                        if s1[i - 1] == key and s2[j - 1] in values:
                            dp[i][j] = dp[i - 1][j - 1] + 1
                            break
                        else:
                            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                # if s1[i - 1] == s2[j - 1] or \
                #     (s1[i - 1] == 'B' and s2[j - 1] == '8') or \
                #     (s1[i - 1] == 'B' and s2[j - 1] == '3') or \
                #     (s1[i - 1] == 'D' and s2[j - 1] == '0') or \
                #     (s1[i - 1] == '8' and s2[j - 1] == '3') or \
                #     (s1[i - 1] == '8' and s2[j - 1] == 'B') or \
                #     (s1[i - 1] == 'G' and s2[j - 1] == '6') or \
                #     (s1[i - 1] == 'G' and s2[j - 1] == '8') or \
                #     (s1[i - 1] == 'G' and s2[j - 1] == '0') or \
                #     (s1[i - 1] == '6' and s2[j - 1] == 'G') or \
                #     (s1[i - 1] == '4' and s2[j - 1] == 'A') or \
                #     (s1[i - 1] == '4' and s2[j - 1] == 'R') or \
                #     (s1[i - 1] == '2' and s2[j - 1] == 'Z') or \
                #     (s1[i - 1] == 'L' and s2[j - 1] == '1') or \
                #     (s1[i - 1] == '1' and s2[j - 1] == 'T') or \
                #     (s1[i - 1] == 'C' and s2[j - 1] == '0') or \
                #     (s1[i - 1] == 'C' and s2[j - 1] == '6') or \
                #     (s1[i - 1] == '0' and s2[j - 1] == 'Q') or \
                #     (s1[i - 1] == '0' and s2[j - 1] == 'D') or \
                #     (s1[i - 1] == '5' and s2[j - 1] == 'S'):

                #     dp[i][j] = dp[i - 1][j - 1] + 1
                # else:
                #     dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]

    res_fpc = 'others'
    # Scenario 1: ÎÞfpc, ÎÞbatch
    if len(ocr_fpc_list) == 0 and len(ocr_batch_list) == 0:
        return 'others'

    # Scenario 2: ÎÞfpc
    elif len(ocr_fpc_list) == 0:

        max_lcs_length_batch = 0
        for index, row  in df2_copy.iterrows():
            fpc_batch = row['fpc_batch']
            str_fpc_batch = str(fpc_batch).split('_')
            fpc = str_fpc_batch[0]
            batch = str_fpc_batch[1]
            for ocr_batch in ocr_batch_list:
                curr_lcs_length_batch = longest_common_subsequence(batch, ocr_batch)
                if curr_lcs_length_batch > max_lcs_length_batch:
                    res_batch = batch
                    res_fpc = fpc
                    max_lcs_length_batch = curr_lcs_length_batch

    # Scenario 3: ÎÞbatch
    elif len(ocr_batch_list) == 0:
        max_lcs_length_fpc = 0
        for index, row  in df2_copy.iterrows():
            fpc_batch = row['fpc_batch']
            str_fpc_batch = str(fpc_batch).split('_')
            fpc = str_fpc_batch[0]
            batch = str_fpc_batch[1]
            for ocr_fpc in ocr_fpc_list:
                curr_lcs_length_fpc = longest_common_subsequence(fpc, ocr_fpc)
                if curr_lcs_length_fpc > max_lcs_length_fpc:
                    res_batch = batch
                    res_fpc = fpc
                    max_lcs_length_fpc = curr_lcs_length_fpc

    # Scenario 4: fpc, batch¶¼ÓÐ
    else:

        max_lcs_length_fpc = 0
        max_lcs_length_batch = 0
        for index, row  in df2_copy.iterrows():
            fpc_batch = row['fpc_batch']
            str_fpc_batch = str(fpc_batch).split('_')
            fpc = str_fpc_batch[0]
            batch = str_fpc_batch[1]
            for ocr_fpc in ocr_fpc_list:
                for ocr_batch in ocr_batch_list:
                    curr_lcs_length_fpc = longest_common_subsequence(fpc, ocr_fpc)
                    curr_lcs_length_batch = longest_common_subsequence(batch, ocr_batch)
                    if curr_lcs_length_fpc > max_lcs_length_fpc:
                        res_fpc = fpc
                        res_batch = batch
                        max_lcs_length_fpc = curr_lcs_length_fpc
                        max_lcs_length_batch = curr_lcs_length_batch
                    elif curr_lcs_length_fpc == max_lcs_length_fpc and curr_lcs_length_batch > max_lcs_length_batch:
                        res_fpc = fpc
                        res_batch = batch
                        max_lcs_length_batch = curr_lcs_length_batch
    
    unique_pass = False
    counter = 0
    for index, row in df2_copy.iterrows():
        if res_fpc == row['fpc_batch'].split('_')[0]:
            counter += 1
    if counter == 1:
        unique_pass = True

    if len(ocr_fpc_list) > 0:
        fpc_pass = max_lcs_length_fpc / len(res_fpc) >= conf_level
    else:
        fpc_pass = False

    if len(ocr_batch_list) > 0:
        batch_pass = max_lcs_length_batch / len(res_batch) >= conf_level
    else:
        batch_pass = False
    
    if batch_pass or ((not batch_pass) and fpc_pass and unique_pass):
        #2023 01 05 ÐÞ¸Ä ·µ»Ø fpc_batch
        #return res_fpc, res_batch
        fpc_batch = res_fpc + '_' + res_batch
        return fpc_batch
    else:
        return 'others'
    
def load_ai_module(path, bath_size, anchor_sizes, anchor_ratios, num_classes, accept_score):
    """
    Load the AI module with the specified parameters.

    Args:
        path (str): The path to the AI module.
        bath_size (int): The batch size for prediction.
        anchor_sizes (list): The sizes of the anchor boxes.
        anchor_ratios (list): The ratios of the anchor boxes.
        num_classes (int): The number of classes for prediction.
        accept_score (float): The minimum score to accept a prediction.

    Returns:
        object: The loaded AI module.

    """
    return ocr_ai.load_predictor(path, bath_size, anchor_sizes, anchor_ratios, num_classes, accept_score)

class pandasModel(QtCore.QAbstractTableModel):
    """
    A custom model class for displaying pandas DataFrame in a Qt table view.
    """

    def __init__(self, data):
        """
        Initialize the pandasModel object.

        Parameters:
        - data: pandas DataFrame object to be displayed in the table view.
        """
        QtCore.QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        """
        Get the number of rows in the model.

        Parameters:
        - parent: QModelIndex object representing the parent index.

        Returns:
        - The number of rows in the model.
        """
        return len(self._data.index)

    def columnCount(self, parnet=None):
        """
        Get the number of columns in the model.

        Parameters:
        - parent: QModelIndex object representing the parent index.

        Returns:
        - The number of columns in the model.
        """
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """
        Get the data for a specific index and role.

        Parameters:
        - index: QModelIndex object representing the index of the data.
        - role: Role of the data to be retrieved.

        Returns:
        - The data for the specified index and role.
        """
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
            elif role == QtCore.Qt.BackgroundRole:
                if index.row() % 2 != 0:  # Change the background color of every even row
                    return QtGui.QColor(212,212,212)
                else:  # Change the background color of every odd row
                    return QtGui.QColor(229,229,229)
            elif role == QtCore.Qt.ForegroundRole:
                if index.row() % 2 != 0:  # Change the font color of every even row
                    return QtGui.QColor(63,63,63)
                else:  # Change the font color of every odd row
                    return QtGui.QColor(91,91,91)
        return None

    def headerData(self, col, orientation, role):
        """
        Get the header data for a specific column, orientation, and role.

        Parameters:
        - col: Column index.
        - orientation: Orientation of the header (Horizontal or Vertical).
        - role: Role of the header data to be retrieved.

        Returns:
        - The header data for the specified column, orientation, and role.
        """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None
    
    def sizeHintForColumn(self):
        """
        Get the size hint for a specific column.

        Returns:
        - The size hint for the column.
        """
        return 20000

class thread1_ocr_plc_message(QtCore.QThread):

    button_generate_case_visable = QtCore.pyqtSignal(bool)

    thread1_status = QtCore.pyqtSignal(bool)

    thread1_error_message = QtCore.pyqtSignal(object)
    
    def __init__(self):
        """
        Initializes the thread1_ocr_plc_message object.
        """
        super(thread1_ocr_plc_message, self).__init__()
        print('thread1 init sucess')
        self.isRunning = False
        self.plc_ip_address = None
        self.plc_connect_type = None
        self.thread_Mode = None
        self.serial_num = None 
        self.generate_case = False

    def run(self):
        """
        Executes the main logic of the program.
        This method is responsible for controlling the flow of the program based on the selected thread mode.
        If the thread mode is 3, it establishes a connection with a PLC and continuously reads and writes data to it.
        If the thread mode is 1, it generates cases based on certain conditions.
        """
        # Existing code...
        # update_ocr_sort_info_new_case()
        self.isRunning = True
        global df1_ocr_sort_info
        program_run_once = True
        #now = datetime.datetime.now()
        #image_capture_tm = now.strftime("%Y%m%d%H%M%S")
        if self.thread_Mode == 3:
            try:
                _plc_ocr = plc.plc_connect(self.plc_ip_address,self.plc_connect_type)
                plc.write_bool(_plc_ocr, 1, 2, 1)
                plc_connect_success = True
            except Exception as e:
                self.thread1_error_message.emit(e)
                self.isRunning = False
                plc_connect_success = False

        

        self.thread1_status.emit(self.isRunning)


           
        if self.thread_Mode == 3 and plc_connect_success == True:
                
            while self.isRunning:

                time.sleep(0.001)
                
                try:

                    if plc.read_bool(_plc_ocr,1,3) and not plc.read_bool(_plc_ocr,1,4):

                        sensor_on_tm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]

                        new_row = pd.Series({'serial_num': self.serial_num, 'sensor_on_tm': sensor_on_tm}) 

                        df1_ocr_sort_info = pd.concat([df1_ocr_sort_info, new_row.to_frame().T], ignore_index=True)     

                                          

                        plc.write_bool(_plc_ocr, 1, 4, 1)

                        #print(df1_ocr_sort_info)

                    elif not plc.read_bool(_plc_ocr, 1, 3) and plc.read_bool(_plc_ocr, 1, 4):

                        plc.write_bool(_plc_ocr, 1, 4, 0)
                    
                    if plc.read_bool(_plc_ocr, 1, 1) and not plc.read_bool(_plc_ocr, 1, 2) and len(df1_ocr_sort_info) > self.serial_num:

                        sensor_off_tm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]

                        df1_ocr_sort_info.loc[self.serial_num,'sensor_off_tm'] = sensor_off_tm

                        self.serial_num += 1 
                        
                        plc.write_bool(_plc_ocr, 1, 2, 1)

                        print(df1_ocr_sort_info)
                            
                        # new_case_info.start()
                    elif not plc.read_bool(_plc_ocr, 1, 1) and plc.read_bool(_plc_ocr, 1, 2):

                        plc.write_bool(_plc_ocr, 1, 2, 0)

                        program_run_once = True

                        
                    
                except Exception as e:
                    
                    e = 'Thread1 Stopped' + str(e)
                    self.thread1_error_message.emit(e)
                    print(traceback.print_exc())
                  
                    plc_connect_success = False
                    break
            
        if self.thread_Mode == 1:
            
            while self.isRunning:

                time.sleep(0.001)

                self.button_generate_case_visable.emit(True)

                if self.generate_case:

                    sensor_on_tm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]

                    new_row = pd.Series({'serial_num': self.serial_num, 'sensor_on_tm': sensor_on_tm}) 

                    df1_ocr_sort_info = pd.concat([df1_ocr_sort_info, new_row.to_frame().T], ignore_index=True)     

                    

                    self.generate_case = False
                
                if len(df1_ocr_sort_info) > self.serial_num and \
                 (datetime.datetime.now() - datetime.datetime.strptime(df1_ocr_sort_info.loc[self.serial_num,'sensor_on_tm'],"%Y-%m-%d %H:%M:%S:%f")).microseconds > random.randint(300000,600000) :
                    
                                         
                    sensor_off_tm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]

                    df1_ocr_sort_info.loc[self.serial_num,'sensor_off_tm'] = sensor_off_tm

                    self.serial_num += 1 
                      

        if self.thread_Mode!= 1 and plc_connect_success == True:

            plc.plc_con_close(_plc_ocr)
        
        if self.thread_Mode == 1 :
            self.button_generate_case_visable.emit(False)

        self.isRunning = False

        self.thread1_status.emit(self.isRunning)
    
    def stop(self):
        """
        Stops the execution of the program.
        """
        self.isRunning = False

class thread2_camera_capture(QtCore.QThread):

        new_image_name = QtCore.pyqtSignal(str)

        update_df1_ocr_sort_info = QtCore.pyqtSignal(object)

        thread2_error_message = QtCore.pyqtSignal(object)

        thread2_status = QtCore.pyqtSignal(bool)
       
        def __init__(self):

            super(thread2_camera_capture, self).__init__()

            print('thread2_camera_capture init sucess')

            self.camera = None

            self.image_capture_id = None

            self.thread_Mode = None
                   
        def run(self):

            global df1_ocr_sort_info

            self.image_capture_id = 0

            self.isRunning = True

            self.thread2_status.emit(self.isRunning)

            camera_connect_success = False
            

            if self.thread_Mode == 3:

                try:
                   
                    _camera = camera.camera_connect(self.camera)

                    camera_connect_success = True

                except Exception as e:

                    self.thread2_error_message.emit(e)

                    self.isRunning = False

                    camera_connect_success = False

                while self.isRunning:
                   
                    time.sleep(0.001)
                    
                    try:

                        if df1_ocr_sort_info.shape[0] > self.image_capture_id and not pd.isna(df1_ocr_sort_info.loc[self.image_capture_id, 'sensor_off_tm']):
                                                     
                            sensor_off_tm = df1_ocr_sort_info.loc[self.image_capture_id, 'sensor_off_tm']

                            sensor_off_time = datetime.datetime.strptime(sensor_off_tm, '%Y-%m-%d %H:%M:%S:%f')
          
                            if (datetime.datetime.now() - sensor_off_time).microseconds >= 700000:

                                thread2_start_time = datetime.datetime.now()

                                '''
                                1. ´¥·¢Ïà»úÅÄÕÕ
                                '''
                                image, teat = camera.camera_grap_image(self.camera)

                                '''
                                2. ´æÍ¼/media/psic/PortableSSD/model_final.pth
                                '''
                                image_capture_tm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]
                                # save_tm = datetime.datetime.now().strftime("%Y%m%d %H%M%S%f")[:-3]

                                #df1_ocr_sort_info.at[self.image_capture_id,'img']= image
                               
                                cv2.imwrite('pic/pic_camera/' + image_capture_tm + '.jpeg', image)

                                df1_ocr_sort_info.loc[self.image_capture_id,'image_capture_tm'] = image_capture_tm

                                new_image_name = image_capture_tm + '.jpeg'

                                self.new_image_name.emit(new_image_name)

                                self.update_df1_ocr_sort_info.emit(df1_ocr_sort_info)

                                #print(df1_ocr_sort_info)

                                self.image_capture_id += 1   

                                
                                
                    except Exception as e:
                        print(traceback.print_exc())

                        self.thread2_error_message.emit(e)

                        self.isRunning = False
           
            if self.thread_Mode == 1:

                global df2_fpc_batch_summary

                while self.isRunning:

                    time.sleep(0.001)

                    try:

                        now = datetime.datetime.now()

                        if df1_ocr_sort_info.shape[0] > self.image_capture_id and not pd.isna(df1_ocr_sort_info.loc[self.ocr_ai_thread_id, 'sensor_off_tm']):

                            sensor_off_tm = df1_ocr_sort_info.loc[self.ocr_ai_thread_id, 'sensor_off_tm']

                            sensor_off_time = datetime.datetime.strptime(sensor_off_tm, '%Y-%m-%d %H:%M:%S:%f')

                            if (datetime.datetime.now() - sensor_off_time).microseconds >= 750000:

                                random_fpc_batch = df2_fpc_batch_summary.loc[random.randint(0,df2_fpc_batch_summary.shape[0]-1)]['fpc_batch']
                                
                                time.sleep(random.random())

                                ocr_finish_tm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]

                                df1_ocr_sort_info.loc[self.ocr_ai_thread_id, 'ocr_finish_tm'] = ocr_finish_tm                           

                                df1_ocr_sort_info.loc[self.ocr_ai_thread_id, 'fpc_batch'] = random_fpc_batch

                                self.update_df1_ocr_sort_info.emit(df1_ocr_sort_info)
                                
                                self.ocr_ai_thread_id += 1
                    except Exception as e:

                        print(traceback.print_exc())

                        self.thread2_error_message.emit(e)

                        self.isRunning = False

            self.isRunning = False

            self.thread2_status.emit(self.isRunning)

            if camera_connect_success == True:
                ocr_finish_tm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]

        def stop(self):

            self.isRunning = False                   

class thread3_ocr_ai_thread(QtCore.QThread):

        update_df1_ocr_sort_info = QtCore.pyqtSignal(object)

        ocr_result = QtCore.pyqtSignal(object)

        image_ocr_result = QtCore.pyqtSignal(str)

        thread2_error_message = QtCore.pyqtSignal(object)

        thread3_status = QtCore.pyqtSignal(bool)
       
        def __init__(self):

            super(thread3_ocr_ai_thread, self).__init__()

            print('thread3 init sucess')

            self.predictor = None

            self.reader = None

            self.ocr_ai_thread_id = None

            self.thread_Mode = None
                   
        def run(self):

            global df1_ocr_sort_info

            global thread3_ocr_ai_thread_id 

            # self.ocr_ai_thread_id = thread3_ocr_ai_thread_id

            self.ocr_ai_thread_id = 0

            self.isRunning = True

            self.thread3_status.emit(self.isRunning)

            if self.thread_Mode == 3:

                while self.isRunning:
                   
                    time.sleep(0.001)
                    
                    try:

                        if df1_ocr_sort_info.shape[0] > self.ocr_ai_thread_id and not pd.isna(df1_ocr_sort_info.loc[self.ocr_ai_thread_id, 'image_capture_tm']):

                            image_name = df1_ocr_sort_info.loc[self.ocr_ai_thread_id, 'image_capture_tm']

                            img = cv2.imread('pic/pic_camera/' + image_name + '.jpeg')

                            ocr_result = ocr_ai.infer_image_phase1aphase2(self.predictor, self.reader, img, image_name+'.jpeg')

                            ocr_finish_tm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]
                                
                            ocr_fuzzy_match = fuzzy_match(ocr_result[0], ocr_result[1], 0.9)

                            ocr_result_str = '' 

                            for item in ocr_result:

                                for str in item:

                                    ocr_result_str = ocr_result_str +'_' + str
                                    
                            df1_ocr_sort_info.loc[self.ocr_ai_thread_id, 'ocr_result'] = ocr_result_str
                            
                            df1_ocr_sort_info.loc[self.ocr_ai_thread_id, 'ocr_finish_tm'] = ocr_finish_tm                             

                            df1_ocr_sort_info.loc[self.ocr_ai_thread_id, 'fpc_batch'] = ocr_fuzzy_match

                            df1_ocr_sort_info.loc[self.ocr_ai_thread_id, 'img'] = None

                            self.update_df1_ocr_sort_info.emit(df1_ocr_sort_info)

                            # self.image_ocr_result.emit(image_name)

                            self.ocr_ai_thread_id += 1
                                                                          
                    except Exception as e:
                        
                        print(traceback.print_exc())

                        self.thread2_error_message.emit(e)

                        self.isRunning = False
           
            if self.thread_Mode == 1:

                global df2_fpc_batch_summary

                while self.isRunning:

                    time.sleep(0.001)

                    try:

                        now = datetime.datetime.now()

                        if df1_ocr_sort_info.shape[0] > self.ocr_ai_thread_id and not pd.isna(df1_ocr_sort_info.loc[self.ocr_ai_thread_id, 'sensor_off_tm']):

                            sensor_off_tm = df1_ocr_sort_info.loc[self.ocr_ai_thread_id, 'sensor_off_tm']

                            sensor_off_time = datetime.datetime.strptime(sensor_off_tm, '%Y-%m-%d %H:%M:%S:%f')

                            if (datetime.datetime.now() - sensor_off_time).microseconds >= 750000:

                                random_fpc_batch = df2_fpc_batch_summary.loc[random.randint(0,df2_fpc_batch_summary.shape[0]-1)]['fpc_batch']
                                
                                time.sleep(random.random())

                                ocr_finish_tm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]

                                df1_ocr_sort_info.loc[self.ocr_ai_thread_id, 'ocr_finish_tm'] = ocr_finish_tm                           

                                df1_ocr_sort_info.loc[self.ocr_ai_thread_id, 'fpc_batch'] = random_fpc_batch

                                self.update_df1_ocr_sort_info.emit(df1_ocr_sort_info)
                                
                                self.ocr_ai_thread_id += 1
                    except Exception as e:

                        print(traceback.print_exc())

                        self.thread2_error_message.emit(e)

                        self.isRunning = False

            self.isRunning = False

            self.thread3_status.emit(self.isRunning)

        def stop(self):

            self.isRunning = False                   

class thread4_calculate_sorter_output(QtCore.QThread):

    def __init__(self):
        super(thread4_calculate_sorter_output, self).__init__()
        print('thread4 init sucess')

    def run(self):
        global df1_ocr_sort_info,df2_fpc_batch_summary,df3_sorter_output_status

        while True:
            time.sleep(0.001)
            calculate_sorter_output(df1_ocr_sort_info,df2_fpc_batch_summary,df3_sorter_output_status)

class thread5_intralox_plc_message(QtCore.QThread):

    df3_update = QtCore.pyqtSignal(object)
    
    def __init__(self):
        super(thread5_intralox_plc_message, self).__init__()
        
        
        print('thread5 init sucess')

    def get_plc_source(self,plc):
        self.plc = plc   
    
    def run(self):
        """
        This method runs the main logic of the program.
        It communicates with the intralox PLC and updates the status of the sorting process.

        Args:
            None

        Returns:
            None
        """
        global df1_ocr_sort_info, df3_sorter_output_status
        global thread4_case_counter
        thread4_case_counter = 0
        thread4_allocation_num = 0
        intralox_init_serial_num = 0
        intralox_1_OnChute_serial_num = 0
        intralox_2_OnChute_serial_num = 0
        intralox_3_OnChute_serial_num = 0
        intralox_4_OnChute_serial_num = 0
        intralox_5_OnChute_serial_num = 0
        intralox_6_OnChute_serial_num = 0
        intralox_7_OnChute_serial_num = 0
        
        intralox_plc =self.plc
        '''
        intralox plc address configure
        '''
        plc_db_address_intralox_recive = 100
        plc_address_offset_REC_SYSTEM = 0
        plc_address_offset_REC_ID = 2
        plc_address_offset_REC_Destination = 6
        plc_address_offset_REC_ID_Destination = 10

        plc_db_address_intralox_send = 101

        plc_address_offset_SEND_ID_PE = 0
        plc_address_offset_Sorter_ID_OnChute_1 = 4  
        plc_address_offset_Sorter_ID_OnChute_2 = 8  
        plc_address_offset_Sorter_ID_OnChute_3 = 12
        plc_address_offset_Sorter_ID_OnChute_4 = 16
        plc_address_offset_Sorter_ID_OnChute_5 = 20
        plc_address_offset_Sorter_ID_OnChute_6 = 24
        plc_address_offset_Sorter_ID_OnChute_7 = 28
        plc_address_offset_Sorter_ID_End       = 32
        plc_address_offset_SEND_PackageStatus  = 36
        plc_address_offset_SEND_SorterStatus   = 38
        plc_address_offset_SEND_SorterFaulty   = 40
        plc_address_offset_REC_LaneOpen        = 42

        self.df3_update.emit(df3_sorter_output_status)

        while True:
            
            #try:
                #now = datetime.datetime.now()
            '''
            task 1:
            ÐÂÏä×Óµ½Ê±
            Ð´ÐÂµÄÁ÷Ë®ºÅÖÁintralox plc 
            '''
            if df1_ocr_sort_info.shape[0] > thread4_case_counter:

                serial_num = df1_ocr_sort_info.loc[thread4_case_counter, 'serial_num']

                plc.write_db_dint(intralox_plc, plc_db_address_intralox_recive, plc_address_offset_REC_ID, serial_num)
                thread4_case_counter += 1
            
            '''
            task 2:
            ÓÐÐÂµÄ·ÖÅä¿ÚÊ±
            ½«ÐÂÊÕµ½µÄÈË·ÖÅä¿ÚÐÅÏ¢ºÍÁ÷Ë®ºÅÐ´ÖÁintralox plc 
            '''
            if df1_ocr_sort_info.shape[0] > thread4_allocation_num:
               
               if not pd.isna(df1_ocr_sort_info.loc[thread4_allocation_num, 'sorter_output']):
                   
                   serila_num_allocation = int(df1_ocr_sort_info.loc[thread4_allocation_num, 'serial_num'])

                   sorter_output_allocation = int(df1_ocr_sort_info.loc[thread4_allocation_num, 'sorter_output'])
                   
                   plc.write_db_dint(intralox_plc, plc_db_address_intralox_recive, plc_address_offset_REC_Destination, sorter_output_allocation)

                   plc.write_db_dint(intralox_plc, plc_db_address_intralox_recive, plc_address_offset_REC_ID_Destination, serila_num_allocation)
                   

                   thread4_allocation_num += 1

            '''
            task 3:
            ´Óintralox plc¶ÁÈ¡µ½ÐÂµ½µÄÏä×ÓÐòÁÐºÅÊ±
            ½« ÏµÍ³Ê±¼ä Ð´ÈëÖÁ df1_ocr_sort_info ÖÐµÄÐÐÊý¾Ý = ÐÂÏä×ÓµÄÐòºÅºÅÖÐµÄ sorter_enter_tm       ÁÐÖÐ
            ½« True   Ð´ÈëÖÁ df1_ocr_sort_info ÖÐµÄÐÐÊý¾Ý = ÐÂÏä×ÓµÄÐòºÅºÅÖÐµÄ sorter_success_enter  ÁÐÖÐ
            '''
            if  intralox_init_serial_num != plc.read_db_dint(intralox_plc,plc_db_address_intralox_send, plc_address_offset_SEND_ID_PE):

                sorter_enter_tm = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

                intralox_new_serial_num = plc.read_db_dint(intralox_plc,plc_db_address_intralox_send, plc_address_offset_SEND_ID_PE)

                df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_new_serial_num, 'sorter_enter_tm'] = sorter_enter_tm

                df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_new_serial_num, 'sorter_success_enter'] = True

                intralox_init_serial_num = intralox_new_serial_num

            '''
            task 4:
            ´Óintralox plc¶ÁÈ¡µ½1#ÕýÔÚ·Ö¼ðµÄÏä×ÓÐòÁÐºÅ
            Èç¹ûÕýÔÚ·Ö¼ðµÄÏä×ÓÐòÁÐºÅ ²»µÈÓÚ ÉÏÒ»¸ö·Ö¼ðµÄÏä×ÓÐòÁÐºÅ
            ²éÕÒÏä×ÓÐòÁÐºÅ¶ÔÓ¦ÔÚ df1_ocr_sort_info ÖÐµÄ sorter_output ÊÇ·ñÊÇ1ºÅ¿Ú£¬Èç¹ûÊÇ 
            Ôò½«¸ÃÏä×ÓÐòÁÐºÅ¶ÔÔÚ df1_ocr_sort_info ÖÐµÄ success_sort Ð´Îª True
            '''
            if intralox_1_OnChute_serial_num != plc.read_db_dint(intralox_plc, plc_db_address_intralox_send, plc_address_offset_Sorter_ID_OnChute_1):

                intralox_1_OnChute_serial_num = plc.read_db_dint(intralox_plc, plc_db_address_intralox_send, plc_address_offset_Sorter_ID_OnChute_1)

                if not (df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_1_OnChute_serial_num]).empty:
                
                    try:

                        if df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_1_OnChute_serial_num] .iloc[0]['sorter_output'] == '1' :

                            df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_1_OnChute_serial_num, 'success_sort'] = True

                        else:
                            # wait to do
                            # Èç¹û²»Æ¥ÅäÊÇ·ñÍ£Ö¹·Ö¼ð£¿

                            df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_1_OnChute_serial_num, 'success_sort'] = True

                            # logging.debug('serial_num:----'+ intralox_1_OnChute_serial_num + '----´íÎó·ÖÖÁ1#¿Ú')

                            pass

                    except Exception:

                        #print(traceback.print_exc())

                        logging.debug(traceback.print_exc())

            '''
            task 5:
            ´Óintralox plc¶ÁÈ¡µ½2#ÕýÔÚ·Ö¼ðµÄÏä×ÓÐòÁÐºÅ
            Èç¹ûÕýÔÚ·Ö¼ðµÄÏä×ÓÐòÁÐºÅ ²»µÈÓÚ ÉÏÒ»¸ö·Ö¼ðµÄÏä×ÓÐòÁÐºÅ
            ²éÕÒÏä×ÓÐòÁÐºÅ¶ÔÓ¦ÔÚ df1_ocr_sort_info ÖÐµÄ sorter_output ÊÇ·ñÊÇ2ºÅ¿Ú£¬Èç¹ûÊÇ 
            Ôò½«¸ÃÏä×ÓÐòÁÐºÅ¶ÔÔÚ df1_ocr_sort_info ÖÐµÄ success_sort Ð´Îª True
            '''
            if intralox_2_OnChute_serial_num != plc.read_db_dint(intralox_plc, plc_db_address_intralox_send, plc_address_offset_Sorter_ID_OnChute_2):

                intralox_2_OnChute_serial_num = plc.read_db_dint(intralox_plc, plc_db_address_intralox_send, plc_address_offset_Sorter_ID_OnChute_2)

                if not df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_2_OnChute_serial_num].empty:

                    try:

                        if df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_2_OnChute_serial_num] .iloc[0][ 'sorter_output'] == '2' :

                            df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_2_OnChute_serial_num, 'success_sort'] = True  

                        else:
                            # wait to do
                            # Èç¹û²»Æ¥ÅäÊÇ·ñÍ£Ö¹·Ö¼ð£¿

                            df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_2_OnChute_serial_num, 'success_sort'] = True

                            # logging.debug('serial_num:----'+ intralox_2_OnChute_serial_num + '----´íÎó·ÖÖÁ2#¿Ú')

                            pass

                    except Exception:

                        #print(traceback.print_exc())

                        logging.debug(traceback.print_exc())

                                       

            '''
            task 6:
            ´Óintralox plc¶ÁÈ¡µ½3#ÕýÔÚ·Ö¼ðµÄÏä×ÓÐòÁÐºÅ
            Èç¹ûÕýÔÚ·Ö¼ðµÄÏä×ÓÐòÁÐºÅ ²»µÈÓÚ ÉÏÒ»¸ö·Ö¼ðµÄÏä×ÓÐòÁÐºÅ
            ²éÕÒÏä×ÓÐòÁÐºÅ¶ÔÓ¦ÔÚ df1_ocr_sort_info ÖÐµÄ sorter_output ÊÇ·ñÊÇ3ºÅ¿Ú£¬Èç¹ûÊÇ 
            Ôò½«¸ÃÏä×ÓÐòÁÐºÅ¶ÔÔÚ df1_ocr_sort_info ÖÐµÄ success_sort Ð´Îª True
            '''
            if intralox_3_OnChute_serial_num != plc.read_db_dint(intralox_plc, plc_db_address_intralox_send, plc_address_offset_Sorter_ID_OnChute_3):

                intralox_3_OnChute_serial_num = plc.read_db_dint(intralox_plc, plc_db_address_intralox_send, plc_address_offset_Sorter_ID_OnChute_3)

                if not df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_3_OnChute_serial_num].empty:

                    try:


                        if df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_3_OnChute_serial_num] .iloc[0][ 'sorter_output'] == '3' :

                            df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_3_OnChute_serial_num, 'success_sort'] = True  

                        else:
                            # wait to do
                            # Èç¹û²»Æ¥ÅäÊÇ·ñÍ£Ö¹·Ö¼ð£¿

                            df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_3_OnChute_serial_num, 'success_sort'] = True

                            # logging.debug('serial_num:----'+ intralox_3_OnChute_serial_num + '----´íÎó·ÖÖÁ3#¿Ú')

                            pass        

                    except Exception:

                        #print(traceback.print_exc())

                        logging.debug(traceback.print_exc())

            '''
            task 7:
            ´Óintralox plc¶ÁÈ¡µ½4#ÕýÔÚ·Ö¼ðµÄÏä×ÓÐòÁÐºÅ
            Èç¹ûÕýÔÚ·Ö¼ðµÄÏä×ÓÐòÁÐºÅ ²»µÈÓÚ ÉÏÒ»¸ö·Ö¼ðµÄÏä×ÓÐòÁÐºÅ
            ²éÕÒÏä×ÓÐòÁÐºÅ¶ÔÓ¦ÔÚ df1_ocr_sort_info ÖÐµÄ sorter_output ÊÇ·ñÊÇ4ºÅ¿Ú£¬Èç¹ûÊÇ 
            Ôò½«¸ÃÏä×ÓÐòÁÐºÅ¶ÔÔÚ df1_ocr_sort_info ÖÐµÄ success_sort Ð´Îª True
            '''
            if intralox_4_OnChute_serial_num != plc.read_db_dint(intralox_plc, plc_db_address_intralox_send, plc_address_offset_Sorter_ID_OnChute_4):

                intralox_4_OnChute_serial_num = plc.read_db_dint(intralox_plc, plc_db_address_intralox_send, plc_address_offset_Sorter_ID_OnChute_4)

                if not df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_4_OnChute_serial_num].empty:

                    try:


                        if df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_4_OnChute_serial_num] .iloc[0][ 'sorter_output'] == '4' :

                            df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_4_OnChute_serial_num, 'success_sort'] = True  

                        else:
                            # wait to do
                            # Èç¹û²»Æ¥ÅäÊÇ·ñÍ£Ö¹·Ö¼ð£¿

                            df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_4_OnChute_serial_num, 'success_sort'] = True

                            # logging.debug('serial_num:----'+ intralox_4_OnChute_serial_num + '----´íÎó·ÖÖÁ4#¿Ú')

                            pass      
                    
                    except Exception:

                        #print(traceback.print_exc())

                        logging.debug(traceback.print_exc())

            '''
            task 8:
            ´Óintralox plc¶ÁÈ¡µ½5#ÕýÔÚ·Ö¼ðµÄÏä×ÓÐòÁÐºÅ
            Èç¹ûÕýÔÚ·Ö¼ðµÄÏä×ÓÐòÁÐºÅ ²»µÈÓÚ ÉÏÒ»¸ö·Ö¼ðµÄÏä×ÓÐòÁÐºÅ
            ²éÕÒÏä×ÓÐòÁÐºÅ¶ÔÓ¦ÔÚ df1_ocr_sort_info ÖÐµÄ sorter_output ÊÇ·ñÊÇ5ºÅ¿Ú£¬Èç¹ûÊÇ 
            Ôò½«¸ÃÏä×ÓÐòÁÐºÅ¶ÔÔÚ df1_ocr_sort_info ÖÐµÄ success_sort Ð´Îª True
            '''
            if intralox_5_OnChute_serial_num != plc.read_db_dint(intralox_plc, plc_db_address_intralox_send, plc_address_offset_Sorter_ID_OnChute_5):

                intralox_5_OnChute_serial_num = plc.read_db_dint(intralox_plc, plc_db_address_intralox_send, plc_address_offset_Sorter_ID_OnChute_5)

                if not df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_5_OnChute_serial_num].empty:

                    try:

                        if df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_5_OnChute_serial_num] .iloc[0][ 'sorter_output'] == '5' :

                            df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_5_OnChute_serial_num, 'success_sort'] = True  

                        else:
                            # wait to do
                            # Èç¹û²»Æ¥ÅäÊÇ·ñÍ£Ö¹·Ö¼ð£¿

                            df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_5_OnChute_serial_num, 'success_sort'] = True

                            # logging.debug('serial_num:----'+ intralox_5_OnChute_serial_num + '----´íÎó·ÖÖÁ5#¿Ú')

                            pass       
                    
                    except Exception:

                        #print(traceback.print_exc())

                        logging.debug(traceback.print_exc())

            '''
            task 9:
            ´Óintralox plc¶ÁÈ¡µ½6#ÕýÔÚ·Ö¼ðµÄÏä×ÓÐòÁÐºÅ
            Èç¹ûÕýÔÚ·Ö¼ðµÄÏä×ÓÐòÁÐºÅ ²»µÈÓÚ ÉÏÒ»¸ö·Ö¼ðµÄÏä×ÓÐòÁÐºÅ
            ²éÕÒÏä×ÓÐòÁÐºÅ¶ÔÓ¦ÔÚ df1_ocr_sort_info ÖÐµÄ sorter_output ÊÇ·ñÊÇ6ºÅ¿Ú£¬Èç¹ûÊÇ 
            Ôò½«¸ÃÏä×ÓÐòÁÐºÅ¶ÔÔÚ df1_ocr_sort_info ÖÐµÄ success_sort Ð´Îª True
            '''
            if intralox_6_OnChute_serial_num != plc.read_db_dint(intralox_plc, plc_db_address_intralox_send, plc_address_offset_Sorter_ID_OnChute_6):

                intralox_6_OnChute_serial_num = plc.read_db_dint(intralox_plc, plc_db_address_intralox_send, plc_address_offset_Sorter_ID_OnChute_6)

                if not df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_6_OnChute_serial_num].empty:

                    try:


                        if df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_6_OnChute_serial_num] .iloc[0][ 'sorter_output'] == '6' :

                            df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_6_OnChute_serial_num, 'success_sort'] = True  

                        else:
                            # wait to do
                            # Èç¹û²»Æ¥ÅäÊÇ·ñÍ£Ö¹·Ö¼ð£¿

                            df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_6_OnChute_serial_num, 'success_sort'] = True

                            # logging.debug('serial_num:----'+ intralox_6_OnChute_serial_num + '----´íÎó·ÖÖÁ6#¿Ú')

                            pass  
                    
                    except Exception:

                        #print(traceback.print_exc())

                        logging.debug(traceback.print_exc())
            
            '''
            task 10:
            ´Óintralox plc¶ÁÈ¡µ½7#ÕýÔÚ·Ö¼ðµÄÏä×ÓÐòÁÐºÅ
            Èç¹ûÕýÔÚ·Ö¼ðµÄÏä×ÓÐòÁÐºÅ ²»µÈÓÚ ÉÏÒ»¸ö·Ö¼ðµÄÏä×ÓÐòÁÐºÅ
            ²éÕÒÏä×ÓÐòÁÐºÅ¶ÔÓ¦ÔÚ df1_ocr_sort_info ÖÐµÄ sorter_output ÊÇ·ñÊÇ7ºÅ¿Ú£¬Èç¹ûÊÇ 
            Ôò½«¸ÃÏä×ÓÐòÁÐºÅ¶ÔÔÚ df1_ocr_sort_info ÖÐµÄ success_sort Ð´Îª True
            '''
            if intralox_7_OnChute_serial_num != plc.read_db_dint(intralox_plc, plc_db_address_intralox_send, plc_address_offset_Sorter_ID_OnChute_7):

                intralox_7_OnChute_serial_num = plc.read_db_dint(intralox_plc, plc_db_address_intralox_send, plc_address_offset_Sorter_ID_OnChute_7)

                if not df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_7_OnChute_serial_num].empty:
                
                    try:

                        if df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_7_OnChute_serial_num] .iloc[0][ 'sorter_output'] == '7' :

                            df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_7_OnChute_serial_num, 'success_sort'] = True  

                        else:
                            # wait to do
                            # Èç¹û²»Æ¥ÅäÊÇ·ñÍ£Ö¹·Ö¼ð£¿

                            df1_ocr_sort_info.loc[df1_ocr_sort_info['serial_num'] == intralox_7_OnChute_serial_num, 'success_sort'] = True

                            # logging.debug('serial_num:----'+ intralox_7_OnChute_serial_num + '----´íÎó·ÖÖÁ7#¿Ú')

                            pass    

                    except Exception:

                        #print(traceback.print_exc())

                        logging.debug(traceback.print_exc())                      
 
            '''
            task 11:
            ´Óintralox plc¶ÁÈ¡ 1# ·Ö¼ð¿Ú×´Ì¬
            Ð´Èëdf3_sorter_output_status ÖÐ 'sorter_output' == 1 ÖÐµÄ physical_available ÖÐ         
            ´Óintralox plc¶ÁÈ¡ 2# ·Ö¼ð¿Ú×´Ì¬
            Ð´Èëdf3_sorter_output_status ÖÐ 'sorter_output' == 2 ÖÐµÄ physical_available ÖÐ      
            ´Óintralox plc¶ÁÈ¡ 3# ·Ö¼ð¿Ú×´Ì¬
            Ð´Èëdf3_sorter_output_status ÖÐ 'sorter_output' == 3 ÖÐµÄ physical_available ÖÐ 
            ´Óintralox plc¶ÁÈ¡ 4# ·Ö¼ð¿Ú×´Ì¬
            Ð´Èëdf3_sorter_output_status ÖÐ 'sorter_output' == 3 ÖÐµÄ physical_available ÖÐ 
            ´Óintralox plc¶ÁÈ¡ 5# ·Ö¼ð¿Ú×´Ì¬
            Ð´Èëdf3_sorter_output_status ÖÐ 'sorter_output' == 3 ÖÐµÄ physical_available ÖÐ 
            ´Óintralox plc¶ÁÈ¡ 6# ·Ö¼ð¿Ú×´Ì¬
            Ð´Èëdf3_sorter_output_status ÖÐ 'sorter_output' == 3 ÖÐµÄ physical_available ÖÐ 
            ´Óintralox plc¶ÁÈ¡ 7# ·Ö¼ð¿Ú×´Ì¬
            Ð´Èëdf3_sorter_output_status ÖÐ 'sorter_output' == 3 ÖÐµÄ physical_available ÖÐ 
            ''' 

            # 1#·Ö¼ð¿ÚÎïÀí×´Ì¬¸üÐÂ

            if pd.isna(df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '1'].iloc[0]['physical_available']):

                df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '1','physical_available'] = \
                plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,1) 

                self.df3_update.emit(df3_sorter_output_status)

            elif (df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '1'].iloc[0]['physical_available']) != \
                (plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,1)) :

                df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '1','physical_available'] = \
                plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,1) 

                self.df3_update.emit(df3_sorter_output_status)

            # 2#·Ö¼ð¿ÚÎïÀí×´Ì¬¸üÐÂ

            if pd.isna(df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '2'].iloc[0]['physical_available']):

                df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '2','physical_available'] = \
                plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,2) 
        
                self.df3_update.emit(df3_sorter_output_status)

            elif (df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '2'].iloc[0]['physical_available']) != \
                (plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,2)) :

                df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '2','physical_available'] = \
                plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,2) 

                self.df3_update.emit(df3_sorter_output_status)                
             
             # 3#·Ö¼ð¿ÚÎïÀí×´Ì¬¸üÐÂ

            if pd.isna(df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '3'].iloc[0]['physical_available']):

                df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '3','physical_available'] = \
                plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,3) 
        
                self.df3_update.emit(df3_sorter_output_status)

            elif (df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '3'].iloc[0]['physical_available']) != \
                (plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,3)) :

                df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '3','physical_available'] = \
                plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,3) 

                self.df3_update.emit(df3_sorter_output_status)            

              # 4#·Ö¼ð¿ÚÎïÀí×´Ì¬¸üÐÂ

            if pd.isna(df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '4'].iloc[0]['physical_available']):

                df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '4','physical_available'] = \
                plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,4) 
        
                self.df3_update.emit(df3_sorter_output_status)

            elif (df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '4'].iloc[0]['physical_available']) != \
                (plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,4)) :

                df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '4','physical_available'] = \
                plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,4) 

                self.df3_update.emit(df3_sorter_output_status)  

              # 5#·Ö¼ð¿ÚÎïÀí×´Ì¬¸üÐÂ

            if pd.isna(df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '5'].iloc[0]['physical_available']):

                df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '5','physical_available'] = \
                plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,5) 
        
                self.df3_update.emit(df3_sorter_output_status)

            elif (df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '5'].iloc[0]['physical_available']) != \
                (plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,4)) :


                df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '5','physical_available'] = \
                plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,5) 

                self.df3_update.emit(df3_sorter_output_status)  

              # 6#·Ö¼ð¿ÚÎïÀí×´Ì¬¸üÐÂ

            if pd.isna(df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '6'].iloc[0]['physical_available']):

                df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '6','physical_available'] = \
                plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,6) 
        
                self.df3_update.emit(df3_sorter_output_status)

            elif (df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '6'].iloc[0]['physical_available']) != \
                (plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,6)) :

                df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '6','physical_available'] = \
                plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,6) 

                self.df3_update.emit(df3_sorter_output_status)  

              # 7#·Ö¼ð¿ÚÎïÀí×´Ì¬¸üÐÂ

            if pd.isna(df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '7'].iloc[0]['physical_available']):

                df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '7','physical_available'] = \
                plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,7) 
        
                self.df3_update.emit(df3_sorter_output_status)

            elif (df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '7'].iloc[0]['physical_available']) != \
                (plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,7)) :

                df3_sorter_output_status.loc[df3_sorter_output_status['sorter_output'] == '7','physical_available'] = \
                plc.read_db_word_bool(intralox_plc,plc_db_address_intralox_send,plc_address_offset_REC_LaneOpen,7) 

                self.df3_update.emit(df3_sorter_output_status) 
            
            time.sleep(0.001)

class thread6_accumulated_cnt_and_sorter_release(QtCore.QThread):

    def __init__(self):
        super(thread6_accumulated_cnt_and_sorter_release, self).__init__()
        print('thread6 init sucess')
    
    def run(self):
        global df2_fpc_batch_summary,df3_sorter_output_status

        while True:
            time.sleep(0.001)
            accumulated_cnt_and_sorter_release(df2_fpc_batch_summary,df3_sorter_output_status)

class thread7_update_df2_df3(QtCore.QThread):

    df1_update = QtCore.pyqtSignal(object)

    df2_update = QtCore.pyqtSignal(object)

    df3_update = QtCore.pyqtSignal(object)

    def __init__(self):
        super(thread7_update_df2_df3, self).__init__()
        print('thread7 init sucess')

    def run(self):
        """
        This method runs a continuous loop that updates the dataframes df1_ocr_sort_info, df2_fpc_batch_summary, and df3_sorter_output_status.
        It emits signals to update the corresponding dataframes in the UI.
        """
        global df1_ocr_sort_info, df2_fpc_batch_summary, df3_sorter_output_status

        while True:
            time.sleep(2)

            self.df1_update.emit(df1_ocr_sort_info)
            self.df2_update.emit(df2_fpc_batch_summary)
            self.df3_update.emit(df3_sorter_output_status)

class StackedDemo(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super(StackedDemo, self).__init__()
        self.setupUi(self)  # ´´½¨´°Ìå¶ÔÏó
        self.init()

    def init(self):

        # Create a status bar
        self.statusBar = self.statusBar()

        # instantiate the threads           
        self.thread1 = thread1_ocr_plc_message()
        self.thread2 = thread2_camera_capture()
        self.thread3 = thread3_ocr_ai_thread()
        self.thread4 = thread4_calculate_sorter_output()
        self.thread5 = thread5_intralox_plc_message()
        self.thread6 = thread6_accumulated_cnt_and_sorter_release()
        self.thread7 = thread7_update_df2_df3()

        # Change the background color of the status bar and the font color
        self.statusBar.setStyleSheet("background-color: gray; color: white;")

        # Create a QVBoxLayout
        layout = QtWidgets.QVBoxLayout()

        # Create QLabel widgets
        self.label_1 = QtWidgets.QLabel()
        self.label_2 = QtWidgets.QLabel()

        # Add the QLabel widgets to the QVBoxLayout
        layout.addWidget(self.label_1)
        layout.addWidget(self.label_2)

        # Create a QWidget and set the QVBoxLayout as its layout
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        # Add the QWidget to the status bar
        self.statusBar.addWidget(widget)

        # Set the text of the QLabel widgets
        self.label_1.setText("Hello, World!")
        self.label_2.setText("Hello, World!")
        
        self.menubar.setVisible(True)

        self.statusbar.setVisible(True)
      
        self.button_login.clicked.connect(self.login)

        self.pushButton1.clicked.connect(self.belt_run)  

        self.pushButton2.clicked.connect(self.belt_stop)  

        self.pushButton3.clicked.connect(self.load_truck_info)

        self.main_page.triggered.connect(self.main_page_display)

        self.button_generate_case.clicked.connect(self.generate_case)

        self.button_save_df1.clicked.connect(self.save_df1)

        self.button_release_sorter.clicked.connect(self.manual_release_sorter)

        self.ocr_plc_configure.triggered.connect(self.ocr_plc_configure_display)

        self.button_phase1_select_mode_1.clicked.connect(self.phase1_select_model1)

        self.button_phase1_select_mode_2.clicked.connect(self.phase1_select_model2)

        self.button_phase1_select_mode_3.clicked.connect(self.phase1_select_model3)

        self.button_phase1_start.clicked.connect(self.phase1_start)

        self.button_phase1_stop.clicked.connect(self.phase1_stop)

        self.page4_button_phase2_select_mode_1.clicked.connect(self.phase2_select_model1)

        self.page4_button_phase2_select_mode_2.clicked.connect(self.phase2_select_model2)

        self.page4_button_phase2_select_mode_3.clicked.connect(self.phase2_select_model3)

        self.page4_button_phase2_start.clicked.connect(self.phase2_start)

        self.page4_button_phase2_stop.clicked.connect(self.phase2_stop)

        self.ai_ocr_configure.triggered.connect(self.page_ai_module_diplay)

        #display the ocr manual verify page function connect
        self.ocr_manual_verify.triggered.connect(self.page_ocr_manual_verify_display)   

        # init the thread1
        self.thread1.button_generate_case_visable.connect(self.set_button_generate_case_visable)

        self.thread1.thread1_status.connect(self.update_thread1_status)

        self.thread1.thread1_error_message.connect(self.thread_error_message_display)

        self.thread1_mode = None
        
        # init the thread2
        self.thread2_mode = None

        self.thread2.thread2_status.connect(self.update_thread2_status)

        self.thread2.thread2_error_message.connect(self.thread_error_message_display)

        self.intralox_plc_configure.triggered.connect(self.page_intralox_plc_configure_display)

        self.thread2.update_df1_ocr_sort_info.connect(self.update_df1_ocr_sort_info)

        self.thread2.new_image_name.connect(self.image_update)

        self.thread3.ocr_result.connect(self.ocr_result_update)

        self.thread3.image_ocr_result.connect(self.image_ocr_result_update)

        '''
        thread3 start
        '''
        self.thread3.start()
        self.thread4.start()

        """
        Á¬½Óintralox plc
        """
        intralox_plc_ip_address = "192.168.0.100"
        connect_type_intralox_plc = 2
        # intralox_plc = plc.plc_connect(intralox_plc_ip_address, connect_type_intralox_plc)

        '''
        thread5 start
        '''
        # self.thread5.get_plc_source(intralox_plc)
        # self.thread5.start()        
        self.thread5.df3_update.connect(self.update_df3_sorter_output_status)

        '''
        thread6 start
        '''
        self.thread6.start()

        '''
        thread7 start
        '''
        self.thread7.df2_update.connect(self.update_df3_sorter_output_status)
        self.thread7.df3_update.connect(self.update_df3_sorter_output_status)
        self.thread7.df1_update.connect(self.update_df1_ocr_sort_info)
        self.thread7.start()

    def login(self):

        if df_user_congfigure.loc[df_user_congfigure['user']==self.page_login_input_user_name.text()].empty:
            QtWidgets.QMessageBox.critical(None, "Error", "Please Input the Correct User Name")
        elif df_user_congfigure.loc[df_user_congfigure['user']==self.page_login_input_user_name.text()].iloc[0]['password'] != self.page_login_input_password.text() :
            QtWidgets.QMessageBox.critical(None, "Error", "The password isn't match the user name")
        else:
            self.stackedWidget.setCurrentIndex(1)
            self.menubar.setVisible(True)
            self.statusbar.setVisible(True)

    def save_df1(self):
        df1_ocr_sort_info.to_csv('./df1_result.csv', index=False)

    def phase1_select_model1(self):
       
        if self.thread1.isRunning == True:

            QtWidgets.QMessageBox.critical(None, "Error", "Please stop the Phase1")

        else:

            self.Q_label_text_phase1_status.setText("<font color = 'blue',>Phase1 Mode: Simualtion with out PLC</font>")

            self.thread1_mode = 1

    def phase1_select_model2(self):

        if self.thread1.isRunning == True:

            QtWidgets.QMessageBox.critical(None, "Error", "Please stop the Phase1")

        else:

            self.Q_label_text_phase1_status.setText("<font color = 'yellow',>Phase1 Mode: Simualtion with PLC</font>")

            self.thread1_mode = 2

    def phase1_select_model3(self):

        if self.thread1.isRunning == True:

            QtWidgets.QMessageBox.critical(None, "Error", "Please stop the Phase1")

        else:

            self.Q_label_text_phase1_status.setText("<font color = 'green',>Phase1 Mode: Production </font>")

            self.thread1_mode = 3

    def set_button_generate_case_visable(self,visable):

        self.button_generate_case.setVisible(visable)

    def generate_case(self):

        self.thread1.generate_case = True

    def update_thread1_status(self,_thread1_status):

        if _thread1_status == True:

            self.Q_label_text_7.setText("<font color = 'green',>Running</font>")
        
        else:

            self.Q_label_text_7.setText("<font color = 'red',>Stopped</font>")

    def phase1_start(self):

        """
        Á¬½ÓOCR PLC
        """
        if self.thread1_mode == None:
            QtWidgets.QMessageBox.critical(None, "Error", "Please select thread1 run Mode.")
        else:
            self.thread1.thread_Mode = self.thread1_mode
            
            if self.thread1_mode != 1 and \
                  (
                      (not re.match(r'\d+.\d+.\d+.\d+',self.line_edit_ocr_plc_address.text())) 
                      or (not re.match(r'\d+',self.line_edit_ocr_plc_address.text()))
                  ): 
                QtWidgets.QMessageBox.critical(None, "Error", "Please input the correct IP Address and correct connect type ")

            elif self.thread1_mode != 1 :    

                self.thread1.plc_connect_type = int(self.line_edit_ocr_plc_connect_type.text())

                self.thread1.plc_ip_address = self.line_edit_ocr_plc_address.text()
                '''
                thread1 start
                '''
            self.thread1.serial_num = 0
            self.thread1.start()        

    def phase1_stop(self):

        self.thread1.isRunning = False

    def phase2_select_model1(self):
       
        if self.thread2.isRunning == True:

            QtWidgets.QMessageBox.critical(None, "Error", "Please stop the Phase2")

        else:

            self.page4_phase2_status.setText("<font color = 'blue',>Phase1 Mode: Simualtion with out AI Model</font>")

            self.thread2_mode = 1

            self.thread3_mode = 1

    def phase2_select_model2(self):

        if self.thread2.isRunning == True:

            QtWidgets.QMessageBox.critical(None, "Error", "Please stop the Phase2")

        else:

            self.page4_phase2_status.setText("<font color = 'yellow',>Phase1 Mode: Simualtion with AI Model</font>")

            self.thread2_mode = 2

            self.thread3_mode = 2

    def phase2_select_model3(self):

        if self.thread2.isRunning == True:

            QtWidgets.QMessageBox.critical(None, "Error", "Please stop the Phase2")

        else:

            self.page4_phase2_status.setText("<font color = 'green',>Phase1 Mode: Production </font>")

            self.thread2_mode = 3

            self.thread3_mode = 3

    def update_thread2_status(self,_thread2_status):

        if _thread2_status == True:

            self.page4_text_6.setText("<font color = 'green',>Running</font>")
        
        else:

            self.page4_text_6.setText("<font color = 'red',>Stopped</font>")

    def phase2_start(self):

        """
        Á¬½ÓOCR PLC
        """
        if self.thread2_mode == None:
            QtWidgets.QMessageBox.critical(None, "Error", "Please select thread2 run Mode.")
        else:
            self.thread2.thread_Mode = self.thread2_mode

            self.thread3.thread_Mode = self.thread3_mode
  
            if self.thread2_mode == 1 :

                pass

                #QtWidgets.QMessageBox.critical(None, "Error", "Please input the correct IP Address and correct connect type ")

            elif self.thread2_mode == 3 :   

                self.thread3.predictor,self.thread3.reader = ocr_ai.load_predictor(str(self.page4_input_text_model_file_path.text()),
                                                                                   int(self.page4_input_text_Model_Batch_Size.text()),
                                                                                   [[int(x) for x in self.page4_input_text_Model_Anchor_Size.text().split(', ')]],
                                                                                   [[float(x) for x in self.page4_input_text_model_anchor_ratios.text().split(', ')]],                                                               
                                                                                   int(self.page4_input_text_ai_ocr_model_setting_num_classes.text()),
                                                                                   float(self.page4_input_text_ai_ocr_model_setting_accept_score.text())
                                                                                   )

                self.thread2.camera = camera.get_camera_source()
                '''
                thread2 start
                '''

            self.thread2.start()  

            self.thread3.start()

    def phase2_stop(self):

        self.thread2.isRunning = False

    def main_page_display(self):

        self.stackedWidget.setCurrentIndex(1)

    def ocr_plc_configure_display(self):

        self.stackedWidget.setCurrentIndex(2)
    
    def page_intralox_plc_configure_display(self):

        self.stackedWidget.setCurrentIndex(3)

    def page_ai_module_diplay(self):

        self.stackedWidget.setCurrentIndex(4)

    def update_df1_ocr_sort_info(self,df1):

        readonly_df = df1.copy(deep=True)
        # df1_ocr_sort_info = pd.DataFrame(columns=['serial_num', 'sensor_on_tm','image_capture_tm', 'ocr_finish_tm',

        #                                  'fpc_batch','ocr_result', 'sorter_output',

        #                                  'backup_output', 'sorter_enter_tm',

        #                                  'sorter_success_enter', 'success_sort'])

        readonly_df = readonly_df[['serial_num','sensor_off_tm','ocr_finish_tm','fpc_batch','ocr_result','sorter_output','success_sort']]

        if readonly_df.shape[0] >= 20:

            readonly_df = readonly_df.tail(20)
        
        model = pandasModel(readonly_df)
        self.tableView1.setModel(model)
        self.tableView1.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableView1.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)  

    def update_df2_fpc_batch_summary(self,df2):

        readonly_df = df2.copy(deep=True)  

        model = pandasModel(readonly_df)

        self.tableView.setModel(model)     
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)  

    def update_df3_sorter_output_status(self,df3):

        readonly_df3 = df3.copy(deep=True)       
        model = pandasModel(readonly_df3)
        self.tableView2.setModel(model)
        self.tableView2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableView2.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)

    def image_update(self,new_image_name):

        pixmap = QtGui.QPixmap('pic//pic_camera//' +new_image_name)
        pix = pixmap.scaled(QtCore.QSize(500, 500), QtCore.Qt.KeepAspectRatio)
        self.image_raw.setPixmap(pix)
        self.image_raw.setAlignment (QtCore.Qt.AlignCenter)

    def image_ocr_result_update(self, image_ocr_result):
        """
        Update the OCR result image in the UI.

        Args:
            image_ocr_result (str): The filename of the OCR result image.

        Returns:
            None
        """
        pixmap = QtGui.QPixmap('pic//pic_ocr_result//' + image_ocr_result)
        pix = pixmap.scaled(QtCore.QSize(500, 500), QtCore.Qt.KeepAspectRatio)
        self.image_result.setPixmap(pix)
        self.image_result.setAlignment(QtCore.Qt.AlignCenter)

    def ocr_result_update(self, ocr_result):
        """
        Updates the OCR result in the text edit widget.

        Args:
            ocr_result (list): The OCR result as a list of strings.

        Returns:
            None
        """
        ocr_result_str = ''
        for item in ocr_result:
            for str in item:
                ocr_result_str = ocr_result_str + '_' + str
        self.textEdit_ocr_result.setText(ocr_result_str)
        # self.textEdit_ocr_result.setText("<font color = 'white' >ocr_result_str</font>")
        self.textEdit_ocr_result.setStyleSheet("color: white;")
        self.textEdit_ocr_result.setFont(QtGui.QFont('Times', 12))
        
    def belt_run(self):
            """
            Connects to the OCR device and starts the belt run.

            :return: None
            """
            ocr_ip_address = "192.168.3.10"
            connect_type_ocr = 2

            try:
                ocs_siemens_plc = plc.plc_connect(ocr_ip_address, connect_type_ocr)
                plc.write_bool(ocs_siemens_plc, 1, 0, 1)
                plc.plc_con_close(ocs_siemens_plc)

            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", f"Error: {e}")
       
    def belt_stop(self):
        """
        Stops the belt by writing a boolean value to the Siemens PLC.

        :return: None
        """
        ocr_ip_address = "192.168.3.10"
        connect_type_ocr = 2
        try:
            ocs_siemens_plc = plc.plc_connect(ocr_ip_address, connect_type_ocr)
            plc.write_bool(ocs_siemens_plc, 1, 0, 0)
            plc.plc_con_close(ocs_siemens_plc)
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Error: {e}")
    
    def thread_error_message_display(self, e):
        """
        Display an error message box with the given error message.

        Args:
            e (Exception): The exception object representing the error.

        Returns:
            None
        """
        QtWidgets.QMessageBox.critical(None, "Error", f"Error: {e}")

    def load_truck_info(self):
            global df2_fpc_batch_summary
            global df1_ocr_sort_info
            global thread2_ocr_ai_thread_id
            #file_name, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open etx File", "", "xlsx File(*.xlsx);;etx File(*.etx);;csv file(*.csv)")
            file_name, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open etx File", "", "csv file(*.csv)")
            if not file_name:
                QtWidgets.QMessageBox.critical(None, "Error", "Please select an etx file to read.")
                return
            try:

                #df=pd.load(file_name, col_name=None,sheetname='Sheet1',engine="polars")
                df2_fpc_batch_summary_temp = pd.read_csv(file_name)

                df2_fpc_batch_summary = df2_fpc_batch_summary_temp.reindex(columns = df2_fpc_batch_summary_temp.columns.tolist()+ ["actual_qty","completion",'last_enter_tm','sorter_output','waited_tm'])
                new_row = pd.Series({'fpc_batch': 'others','target_qty': 9999, 'actual_qty': 0,'completion':'N'})
                df2_fpc_batch_summary.loc[:,'actual_qty'] = 0
                df2_fpc_batch_summary.loc[:,'completion'] = "N"
                df2_fpc_batch_summary = pd.concat([df2_fpc_batch_summary, new_row.to_frame().T], ignore_index=True)
                df2_fpc_batch_summary['target_qty'] = df2_fpc_batch_summary['target_qty'].astype(int)
                df2_fpc_batch_summary['actual_qty'] = df2_fpc_batch_summary['actual_qty'].astype(int)
                model = pandasModel(df2_fpc_batch_summary)
                self.tableView.setModel(model)
                self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                self.tableView.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)  

                df1_ocr_sort_info = df1_ocr_sort_info.drop(index=range(len(df1_ocr_sort_info)))
                thread2_ocr_ai_thread_id = 0
                model = pandasModel(df1_ocr_sort_info)
                self.tableView1.setModel(model)
                self.tableView1.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                self.tableView1.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)   

                intralox_plc_ip_address = "192.168.0.100"
                connect_type_intralox_plc = 2
                intralox_plc_init = plc.plc_connect(intralox_plc_ip_address, connect_type_intralox_plc)
                plc.write_db_word_bool(intralox_plc_init,100,0,2,1)
                time.sleep(0.1)              
                plc.write_db_word_bool(intralox_plc_init,100,0,2,0)
                plc.plc_con_close(intralox_plc_init)

            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", f"Error: {e}")
    
    def manual_release_sorter(self):

        global df3_sorter_output_status

        try:

            df3_sorter_output_status.loc[self.select_release_sorter.currentIndex(),'logic_available'] = True
                                       
        except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", f"Error: {e}")

    def update_statusbar_message(self,message):

        self.statusBar.showMessage("ready!")

    #define the function to display the ocr manual verify page
    def page_ocr_manual_verify_display(self):
        
        self.stackedWidget.setCurrentIndex(5)       
                 
if __name__ == '__main__':
    #thread1 = threading.Thread(target=TestThread)
    #thread1.start()
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    ui = StackedDemo()
    ui.show()
    sys.exit(app.exec_())