import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
import win32api
import win32con
import threading
import numpy as np
import paddlex as pdx
from natsort import natsort

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer, QPointF

from config import Config
from lab.labelFile import LabelFile
from pred.DR_SD.predict import predict as dr_sd_predict
from view.abstractlist import MyItemDelegate, MyAbstractListModel

class Predict:
	def __init__(self, mainWin):

		self.mainWin = mainWin

		self.all_files = []
		self.all_results = []
		self.all_files_index = 0

		self.memory_path = ''

		self.labelFile = LabelFile()

		self.mainWin.button_save_predict_results.clicked.connect(self.save_predict_results)
		self.mainWin.button_select_file_path.clicked.connect(self.select_file_path)
		self.mainWin.listView_predict_files.clicked.connect(self.click_predict_files)

		self.timer1 = QTimer()
		self.timer1.timeout.connect(self.timer_update_image)
		self.timer1.start(30)

		self.flag_top_window = False
		self.timer2 = QTimer()
		self.timer2.timeout.connect(self.timer_top_window)
		self.timer2.start(200)

		self.batch_predict_progress = 0
		self.timer3 = QTimer()
		self.timer3.timeout.connect(self.timer_batch_predict_progress)
		self.timer3.start(100)

		self.thread_threading_batch_predict = threading.Thread(target=self.threading_batch_predict, daemon=True)
		self.thread_threading_batch_predict.start()

	def timer_update_image(self):
		if self.mainWin.button_batch_predict.isChecked() and \
				self.all_files != [] and self.all_files[self.all_files_index] != self.mainWin.show1.fileName:
			try:
				self.mainWin.listView_predict_files.setCurrentIndex(self.listModel.index(self.all_files_index))
				self.mainWin.show1.fileName = self.all_files[self.all_files_index]
				self.mainWin.scene1.image = self.mainWin.readImage.read_all(self.mainWin.show1.fileName, dtype='uint16', channels=1)
				if Config.bool_check_and_process_image:
					self.mainWin.scene1.image = self.mainWin.check_and_process_image(self.mainWin.scene1.image)
				self.mainWin.show1.show_image(self.mainWin.scene1.image, True, False,
											  result=self.all_results[self.all_files_index])
			except FileNotFoundError as error:
				self.mainWin.logger.error(f'主窗口1显示图像失败，报警如下：{error}。')

	def timer_top_window(self):
		if self.flag_top_window:
			time.sleep(0.2)
			self.flag_top_window = False

			self.mainWin.showMessageBox(self.top_window_icon, '提示', self.top_window_text)

	def timer_batch_predict_progress(self):
		self.mainWin.progressBar_batch_predict.setValue(self.batch_predict_progress)

	def threading_batch_predict(self):
		try:
			self.threading_batch_predict_execute()
		except Exception as e:
			self.mainWin.logger.error(f'predict threading_batch_predict_execute函数运行异常，报警如下：{e}')
		finally:
			pass

	def threading_batch_predict_execute(self):
		while True:
			time.sleep(1)

			if self.mainWin.button_batch_predict.isChecked():
				self.batch_predict_progress = 0

				batch_predict_start_time = time.time()

				total_num = len(self.all_files)

				for i in range(0, total_num, Config.batch_size):
					if not self.mainWin.button_batch_predict.isChecked():
						self.mainWin.logger.info('批量检测中止！')
						self.top_window_icon = 'Information'
						self.top_window_text = '批量检测中止！'
						self.flag_top_window = True
						break

					filepath_batch = self.all_files[i:i + Config.batch_size]

					if self.mainWin.comboBox_model.currentText() == 'DR_SD':
						result_batch = dr_sd_predict(filepath_batch)
					elif self.mainWin.comboBox_model.currentText() == 'DR_LD':
						result_batch = dr_ld_predict(filepath_batch)
					elif self.mainWin.comboBox_model.currentText() == 'RT_SD':
						result_batch = rt_sd_predict(filepath_batch)
					elif self.mainWin.comboBox_model.currentText() == 'RT_LD':
						result_batch = rt_ld_predict(filepath_batch)

					result_batch = [self.english2chinese(result) for result in result_batch]

					self.all_results[i:i + Config.batch_size] = result_batch

					if i + Config.batch_size - 1 < total_num - 1:
						self.all_files_index = i + Config.batch_size - 1
					else:
						self.all_files_index = total_num - 1

					value = i + Config.batch_size
					self.batch_predict_progress = total_num if value >= total_num else value

				if not self.mainWin.button_batch_predict.isChecked():
					continue

				batch_predict_end_time = time.time()

				time_per_sheet = (batch_predict_end_time - batch_predict_start_time) / total_num
				batch_predict_text = f'批量检测完成！一共检测{total_num}张图像，平均用时{time_per_sheet:.2f}秒。'

				self.mainWin.logger.info(batch_predict_text)
				self.top_window_icon = 'Information'
				self.top_window_text = batch_predict_text
				self.flag_top_window = True

				time.sleep(0.2)
				self.mainWin.button_batch_predict.setChecked(False)

	def english2chinese(self, result):
		path = 'classes_en2ch.txt'
		if os.path.exists(path):
			with open(path, 'r', encoding='utf-8') as f:
				classes_en_ch = f.read().split('\n')
				classes_en_ch = [s for s in classes_en_ch if s != '']

			classes_en = []
			classes_ch = []
			for classe_en_ch in classes_en_ch:
				try:
					classe_en, classe_ch = classe_en_ch.split(':')
					classes_en.append(classe_en)
					classes_ch.append(classe_ch)
				except ValueError:
					self.mainWin.logger(f'{path}内容格式不正确，每行内容格式如下，crack:裂纹')

			for i, subresult in enumerate(result):
				try:
					result[i]['category'] = classes_ch[classes_en.index(subresult['category'])]
				except ValueError:
					self.mainWin.logger(f"{path}中不存在{subresult['category']}，请补充")

		return result

	def save_predict_results(self):
		if self.all_files != []:
			for i, path in enumerate(self.all_files):

				shapes = []
				for subresult in self.all_results[i]:
					shape = {}
					shape['label'] = subresult['category']
					try:
						shape['score'] = subresult['score']
					except:
						shape['score'] = 1.0
					x, y, w, h = subresult['bbox']
					shape['points'] = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
					shape['line_color'] = None
					shape['fill_color'] = None
					shape['difficult'] = 0
					shapes.append(shape)

				labelNamePascalVoc = os.path.splitext(path)[0] + '.xml'

				try:
					self.labelFile.savePascalVocFormat(labelNamePascalVoc, shapes, path)
				except Exception as error:
					self.mainWin.logger.error(f'{path}保存XML文件失败，原因如下：{error}')

		self.top_window_icon = 'Information'
		self.top_window_text = '评片结果保存完成！'
		self.flag_top_window = True

	def select_file_path(self):
		if self.memory_path == '':
			self.memory_path = os.getcwd()
		path = QFileDialog.getExistingDirectory(None, "选取文件夹", self.memory_path)
		self.memory_path = path
		self.mainWin.lineEdit_file_path.setText(path)
		self.mainWin.logger.info(f'选择批量评片文件夹：{path}。')

		filepaths = []
		file_path = self.mainWin.lineEdit_file_path.text()
		if os.path.isdir(file_path):
			for dir, dirnames, filenames in os.walk(file_path):
				for filename in natsort(filenames):
					filepath = os.path.join(dir, filename).replace('\\', '/')
					postfix = os.path.splitext(filepath)[1]
					if postfix.lower() in Config.postfix:
						filepaths.append(filepath)
		else:
			self.top_window_icon = 'Warning'
			self.top_window_text = '批量评片目录不存在！'
			self.flag_top_window = True
			return

		total_num = len(filepaths)
		if total_num == 0:
			self.top_window_icon = 'Warning'
			self.top_window_text = '文件夹中没有图像，请重新选择文件夹！'
			self.flag_top_window = True
			return

		self.mainWin.progressBar_batch_predict.setRange(0, total_num)

		self.all_files = filepaths
		self.all_results = [[]] * total_num

		self.refresh_predict_files()

		self.all_files_index = 0
		self.mainWin.listView_predict_files.setCurrentIndex(self.listModel.index(self.all_files_index))
		self.mainWin.show1.fileName = self.all_files[self.all_files_index]
		self.mainWin.scene1.image = self.mainWin.readImage.read_all(self.mainWin.show1.fileName, dtype='uint16', channels=1)
		self.mainWin.show1.show_image(self.mainWin.scene1.image, True, False,
									  result=self.all_results[self.all_files_index])

	def click_predict_files(self, qModelIndex):
		if self.all_files != []:
			self.all_files_index = qModelIndex.row()
			self.mainWin.show1.fileName = self.all_files[self.all_files_index]
			self.mainWin.scene1.image = self.mainWin.readImage.read_all(self.mainWin.show1.fileName, dtype='uint16', channels=1)
			self.mainWin.show1.show_image(self.mainWin.scene1.image, True, False,
										  result=self.all_results[self.all_files_index])

	def refresh_predict_files(self):
		self.listModel = MyAbstractListModel(self.all_files, self.mainWin)
		itemDelegate = MyItemDelegate(self.mainWin)
		self.mainWin.listView_predict_files.setModel(self.listModel)
		self.mainWin.listView_predict_files.setItemDelegate(itemDelegate)

	def prev_image(self):
		if self.all_files != [] and self.all_files_index > 0:
			self.all_files_index -= 1
			self.mainWin.listView_predict_files.setCurrentIndex(self.listModel.index(self.all_files_index))
			self.mainWin.show1.fileName = self.all_files[self.all_files_index]
			self.mainWin.scene1.image = self.mainWin.readImage.read_all(self.mainWin.show1.fileName, dtype='uint16', channels=1)
			self.mainWin.show1.show_image(self.mainWin.scene1.image, True, False,
										  result=self.all_results[self.all_files_index])

	def next_image(self):
		if self.all_files != [] and self.all_files_index < len(self.all_files) - 1:
			self.all_files_index += 1
			self.mainWin.listView_predict_files.setCurrentIndex(self.listModel.index(self.all_files_index))
			self.mainWin.show1.fileName = self.all_files[self.all_files_index]
			self.mainWin.scene1.image = self.mainWin.readImage.read_all(self.mainWin.show1.fileName, dtype='uint16', channels=1)
			self.mainWin.show1.show_image(self.mainWin.scene1.image, True, False,
										  result=self.all_results[self.all_files_index])