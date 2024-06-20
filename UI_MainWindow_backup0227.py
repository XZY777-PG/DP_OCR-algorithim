from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        '''
        主页显示 切换页面时 不更换项目
        '''
        #窗口设置
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #MainWindow.setWindowTitle('P&G Deadpile Project')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #标题栏设置
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 100))
        self.menubar.setFixedHeight(30)
        self.menubar.setObjectName("menubar")
        #标题栏 增加目录1--父项  系统配置
        system_configure = self.menubar.addMenu('System Configure')
        self.menubar.addSeparator()
     

        #标题栏 增加目录1--子项   OCR PLC 配置
        self.ocr_plc_configure = QtWidgets.QAction('Ocr Plc Configure', self.menubar)
        #待删除的两行
        #ocr_plc_configure.triggered.connect(self.load_ocr_plc_configure)
        #ocr_plc_configure.triggered.connect(MainWindow.close) 
        system_configure.addAction(self.ocr_plc_configure)
        
        #标题栏 增加目录1--子项  Intralox PLC 配置
        self.intralox_plc_configure = QtWidgets.QAction('Intralox Plc Configure', self.menubar)
        #intralox_plc_configure.triggered.connect(self.open_new_window)
        system_configure.addAction(self.intralox_plc_configure)
 
        #标题栏 增加目录1--子项  AI配置 包含相机
        self.ai_ocr_configure = QtWidgets.QAction('Ai_Ocr_Configure', self.menubar)
        #ai_ocr_configure.triggered.connect(self.open_new_window)
        system_configure.addAction(self.ai_ocr_configure)    

        
        #标题栏 增加目录2--父项  用户
        user = self.menubar.addMenu('User')

        
        #标题栏 增加目录2--子项  用户登录
        self.user_login = QtWidgets.QAction('User Login', self.menubar)
        #user_login.triggered.connect(self.load_truck_info)
        user.addAction(self.user_login)
        
        #标题栏 增加目录2--子项  用户管理
        self.user_management = QtWidgets.QAction('User_Management',self.menubar)
        #user_management.triggered.connect(self.load_truck_info)
        user.addAction(self.user_management)

        #标题栏 增加目录2--父项  main_page
        self.main_page = QtWidgets.QAction('main_page',self.menubar)
        self.menubar.addAction(self.main_page)

        #标题栏 增加目录2--父项  退出
        exit = QtWidgets.QAction('Exit',self.menubar)
        exit.triggered.connect(MainWindow.close)
        self.menubar.addAction(exit)        
        MainWindow.setMenuBar(self.menubar)
        self.menubar.setVisible(False)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setFixedHeight(50)
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.setVisible(False)

        '''
        页面推叠
        '''
        #堆叠区域设置？
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1920, 1000))
        self.stackedWidget.setObjectName("stackedWidget")

        '''
        log in 画面
        
        '''
        self.page_login = QtWidgets.QWidget()
        self.page_login.setObjectName("login")

        self.page_login_text1 = QtWidgets.QLabel(self.page_login)
        self.page_login_text1.setGeometry(QtCore.QRect(550, 200, 820, 50))
        self.page_login_text1.setObjectName('Main Display Login')
        self.page_login_text1.setText("<font color = 'white' >P&G Deadpile Pilot Line Control System</font>")
        self.page_login_text1.setFont(QtGui.QFont('Times', 26))
        self.page_login_text1.setAlignment(QtCore.Qt.AlignCenter)

        self.page_login_text2 = QtWidgets.QLabel(self.page_login)
        self.page_login_text2.setGeometry(QtCore.QRect(550, 350, 820, 50))
        self.page_login_text2.setObjectName('Main Display Login')
        self.page_login_text2.setText("<font color = 'white' >User Login</font>")
        self.page_login_text2.setFont(QtGui.QFont('Times', 24))
        self.page_login_text2.setAlignment(QtCore.Qt.AlignCenter)

        self.page_login_text3 = QtWidgets.QLabel(self.page_login)
        self.page_login_text3.setGeometry(QtCore.QRect(800, 450, 160, 30))
        self.page_login_text3.setObjectName('User')
        self.page_login_text3.setText("<font color = 'white' >User:</font>")
        self.page_login_text3.setFont(QtGui.QFont('Times', 20))
        self.page_login_text3.setAlignment(QtCore.Qt.AlignRight)

        self.page_login_input_user_name  = QtWidgets.QLineEdit(self.page_login)
        self.page_login_input_user_name.setGeometry(QtCore.QRect(960,450,200,30))
        self.page_login_input_user_name.setObjectName('Input User Name')
        self.page_login_input_user_name.setText('user')
        self.page_login_input_user_name.setFont(QtGui.QFont('Times', 20)) 
        self.page_login_input_user_name.setStyleSheet('QLineEdit{background-color: gray;border-radius: 5px;}')
        self.page_login_input_user_name.setAlignment(QtCore.Qt.AlignLeft)

        self.page_login_text4 = QtWidgets.QLabel(self.page_login)
        self.page_login_text4.setGeometry(QtCore.QRect(800, 500, 160, 30))
        self.page_login_text4.setObjectName('Password')
        self.page_login_text4.setText("<font color = 'white' >Password:</font>")
        self.page_login_text4.setFont(QtGui.QFont('Times', 20))
        self.page_login_text4.setAlignment(QtCore.Qt.AlignRight)

        self.page_login_input_password  = QtWidgets.QLineEdit(self.page_login)
        self.page_login_input_password.setGeometry(QtCore.QRect(960,500,200,30))
        self.page_login_input_password.setObjectName('Input password')
        self.page_login_input_password.setText('password')
        self.page_login_input_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.page_login_input_password.setFont(QtGui.QFont('Times', 20)) 
        self.page_login_input_password.setStyleSheet('QLineEdit{border-radius: 5px;}')
        self.page_login_input_password.setAlignment(QtCore.Qt.AlignLeft)

        self.button_login =QtWidgets.QPushButton(self.page_login)
        self.button_login.setGeometry(QtCore.QRect(935, 550, 100, 40))
        self.button_login.setObjectName("Login")
        self.button_login.setText('Login')    
        self.button_login.setGraphicsEffect(QtWidgets.QGraphicsOpacityEffect().setOpacity(0.1))
        self.button_login.setFont(QtGui.QFont('Times', 15)) 
        self.button_login.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_login.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')

        self.button_exit =QtWidgets.QPushButton(self.page_login)
        self.button_exit.setGeometry(QtCore.QRect(1060, 550, 100, 40))
        self.button_exit.setObjectName("Exit")
        self.button_exit.setText('Exit')    
        self.button_exit.setFont(QtGui.QFont('Times', 15))
        # self.button_exit.setGraphicsEffect(QtWidgets.QGraphicsOpacityEffect().setOpacity(0.1))
        self.button_exit.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')
        self.button_exit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_exit.clicked.connect(MainWindow.close)







        pixmap = QtGui.QPixmap('Picture1.png')
        palette = self.palette()
        brush = QtGui.QBrush(pixmap)
        palette.setBrush(QtGui.QPalette.Background, brush)
        self.page_login.setAutoFillBackground(True)
        self.page_login.setPalette(palette)
        self.stackedWidget.addWidget(self.page_login)   

        '''
        堆叠区域1 Layout
        '''
        self.page_first = QtWidgets.QWidget()
        self.page_first.setObjectName("page_first")

        # self.pushButton = QtWidgets.QPushButton(self.page_first)
        # self.pushButton.setGeometry(QtCore.QRect(0, 20, 150, 50))
        # self.pushButton.setObjectName("pushButton")   
        # self.pushButton.clicked.connect(MainWindow.close) # type: ignore     

        self.pushButton1 = QtWidgets.QPushButton(self.page_first)
        self.pushButton1.setGeometry(QtCore.QRect(0, 2, 120, 40))
        self.pushButton1.setObjectName("belt start")
        self.pushButton1.setText('Belt Start')    
        self.pushButton1.setGraphicsEffect(QtWidgets.QGraphicsOpacityEffect().setOpacity(0.1))
        self.pushButton1.setFont(QtGui.QFont('Times', 15))
        self.pushButton1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        #self.pushButton1.setStyleSheet('QPushButton{background-color: blue; color: white;border-width: 2px; border-style: solid; border-color: red;border-radius: 30px;}')
        self.pushButton1.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;border-style: solid; border-color: white;color: black;}')

        self.pushButton2 = QtWidgets.QPushButton(self.page_first)
        self.pushButton2.setGeometry(QtCore.QRect(125, 2, 120, 40))
        self.pushButton2.setObjectName("belt_stop")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.pushButton2.setFont(QtGui.QFont('Times', 15))
        self.pushButton2.setText('Belt Stop')
        self.pushButton2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton2.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')

        

        self.pushButton3 = QtWidgets.QPushButton(self.page_first)
        self.pushButton3.setGeometry(QtCore.QRect(250, 2, 150, 40))
        self.pushButton3.setObjectName("load_truck_info")
        self.pushButton3.setText('Load Truck Info')  
        self.pushButton3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton3.setFont(QtGui.QFont('Times', 15))
        self.pushButton3.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')   

        self.button_generate_case = QtWidgets.QPushButton(self.page_first)
        self.button_generate_case.setGeometry(QtCore.QRect(405, 2, 150, 40))
        self.button_generate_case.setObjectName("generate_case")
        self.button_generate_case.setText('generate_case')     
        self.button_generate_case.setVisible(False)
        self.button_generate_case.setFont(QtGui.QFont('Times', 15))
        self.button_generate_case.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_generate_case.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')   

        self.button_save_df1 = QtWidgets.QPushButton(self.page_first)
        self.button_save_df1.setGeometry(QtCore.QRect(560, 2, 150, 40))
        self.button_save_df1.setObjectName("save df1 to csv")
        self.button_save_df1.setText('save df1 to csv')     
        self.button_save_df1.setVisible(True)
        self.button_save_df1.setFont(QtGui.QFont('Times', 15))
        self.button_save_df1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_save_df1.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')  

        self.button_release_sorter = QtWidgets.QPushButton(self.page_first)
        self.button_release_sorter.setGeometry(QtCore.QRect(720, 2, 150, 40))
        self.button_release_sorter.setObjectName("release sorter")
        self.button_release_sorter.setText('release sorter')     
        self.button_release_sorter.setVisible(True)
        self.button_release_sorter.setFont(QtGui.QFont('Times', 15))
        self.button_release_sorter.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_release_sorter.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')  

        self.select_release_sorter = QtWidgets.QComboBox(self.page_first)
        self.select_release_sorter.setGeometry(QtCore.QRect(870, 2, 40, 40))
        self.select_release_sorter.addItems(['1','2','3','4','5','6'])



        self.textEdit_ocr = QtWidgets.QLabel(self.page_first)
        self.textEdit_ocr.setGeometry(QtCore.QRect(920, 0, 150, 50))
        self.textEdit_ocr.setObjectName('OCR_Text')
        #self.textEdit_ocr.setText('OCR_Result:')
        self.textEdit_ocr.setText("<font color = 'white' >OCR_Result:</font>")
        self.textEdit_ocr.setFont(QtGui.QFont('Times', 12))

        self.textEdit_ocr_result = QtWidgets.QLabel(self.page_first)
        self.textEdit_ocr_result.setGeometry(QtCore.QRect(1080, 0, 620, 50))
        self.textEdit_ocr_result.setObjectName('OCR_Result')
        self.textEdit_ocr_result.setText('')

        '''
        df2_fpc_batch_summary UI 显示
        '''
        self.tableView = QtWidgets.QTableView(self.page_first)
        self.tableView.setGeometry(QtCore.QRect(0, 80, 800, 310))
        self.tableView.setObjectName("tableView")
        #model = pandasModel(df2_fpc_batch_summary)
        #self.tableView.setModel(model)        

        '''
        df1_ocr_sort_info UI 显示
        '''
        self.tableView1 = QtWidgets.QTableView(self.page_first)
        self.tableView1.setGeometry(QtCore.QRect(0, 400, 1420, 600))
        self.tableView1.setObjectName("tableView")
        #model = pandasModel(df1_ocr_sort_info)
        #self.tableView1.setModel(model)

        '''
        df3_sorter_output_status UI 显示
        '''
        self.tableView2 = QtWidgets.QTableView(self.page_first)
        self.tableView2.setGeometry(QtCore.QRect(820, 150, 600, 240))
        self.tableView2.setObjectName("tableView")
        self.tableView2.setGraphicsEffect(QtWidgets.QGraphicsOpacityEffect().setOpacity(0.1))
        #model = pandasModel(df3_sorter_output_status)
        #self.tableView2.setModel(model)

        '''
        相机图片 UI 显示
        '''
        self.image_raw = QtWidgets.QLabel(self.page_first)
        self.image_raw.setGeometry(QtCore.QRect(1420, 0, 500, 500))
        self.image_raw.setObjectName("image_raw")    
        pixmap_image_raw = QtGui.QPixmap('OIP-C.jpeg')
        pix_image_raw = pixmap_image_raw.scaled(QtCore.QSize(500, 500), QtCore.Qt.KeepAspectRatio)
        self.image_raw.setPixmap(pix_image_raw)
        self.image_raw.setAlignment (QtCore.Qt.AlignCenter)        

        '''
        ocr AI result UI 显示
        '''
        self.image_result = QtWidgets.QLabel(self.page_first)
        self.image_result.setGeometry(QtCore.QRect(1420, 500, 500, 500))
        self.image_result.setObjectName("image_result")    
        pixmap_image_result = QtGui.QPixmap('OIP-C.jpeg')
        pix_image_result = pixmap_image_result.scaled(QtCore.QSize(500, 500), QtCore.Qt.KeepAspectRatio)
        self.image_result.setPixmap(pix_image_result)
        self.image_result.setAlignment (QtCore.Qt.AlignCenter)  
        

        self.page_first.setAutoFillBackground(True)
        self.page_first.setPalette(palette)
        self.stackedWidget.addWidget(self.page_first)   

        '''
        堆叠区域2 Layout
        '''
        self.page_ocr_plc_configure = QtWidgets.QWidget()
        self.page_ocr_plc_configure.setObjectName("page_ocr_plc_configure")

        self.Q_label_text_1 = QtWidgets.QLabel(self.page_ocr_plc_configure)
        self.Q_label_text_1.setGeometry(QtCore.QRect(800, 0, 320, 100))
        self.Q_label_text_1.setObjectName('Ocr Plc Configure')
        self.Q_label_text_1.setText("<font color = 'white' >OCR PLC CONFIGURE</font>")
        self.Q_label_text_1.setFont(QtGui.QFont('Times', 24))
        self.Q_label_text_1.setAlignment(QtCore.Qt.AlignCenter)

        # OCR Phase1 Module Select
        self.Q_label_text_2 = QtWidgets.QLabel(self.page_ocr_plc_configure)
        self.Q_label_text_2.setGeometry(QtCore.QRect(0, 150, 640, 50))
        self.Q_label_text_2.setObjectName('Select OCR Phase Model')
        self.Q_label_text_2.setText("<font color = 'white'>Select OCR Phase Model</font>")
        self.Q_label_text_2.setFont(QtGui.QFont('Times', 20)) 
        self.Q_label_text_2.setAlignment(QtCore.Qt.AlignCenter)

        self.Q_label_text_3 = QtWidgets.QLabel(self.page_ocr_plc_configure)
        self.Q_label_text_3.setGeometry(QtCore.QRect(0, 250, 640, 50))
        self.Q_label_text_3.setObjectName('Current Select OCR Phase Model')
        self.Q_label_text_3.setText("<font color = 'white',>Current Select OCR Phase Model</font>")
        self.Q_label_text_3.setFont(QtGui.QFont('Times', 15)) 
        self.Q_label_text_3.setAlignment(QtCore.Qt.AlignCenter)

        self.Q_label_text_phase1_status = QtWidgets.QLabel(self.page_ocr_plc_configure)
        self.Q_label_text_phase1_status.setGeometry(QtCore.QRect(0, 300, 640, 50))
        self.Q_label_text_phase1_status.setObjectName('Current Select OCR Phase Model')
        self.Q_label_text_phase1_status.setText("<font color = 'Red',>no Phase Module Select</font>")
        self.Q_label_text_phase1_status.setFont(QtGui.QFont('Times', 15)) 
        self.Q_label_text_phase1_status.setAlignment(QtCore.Qt.AlignCenter)


        self.button_phase1_select_mode_1 = QtWidgets.QPushButton(self.page_ocr_plc_configure)
        self.button_phase1_select_mode_1.setGeometry(QtCore.QRect(170, 400, 300, 50))
        self.button_phase1_select_mode_1.setObjectName("Simualtion With Out PLC")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.button_phase1_select_mode_1.setStyleSheet("background-color : white")
        self.button_phase1_select_mode_1.setText('Simualtion With Out PLC')
        self.button_phase1_select_mode_1.setFont(QtGui.QFont('Times', 15))
        self.button_phase1_select_mode_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_phase1_select_mode_1.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')

        self.button_phase1_select_mode_2 = QtWidgets.QPushButton(self.page_ocr_plc_configure)
        self.button_phase1_select_mode_2.setGeometry(QtCore.QRect(170, 500, 300, 50))
        self.button_phase1_select_mode_2.setObjectName("Simualtion With PLC")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.button_phase1_select_mode_2.setStyleSheet("background-color : white")
        self.button_phase1_select_mode_2.setText('Simualtion With PLC')
        self.button_phase1_select_mode_2.setFont(QtGui.QFont('Times', 15))
        self.button_phase1_select_mode_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_phase1_select_mode_2.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')


        self.button_phase1_select_mode_3 = QtWidgets.QPushButton(self.page_ocr_plc_configure)
        self.button_phase1_select_mode_3.setGeometry(QtCore.QRect(170, 600, 300, 50))
        self.button_phase1_select_mode_3.setObjectName("Production")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.button_phase1_select_mode_3.setStyleSheet("background-color : white")
        self.button_phase1_select_mode_3.setText('Production')
        self.button_phase1_select_mode_3.setFont(QtGui.QFont('Times', 15))
        self.button_phase1_select_mode_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_phase1_select_mode_3.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')


        # OCR Phase1 Module Control
        self.Q_label_text_5 = QtWidgets.QLabel(self.page_ocr_plc_configure)
        self.Q_label_text_5.setGeometry(QtCore.QRect(640, 150, 640, 50))
        self.Q_label_text_5.setObjectName('OCR PLC Phase Control')
        self.Q_label_text_5.setText("<font color = 'white'>OCR PLC Phase Control</font>")
        self.Q_label_text_5.setFont(QtGui.QFont('Times', 20)) 
        self.Q_label_text_5.setAlignment(QtCore.Qt.AlignCenter)        

        self.Q_label_text_6 = QtWidgets.QLabel(self.page_ocr_plc_configure)
        self.Q_label_text_6.setGeometry(QtCore.QRect(640, 250, 640, 50))
        self.Q_label_text_6.setObjectName('Ocr Plc Phase Mode Status')
        self.Q_label_text_6.setText("<font color = 'white',>Ocr Plc Phase Mode Status</font>")
        self.Q_label_text_6.setFont(QtGui.QFont('Times', 15)) 
        self.Q_label_text_6.setAlignment(QtCore.Qt.AlignCenter)

        self.Q_label_text_7 = QtWidgets.QLabel(self.page_ocr_plc_configure)
        self.Q_label_text_7.setGeometry(QtCore.QRect(640, 300, 640, 50))
        self.Q_label_text_7.setObjectName('Status')
        self.Q_label_text_7.setText("<font color = 'Red',>Stopped</font>")
        self.Q_label_text_7.setFont(QtGui.QFont('Times', 15)) 
        self.Q_label_text_7.setAlignment(QtCore.Qt.AlignCenter)


        self.button_phase1_start = QtWidgets.QPushButton(self.page_ocr_plc_configure)
        self.button_phase1_start.setGeometry(QtCore.QRect(860, 400, 200, 50))
        self.button_phase1_start.setObjectName("Phase1 Start")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.button_phase1_start.setStyleSheet("background-color : white")
        self.button_phase1_start.setText('Phase1 Start')
        self.button_phase1_start.setFont(QtGui.QFont('Times', 15))
        self.button_phase1_start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_phase1_start.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')



        self.button_phase1_stop = QtWidgets.QPushButton(self.page_ocr_plc_configure)
        self.button_phase1_stop.setGeometry(QtCore.QRect(860, 500, 200, 50))
        self.button_phase1_stop.setObjectName("Phase1 Stop")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.button_phase1_stop.setStyleSheet("background-color : white")
        self.button_phase1_stop.setText('Phase1 Stop')
        self.button_phase1_stop.setFont(QtGui.QFont('Times', 15))
        self.button_phase1_stop.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_phase1_stop.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')


        # OCR PLC Setting
        self.Q_label_text_8 = QtWidgets.QLabel(self.page_ocr_plc_configure)
        self.Q_label_text_8.setGeometry(QtCore.QRect(1280, 150, 640, 50))
        self.Q_label_text_8.setObjectName('OCR PLC Setting')
        self.Q_label_text_8.setText("<font color = 'white'>OCR PLC Setting</font>")
        self.Q_label_text_8.setFont(QtGui.QFont('Times', 20)) 
        self.Q_label_text_8.setAlignment(QtCore.Qt.AlignCenter)        

        self.Q_label_text_9 = QtWidgets.QLabel(self.page_ocr_plc_configure)
        self.Q_label_text_9.setGeometry(QtCore.QRect(1280, 250, 640, 50))
        self.Q_label_text_9.setObjectName('PLC Connect Test Result')
        self.Q_label_text_9.setText("<font color = 'white',>PLC Connect Test Result</font>")
        self.Q_label_text_9.setFont(QtGui.QFont('Times', 15)) 
        self.Q_label_text_9.setAlignment(QtCore.Qt.AlignCenter)

        self.Q_label_ocr_connect_test_result = QtWidgets.QLabel(self.page_ocr_plc_configure)
        self.Q_label_ocr_connect_test_result.setGeometry(QtCore.QRect(1280, 300, 640, 50))
        self.Q_label_ocr_connect_test_result.setObjectName('Status')
        self.Q_label_ocr_connect_test_result.setText("<font color = 'Red',>Connect Test None</font>")
        self.Q_label_ocr_connect_test_result.setFont(QtGui.QFont('Times', 15)) 
        self.Q_label_ocr_connect_test_result.setAlignment(QtCore.Qt.AlignCenter)


        self.button_phase1_ocr_plc_connect_test = QtWidgets.QPushButton(self.page_ocr_plc_configure)
        self.button_phase1_ocr_plc_connect_test.setGeometry(QtCore.QRect(1500, 400, 200, 50))
        self.button_phase1_ocr_plc_connect_test.setObjectName("Phase1 Start")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.button_phase1_ocr_plc_connect_test.setStyleSheet("background-color : white")
        self.button_phase1_ocr_plc_connect_test.setText('PLC Connect Test')
        self.button_phase1_ocr_plc_connect_test.setFont(QtGui.QFont('Times', 15))
        self.button_phase1_ocr_plc_connect_test.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_phase1_ocr_plc_connect_test.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')


        self.Q_label_text_10 = QtWidgets.QLabel(self.page_ocr_plc_configure)
        self.Q_label_text_10.setGeometry(QtCore.QRect(1380, 500, 200, 30))
        self.Q_label_text_10.setObjectName('OCR PLC IP Address')
        self.Q_label_text_10.setText("<font color = 'white',>OCR PLC IP Address:</font>")
        self.Q_label_text_10.setFont(QtGui.QFont('Times', 15)) 
        self.Q_label_text_10.setAlignment(QtCore.Qt.AlignRight)

        self.line_edit_ocr_plc_address  = QtWidgets.QLineEdit(self.page_ocr_plc_configure)
        self.line_edit_ocr_plc_address.setGeometry(QtCore.QRect(1600,500,150,30))
        self.line_edit_ocr_plc_address.setObjectName('OCR PLC Address Setting')
        self.line_edit_ocr_plc_address.setText('192.168.3.10')
        self.line_edit_ocr_plc_address.setFont(QtGui.QFont('Times', 15)) 
        self.line_edit_ocr_plc_address.setAlignment(QtCore.Qt.AlignLeft)


        self.Q_label_text_11 = QtWidgets.QLabel(self.page_ocr_plc_configure)
        self.Q_label_text_11.setGeometry(QtCore.QRect(1280, 600, 300, 30))
        self.Q_label_text_11.setObjectName('OCR PLC Connect Type')
        self.Q_label_text_11.setText("<font color = 'white',>OCR PLC Connect Type:</font>")
        self.Q_label_text_11.setFont(QtGui.QFont('Times', 15)) 
        self.Q_label_text_11.setAlignment(QtCore.Qt.AlignRight)

        self.line_edit_ocr_plc_connect_type  = QtWidgets.QLineEdit(self.page_ocr_plc_configure)
        self.line_edit_ocr_plc_connect_type.setGeometry(QtCore.QRect(1600,600,20,30))
        self.line_edit_ocr_plc_connect_type.setObjectName('OCR PLC Connect Type')
        self.line_edit_ocr_plc_connect_type.setText('2')
        self.line_edit_ocr_plc_connect_type.setFont(QtGui.QFont('Times', 15)) 
        self.line_edit_ocr_plc_connect_type.setAlignment(QtCore.Qt.AlignLeft)
  
        # self.button_phase1_stop = QtWidgets.QPushButton(self.page_ocr_plc_configure)
        # self.button_phase1_stop.setGeometry(QtCore.QRect(860, 500, 200, 50))
        # self.button_phase1_stop.setObjectName("Phase1 Stop")
        # #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        # self.button_phase1_stop.setStyleSheet("background-color : white")
        # self.button_phase1_stop.setText('Phase1 Stop')
        # self.button_phase1_stop.setFont(QtGui.QFont('Times', 15))

        self.page_ocr_plc_configure.setAutoFillBackground(True)
        self.page_ocr_plc_configure.setPalette(palette)
        self.stackedWidget.addWidget(self.page_ocr_plc_configure)  

        '''
        堆叠区域3 Layout
        '''
        self.page_intralox_plc_configure = QtWidgets.QWidget()
        self.page_intralox_plc_configure.setObjectName("page_intralox_plc_configure")

        self.page3_text_1 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_1.setGeometry(QtCore.QRect(750, 0, 420, 50))
        self.page3_text_1.setObjectName('Intralox Plc Configure')
        self.page3_text_1.setText("<font color = 'white' >INTRALOX PLC CONFIGURE</font>")
        self.page3_text_1.setFont(QtGui.QFont('Times', 24))
        self.page3_text_1.setAlignment(QtCore.Qt.AlignCenter)



        # Intralox PLC Phase2 Module Select
        self.page3_text_2 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_2.setGeometry(QtCore.QRect(0, 100, 640, 50))
        self.page3_text_2.setObjectName('Select Intralox PLC Phase Mode')
        self.page3_text_2.setText("<font color = 'white'>Select Intralox PLC Phase Mode</font>")
        self.page3_text_2.setFont(QtGui.QFont('Times', 20)) 
        self.page3_text_2.setAlignment(QtCore.Qt.AlignCenter)

        self.page3_text_3 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_3.setGeometry(QtCore.QRect(0, 200, 640, 50))
        self.page3_text_3.setObjectName('Current Select Intralox PLC Phase Mode')
        self.page3_text_3.setText("<font color = 'white',>Current Select Intralox PLC Phase Mode</font>")
        self.page3_text_3.setFont(QtGui.QFont('Times', 15)) 
        self.page3_text_3.setAlignment(QtCore.Qt.AlignCenter)

        self.page3_phase2_status = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_phase2_status.setGeometry(QtCore.QRect(0, 250, 640, 50))
        self.page3_phase2_status.setObjectName('Current Select OCR Phase Model')
        self.page3_phase2_status.setText("<font color = 'Red',>no Phase Module Select</font>")
        self.page3_phase2_status.setFont(QtGui.QFont('Times', 15)) 
        self.page3_phase2_status.setAlignment(QtCore.Qt.AlignCenter)

        self.page3_button_phase2_select_mode_1 = QtWidgets.QPushButton(self.page_intralox_plc_configure)
        self.page3_button_phase2_select_mode_1.setGeometry(QtCore.QRect(170, 400, 300, 50))
        self.page3_button_phase2_select_mode_1.setObjectName("Simualtion With Out Intralox PLC")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.page3_button_phase2_select_mode_1.setStyleSheet("background-color : white")
        self.page3_button_phase2_select_mode_1.setText('Simualtion With Out Intralox PLC')
        self.page3_button_phase2_select_mode_1.setFont(QtGui.QFont('Times', 15))
        self.page3_button_phase2_select_mode_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.page3_button_phase2_select_mode_1.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')

        self.page3_button_phase2_select_mode_2 = QtWidgets.QPushButton(self.page_intralox_plc_configure)
        self.page3_button_phase2_select_mode_2.setGeometry(QtCore.QRect(170, 500, 300, 50))
        self.page3_button_phase2_select_mode_2.setObjectName("Simualtion With Intralox PLC")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.page3_button_phase2_select_mode_2.setStyleSheet("background-color : white")
        self.page3_button_phase2_select_mode_2.setText('Simualtion With Intralox PLC')
        self.page3_button_phase2_select_mode_2.setFont(QtGui.QFont('Times', 15))
        self.page3_button_phase2_select_mode_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.page3_button_phase2_select_mode_2.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')

        self.page3_button_phase2_select_mode_3 = QtWidgets.QPushButton(self.page_intralox_plc_configure)
        self.page3_button_phase2_select_mode_3.setGeometry(QtCore.QRect(170, 600, 300, 50))
        self.page3_button_phase2_select_mode_3.setObjectName("Production")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.page3_button_phase2_select_mode_3.setStyleSheet("background-color : white")
        self.page3_button_phase2_select_mode_3.setText('Production')
        self.page3_button_phase2_select_mode_3.setFont(QtGui.QFont('Times', 15))
        self.page3_button_phase2_select_mode_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.page3_button_phase2_select_mode_3.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')

        #Intralox PLC Phase2 Module Control
        self.page3_text_4 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_4.setGeometry(QtCore.QRect(640, 150, 640, 50))
        self.page3_text_4.setObjectName('Intralox PLC Phase Control')
        self.page3_text_4.setText("<font color = 'white'>Intralox PLC Phase Control</font>")
        self.page3_text_4.setFont(QtGui.QFont('Times', 20)) 
        self.page3_text_4.setAlignment(QtCore.Qt.AlignCenter)        

        self.page3_text_5 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_5.setGeometry(QtCore.QRect(640, 250, 640, 50))
        self.page3_text_5.setObjectName('Intralox Plc Phase Mode Status')
        self.page3_text_5.setText("<font color = 'white',>Intralox Plc Phase Mode Status</font>")
        self.page3_text_5.setFont(QtGui.QFont('Times', 15)) 
        self.page3_text_5.setAlignment(QtCore.Qt.AlignCenter)

        self.page3_text_6 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_6.setGeometry(QtCore.QRect(640, 300, 640, 50))
        self.page3_text_6.setObjectName('Status')
        self.page3_text_6.setText("<font color = 'Red',>Stopped</font>")
        self.page3_text_6.setFont(QtGui.QFont('Times', 15)) 
        self.page3_text_6.setAlignment(QtCore.Qt.AlignCenter)


        self.page3_button_phase2_start = QtWidgets.QPushButton(self.page_intralox_plc_configure)
        self.page3_button_phase2_start.setGeometry(QtCore.QRect(860, 400, 200, 50))
        self.page3_button_phase2_start.setObjectName("Phase2 Start")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.page3_button_phase2_start.setStyleSheet("background-color : white")
        self.page3_button_phase2_start.setText('Phase2 Start')
        self.page3_button_phase2_start.setFont(QtGui.QFont('Times', 15))
        self.page3_button_phase2_start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.page3_button_phase2_start.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')
        

        self.page3_button_phase2_stop = QtWidgets.QPushButton(self.page_intralox_plc_configure)
        self.page3_button_phase2_stop.setGeometry(QtCore.QRect(860, 500, 200, 50))
        self.page3_button_phase2_stop.setObjectName("Phase2 Stop")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.page3_button_phase2_stop.setStyleSheet("background-color : white")
        self.page3_button_phase2_stop.setText('Phase2 Stop')
        self.page3_button_phase2_stop.setFont(QtGui.QFont('Times', 15))
        self.page3_button_phase2_stop.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.page3_button_phase2_stop.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')

        # Intralox PLC Setting
        self.page3_text_8 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_8.setGeometry(QtCore.QRect(1280, 100, 640, 50))
        self.page3_text_8.setObjectName('OCR PLC Setting')
        self.page3_text_8.setText("<font color = 'white'>OCR PLC Setting</font>")
        self.page3_text_8.setFont(QtGui.QFont('Times', 20)) 
        self.page3_text_8.setAlignment(QtCore.Qt.AlignCenter)        

        self.page3_text_9 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_9.setGeometry(QtCore.QRect(1280, 150, 640, 30))
        self.page3_text_9.setObjectName('PLC Connect Test Result')
        self.page3_text_9.setText("<font color = 'white',>PLC Connect Test Result</font>")
        self.page3_text_9.setFont(QtGui.QFont('Times', 15)) 
        self.page3_text_9.setAlignment(QtCore.Qt.AlignCenter)

        self.page3_intralox_connect_test_result = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_intralox_connect_test_result.setGeometry(QtCore.QRect(1280, 180, 640, 50))
        self.page3_intralox_connect_test_result.setObjectName('Status')
        self.page3_intralox_connect_test_result.setText("<font color = 'Red',>Connect Test None</font>")
        self.page3_intralox_connect_test_result.setFont(QtGui.QFont('Times', 15)) 
        self.page3_intralox_connect_test_result.setAlignment(QtCore.Qt.AlignCenter)


        self.page3_button_plc_connect_test = QtWidgets.QPushButton(self.page_intralox_plc_configure)
        self.page3_button_plc_connect_test.setGeometry(QtCore.QRect(1500, 250, 200, 40))
        self.page3_button_plc_connect_test.setObjectName("Phase1 Start")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.page3_button_plc_connect_test.setStyleSheet("background-color : white")
        self.page3_button_plc_connect_test.setText('PLC Connect Test')
        self.page3_button_plc_connect_test.setFont(QtGui.QFont('Times', 15))
        self.page3_button_plc_connect_test.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.page3_button_plc_connect_test.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')


        self.page3_text_10 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_10.setGeometry(QtCore.QRect(1380, 300, 200, 30))
        self.page3_text_10.setObjectName('OCR PLC IP Address')
        self.page3_text_10.setText("<font color = 'white',>OCR PLC IP Address:</font>")
        self.page3_text_10.setFont(QtGui.QFont('Times', 15)) 
        self.page3_text_10.setAlignment(QtCore.Qt.AlignRight)

        self.page3_input_text_intralox_plc_address  = QtWidgets.QLineEdit(self.page_intralox_plc_configure)
        self.page3_input_text_intralox_plc_address.setGeometry(QtCore.QRect(1600,300,150,30))
        self.page3_input_text_intralox_plc_address.setObjectName('OCR PLC Address Setting')
        self.page3_input_text_intralox_plc_address.setText('192.168.3.10')
        self.page3_input_text_intralox_plc_address.setFont(QtGui.QFont('Times', 15)) 
        self.page3_input_text_intralox_plc_address.setAlignment(QtCore.Qt.AlignLeft)


        self.page3_text_11 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_11.setGeometry(QtCore.QRect(1280, 340, 300, 30))
        self.page3_text_11.setObjectName('OCR PLC Connect Type')
        self.page3_text_11.setText("<font color = 'white',>OCR PLC Connect Type:</font>")
        self.page3_text_11.setFont(QtGui.QFont('Times', 15)) 
        self.page3_text_11.setAlignment(QtCore.Qt.AlignRight)

        self.page3_input_text_intralox_plc_connect_type  = QtWidgets.QLineEdit(self.page_intralox_plc_configure)
        self.page3_input_text_intralox_plc_connect_type.setGeometry(QtCore.QRect(1600,340,20,30))
        self.page3_input_text_intralox_plc_connect_type.setObjectName('OCR PLC Connect Type')
        self.page3_input_text_intralox_plc_connect_type.setText('2')
        self.page3_input_text_intralox_plc_connect_type.setFont(QtGui.QFont('Times', 15)) 
        self.page3_input_text_intralox_plc_connect_type.setAlignment(QtCore.Qt.AlignLeft)

        self.page3_text_12 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_12.setGeometry(QtCore.QRect(1280, 380, 640, 30))
        self.page3_text_12.setObjectName('intralox plc send address configure')
        self.page3_text_12.setText("<font color = 'white',>PLC Recive Address Configure</font>")
        self.page3_text_12.setFont(QtGui.QFont('Times', 15)) 
        self.page3_text_12.setAlignment(QtCore.Qt.AlignCenter)

        self.page3_text_13 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_13.setGeometry(QtCore.QRect(1280, 410, 320, 25))
        self.page3_text_13.setObjectName('recive_DB_address')
        self.page3_text_13.setText("<font color = 'white',>DB Address:</font>")
        self.page3_text_13.setFont(QtGui.QFont('Times', 12)) 
        self.page3_text_13.setAlignment(QtCore.Qt.AlignRight)

        self.page3_input_text_intralox_plc_recive_DB_address  = QtWidgets.QLineEdit(self.page_intralox_plc_configure)
        self.page3_input_text_intralox_plc_recive_DB_address.setGeometry(QtCore.QRect(1600,410,50,25))
        self.page3_input_text_intralox_plc_recive_DB_address.setObjectName('recive_DB_address input')
        self.page3_input_text_intralox_plc_recive_DB_address.setText('2')
        self.page3_input_text_intralox_plc_recive_DB_address.setFont(QtGui.QFont('Times', 12)) 
        self.page3_input_text_intralox_plc_recive_DB_address.setAlignment(QtCore.Qt.AlignLeft)

        self.page3_text_14 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_14.setGeometry(QtCore.QRect(1280, 450, 300, 20))
        self.page3_text_14.setObjectName('REC SYSTEM')
        self.page3_text_14.setText("<font color = 'white',>REC SYSTEM:</font>")
        self.page3_text_14.setFont(QtGui.QFont('Times', 10)) 
        self.page3_text_14.setAlignment(QtCore.Qt.AlignRight)

        self.page3_input_text_intralox_plc_recive_REC_SYSTEM_address = QtWidgets.QLineEdit(self.page_intralox_plc_configure)
        self.page3_input_text_intralox_plc_recive_REC_SYSTEM_address.setGeometry(QtCore.QRect(1600,450,50,20))
        self.page3_input_text_intralox_plc_recive_REC_SYSTEM_address.setObjectName('REC SYSTEM')
        self.page3_input_text_intralox_plc_recive_REC_SYSTEM_address.setText('2')
        self.page3_input_text_intralox_plc_recive_REC_SYSTEM_address.setFont(QtGui.QFont('Times', 10)) 
        self.page3_input_text_intralox_plc_recive_REC_SYSTEM_address.setAlignment(QtCore.Qt.AlignLeft)

        self.page3_text_15 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_15.setGeometry(QtCore.QRect(1280, 470, 300, 20))
        self.page3_text_15.setObjectName('REC ID')
        self.page3_text_15.setText("<font color = 'white',>REC ID:</font>")
        self.page3_text_15.setFont(QtGui.QFont('Times', 10)) 
        self.page3_text_15.setAlignment(QtCore.Qt.AlignRight)

        self.page3_input_text_intralox_plc_recive_REC_ID_address  = QtWidgets.QLineEdit(self.page_intralox_plc_configure)
        self.page3_input_text_intralox_plc_recive_REC_ID_address.setGeometry(QtCore.QRect(1600,470,50,20))
        self.page3_input_text_intralox_plc_recive_REC_ID_address.setObjectName('REC ID')
        self.page3_input_text_intralox_plc_recive_REC_ID_address.setText('2')
        self.page3_input_text_intralox_plc_recive_REC_ID_address.setFont(QtGui.QFont('Times', 10)) 
        self.page3_input_text_intralox_plc_recive_REC_ID_address.setAlignment(QtCore.Qt.AlignLeft)

        self.page3_text_16 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_16.setGeometry(QtCore.QRect(1280, 490, 300, 20))
        self.page3_text_16.setObjectName('REC DESTINATION')
        self.page3_text_16.setText("<font color = 'white',>REC DESTINATION:</font>")
        self.page3_text_16.setFont(QtGui.QFont('Times', 10)) 
        self.page3_text_16.setAlignment(QtCore.Qt.AlignRight)

        self.page3_input_text_intralox_plc_recive_REC_DESTINATION_address  = QtWidgets.QLineEdit(self.page_intralox_plc_configure)
        self.page3_input_text_intralox_plc_recive_REC_DESTINATION_address.setGeometry(QtCore.QRect(1600, 490, 50, 20))
        self.page3_input_text_intralox_plc_recive_REC_DESTINATION_address.setObjectName('REC DESTINATION')
        self.page3_input_text_intralox_plc_recive_REC_DESTINATION_address.setText('2')
        self.page3_input_text_intralox_plc_recive_REC_DESTINATION_address.setFont(QtGui.QFont('Times', 10)) 
        self.page3_input_text_intralox_plc_recive_REC_DESTINATION_address.setAlignment(QtCore.Qt.AlignLeft)

        self.page3_text_17 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_17.setGeometry(QtCore.QRect(1280, 510, 300, 20))
        self.page3_text_17.setObjectName('REC DESTINATION ID')
        self.page3_text_17.setText("<font color = 'white',>REC DESTINATION ID:</font>")
        self.page3_text_17.setFont(QtGui.QFont('Times', 10)) 
        self.page3_text_17.setAlignment(QtCore.Qt.AlignRight)

        self.page3_input_text_intralox_plc_recive_REC_DESTINATION_address  = QtWidgets.QLineEdit(self.page_intralox_plc_configure)
        self.page3_input_text_intralox_plc_recive_REC_DESTINATION_address.setGeometry(QtCore.QRect(1600, 510, 50, 20))
        self.page3_input_text_intralox_plc_recive_REC_DESTINATION_address.setObjectName('REC DESTINATION ID')
        self.page3_input_text_intralox_plc_recive_REC_DESTINATION_address.setText('2')
        self.page3_input_text_intralox_plc_recive_REC_DESTINATION_address.setFont(QtGui.QFont('Times', 10)) 
        self.page3_input_text_intralox_plc_recive_REC_DESTINATION_address.setAlignment(QtCore.Qt.AlignLeft)

        self.page3_text_18 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_18.setGeometry(QtCore.QRect(1280, 550, 640, 30))
        self.page3_text_18.setObjectName('intralox plc send address configure')
        self.page3_text_18.setText("<font color = 'white',>PLC Send Address Configure</font>")
        self.page3_text_18.setFont(QtGui.QFont('Times', 15)) 
        self.page3_text_18.setAlignment(QtCore.Qt.AlignCenter)

        self.page3_text_19 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_19.setGeometry(QtCore.QRect(1280, 580, 320, 25))
        self.page3_text_19.setObjectName('Send_DB_address')
        self.page3_text_19.setText("<font color = 'white',>DB Address:</font>")
        self.page3_text_19.setFont(QtGui.QFont('Times', 12)) 
        self.page3_text_19.setAlignment(QtCore.Qt.AlignRight)

        self.page3_input_text_intralox_plc_send_DB_address  = QtWidgets.QLineEdit(self.page_intralox_plc_configure)
        self.page3_input_text_intralox_plc_send_DB_address.setGeometry(QtCore.QRect(1600, 580, 50,25))
        self.page3_input_text_intralox_plc_send_DB_address.setObjectName('Send_DB_address input')
        self.page3_input_text_intralox_plc_send_DB_address.setText('2')
        self.page3_input_text_intralox_plc_send_DB_address.setFont(QtGui.QFont('Times', 12)) 
        self.page3_input_text_intralox_plc_send_DB_address.setAlignment(QtCore.Qt.AlignLeft)

        self.page3_text_20 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_20.setGeometry(QtCore.QRect(1280, 620, 300, 20))
        self.page3_text_20.setObjectName('SEND ID PE')
        self.page3_text_20.setText("<font color = 'white',>SEND ID PE:</font>")
        self.page3_text_20.setFont(QtGui.QFont('Times', 10)) 
        self.page3_text_20.setAlignment(QtCore.Qt.AlignRight)

        self.page3_input_text_intralox_plc_send_SEND_ID_PE_address = QtWidgets.QLineEdit(self.page_intralox_plc_configure)
        self.page3_input_text_intralox_plc_send_SEND_ID_PE_address.setGeometry(QtCore.QRect(1600,620,50,20))
        self.page3_input_text_intralox_plc_send_SEND_ID_PE_address.setObjectName('SEND ID PE')
        self.page3_input_text_intralox_plc_send_SEND_ID_PE_address.setText('2')
        self.page3_input_text_intralox_plc_send_SEND_ID_PE_address.setFont(QtGui.QFont('Times', 10)) 
        self.page3_input_text_intralox_plc_send_SEND_ID_PE_address.setAlignment(QtCore.Qt.AlignLeft)

        self.page3_text_21 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_21.setGeometry(QtCore.QRect(1280, 640, 300, 20))
        self.page3_text_21.setObjectName('SORTER ID ON CHUTE')
        self.page3_text_21.setText("<font color = 'white',>SORTER ID ON CHUTE:</font>")
        self.page3_text_21.setFont(QtGui.QFont('Times', 10)) 
        self.page3_text_21.setAlignment(QtCore.Qt.AlignRight)

        self.page3_input_text_intralox_plc_send_SORTER_ID_ON_CHUTE_address  = QtWidgets.QLineEdit(self.page_intralox_plc_configure)
        self.page3_input_text_intralox_plc_send_SORTER_ID_ON_CHUTE_address.setGeometry(QtCore.QRect(1600, 640, 50, 20))
        self.page3_input_text_intralox_plc_send_SORTER_ID_ON_CHUTE_address.setObjectName('SORTER ID ON CHUTE')
        self.page3_input_text_intralox_plc_send_SORTER_ID_ON_CHUTE_address.setText('2')
        self.page3_input_text_intralox_plc_send_SORTER_ID_ON_CHUTE_address.setFont(QtGui.QFont('Times', 10)) 
        self.page3_input_text_intralox_plc_send_SORTER_ID_ON_CHUTE_address.setAlignment(QtCore.Qt.AlignLeft)

        self.page3_text_22 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_22.setGeometry(QtCore.QRect(1280, 660, 300, 20))
        self.page3_text_22.setObjectName('SORTER ID END')
        self.page3_text_22.setText("<font color = 'white',>SORTER ID END:</font>")
        self.page3_text_22.setFont(QtGui.QFont('Times', 10)) 
        self.page3_text_22.setAlignment(QtCore.Qt.AlignRight)

        self.page3_input_text_intralox_plc_send_SORTER_ID_END_address  = QtWidgets.QLineEdit(self.page_intralox_plc_configure)
        self.page3_input_text_intralox_plc_send_SORTER_ID_END_address.setGeometry(QtCore.QRect(1600, 660, 50, 20))
        self.page3_input_text_intralox_plc_send_SORTER_ID_END_address.setObjectName('SORTER ID END')
        self.page3_input_text_intralox_plc_send_SORTER_ID_END_address.setText('2')
        self.page3_input_text_intralox_plc_send_SORTER_ID_END_address.setFont(QtGui.QFont('Times', 10)) 
        self.page3_input_text_intralox_plc_send_SORTER_ID_END_address.setAlignment(QtCore.Qt.AlignLeft)

        self.page3_text_23 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_23.setGeometry(QtCore.QRect(1280, 680, 300, 20))
        self.page3_text_23.setObjectName('SEND PACKAGESTATUS')
        self.page3_text_23.setText("<font color = 'white',>SEND PACKAGESTATUS:</font>")
        self.page3_text_23.setFont(QtGui.QFont('Times', 10)) 
        self.page3_text_23.setAlignment(QtCore.Qt.AlignRight)

        self.page3_input_text_intralox_plc_send_SEND_PACKAGESTATUS_address  = QtWidgets.QLineEdit(self.page_intralox_plc_configure)
        self.page3_input_text_intralox_plc_send_SEND_PACKAGESTATUS_address.setGeometry(QtCore.QRect(1600, 680, 50, 20))
        self.page3_input_text_intralox_plc_send_SEND_PACKAGESTATUS_address.setObjectName('SEND PACKAGESTATUS')
        self.page3_input_text_intralox_plc_send_SEND_PACKAGESTATUS_address.setText('2')
        self.page3_input_text_intralox_plc_send_SEND_PACKAGESTATUS_address.setFont(QtGui.QFont('Times', 10)) 
        self.page3_input_text_intralox_plc_send_SEND_PACKAGESTATUS_address.setAlignment(QtCore.Qt.AlignLeft)

        self.page3_text_24 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_24.setGeometry(QtCore.QRect(1280, 700, 300, 20))
        self.page3_text_24.setObjectName('SEND SORTERSTATUS')
        self.page3_text_24.setText("<font color = 'white',>SEND SORTERSTATUS:</font>")
        self.page3_text_24.setFont(QtGui.QFont('Times', 10)) 
        self.page3_text_24.setAlignment(QtCore.Qt.AlignRight)

        self.page3_input_text_intralox_plc_send_SEND_SORTERSTATUS_address  = QtWidgets.QLineEdit(self.page_intralox_plc_configure)
        self.page3_input_text_intralox_plc_send_SEND_SORTERSTATUS_address.setGeometry(QtCore.QRect(1600, 700, 50, 20))
        self.page3_input_text_intralox_plc_send_SEND_SORTERSTATUS_address.setObjectName('SEND SORTERSTATUS')
        self.page3_input_text_intralox_plc_send_SEND_SORTERSTATUS_address.setText('2')
        self.page3_input_text_intralox_plc_send_SEND_SORTERSTATUS_address.setFont(QtGui.QFont('Times', 10)) 
        self.page3_input_text_intralox_plc_send_SEND_SORTERSTATUS_address.setAlignment(QtCore.Qt.AlignLeft)

        self.page3_text_25 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_25.setGeometry(QtCore.QRect(1280, 720, 300, 20))
        self.page3_text_25.setObjectName('SEND SORTERFAULT')
        self.page3_text_25.setText("<font color = 'white',>SEND SORTERFAULT:</font>")
        self.page3_text_25.setFont(QtGui.QFont('Times', 10)) 
        self.page3_text_25.setAlignment(QtCore.Qt.AlignRight)

        self.page3_input_text_intralox_plc_send_SEND_SORTERFAULT_address  = QtWidgets.QLineEdit(self.page_intralox_plc_configure)
        self.page3_input_text_intralox_plc_send_SEND_SORTERFAULT_address.setGeometry(QtCore.QRect(1600, 720, 50, 20))
        self.page3_input_text_intralox_plc_send_SEND_SORTERFAULT_address.setObjectName('SEND SORTERFAULT')
        self.page3_input_text_intralox_plc_send_SEND_SORTERFAULT_address.setText('2')
        self.page3_input_text_intralox_plc_send_SEND_SORTERFAULT_address.setFont(QtGui.QFont('Times', 10)) 
        self.page3_input_text_intralox_plc_send_SEND_SORTERFAULT_address.setAlignment(QtCore.Qt.AlignLeft)

        self.page3_text_26 = QtWidgets.QLabel(self.page_intralox_plc_configure)
        self.page3_text_26.setGeometry(QtCore.QRect(1280, 740, 300, 20))
        self.page3_text_26.setObjectName('SEND LANE_OPEN')
        self.page3_text_26.setText("<font color = 'white',>SEND LANE OPEN:</font>")
        self.page3_text_26.setFont(QtGui.QFont('Times', 10)) 
        self.page3_text_26.setAlignment(QtCore.Qt.AlignRight)

        self.page3_input_text_intralox_plc_send_SEND_SORTERFAULT_address  = QtWidgets.QLineEdit(self.page_intralox_plc_configure)
        self.page3_input_text_intralox_plc_send_SEND_SORTERFAULT_address.setGeometry(QtCore.QRect(1600, 740, 50, 20))
        self.page3_input_text_intralox_plc_send_SEND_SORTERFAULT_address.setObjectName('SEND LANE OPEN')
        self.page3_input_text_intralox_plc_send_SEND_SORTERFAULT_address.setText('2')
        self.page3_input_text_intralox_plc_send_SEND_SORTERFAULT_address.setFont(QtGui.QFont('Times', 10)) 
        self.page3_input_text_intralox_plc_send_SEND_SORTERFAULT_address.setAlignment(QtCore.Qt.AlignLeft)
        


        self.page_intralox_plc_configure.setAutoFillBackground(True)
        self.page_intralox_plc_configure.setPalette(palette)
        self.stackedWidget.addWidget(self.page_intralox_plc_configure)  


        '''
        堆叠区域4 Layout
        '''
        self.page_ai_ocr_module_configure = QtWidgets.QWidget()
        self.page_ai_ocr_module_configure.setObjectName("page_ai_ocr_module_configure")

        self.page4_text_1 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_1.setGeometry(QtCore.QRect(750, 0, 420, 50))
        self.page4_text_1.setObjectName('Intralox Plc Configure')
        self.page4_text_1.setText("<font color = 'white' >OCR AI MODULE CONFIGURE</font>")
        self.page4_text_1.setFont(QtGui.QFont('Times', 24))
        self.page4_text_1.setAlignment(QtCore.Qt.AlignCenter)

        # OCR Phase1 Module Select
        self.page4_text_2 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_2.setGeometry(QtCore.QRect(0, 100, 640, 50))
        self.page4_text_2.setObjectName('Select OCR Phase Model')
        self.page4_text_2.setText("<font color = 'white'>Select OCR AI Phase Model</font>")
        self.page4_text_2.setFont(QtGui.QFont('Times', 20)) 
        self.page4_text_2.setAlignment(QtCore.Qt.AlignCenter)

        self.page4_text_3 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_3.setGeometry(QtCore.QRect(0, 200, 640, 50))
        self.page4_text_3.setObjectName('Current Select OCR Phase Model')
        self.page4_text_3.setText("<font color = 'white',>Current Selected OCR AI Phase Run Mode</font>")
        self.page4_text_3.setFont(QtGui.QFont('Times', 15)) 
        self.page4_text_3.setAlignment(QtCore.Qt.AlignCenter)

        self.page4_phase2_status = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_phase2_status.setGeometry(QtCore.QRect(0, 250, 640, 50))
        self.page4_phase2_status.setObjectName('Current Select OCR Phase Model')
        self.page4_phase2_status.setText("<font color = 'Red',>no Phase Module Select</font>")
        self.page4_phase2_status.setFont(QtGui.QFont('Times', 15)) 
        self.page4_phase2_status.setAlignment(QtCore.Qt.AlignCenter)

        self.page4_button_phase2_select_mode_1 = QtWidgets.QPushButton(self.page_ai_ocr_module_configure)
        self.page4_button_phase2_select_mode_1.setGeometry(QtCore.QRect(170, 400, 300, 50))
        self.page4_button_phase2_select_mode_1.setObjectName("Simualtion With Out AI Module")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.page4_button_phase2_select_mode_1.setStyleSheet("background-color : white")
        self.page4_button_phase2_select_mode_1.setText('Simualtion With Out AI Module')
        self.page4_button_phase2_select_mode_1.setFont(QtGui.QFont('Times', 15))
        self.page4_button_phase2_select_mode_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.page4_button_phase2_select_mode_1.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')


        self.page4_button_phase2_select_mode_2 = QtWidgets.QPushButton(self.page_ai_ocr_module_configure)
        self.page4_button_phase2_select_mode_2.setGeometry(QtCore.QRect(170, 500, 300, 50))
        self.page4_button_phase2_select_mode_2.setObjectName("Simualtion With AI")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.page4_button_phase2_select_mode_2.setStyleSheet("background-color : white")
        self.page4_button_phase2_select_mode_2.setText('Simualtion With AI Module')
        self.page4_button_phase2_select_mode_2.setFont(QtGui.QFont('Times', 15))
        self.page4_button_phase2_select_mode_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.page4_button_phase2_select_mode_2.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')

        self.page4_button_phase2_select_mode_3 = QtWidgets.QPushButton(self.page_ai_ocr_module_configure)
        self.page4_button_phase2_select_mode_3.setGeometry(QtCore.QRect(170, 600, 300, 50))
        self.page4_button_phase2_select_mode_3.setObjectName("Production")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.page4_button_phase2_select_mode_3.setStyleSheet("background-color : white")
        self.page4_button_phase2_select_mode_3.setText('Production')
        self.page4_button_phase2_select_mode_3.setFont(QtGui.QFont('Times', 15))
        self.page4_button_phase2_select_mode_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.page4_button_phase2_select_mode_3.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')

        #Intralox PLC Phase2 Module Control
        self.page4_text_4 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_4.setGeometry(QtCore.QRect(640, 150, 640, 50))
        self.page4_text_4.setObjectName('Intralox PLC Phase Control')
        self.page4_text_4.setText("<font color = 'white'>OCR AI Module Phase Control</font>")
        self.page4_text_4.setFont(QtGui.QFont('Times', 20)) 
        self.page4_text_4.setAlignment(QtCore.Qt.AlignCenter)        

        self.page4_text_5 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_5.setGeometry(QtCore.QRect(640, 250, 640, 50))
        self.page4_text_5.setObjectName('Intralox Plc Phase Mode Status')
        self.page4_text_5.setText("<font color = 'white',>OCR AI Module Phase Mode Status</font>")
        self.page4_text_5.setFont(QtGui.QFont('Times', 15)) 
        self.page4_text_5.setAlignment(QtCore.Qt.AlignCenter)

        self.page4_text_6 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_6.setGeometry(QtCore.QRect(640, 300, 640, 50))
        self.page4_text_6.setObjectName('Status')
        self.page4_text_6.setText("<font color = 'Red',>Stopped</font>")
        self.page4_text_6.setFont(QtGui.QFont('Times', 15)) 
        self.page4_text_6.setAlignment(QtCore.Qt.AlignCenter)


        self.page4_button_phase2_start = QtWidgets.QPushButton(self.page_ai_ocr_module_configure)
        self.page4_button_phase2_start.setGeometry(QtCore.QRect(860, 400, 200, 50))
        self.page4_button_phase2_start.setObjectName("Phase2 Start")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.page4_button_phase2_start.setStyleSheet("background-color : white")
        self.page4_button_phase2_start.setText('Phase2 Start')
        self.page4_button_phase2_start.setFont(QtGui.QFont('Times', 15))
        self.page4_button_phase2_start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.page4_button_phase2_start.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')
       
        self.page4_button_phase2_stop = QtWidgets.QPushButton(self.page_ai_ocr_module_configure)
        self.page4_button_phase2_stop.setGeometry(QtCore.QRect(860, 500, 200, 50))
        self.page4_button_phase2_stop.setObjectName("Phase2 Stop")
        #self.pushButton2.setAlignment(QtCore.Qt.AlignCenter) 
        self.page4_button_phase2_stop.setStyleSheet("background-color : white")
        self.page4_button_phase2_stop.setText('Phase2 Stop')
        self.page4_button_phase2_stop.setFont(QtGui.QFont('Times', 15))
        self.page4_button_phase2_stop.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.page4_button_phase2_stop.setStyleSheet('QPushButton{background-color: white; border-radius: 5px;}')

        # OCR AI Setting
        self.page4_text_8 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_8.setGeometry(QtCore.QRect(1280, 100, 640, 50))
        self.page4_text_8.setObjectName('OCR AI Setting')
        self.page4_text_8.setText("<font color = 'white'>OCR AI Setting</font>")
        self.page4_text_8.setFont(QtGui.QFont('Times', 20)) 
        self.page4_text_8.setAlignment(QtCore.Qt.AlignCenter)        

        self.page4_text_9 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_9.setGeometry(QtCore.QRect(1280, 150, 640, 30))
        self.page4_text_9.setObjectName('OCR AI MODEL SETTING')
        self.page4_text_9.setText("<font color = 'white',>OCR AI MODEL SETTING</font>")
        self.page4_text_9.setFont(QtGui.QFont('Times', 15)) 
        self.page4_text_9.setAlignment(QtCore.Qt.AlignCenter)

        self.page4_text_10 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_10.setGeometry(QtCore.QRect(1300, 190, 200, 25))
        self.page4_text_10.setObjectName('Model_File_Path')
        self.page4_text_10.setText("<font color = 'white',>Model File Path:</font>")
        self.page4_text_10.setFont(QtGui.QFont('Times', 12)) 
        self.page4_text_10.setAlignment(QtCore.Qt.AlignRight)

        self.page4_input_text_model_file_path  = QtWidgets.QLineEdit(self.page_ai_ocr_module_configure)
        self.page4_input_text_model_file_path.setGeometry(QtCore.QRect(1500, 190, 250, 25))
        self.page4_input_text_model_file_path.setObjectName('Model_File_Path')
        self.page4_input_text_model_file_path.setText('ocr_ai_fodler/module/model_final.pth')
        self.page4_input_text_model_file_path.setFont(QtGui.QFont('Times', 10)) 
        self.page4_input_text_model_file_path.setAlignment(QtCore.Qt.AlignLeft)
        self.page4_input_text_model_file_path.setAlignment(QtCore.Qt.AlignVCenter)

        self.page4_text_11 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_11.setGeometry(QtCore.QRect(1200, 215, 300, 25))
        self.page4_text_11.setObjectName('Model_Batch_Size')
        self.page4_text_11.setText("<font color = 'white',>Model Batch Size:</font>")
        self.page4_text_11.setFont(QtGui.QFont('Times', 12)) 
        self.page4_text_11.setAlignment(QtCore.Qt.AlignRight)

        self.page4_input_text_Model_Batch_Size  = QtWidgets.QLineEdit(self.page_ai_ocr_module_configure)
        self.page4_input_text_Model_Batch_Size.setGeometry(QtCore.QRect(1500,215,60,25))
        self.page4_input_text_Model_Batch_Size.setObjectName('Model_Batch_Size')
        self.page4_input_text_Model_Batch_Size.setText('32')
        self.page4_input_text_Model_Batch_Size.setFont(QtGui.QFont('Times', 12)) 
        self.page4_input_text_Model_Batch_Size.setAlignment(QtCore.Qt.AlignLeft)

        self.page4_text_12 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_12.setGeometry(QtCore.QRect(1200, 240, 300, 30))
        self.page4_text_12.setObjectName('Model_Anchor_Size')
        self.page4_text_12.setText("<font color = 'white',>Model Anchor Size:</font>")
        self.page4_text_12.setFont(QtGui.QFont('Times', 12)) 
        self.page4_text_12.setAlignment(QtCore.Qt.AlignVCenter)
        self.page4_text_12.setAlignment(QtCore.Qt.AlignRight)

        self.page4_input_text_Model_Anchor_Size  = QtWidgets.QLineEdit(self.page_ai_ocr_module_configure)
        self.page4_input_text_Model_Anchor_Size.setGeometry(QtCore.QRect(1500 ,240, 240, 25))
        self.page4_input_text_Model_Anchor_Size.setObjectName('Model_Batch_Size')
        self.page4_input_text_Model_Anchor_Size.setText('32, 64, 128, 256, 512')
        self.page4_input_text_Model_Anchor_Size.setFont(QtGui.QFont('Times', 11)) 
        self.page4_input_text_Model_Batch_Size.setAlignment(QtCore.Qt.AlignLeft)

        self.page4_text_13 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_13.setGeometry(QtCore.QRect(1200, 265, 300, 25))
        self.page4_text_13.setObjectName('Model_Anchor_Ratio')
        self.page4_text_13.setText("<font color = 'white',>Model Anchor Ratio:</font>")
        self.page4_text_13.setFont(QtGui.QFont('Times', 12)) 
        self.page4_text_13.setAlignment(QtCore.Qt.AlignRight)

        self.page4_input_text_model_anchor_ratios = QtWidgets.QLineEdit(self.page_ai_ocr_module_configure)
        self.page4_input_text_model_anchor_ratios.setGeometry(QtCore.QRect(1500, 265, 250, 25))
        self.page4_input_text_model_anchor_ratios.setObjectName('Model_Anchor_Ratio')
        self.page4_input_text_model_anchor_ratios.setText('0.1, 0.15, 0.2, 0.25, 0.33')
        self.page4_input_text_model_anchor_ratios.setFont(QtGui.QFont('Times', 11)) 
        self.page4_input_text_model_anchor_ratios.setAlignment(QtCore.Qt.AlignLeft)

        self.page4_text_14 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_14.setGeometry(QtCore.QRect(1200, 290, 300, 25))
        self.page4_text_14.setObjectName('Num_Classes')
        self.page4_text_14.setText("<font color = 'white',>Num Classes:</font>")
        self.page4_text_14.setFont(QtGui.QFont('Times', 12)) 
        self.page4_text_14.setAlignment(QtCore.Qt.AlignRight)

        self.page4_input_text_ai_ocr_model_setting_num_classes = QtWidgets.QLineEdit(self.page_ai_ocr_module_configure)
        self.page4_input_text_ai_ocr_model_setting_num_classes.setGeometry(QtCore.QRect(1500,290,50,25))
        self.page4_input_text_ai_ocr_model_setting_num_classes.setObjectName('Num Classes')
        self.page4_input_text_ai_ocr_model_setting_num_classes.setText('3')
        self.page4_input_text_ai_ocr_model_setting_num_classes.setFont(QtGui.QFont('Times', 11)) 
        self.page4_input_text_ai_ocr_model_setting_num_classes.setAlignment(QtCore.Qt.AlignLeft)

        self.page4_text_15 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_15.setGeometry(QtCore.QRect(1200, 315, 300, 25))
        self.page4_text_15.setObjectName('Accept Score')
        self.page4_text_15.setText("<font color = 'white',>Accept Score:</font>")
        self.page4_text_15.setFont(QtGui.QFont('Times', 12)) 
        self.page4_text_15.setAlignment(QtCore.Qt.AlignRight)

        self.page4_input_text_ai_ocr_model_setting_accept_score  = QtWidgets.QLineEdit(self.page_ai_ocr_module_configure)
        self.page4_input_text_ai_ocr_model_setting_accept_score.setGeometry(QtCore.QRect(1500, 315, 50, 25))
        self.page4_input_text_ai_ocr_model_setting_accept_score.setObjectName('Accept Score')
        self.page4_input_text_ai_ocr_model_setting_accept_score.setText('0.65')
        self.page4_input_text_ai_ocr_model_setting_accept_score.setFont(QtGui.QFont('Times', 11)) 
        self.page4_input_text_ai_ocr_model_setting_accept_score.setAlignment(QtCore.Qt.AlignLeft)

        self.page4_text_16 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_16.setGeometry(QtCore.QRect(1200, 340, 300, 25))
        self.page4_text_16.setObjectName('CUDA or CPU')
        self.page4_text_16.setText("<font color = 'white',>CUDA or CPU:</font>")
        self.page4_text_16.setFont(QtGui.QFont('Times', 12)) 
        self.page4_text_16.setAlignment(QtCore.Qt.AlignRight)

        self.page4_input_text_ai_ocr_model_setting_cuda_or_cpu  = QtWidgets.QLineEdit(self.page_ai_ocr_module_configure)
        self.page4_input_text_ai_ocr_model_setting_cuda_or_cpu.setGeometry(QtCore.QRect(1500, 340, 75, 25))
        self.page4_input_text_ai_ocr_model_setting_cuda_or_cpu.setObjectName('CUDA or CPU')
        self.page4_input_text_ai_ocr_model_setting_cuda_or_cpu.setText('cuda')
        self.page4_input_text_ai_ocr_model_setting_cuda_or_cpu.setFont(QtGui.QFont('Times', 11)) 
        self.page4_input_text_ai_ocr_model_setting_cuda_or_cpu.setAlignment(QtCore.Qt.AlignLeft)

        self.page4_other_settings = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_other_settings.setGeometry(QtCore.QRect(1280, 380, 640, 30))
        self.page4_other_settings.setObjectName('OCR AI PIC SAVE SETTING')
        self.page4_other_settings.setText("<font color = 'white',>OCR AI PIC SAVE SETTING</font>")
        self.page4_other_settings.setFont(QtGui.QFont('Times', 15)) 
        self.page4_other_settings.setAlignment(QtCore.Qt.AlignCenter)
       
        self.page4_text_17 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_17.setGeometry(QtCore.QRect(1200, 420, 300, 25))
        self.page4_text_17.setObjectName('SAVE RAW IAMGE')
        self.page4_text_17.setText("<font color = 'white'>SAVE RAW IAMGE:</font>")
        self.page4_text_17.setFont(QtGui.QFont('Times', 12)) 
        self.page4_text_17.setAlignment(QtCore.Qt.AlignRight)

        self.page4_input_text_ai_ocr_model_setting_save_raw_image_enable  = QtWidgets.QLineEdit(self.page_ai_ocr_module_configure)
        self.page4_input_text_ai_ocr_model_setting_save_raw_image_enable.setGeometry(QtCore.QRect(1500, 420, 50, 25))
        self.page4_input_text_ai_ocr_model_setting_save_raw_image_enable.setObjectName('SAVE RAW IAMGE')
        self.page4_input_text_ai_ocr_model_setting_save_raw_image_enable.setText('1')
        self.page4_input_text_ai_ocr_model_setting_save_raw_image_enable.setFont(QtGui.QFont('Times', 11)) 
        self.page4_input_text_ai_ocr_model_setting_save_raw_image_enable.setAlignment(QtCore.Qt.AlignLeft)

        self.page4_text_18 = QtWidgets.QLabel(self.page_ai_ocr_module_configure)
        self.page4_text_18.setGeometry(QtCore.QRect(1200, 445, 300, 25))
        self.page4_text_18.setObjectName('SAVE RESULT IAMGE')
        self.page4_text_18.setText("<font color = 'white',>SAVE RESULT IAMGE:</font>")
        self.page4_text_18.setFont(QtGui.QFont('Times', 12)) 
        self.page4_text_18.setAlignment(QtCore.Qt.AlignRight)

        self.page4_input_text_ai_ocr_model_setting_save_result_image_enable  = QtWidgets.QLineEdit(self.page_ai_ocr_module_configure)
        self.page4_input_text_ai_ocr_model_setting_save_result_image_enable.setGeometry(QtCore.QRect(1500, 445, 50,25))
        self.page4_input_text_ai_ocr_model_setting_save_result_image_enable.setObjectName('SAVE RESULT IAMGE')
        self.page4_input_text_ai_ocr_model_setting_save_result_image_enable.setText('1')
        self.page4_input_text_ai_ocr_model_setting_save_result_image_enable.setFont(QtGui.QFont('Times', 11)) 
        self.page4_input_text_ai_ocr_model_setting_save_result_image_enable.setAlignment(QtCore.Qt.AlignLeft)

        self.page_ai_ocr_module_configure.setAutoFillBackground(True)
        self.page_ai_ocr_module_configure.setPalette(palette)
        self.stackedWidget.addWidget(self.page_ai_ocr_module_configure)  

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
       
    def retranslateUi(self, MainWindow):

        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(_translate("MainWindow", "P&G Deadpile Project"))
        