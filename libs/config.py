import numpy as np

class Config:
	company_name = 'Label and Test Software V2.0.0   '

	label_file = ''

	bool_predict_on = False

	bool_show_length = False
	bool_show_score_w_h = True

	bool_check_and_process_image = True

	bool_cut_weld = False
	bool_cut_cdh = True
	bool_cut_rhx = True

	# 设置圆形图元的半径
	circle_radius = 1

	# 当矩形框低于最小尺寸时，将不能调节对比度或创建矩形框
	min_width_of_box = 3
	min_height_of_box = 3

	# 用于多边形框闭合
	margin_i_in_0 = 4

	# 用于批量评片
	batch_size = 1

	# 可识别图像类型
	postfix = ['.jpg', '.png', '.tif', '.tiff', '.bmp', '.dcm', '.diconde']

	# 浮雕核
	kernel_relief = np.array([[1, 0], [0, -1]])

	# 锐化核
	kernel_sharpen = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

	# log路径
	log_dirname = 'logs'