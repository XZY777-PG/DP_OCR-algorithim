import pandas as pd
import shutil

RAW_DATA_PATH = './results/'
CSV_NAME = 'df1_result_20240125_W6.csv'
IMAGE_FOLDER_PATH = './pic/pic_camera/'
NG_FOLDER = './results/NG/20240125_W6_NG/'

# import data
df = pd.read_csv(RAW_DATA_PATH + CSV_NAME)

# filter NG output
df_ng = df.loc[df['fpc_batch'] == 'others']
df_ng.to_csv(NG_FOLDER + 'df1_result_20240125_W6_NG.csv', index=False)

for index, row in df_ng.iterrows():
    image_name = row[2].replace('-', '')
    image_name = image_name.replace(':', '')
    image_name = image_name.replace(' ', '')
    image = IMAGE_FOLDER_PATH + image_name + '.jpeg'
    shutil.copy(image, NG_FOLDER)