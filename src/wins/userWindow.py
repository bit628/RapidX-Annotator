import os
import hashlib
import win32api
import win32con

from PyQt5 import QtWidgets

from wins.ui.ui_userWindow import Ui_UserWindow

class UserWindow(QtWidgets.QDialog, Ui_UserWindow):
	def __init__(self, id_current, parent=None):
		super(UserWindow, self).__init__(parent)
		self.setupUi(self)
		self.setFixedSize(600, 300)

		self.id_current = id_current
		self.file_users = 'users.txt'

		self.lineEdit_password_add.setEchoMode(QtWidgets.QLineEdit.Password)
		self.lineEdit_password_add_again.setEchoMode(QtWidgets.QLineEdit.Password)
		self.lineEdit_password_old.setEchoMode(QtWidgets.QLineEdit.Password)
		self.lineEdit_password_new.setEchoMode(QtWidgets.QLineEdit.Password)
		self.lineEdit_password_new_again.setEchoMode(QtWidgets.QLineEdit.Password)

		self.add_user_button.clicked.connect(self.add_user)
		self.modify_password_button.clicked.connect(self.modify_password)

	def add_user(self):
		if self.id_current == 'admin':
			id_add = self.lineEdit_id_add.text()
			password_add = self.lineEdit_password_add.text()
			password_add_again = self.lineEdit_password_add_again.text()
			if password_add == password_add_again:
				with open(self.file_users,'a') as f:
					password_add = hashlib.sha256(password_add.encode('utf-8')).hexdigest()
					f.write('{} {}\n'.format(id_add, password_add))
					win32api.MessageBox(0, '新增用户成功！', '提示', win32con.MB_ICONWARNING)
			else:
				win32api.MessageBox(0, '密码输入不一致！', '提示', win32con.MB_ICONWARNING)
		else:
			win32api.MessageBox(0, '不是管理员权限，无法新增用户！', '提示', win32con.MB_ICONWARNING)

	def modify_password(self):
		password_old = self.lineEdit_password_old.text()
		password_old = hashlib.sha256(password_old.encode('utf-8')).hexdigest()
		password_new = self.lineEdit_password_new.text()
		password_new_again = self.lineEdit_password_new_again.text()
		flag_modify = False
		# 验证用户管理文件是否存在
		if os.path.exists(self.file_users):
			# 验证新密码是否一致
			if password_new == password_new_again:
				with open(self.file_users,'r') as f:
					users = f.readlines()
					for idx, user in enumerate(users):
						id, password = user.split(' ')
						# 验证原密码是否输入正确
						if self.id_current == id and password_old == password[:-1]:
							password_new = hashlib.sha256(password_new.encode('utf-8')).hexdigest()
							# 修改密码
							users[idx] = '{} {}\n'.format(self.id_current, password_new)
							flag_modify = True
							break
					if flag_modify:
						with open(self.file_users, 'w') as f:
							# 重新生成用户管理文件
							for user in users:
								f.write('{}'.format(user))
							win32api.MessageBox(0, '修改密码成功！', '提示', win32con.MB_ICONWARNING)
					else:
						win32api.MessageBox(0, '原密码输入错误！', '提示', win32con.MB_ICONWARNING)
			else:
				win32api.MessageBox(0, '新密码输入不一致！', '提示', win32con.MB_ICONWARNING)
		else:
			win32api.MessageBox(0, '用户管理文件丢失！', '提示', win32con.MB_ICONWARNING)