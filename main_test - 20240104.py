# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 11:16:58 2024

@author: liu.zi
"""
import pandas as pd
from datetime import datetime
import random
from time import sleep

# import the thread3 and 5
from Modules.thread3_calculate_sorter_output import repeat_calculate_sorter_output
from Modules.thread5_accumulated_cnt_and_sorter_release import repeat_accumulated_cnt_and_sorter_release
from threading import Thread


################## 临时使用本地的excel #########################################
df1_ocr_sort_info = pd.read_excel('ocr_sort_data.xlsx', sheet_name='Sheet1')  
df1_ocr_sort_info.set_index('serial_num', inplace=True)

df2_fpc_batch_summary = pd.read_excel('ocr_sort_data.xlsx', sheet_name='Sheet2')
df2_fpc_batch_summary.set_index('fpc_batch', inplace=True)

df3_sorter_output_status = pd.read_excel('ocr_sort_data.xlsx', sheet_name='Sheet3')
df3_sorter_output_status.set_index('sorter_output', inplace=True)
###############################################################################



def dummy_case_arrive():
    global df1_ocr_sort_info
    cnt = len(df1_ocr_sort_info) 
    
    # make dummy case
    case_list = ['22222222_20230808', '55555555_20220101', '77777777_20220303' ]
    
    while(1):
        df1_ocr_sort_info.loc[cnt, 'image_capture_tm'] = datetime.now()
        random_num = random.randint(0, 2)
        df1_ocr_sort_info.loc[cnt, 'fpc_batch'] = case_list[random_num]
        print(f'thread1: a case index {cnt} arrive, the fpc_code is {case_list[random_num]}')
        cnt += 1
        sleep(2)

# 创建 Thread 实例
t1 = Thread(target=dummy_case_arrive)
t3 = Thread(target=repeat_calculate_sorter_output, args= (df1_ocr_sort_info, df2_fpc_batch_summary, df3_sorter_output_status))
t5 = Thread(target=repeat_accumulated_cnt_and_sorter_release, args= (df2_fpc_batch_summary, df3_sorter_output_status))

# 启动线程运行
t1.start()
t3.start()
t5.start()

# 等待所有线程执行完毕
t1.join()
t3.join()  # join() 等待线程终止，要不然一直挂起
t5.join()

'''
###############################################################################    
if __name__=='__main__':
    while (1):
        accumulated_cnt_and_sorter_release()
        print('done')
###############################################################################
'''