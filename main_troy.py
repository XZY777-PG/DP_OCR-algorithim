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
df_ocr_sort_info = pd.DataFrame(columns=['serial_num', 'image_capture_tm', 'ocr_finish_tm',

                                         'fpc_num', 'batch_code', 'sorter_output',

                                         'backup_output', 'sorter_enter_tm',

                                         'sorter_success_enter', 'success_sort'])

df_ocr_sort_info.set_index('serial_num', inplace=True)  # make the type as index, then easy to retrieve the data

df_fpc_batch_summary = pd.DataFrame(columns=['fpc_batch', 'target_qty', 'actual_qty',

                                             'completion', 'last_enter_tm', 'sorter_output'])

# df_fpc_batch_summary.set_index('sku_batch', inplace=True)  # make the type as index, then easy to retrieve the data

df_sorter_output_status = pd.DataFrame(columns=['sorter_output', 'logic_available', 'physical_available',

                                                'previous_fpc'])

df_sorter_output_status.set_index('sorter_output',
                                  inplace=True)  # make the type as index, then easy to retrieve the data


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def load_ai_module(path, bath_size, anchor_sizes, anchor_ratios, num_classes, accept_score):
    return Ocr.load_predictor(path, bath_size, anchor_sizes, anchor_ratios, num_classes, accept_score)


def infer_image_phase1(predictor1, img1):
    return Ocr.infer_image_phase1(img1, predictor1)


def ocr_plc_connect(ip_address, connect_type):
    try:
        siemens_plc = plc.plc_connect(ip_address, connect_type)
        print('PLC Connect Success')
        return siemens_plc

    except Exception:
        print(traceback.print_exc())
        print("PLC Connect Failure")

        return False


def update_ocr_sort_info_new_case(siemens_plc):
    #
    # update_ocr_sort_info_new_case()
    global df_ocr_sort_info
    plc_connect_success = True
    program_run_once = True
    serial_num = 1
    #now = datetime.datetime.now()
    #image_capture_tm = now.strftime("%Y%m%d%H%M%S")

    while True:
        try:
            now = datetime.datetime.now()

            #print(plc.read_bool(siemens_plc, 1, 1),plc.read_bool(siemens_plc, 1, 2))
            if plc.read_bool(siemens_plc, 1, 1) and not plc.read_bool(siemens_plc, 1, 2):
                now = datetime.datetime.now()
                image_capture_tm = now.strftime("%Y%m%d%H%M%S%f")
                print(image_capture_tm)
                new_row = pd.Series({'serial_num': serial_num, 'image_capture_tm': image_capture_tm})
                df_ocr_sort_info = pd.concat([df_ocr_sort_info, new_row.to_frame().T], ignore_index=True)
                serial_num += 1
                #plc.write_bool(siemens_plc, 1, 2, 1)
                # print(df_ocr_sort_info[df_ocr_sort_info['ocr_finish_tm'].isna()].loc[0]['image_capture_tm'])
                # new_case_info.start()
            elif not plc.read_bool(siemens_plc, 1, 1) and plc.read_bool(siemens_plc, 1, 2):
                #plc.write_bool(siemens_plc, 1, 2, 0)
                program_run_once = True
                # print('stopped')
            #print(datetime.datetime.now() - now)
        except Exception:
            print(traceback.print_exc())
            print("PLC Connect Failure")
            plc_connect_success = False


def camera_thread(camera_use):
    global df_ocr_sort_info
    camera.camera_connect(camera_use)
    # global camera_grap_image_success
    # while camera_grap_image_success:
    id = 0
    while True:
        try:
            if df_ocr_sort_info.shape[0] > id:
                # print(len(df_ocr_sort_info[df_ocr_sort_info['ocr_finish_tm'].isna()]))
                # print(df_ocr_sort_info)
                # print(df_ocr_sort_info[df_ocr_sort_info['ocr_finish_tm'].isna()])
                image_capture_tm = df_ocr_sort_info.loc[id, 'image_capture_tm']
                sensor_off_time = datetime.datetime.strptime(image_capture_tm, '%Y%m%d%H%M%S%f')
                #print(sensor_off_time)
                if (datetime.datetime.now() - sensor_off_time).microseconds > 550000:
                    image, teat = camera.camera_grap_image(camera_use)
                    cv2.imwrite('Test.jpeg', image)
                    now = datetime.datetime.now()
                    ocr_finish_tm = now.strftime("%Y%m%d%H%M%S%f")
                    # print(df_ocr_sort_info[df_ocr_sort_info['ocr_finish_tm'].isna()].loc[0]['serial_num'])
                    df_ocr_sort_info.loc[id, 'ocr_finish_tm'] = ocr_finish_tm
                    id += 1

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
    print_hi('PyCharm')
    """
    定义global变量
    """
    camera_grap_image_success = False
    basler_camera_use = camera.get_camera_source()

    """
    连接OCR PLC
    """
    ocr_ip_address = "192.168.3.10"
    connect_type_ocr = 2
    ocs_siemens_plc = ocr_plc_connect(ocr_ip_address, connect_type_ocr)
    #time.sleep(0.2)
    ocs_siemens_plc2 = ocr_plc_connect(ocr_ip_address, connect_type_ocr)
    #time.sleep(0.2)
    #ocs_siemens_plc3 = ocr_plc_connect(ocr_ip_address, connect_type_ocr)

    """
    线程1启动
    """
    new_case_info = threading.Thread(target=update_ocr_sort_info_new_case, args={ocs_siemens_plc2})
    new_case_info.start()
    grap_image = threading.Thread(target=camera_thread, args={basler_camera_use})
    grap_image.start()

    """
    线程2启动
    
    time.sleep(1)
    if not camera_grap_image_success:
        try:
            basler_camera_use = camera.get_camera_source()
            camera_grap_image_success = True
        except Exception:
            print(traceback.print_exc())
            print("camera connect  Failure")
            camera_grap_image_success = False
    if camera_grap_image_success:
        grap_image = threading.Thread(target=camera_thread, args={ocs_siemens_plc2, basler_camera_use})
        grap_image.start()

    """
