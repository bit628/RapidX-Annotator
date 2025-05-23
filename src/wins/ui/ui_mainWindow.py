# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'en\ui_mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1755, 1500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMouseTracking(False)
        MainWindow.setWindowTitle("")
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("QWidget {color: rgb(187, 187, 187);}\n"
"QWidget {background-color: rgb(60, 63, 65);}\n"
"QGraphicsView {background-color: rgb(43, 43, 43);}\n"
"QDockWidget {background-color: rgb(100,100,100);}\n"
"QPushButton {background-color: rgb(100,100,100);}\n"
"QPushButton:pressed {background-color: rgb(43, 43, 43);}\n"
"QPushButton:checked {background-color: rgb(43, 43, 43);}\n"
"QComboBox {border: 1px solid rgb(100,100,100);}\n"
"QLineEdit {border: 1px solid rgb(100,100,100);}\n"
"QGroupBox {border: 2px solid rgb(100,100,100);padding:10 0 0 0px;}")
        MainWindow.setIconSize(QtCore.QSize(30, 30))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.graphicsView_1 = QtWidgets.QGraphicsView(self.splitter)
        self.graphicsView_1.setMouseTracking(True)
        self.graphicsView_1.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.graphicsView_1.setAcceptDrops(True)
        self.graphicsView_1.setStyleSheet("")
        self.graphicsView_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView_1.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.graphicsView_1.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.graphicsView_1.setObjectName("graphicsView_1")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.splitter)
        self.graphicsView_2.setMouseTracking(True)
        self.graphicsView_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.graphicsView_2.setAcceptDrops(True)
        self.graphicsView_2.setStyleSheet("")
        self.graphicsView_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView_2.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.graphicsView_2.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.verticalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1755, 26))
        self.menubar.setStyleSheet("")
        self.menubar.setObjectName("menubar")
        self.menu_system = QtWidgets.QMenu(self.menubar)
        self.menu_system.setStyleSheet("background-color: rgb(80, 83, 85);\n"
"selection-background-color: rgb(100, 103, 105);")
        self.menu_system.setObjectName("menu_system")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setStyleSheet("background-color: rgb(80, 83, 85);\n"
"selection-background-color: rgb(100, 103, 105);")
        self.menu_file.setObjectName("menu_file")
        self.menu_look = QtWidgets.QMenu(self.menubar)
        self.menu_look.setStyleSheet("background-color: rgb(80, 83, 85);\n"
"selection-background-color: rgb(100, 103, 105);")
        self.menu_look.setObjectName("menu_look")
        self.menu_module = QtWidgets.QMenu(self.menubar)
        self.menu_module.setStyleSheet("background-color: rgb(80, 83, 85);\n"
"selection-background-color: rgb(100, 103, 105);")
        self.menu_module.setObjectName("menu_module")
        self.menu_7 = QtWidgets.QMenu(self.menu_module)
        self.menu_7.setObjectName("menu_7")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar_file = QtWidgets.QToolBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar_file.sizePolicy().hasHeightForWidth())
        self.toolBar_file.setSizePolicy(sizePolicy)
        self.toolBar_file.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar_file.setStyleSheet("border-color: rgb(0, 0, 0);")
        self.toolBar_file.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar_file.setObjectName("toolBar_file")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_file)
        self.toolBar_look = QtWidgets.QToolBar(MainWindow)
        self.toolBar_look.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar_look.setStyleSheet("border-color: rgb(0, 0, 0);")
        self.toolBar_look.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar_look.setObjectName("toolBar_look")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar_look)
        self.toolBar_label = QtWidgets.QToolBar(MainWindow)
        self.toolBar_label.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar_label.setStyleSheet("border-color: rgb(0, 0, 0);")
        self.toolBar_label.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar_label.setObjectName("toolBar_label")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_label)
        self.toolBar_predict = QtWidgets.QToolBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar_predict.sizePolicy().hasHeightForWidth())
        self.toolBar_predict.setSizePolicy(sizePolicy)
        self.toolBar_predict.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar_predict.setStyleSheet("border-color: rgb(0, 0, 0);")
        self.toolBar_predict.setIconSize(QtCore.QSize(30, 30))
        self.toolBar_predict.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar_predict.setObjectName("toolBar_predict")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_predict)
        self.dockWidget_label = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_label.setStyleSheet("")
        self.dockWidget_label.setObjectName("dockWidget_label")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.scrollArea_label = QtWidgets.QScrollArea(self.dockWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_label.sizePolicy().hasHeightForWidth())
        self.scrollArea_label.setSizePolicy(sizePolicy)
        self.scrollArea_label.setMinimumSize(QtCore.QSize(550, 0))
        self.scrollArea_label.setWidgetResizable(True)
        self.scrollArea_label.setObjectName("scrollArea_label")
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 548, 641))
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.verticalLayout_30 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_5)
        self.verticalLayout_30.setObjectName("verticalLayout_30")
        self.groupBox_301 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_301.sizePolicy().hasHeightForWidth())
        self.groupBox_301.setSizePolicy(sizePolicy)
        self.groupBox_301.setObjectName("groupBox_301")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_301)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.checkBox_difficult = QtWidgets.QCheckBox(self.groupBox_301)
        self.checkBox_difficult.setObjectName("checkBox_difficult")
        self.verticalLayout_9.addWidget(self.checkBox_difficult)
        self.checkBox_save_image = QtWidgets.QCheckBox(self.groupBox_301)
        self.checkBox_save_image.setObjectName("checkBox_save_image")
        self.verticalLayout_9.addWidget(self.checkBox_save_image)
        self.checkBox_preset = QtWidgets.QCheckBox(self.groupBox_301)
        self.checkBox_preset.setObjectName("checkBox_preset")
        self.verticalLayout_9.addWidget(self.checkBox_preset)
        self.checkBox_auto_rotate = QtWidgets.QCheckBox(self.groupBox_301)
        self.checkBox_auto_rotate.setObjectName("checkBox_auto_rotate")
        self.verticalLayout_9.addWidget(self.checkBox_auto_rotate)
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.label_301 = QtWidgets.QLabel(self.groupBox_301)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_301.sizePolicy().hasHeightForWidth())
        self.label_301.setSizePolicy(sizePolicy)
        self.label_301.setObjectName("label_301")
        self.horizontalLayout_28.addWidget(self.label_301)
        self.comboBox_preset_label = QtWidgets.QComboBox(self.groupBox_301)
        self.comboBox_preset_label.setStyleSheet("")
        self.comboBox_preset_label.setObjectName("comboBox_preset_label")
        self.horizontalLayout_28.addWidget(self.comboBox_preset_label)
        self.verticalLayout_9.addLayout(self.horizontalLayout_28)
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.lineEdit_select_label_file = QtWidgets.QLineEdit(self.groupBox_301)
        self.lineEdit_select_label_file.setObjectName("lineEdit_select_label_file")
        self.horizontalLayout_29.addWidget(self.lineEdit_select_label_file)
        self.button_select_label_file = QtWidgets.QPushButton(self.groupBox_301)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_select_label_file.sizePolicy().hasHeightForWidth())
        self.button_select_label_file.setSizePolicy(sizePolicy)
        self.button_select_label_file.setMinimumSize(QtCore.QSize(0, 0))
        self.button_select_label_file.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_select_label_file.setIconSize(QtCore.QSize(32, 32))
        self.button_select_label_file.setObjectName("button_select_label_file")
        self.horizontalLayout_29.addWidget(self.button_select_label_file)
        self.button_jump_label_file = QtWidgets.QPushButton(self.groupBox_301)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_jump_label_file.sizePolicy().hasHeightForWidth())
        self.button_jump_label_file.setSizePolicy(sizePolicy)
        self.button_jump_label_file.setMinimumSize(QtCore.QSize(0, 0))
        self.button_jump_label_file.setIconSize(QtCore.QSize(32, 32))
        self.button_jump_label_file.setObjectName("button_jump_label_file")
        self.horizontalLayout_29.addWidget(self.button_jump_label_file)
        self.verticalLayout_9.addLayout(self.horizontalLayout_29)
        self.verticalLayout_30.addWidget(self.groupBox_301)
        self.groupBox_410 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_410.sizePolicy().hasHeightForWidth())
        self.groupBox_410.setSizePolicy(sizePolicy)
        self.groupBox_410.setObjectName("groupBox_410")
        self.verticalLayout_53 = QtWidgets.QVBoxLayout(self.groupBox_410)
        self.verticalLayout_53.setObjectName("verticalLayout_53")
        self.listView_dir_files = QtWidgets.QListView(self.groupBox_410)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_dir_files.sizePolicy().hasHeightForWidth())
        self.listView_dir_files.setSizePolicy(sizePolicy)
        self.listView_dir_files.setMinimumSize(QtCore.QSize(0, 0))
        self.listView_dir_files.setObjectName("listView_dir_files")
        self.verticalLayout_53.addWidget(self.listView_dir_files)
        self.verticalLayout_30.addWidget(self.groupBox_410)
        self.scrollArea_label.setWidget(self.scrollAreaWidgetContents_5)
        self.verticalLayout_8.addWidget(self.scrollArea_label)
        self.dockWidget_label.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_label)
        self.dockWidget_predict = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_predict.setStyleSheet("")
        self.dockWidget_predict.setObjectName("dockWidget_predict")
        self.dockWidgetContents_4 = QtWidgets.QWidget()
        self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.dockWidgetContents_4)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.scrollArea_predict = QtWidgets.QScrollArea(self.dockWidgetContents_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_predict.sizePolicy().hasHeightForWidth())
        self.scrollArea_predict.setSizePolicy(sizePolicy)
        self.scrollArea_predict.setMinimumSize(QtCore.QSize(550, 0))
        self.scrollArea_predict.setWidgetResizable(True)
        self.scrollArea_predict.setObjectName("scrollArea_predict")
        self.scrollAreaWidgetContents_6 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_6.setGeometry(QtCore.QRect(0, 0, 548, 641))
        self.scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_405 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_405.sizePolicy().hasHeightForWidth())
        self.groupBox_405.setSizePolicy(sizePolicy)
        self.groupBox_405.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_405.setObjectName("groupBox_405")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_405)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_419 = QtWidgets.QLabel(self.groupBox_405)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_419.sizePolicy().hasHeightForWidth())
        self.label_419.setSizePolicy(sizePolicy)
        self.label_419.setObjectName("label_419")
        self.horizontalLayout_2.addWidget(self.label_419)
        self.comboBox_model = QtWidgets.QComboBox(self.groupBox_405)
        self.comboBox_model.setObjectName("comboBox_model")
        self.comboBox_model.addItem("")
        self.comboBox_model.addItem("")
        self.comboBox_model.addItem("")
        self.comboBox_model.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox_model)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.label_418 = QtWidgets.QLabel(self.groupBox_405)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_418.sizePolicy().hasHeightForWidth())
        self.label_418.setSizePolicy(sizePolicy)
        self.label_418.setObjectName("label_418")
        self.horizontalLayout_30.addWidget(self.label_418)
        self.lineEdit_file_path = QtWidgets.QLineEdit(self.groupBox_405)
        self.lineEdit_file_path.setObjectName("lineEdit_file_path")
        self.horizontalLayout_30.addWidget(self.lineEdit_file_path)
        self.button_select_file_path = QtWidgets.QPushButton(self.groupBox_405)
        self.button_select_file_path.setIconSize(QtCore.QSize(32, 32))
        self.button_select_file_path.setObjectName("button_select_file_path")
        self.horizontalLayout_30.addWidget(self.button_select_file_path)
        self.verticalLayout_2.addLayout(self.horizontalLayout_30)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_batch_predict = QtWidgets.QPushButton(self.groupBox_405)
        self.button_batch_predict.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_batch_predict.setStyleSheet("")
        self.button_batch_predict.setCheckable(True)
        self.button_batch_predict.setObjectName("button_batch_predict")
        self.horizontalLayout.addWidget(self.button_batch_predict)
        self.button_save_predict_results = QtWidgets.QPushButton(self.groupBox_405)
        self.button_save_predict_results.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_save_predict_results.setStyleSheet("")
        self.button_save_predict_results.setCheckable(False)
        self.button_save_predict_results.setObjectName("button_save_predict_results")
        self.horizontalLayout.addWidget(self.button_save_predict_results)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.progressBar_batch_predict = QtWidgets.QProgressBar(self.groupBox_405)
        self.progressBar_batch_predict.setProperty("value", 0)
        self.progressBar_batch_predict.setObjectName("progressBar_batch_predict")
        self.verticalLayout_2.addWidget(self.progressBar_batch_predict)
        self.verticalLayout_3.addWidget(self.groupBox_405)
        self.groupBox_406 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_406.sizePolicy().hasHeightForWidth())
        self.groupBox_406.setSizePolicy(sizePolicy)
        self.groupBox_406.setObjectName("groupBox_406")
        self.verticalLayout_51 = QtWidgets.QVBoxLayout(self.groupBox_406)
        self.verticalLayout_51.setObjectName("verticalLayout_51")
        self.listView_predict_files = QtWidgets.QListView(self.groupBox_406)
        self.listView_predict_files.setMinimumSize(QtCore.QSize(0, 200))
        self.listView_predict_files.setObjectName("listView_predict_files")
        self.verticalLayout_51.addWidget(self.listView_predict_files)
        self.verticalLayout_3.addWidget(self.groupBox_406)
        self.scrollArea_predict.setWidget(self.scrollAreaWidgetContents_6)
        self.verticalLayout_11.addWidget(self.scrollArea_predict)
        self.dockWidget_predict.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_predict)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setStyleSheet("border-color: rgb(0, 0, 0);")
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.action_user = QtWidgets.QAction(MainWindow)
        self.action_user.setObjectName("action_user")
        self.action_open_image = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("en\\icons/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_open_image.setIcon(icon)
        self.action_open_image.setObjectName("action_open_image")
        self.action_open_directory = QtWidgets.QAction(MainWindow)
        self.action_open_directory.setIcon(icon)
        self.action_open_directory.setObjectName("action_open_directory")
        self.action_prev_image = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("en\\icons/prev.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_prev_image.setIcon(icon1)
        self.action_prev_image.setObjectName("action_prev_image")
        self.action_next_image = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("en\\icons/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_next_image.setIcon(icon2)
        self.action_next_image.setObjectName("action_next_image")
        self.action_fit_window = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("en\\icons/fit-window.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_fit_window.setIcon(icon3)
        self.action_fit_window.setObjectName("action_fit_window")
        self.action_init_size = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("en\\icons/zoom.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_init_size.setIcon(icon4)
        self.action_init_size.setObjectName("action_init_size")
        self.action_hide_box = QtWidgets.QAction(MainWindow)
        self.action_hide_box.setCheckable(True)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("en\\icons/eye2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_hide_box.setIcon(icon5)
        self.action_hide_box.setObjectName("action_hide_box")
        self.action_save_file = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("en\\icons/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_save_file.setIcon(icon6)
        self.action_save_file.setObjectName("action_save_file")
        self.action_undo = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("en\\icons/undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_undo.setIcon(icon7)
        self.action_undo.setObjectName("action_undo")
        self.action_change_directory = QtWidgets.QAction(MainWindow)
        self.action_change_directory.setIcon(icon)
        self.action_change_directory.setObjectName("action_change_directory")
        self.action_other_image = QtWidgets.QAction(MainWindow)
        self.action_other_image.setCheckable(True)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("en\\icons/other.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_other_image.setIcon(icon8)
        self.action_other_image.setObjectName("action_other_image")
        self.action_black_white_convert = QtWidgets.QAction(MainWindow)
        self.action_black_white_convert.setCheckable(True)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("en\\icons/black_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_black_white_convert.setIcon(icon9)
        self.action_black_white_convert.setObjectName("action_black_white_convert")
        self.action_relief_image = QtWidgets.QAction(MainWindow)
        self.action_relief_image.setCheckable(True)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("en\\icons/relief.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_relief_image.setIcon(icon10)
        self.action_relief_image.setObjectName("action_relief_image")
        self.action_sharpen_image = QtWidgets.QAction(MainWindow)
        self.action_sharpen_image.setCheckable(True)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("en\\icons/sharpen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_sharpen_image.setIcon(icon11)
        self.action_sharpen_image.setObjectName("action_sharpen_image")
        self.action_rotate_left = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("en\\icons/rotate_left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_rotate_left.setIcon(icon12)
        self.action_rotate_left.setObjectName("action_rotate_left")
        self.action_rotate_right = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("en\\icons/rotate_right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_rotate_right.setIcon(icon13)
        self.action_rotate_right.setObjectName("action_rotate_right")
        self.action_overturn_x = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("en\\icons/overturn_x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_overturn_x.setIcon(icon14)
        self.action_overturn_x.setObjectName("action_overturn_x")
        self.action_overturn_y = QtWidgets.QAction(MainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("en\\icons/overturn_y.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_overturn_y.setIcon(icon15)
        self.action_overturn_y.setObjectName("action_overturn_y")
        self.action_blur_image = QtWidgets.QAction(MainWindow)
        self.action_blur_image.setCheckable(True)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap("en\\icons/blur.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_blur_image.setIcon(icon16)
        self.action_blur_image.setObjectName("action_blur_image")
        self.action_false_color_image = QtWidgets.QAction(MainWindow)
        self.action_false_color_image.setCheckable(True)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap("en\\icons/false_color.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_false_color_image.setIcon(icon17)
        self.action_false_color_image.setObjectName("action_false_color_image")
        self.action_image_enhance1 = QtWidgets.QAction(MainWindow)
        self.action_image_enhance1.setCheckable(True)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap("en\\icons/enhance1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_image_enhance1.setIcon(icon18)
        self.action_image_enhance1.setObjectName("action_image_enhance1")
        self.action_image_enhance2 = QtWidgets.QAction(MainWindow)
        self.action_image_enhance2.setCheckable(True)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap("en\\icons/enhance2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_image_enhance2.setIcon(icon19)
        self.action_image_enhance2.setObjectName("action_image_enhance2")
        self.action_enhance_para = QtWidgets.QAction(MainWindow)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap("en\\icons/setting.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_enhance_para.setIcon(icon20)
        self.action_enhance_para.setObjectName("action_enhance_para")
        self.action_image_enhance3 = QtWidgets.QAction(MainWindow)
        self.action_image_enhance3.setCheckable(True)
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap("en\\icons/enhance3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_image_enhance3.setIcon(icon21)
        self.action_image_enhance3.setObjectName("action_image_enhance3")
        self.action_source_image = QtWidgets.QAction(MainWindow)
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap("en\\icons/source.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_source_image.setIcon(icon22)
        self.action_source_image.setObjectName("action_source_image")
        self.menu_system.addAction(self.action_user)
        self.menu_file.addAction(self.action_open_image)
        self.menu_file.addAction(self.action_open_directory)
        self.menu_file.addAction(self.action_prev_image)
        self.menu_file.addAction(self.action_next_image)
        self.menu_file.addAction(self.action_other_image)
        self.menu_file.addAction(self.action_rotate_left)
        self.menu_file.addAction(self.action_rotate_right)
        self.menu_file.addAction(self.action_overturn_x)
        self.menu_file.addAction(self.action_overturn_y)
        self.menu_look.addAction(self.action_fit_window)
        self.menu_look.addAction(self.action_init_size)
        self.menu_look.addSeparator()
        self.menu_look.addAction(self.action_sharpen_image)
        self.menu_look.addAction(self.action_relief_image)
        self.menu_look.addAction(self.action_blur_image)
        self.menu_look.addAction(self.action_false_color_image)
        self.menu_look.addAction(self.action_black_white_convert)
        self.menu_look.addAction(self.action_image_enhance1)
        self.menu_look.addAction(self.action_image_enhance2)
        self.menu_look.addAction(self.action_image_enhance3)
        self.menu_look.addAction(self.action_source_image)
        self.menu_look.addAction(self.action_enhance_para)
        self.menu_look.addSeparator()
        self.menu_7.addAction(self.action_undo)
        self.menu_7.addAction(self.action_hide_box)
        self.menu_7.addAction(self.action_change_directory)
        self.menu_7.addAction(self.action_save_file)
        self.menu_module.addAction(self.menu_7.menuAction())
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_look.menuAction())
        self.menubar.addAction(self.menu_module.menuAction())
        self.menubar.addAction(self.menu_system.menuAction())
        self.toolBar_file.addAction(self.action_open_image)
        self.toolBar_file.addAction(self.action_open_directory)
        self.toolBar_file.addAction(self.action_prev_image)
        self.toolBar_file.addAction(self.action_next_image)
        self.toolBar_file.addAction(self.action_other_image)
        self.toolBar_file.addAction(self.action_rotate_left)
        self.toolBar_file.addAction(self.action_rotate_right)
        self.toolBar_file.addAction(self.action_overturn_x)
        self.toolBar_file.addAction(self.action_overturn_y)
        self.toolBar_look.addAction(self.action_fit_window)
        self.toolBar_look.addAction(self.action_init_size)
        self.toolBar_look.addSeparator()
        self.toolBar_look.addAction(self.action_sharpen_image)
        self.toolBar_look.addAction(self.action_relief_image)
        self.toolBar_look.addAction(self.action_blur_image)
        self.toolBar_look.addAction(self.action_false_color_image)
        self.toolBar_look.addAction(self.action_black_white_convert)
        self.toolBar_look.addAction(self.action_image_enhance1)
        self.toolBar_look.addAction(self.action_image_enhance2)
        self.toolBar_look.addAction(self.action_image_enhance3)
        self.toolBar_look.addAction(self.action_source_image)
        self.toolBar_label.addAction(self.action_undo)
        self.toolBar_label.addAction(self.action_hide_box)
        self.toolBar_label.addAction(self.action_change_directory)
        self.toolBar_label.addAction(self.action_save_file)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.menu_system.setTitle(_translate("MainWindow", "System"))
        self.menu_file.setTitle(_translate("MainWindow", "File"))
        self.menu_look.setTitle(_translate("MainWindow", "Look"))
        self.menu_module.setTitle(_translate("MainWindow", "Function"))
        self.menu_7.setTitle(_translate("MainWindow", "Label"))
        self.toolBar_file.setWindowTitle(_translate("MainWindow", "File"))
        self.toolBar_look.setWindowTitle(_translate("MainWindow", "Look"))
        self.toolBar_label.setWindowTitle(_translate("MainWindow", "Label"))
        self.toolBar_predict.setWindowTitle(_translate("MainWindow", "评片"))
        self.dockWidget_label.setWindowTitle(_translate("MainWindow", "Annotation Property Editor"))
        self.groupBox_301.setTitle(_translate("MainWindow", "Parameter Settings"))
        self.checkBox_difficult.setText(_translate("MainWindow", "Set Difficult"))
        self.checkBox_save_image.setText(_translate("MainWindow", "Save Image Data"))
        self.checkBox_preset.setText(_translate("MainWindow", "Use Preset Label"))
        self.checkBox_auto_rotate.setText(_translate("MainWindow", "Longer Is Horizontal"))
        self.label_301.setText(_translate("MainWindow", "Preset Label"))
        self.button_select_label_file.setText(_translate("MainWindow", "Select"))
        self.button_jump_label_file.setText(_translate("MainWindow", "Jump"))
        self.groupBox_410.setTitle(_translate("MainWindow", "File List"))
        self.dockWidget_predict.setWindowTitle(_translate("MainWindow", "Prediction Property Editor"))
        self.groupBox_405.setTitle(_translate("MainWindow", "Parameter Settings"))
        self.label_419.setText(_translate("MainWindow", "Model"))
        self.comboBox_model.setItemText(0, _translate("MainWindow", "DR_SD"))
        self.comboBox_model.setItemText(1, _translate("MainWindow", "DR_LD"))
        self.comboBox_model.setItemText(2, _translate("MainWindow", "RT_SD"))
        self.comboBox_model.setItemText(3, _translate("MainWindow", "RT_LD"))
        self.label_418.setText(_translate("MainWindow", "Folder"))
        self.button_select_file_path.setText(_translate("MainWindow", "Select"))
        self.button_batch_predict.setText(_translate("MainWindow", "Batch Predict"))
        self.button_save_predict_results.setText(_translate("MainWindow", "Save File"))
        self.groupBox_406.setTitle(_translate("MainWindow", "File List"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "测量"))
        self.action_user.setText(_translate("MainWindow", "User Management"))
        self.action_open_image.setText(_translate("MainWindow", "Open Image"))
        self.action_open_image.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_open_directory.setText(_translate("MainWindow", "Open Folder"))
        self.action_prev_image.setText(_translate("MainWindow", "Previous Image"))
        self.action_prev_image.setShortcut(_translate("MainWindow", "Left"))
        self.action_next_image.setText(_translate("MainWindow", "Next Image"))
        self.action_next_image.setShortcut(_translate("MainWindow", "Right"))
        self.action_fit_window.setText(_translate("MainWindow", "Fit to Window"))
        self.action_init_size.setText(_translate("MainWindow", "Original Size"))
        self.action_hide_box.setText(_translate("MainWindow", "Hide Box"))
        self.action_hide_box.setShortcut(_translate("MainWindow", "Ctrl+H"))
        self.action_save_file.setText(_translate("MainWindow", "Save File"))
        self.action_save_file.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action_undo.setText(_translate("MainWindow", "Undo Box"))
        self.action_undo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.action_change_directory.setText(_translate("MainWindow", "Change Directory"))
        self.action_other_image.setText(_translate("MainWindow", "Contrast Image"))
        self.action_black_white_convert.setText(_translate("MainWindow", "Invert Colors"))
        self.action_relief_image.setText(_translate("MainWindow", "Emboss"))
        self.action_sharpen_image.setText(_translate("MainWindow", "Sharpen"))
        self.action_rotate_left.setText(_translate("MainWindow", "Rotate Counterclockwise"))
        self.action_rotate_right.setText(_translate("MainWindow", "Rotate Clockwise"))
        self.action_overturn_x.setText(_translate("MainWindow", "Flip Vertical"))
        self.action_overturn_y.setText(_translate("MainWindow", "Flip Horizontal"))
        self.action_blur_image.setText(_translate("MainWindow", "Noise Reduction"))
        self.action_false_color_image.setText(_translate("MainWindow", "Pseudocolor"))
        self.action_image_enhance1.setText(_translate("MainWindow", "Image Enhancement 1"))
        self.action_image_enhance2.setText(_translate("MainWindow", "Image Enhancement 2"))
        self.action_enhance_para.setText(_translate("MainWindow", "Parameter Settings"))
        self.action_image_enhance3.setText(_translate("MainWindow", "Image Enhancement 3"))
        self.action_source_image.setText(_translate("MainWindow", "View Original"))
