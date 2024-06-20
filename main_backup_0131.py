# This is a sample Python script.
import threading
import time
import cv2

from Modules import ocrModule as Ocr
from Modules import ocr_plc_connect as plc
import pandas as pd
import traceback
import datetime
from Modules import basler_camera as camera

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


"""
define the DataFrame for  program
"""

mutex = threading.Lock()

df_ocr_sort_info = pd.DataFrame(columns=['serial_num', 'image_capture_tm', 'ocr_finish_tm',

                                         'fpc_num', 'batch_code', 'sorter_output',

                                         'backup_output', 'sorter_enter_tm',

                                         'sorter_success_enter', 'success_sort'])

df_ocr_sort_info.set_index('serial_num', inplace=True)  # make the type as index, then easy to retrieve the data

df_fpc_batch_summary = pd.DataFrame(columns=['fpc_batch', 'target_qty', 'actual_qty',

                                             'completion', 'last_enter_tm', 'sorter_output'])

df_fpc_batch_summary.set_index('sku_batch', inplace=True)  # make the type as index, then easy to retrieve the data

df_sorter_output_status = pd.DataFrame(columns=['sorter_output', 'logic_available', 'physical_available',

                                                'previous_fpc'])

df_sorter_output_status.set_index('sorter_output',
                                  inplace=True)  # make the type as index, then easy to retrieve the data

'''
ai 模型 载入函数
'''


def load_ai_module(path, bath_size, anchor_sizes, anchor_ratios, num_classes, accept_score):
    return Ocr.load_predictor(path, bath_size, anchor_sizes, anchor_ratios, num_classes, accept_score)


'''
ai 模型 推导函数
'''


def infer_image_phase1(predictor1, img1):
    return Ocr.infer_image_phase1(img1, predictor1)


'''
fpc batch code 模糊匹配函数
返回fpc 和 batch匹配结果,已经匹配对的字符数
如果fpc 在订单数据中唯一,batch用唯一结果匹配字符数与订单数据中的字符数一样
'''
truck_info = pd.DataFrame(data=[['80000001', '1293D3772A', 120],
                                ['80000001', '1296D3773C', 60],
                                ['80000002', '2047D3771B', 20]],
                          columns=['fpc', 'batch', 'qty'])

def fuzzy_match(ocr_fpc: str, ocr_batch: str) -> (str, str):
    global df_fpc_batch_summary
    res_batch = []
    res_fpc = []


    def longest_common_subsequence(s1: str, s2: str):
        m = len(s1)
        n = len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]

    max_lcs_length_fpc = 0
    max_lcs_length_batch = 0
    # print(res_fpc)

    for row in df_fpc_batch_summary.iterrows():
        fpc_batch = row[0]
        fpc, batch = fpc_batch.split('_')
        #fpc, batch = row[0], row[1]
        curr_lcs_length_fpc = longest_common_subsequence(fpc, ocr_fpc)
        curr_lcs_length_batch = longest_common_subsequence(batch, ocr_batch)
        if curr_lcs_length_fpc > max_lcs_length_fpc:
            res_fpc = fpc
            res_batch = batch
            max_lcs_length_fpc = curr_lcs_length_fpc
            max_lcs_length_batch = curr_lcs_length_batch
        elif curr_lcs_length_fpc == max_lcs_length_fpc and curr_lcs_length_batch > max_lcs_length_batch:
            res_batch = batch
            max_lcs_length_batch = curr_lcs_length_batch
    if len(res_fpc) > 0:
        counter = 0 
        temp_res_batch = res_batch
        temp_max_lcs_length_batch = max_lcs_length_batch
        for row in df_fpc_batch_summary.iterrows():
            fpc_batch = row[0]
            fpc, batch = fpc_batch.split('_')
            if fpc == res_fpc:
                counter += 1
                res_batch = batch
                max_lcs_length_batch =len(res_batch)
                if counter > 2:
                    res_batch = temp_res_batch
                    max_lcs_length_batch = temp_max_lcs_length_batch
                    break                                      
        # if truck_info['fpc'].value_counts()[res_fpc] == 1:
        #     res_fpc = res_fpc
        #     res_batch = truck_info.loc[truck_info['fpc'] == res_fpc]['batch'].values[0]
        #     max_lcs_length_batch = len(res_batch)
    return res_fpc, res_batch, max_lcs_length_fpc, max_lcs_length_batch


'''
ocr plc 连接函数
'''


def ocr_plc_connect(ip_address, connect_type):
    try:
        siemens_plc = plc.plc_connect(ip_address, connect_type)
        print('PLC Connect Success')
        return siemens_plc

    except Exception:
        print(traceback.print_exc())
        print("PLC Connect Failure")

        return False


'''
ocr plc 连接函数
'''


def update_ocr_sort_info_new_case(siemens_plc):
    #
    # update_ocr_sort_info_new_case()
    global df_ocr_sort_info
    plc_connect_success = True
    program_run_once = True
    serial_num_case = 1
    # now = datetime.datetime.now()
    # image_capture_tm = now.strftime("%Y%m%d%H%M%S")
    plc.write_bool(siemens_plc, 1, 2, 1)

    while True:
        try:
            now = datetime.datetime.now()
            # print(plc.read_bool(siemens_plc, 1, 1),plc.read_bool(siemens_plc, 1, 2))
            if plc.read_bool(siemens_plc, 1, 1) and not plc.read_bool(siemens_plc, 1, 2):
                now = datetime.datetime.now()
                image_capture_tm = now.strftime("%Y%m%d%H%M%S%f")
                print(f'Thread1-{image_capture_tm}')
                new_row = pd.Series({'serial_num': serial_num_case, 'image_capture_tm': image_capture_tm})
                df_ocr_sort_info = pd.concat([df_ocr_sort_info, new_row.to_frame().T], ignore_index=True)
                serial_num_case += 1
                plc.write_bool(siemens_plc, 1, 2, 1)
                # print(df_ocr_sort_info[df_ocr_sort_info['ocr_finish_tm'].isna()].loc[0]['image_capture_tm'])
                # new_case_info.start()
            elif not plc.read_bool(siemens_plc, 1, 1) and plc.read_bool(siemens_plc, 1, 2):
                plc.write_bool(siemens_plc, 1, 2, 0)
                program_run_once = True
                # print('stopped')
            # print('Thread1 run time:',datetime.datetime.now() - now)
        except Exception:
            print(traceback.print_exc())
            print("PLC Connect Failure")
            plc_connect_success = False


def camera_thread(camera_use, predictor, reader):
    global df_ocr_sort_info
    camera.camera_connect(camera_use)
    id = 0
    # global camera_grap_image_success
    # while camera_grap_image_success:
    while True:
        try:

            # print('Thread2 condition:',len(df_ocr_sort_info[df_ocr_sort_info['ocr_finish_tm'].isna()]))
            now = datetime.datetime.now()

            if df_ocr_sort_info.shape[0] > id:
                # print(len(df_ocr_sort_info[df_ocr_sort_info['ocr_finish_tm'].isna()]))
                # print(df_ocr_sort_info)
                # print(df_ocr_sort_info[df_ocr_sort_info['ocr_finish_tm'].isna()])
                image_capture_tm = df_ocr_sort_info.loc[id, 'image_capture_tm']
                sensor_off_time = datetime.datetime.strptime(image_capture_tm, '%Y%m%d%H%M%S%f')
                # print(sensor_off_time)
                if (datetime.datetime.now() - sensor_off_time).microseconds > 750000:

                    '''
                    1. 触发相机拍照
                    '''
                    image, teat = camera.camera_grap_image(camera_use)

                    '''
                    2. 存图
                    '''
                    now1 = datetime.datetime.now()
                    grap_finish_tm = now1.strftime("%Y%m%d%H%M%S%f")
                    cv2.imwrite('pic/pic_camera/'+grap_finish_tm + '.jpeg', image)

                    '''
                    3.ocr 推导
                    '''
                    ocr_result = Ocr.infer_image_phase1aphase2(predictor, reader, image)
                    now = datetime.datetime.now()
                    ocr_finish_tm = now.strftime("%Y%m%d%H%M%S%f")

                    '''
                    4.ocr结果进行模糊匹配  
                    将OCR返回数据放入模糊匹配函数中进行匹配
                    目前逻辑：
                    4.1.遍历所有ocr结果,组合成ocr_fpc 和 ocr_batch,放入模糊匹配函数进行匹配
                    4.2.根据返回的模糊匹配结果,选择最佳结果
                       选择原则
                       1.优选fpc匹配的字符个数最多的选项
                       2.如果fpc匹配的字符个数相同，选择batch字符数匹配多的
                    4.3.如果fpc 和 batch匹配的字符数都大于N个,认为ocr识别成功
                    '''
                    ocr_fuzzy_match = []
                    ocr_fuzzy_match_temp = []
                    if len(ocr_result) > 1:
                        for i in range(0, len(ocr_result) - 1):
                            for j in range(i + 1, len(ocr_result)):
                                fuzzy_match_1 = fuzzy_match(ocr_result[i], ocr_result[j])
                                fuzzy_match_2 = fuzzy_match(ocr_result[j], ocr_result[i])
                                if fuzzy_match_1[2] > fuzzy_match_2[2]:
                                    ocr_fuzzy_match_temp = fuzzy_match_1
                                elif fuzzy_match_1[2] < fuzzy_match_2[2]:
                                    ocr_fuzzy_match_temp = fuzzy_match_2
                                elif fuzzy_match_1[2] == fuzzy_match_2[2] and fuzzy_match_1[3] >= fuzzy_match_2[3]:
                                    ocr_fuzzy_match_temp = fuzzy_match_1
                                elif fuzzy_match_1[2] == fuzzy_match_2[2] and fuzzy_match_1[3] < fuzzy_match_2[3]:
                                    ocr_fuzzy_match_temp = fuzzy_match_2
                                if not ocr_fuzzy_match:
                                    ocr_fuzzy_match = ocr_fuzzy_match_temp
                                elif ocr_fuzzy_match_temp[2] > ocr_fuzzy_match[2] or (
                                        ocr_fuzzy_match_temp[2] == ocr_fuzzy_match[2] and ocr_fuzzy_match_temp[3] >
                                        ocr_fuzzy_match[2]):
                                    ocr_fuzzy_match = ocr_fuzzy_match_temp
                    elif len(ocr_result) == 1:
                        fuzzy_match_1 = fuzzy_match(ocr_result[0], '')
                        fuzzy_match_2 = fuzzy_match('', ocr_result[0])
                        if fuzzy_match_1[2] > fuzzy_match_2[2]:
                            ocr_fuzzy_match = fuzzy_match_1
                        elif fuzzy_match_1[2] < fuzzy_match_2[2]:
                            ocr_fuzzy_match = fuzzy_match_2
                        elif fuzzy_match_1[2] == fuzzy_match_2[2] and fuzzy_match_1[3] >= fuzzy_match_2[3]:
                            ocr_fuzzy_match = fuzzy_match_1
                        elif fuzzy_match_1[2] == fuzzy_match_2[2] and fuzzy_match_1[3] < fuzzy_match_2[3]:
                            ocr_fuzzy_match = fuzzy_match_2
                    if ocr_fuzzy_match[2] < 5 and ocr_fuzzy_match[3] < 5:
                        ocr_fuzzy_match = ['NG', 'NG', 0, 0]

                    '''
                    5.更新df_ocr_sort_info中 'ocr_finish_tm' 'fpc_num'  'batch_code' 数据列
                    '''
                    df_ocr_sort_info.loc[id, 'ocr_finish_tm'] = ocr_finish_tm
                    df_ocr_sort_info.loc[id, 'fpc_num'] = ocr_fuzzy_match[0]
                    df_ocr_sort_info.loc[id, 'batch_code'] = ocr_fuzzy_match[1]
                    id += 1
                    print('thread2_time:', datetime.datetime.now() - now1)

            '''
            if len(df_ocr_sort_info[df_ocr_sort_info['ocr_finish_tm'].isna()]) > 0:
                # print(len(df_ocr_sort_info[df_ocr_sort_info['ocr_finish_tm'].isna()]))
                # print(df_ocr_sort_info)
                # print(df_ocr_sort_info[df_ocr_sort_info['ocr_finish_tm'].isna()])
                image_capture_tm = df_ocr_sort_info[df_ocr_sort_info['ocr_finish_tm'].isna()].iloc[0, 0]
                sensor_off_time = datetime.datetime.strptime(image_capture_tm, '%Y%m%d%H%M%S%f')
                #print(sensor_off_time)
                if (datetime.datetime.now() - sensor_off_time).microseconds > 700000:
                    now = datetime.datetime.now()
                    ocr_finish_tm = now.strftime("%Y%m%d%H%M%S%f")
                    image, teat = camera.camera_grap_image(camera_use)
                    cv2.imwrite(ocr_finish_tm+'.jpeg', image)
                    # print(df_ocr_sort_info[df_ocr_sort_info['ocr_finish_tm'].isna()].loc[0]['serial_num'])
                    serial_num = df_ocr_sort_info[df_ocr_sort_info['ocr_finish_tm'].isna()].iloc[0][-1]
                    #mutux.acquire(1)
                    df_ocr_sort_info.loc[df_ocr_sort_info['serial_num'] == serial_num, 'ocr_finish_tm'] = ocr_finish_tm
                    #mutux.release()
                    print('Thread2 result:',df_ocr_sort_info)
            #print('Thread2 run time:',datetime.datetime.now() - now)
                    # df_ocr_sort_info[df_ocr_sort_info['ocr_finish_tm'].isna()].loc[0]['ocr_finish_tm'] = ocr_finish_tm
            '''

            '''
            if plc.read_bool(siemens_plc, 1, 1) and program_run_once:
                camera.camera_connect(camera_use)
                time.sleep(1.4)
                program_run_once = False
                image, teat = camera.camera_grap_image(camera_use)
                cv2.imwrite('Test.jpeg', image)
                camera.camera_disconnect(camera_use)
                print("Finished_Grap_Image")
            elif plc.read_bool(siemens_plc, 1, 1) == 0 and not program_run_once:
                program_run_once = True
            '''
        except Exception:
            print(traceback.print_exc())
            print("camera grap image  Failure")
            # camera_grap_image_success = False
            camera.camera_disconnect(camera_use)


# Thread 4-1

def update_intralox_sort_enter_new_case(intralox_plc):
    global df_ocr_sort_info
    plc_connect_success = True
    program_run_once = True
    now = datetime.datetime.now()
    sorter_enter_tm = now.strftime("%Y%m%d%H%M%S")
    while plc_connect_success:
        try:
            if plc.read_bool(intralox_plc, 1, 1) == 1 and program_run_once:
                program_run_once = False
                # read serial_num from intralox_plc
                intralox_serial_num = 4  # NEED UPDATE
                # record sorting enter time
                now = datetime.datetime.now()
                sorter_enter_tm = now.strftime("%Y%m%d%H%M%S%f")
                print(sorter_enter_tm)
                # update info
                df_ocr_sort_info.loc[
                    df_ocr_sort_info['serial_num'] == intralox_serial_num, 'sorter_enter_tm'] = sorter_enter_tm
                df_ocr_sort_info.loc[df_ocr_sort_info['serial_num'] == intralox_serial_num, 'sorter_success_enter'] = 1
                print(df_ocr_sort_info)
            elif plc.read_bool(intralox_plc, 1, 1) == 0 and not program_run_once:
                program_run_once = True
                print('stopped')
        except Exception:
            print(traceback.print_exc())
            print("PLC Connect Failure")
            plc_connect_success = False


if __name__ == '__main__':

    '''
    AI Module global 变量
    '''
    path = 'ocr_ai_fodler/module/model_final.pth'
    bath_size = 32
    anchor_sizes = [[32, 64, 128, 256, 512]]
    anchor_ratios = [[0.1, 0.15, 0.2, 0.25, 0.33]]
    num_classes = 3
    accept_score = 0.45
    """
    查找basler相机资源
    """
    basler_camera_use = camera.get_camera_source()
    '''
    load AI Module:phase1 数据模型 和 OCR数据模型
    '''
    predictor, reader = load_ai_module(path, bath_size, anchor_sizes, anchor_ratios, num_classes, accept_score)
    """
    连接OCR PLC
    """
    ocr_ip_address = "192.168.3.10"
    connect_type_ocr = 2
    ocs_siemens_plc = ocr_plc_connect(ocr_ip_address, connect_type_ocr)
    """
    线程1启动
    线程1:
    1.每当case触发sensor,递增流水号,在DataFrame:df_ocr_sort_info新增一行,并将流水号和触发时间写至新行中的'serial_num' 和 'image_capture_tm' 
    2.将新增加的'serial_num'转发至Intralox PLC
    """
    new_case_info = threading.Thread(target=update_ocr_sort_info_new_case, args={ocs_siemens_plc})
    new_case_info.start()
    """
    线程2启动
    线程2:
    如果DataFrame:df_ocr_sort_info 中的行数大于已经拍照数据：
        取DataFrame:df_ocr_sort_info 中的image_capture_tm,并且与系统现有时间进行比较，如果达到设定值：
          1.触发相机拍照  --- finished
          2.存图         --- finished
          3.AI 分析相机图片,返回ocr结果    --- finished
          4.ocr结果进行模糊匹配,得到最终结果  -- finished
          5.更新DataFrame:df_ocr_sort_info中的'ocr_finish_tm','fpc_num', 'batch_code'  --- finished
    """
    grap_image = threading.Thread(target=camera_thread, args=(basler_camera_use, predictor, reader))
    grap_image.start()
    serial_num = 1
    while True:
        '''
        后续工作
        1. 子线程停止条件
        2. 子线程停止后，内存数据处理
        3. 其他后续工作
        '''
