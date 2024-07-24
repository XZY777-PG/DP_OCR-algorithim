# 📚 P&G Dead Pile unloading(loading) TechDocs 
![Static Badge](https://img.shields.io/badge/https%3A%2F%2Fgithub.com%2FXZY777-PG%2FDP_OCR-algorithim%2F)
## Introduction
DP_OCR-algorithim is an optical character recognition (OCR) algorithm designed to extract text from images with high accuracy. This project aims to provide a robust and efficient OCR solution for various applications such as document scanning, image-to-text conversion, and more.
## 🏗️ Code structue overview  
├── .gitignore  --------------------- git配置文件  
├── apprcc_rc.py -------------------- PyQt配置文件  
├── config/ ------------------------- 配置文件夹  
│   ├── fold.json ------------------- 文件夹路径设置  
│   ├── ip.json --------------------- ip配置  
│   ├── setting.json ---------------- 超参数配置  
├── eng_folder/ --------------------- 测试文件夹  
│   ├── start_infer_test.jpeg  ------ 测试图片  
├── icon/ --------------------------- ui图片存储文件夹  
├── main.py ------------------------- 主程序  
├── main_winodw/ -------------------- ui窗口配置文件夹   
│   ├── win.py ---------------------- ui窗口设置  
├── models/ ------------------------- 模块编译文件夹  
│   ├── common.py ------------------- 通用模块1  
│   ├── common_runtime.py  ---------- 通用模块2  
│   ├── image_batcher.py ------------ 图片预处理模块  
│   ├── ocrModule.py ---------------- ocr识别模块  
├── MouseLabel.py ------------------- ui事件配置  
├── ocrModule.py -------------------- ocr识别模块  
├── Readme.md  
├── requirement.txt ----------------- 算法环境配置要求  
├── utils/  
│   ├── capnums.py ------------------ 摄像头参数获取？  
│   ├── CustomMessageBox.py --------- ui事件设置  
## 📘 Get Started  
### 1️⃣ Install
Clone the repository
```
git clone git@github.com:AbletiveSkye/PG-Dead-Pile-OCR.git
```
load your path to the project
```
!cd (yourpath to PG-Dead-Pile-OCR)
```
Download the enssential environments for the algorithim.
```
!pip install requirements.txt
```
Compile your code on the local environment
```
!python setup.py
```
Run the graphic page
```
!python main.py
```

### 2️⃣ 训练（开发环境）
### 3️⃣ 测试（生产环境）

## 🔎 update
2024-07-15  
桌面系统 draft    
2024-07-16  
添加手动输入文件，进行推理代码  
发现问题--- tensorRT 版本与agx orin的版本不一致 tensorrt eng 文件不兼容  
2024 07-17  
添加图片显示    
2024 07-18  
添加相机支持    
2024 07-19  
继续添加相机相关路径 修改界面 添加模式选择 添加当前模式显示 添加相机自动搜索功能  
## ⭐ License
This project is licensed under the Apache 2.0 License - see the LICENSE file(暂时未放进仓库) for details.

## 🤝 Contribution    
Contributions are welcome! Please follow these steps to contribute:  
Fork the repository by clicking on the "Fork" button at the top right corner of the repository page.  
Clone your forked repository to your local machine:  
```
git clone https://github.com/your-username/DP_OCR-algorithim.git
```
Create a new branch for your feature or bugfix:  
```
git checkout -b feature/AmazingFeature
```
Make your changes and commit them with a descriptive commit message:
```
git commit -m 'Add some AmazingFeature'
```
Push your changes to your forked repository:
```
git push origin feature/AmazingFeature
```
Open a Pull Request in the original repository: https://github.com/XZY777-PG/DP_OCR-algorithim and provide a detailed description of your changes.

## ✉️ Contact us  
Alan Liu - liu.zi@pg.com  
Jerry Xu - xu.h.14@pg.com  
Troy Gao - gao.y.32@pg.com  
Lane Chen - chen.la@pg.com  
Gan Mi - gan.m.5@pg.com  
Xu Zhiyuan - xu.z.29@pg.com  
