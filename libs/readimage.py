import os
import cv2
import array
import win32api
import win32con
import pydicom
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from PIL import Image

class ReadImage():
    def convert_image(self, image, dtype='uint16', channels=1, flag_pil=False):
        """
        这个函数的作用是转换数组图像的深度和通道数。

        参数：
            参数1：待转换的数组图像
            参数2：想要转换成多大深度
            参数3：想要转换成多大通道数
            参数4：待转换的数组图像的三原色顺序是否为RGB或RGBA

        返回值：
            返回值1：已转换的数组图像
        """

        if image is None:
            return image

        idtype = image.dtype
        ichannels = image.shape[2] if len(image.shape) > 2 else 1
        if dtype == 'uint8' and channels == 1:
            if idtype == 'uint8' and ichannels == 1:
                pass
            elif idtype == 'uint8' and ichannels == 3:
                if flag_pil:
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            elif idtype == 'uint8' and ichannels == 4:
                if flag_pil:
                    image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
            else:
                image = (image / 257).astype(np.uint8)
        elif dtype == 'uint8' and channels == 3:
            if idtype == 'uint8' and ichannels == 1:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            elif idtype == 'uint8' and ichannels == 3:
                pass
            elif idtype == 'uint8' and ichannels == 4:
                if flag_pil:
                    image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
            else:
                image = (image / 257).astype(np.uint8)
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        elif dtype == 'uint8' and channels == 4:
            if idtype == 'uint8' and ichannels == 1:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)
            elif idtype == 'uint8' and ichannels == 3:
                if flag_pil:
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
            elif idtype == 'uint8' and ichannels == 4:
                pass
            else:
                image = (image / 257).astype(np.uint8)
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)
        else:
            if idtype == 'uint8' and ichannels == 1:
                pass
            elif idtype == 'uint8' and ichannels == 3:
                if flag_pil:
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            elif idtype == 'uint8' and ichannels == 4:
                if flag_pil:
                    image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
            else:
                pass

        return image

    def read_dcm(self, path, dtype='uint16', channels=1):
        """
        这个函数的作用是通过dcm路径读取图像

        参数：
            参数1：dcm路径
            参数2：想要转换成多大深度
            参数3：想要转换成多大通道数

        返回值：
            返回值1：读取到的数组图像
        """

        image = None

        try:
            dataset = pydicom.dcmread(path, force=True)
        except:
            win32api.MessageBox(0, '图像打开失败！', '提示', win32con.MB_ICONWARNING)
            return

        try:
            image = dataset.pixel_array
            image = self.convert_image(image, dtype, channels)
            return image
        except:
            pass

        if 'PixelRepresentation' not in dataset:
            dataset.PixelRepresentation = 0

        def reshape_image(image, dataset):
            pixels = len(image)
            rows = dataset.Rows
            columns = dataset.Columns
            rice = pixels % columns
            if rice == 0:
                image = image.reshape(rows, columns)
            else:
                image = image[:-rice].reshape(pixels // columns, columns)
            return image

        try:
            image = np.array(array.array('B', dataset.PixelData))
            image = reshape_image(image, dataset)
        except:
            image = np.array(array.array('H', dataset.PixelData))
            image = reshape_image(image, dataset)

        image = self.convert_image(image, dtype, channels)

        return image

    def read_nii(self, path, dtype='uint16', channels=1):
        """
        这个函数的作用是通过nii路径读取图像

        参数：
            参数1：nii路径
            参数2：想要转换成多大深度
            参数3：想要转换成多大通道数

        返回值：
            返回值1：读取到的数组图像
        """

        data = nib.load(path)
        image = data.get_fdata()

        image = self.convert_image(image, dtype, channels)

        return image

    def read_undcm(self, path, dtype='uint16', channels=1):
        """
        这个函数的作用是通过非dcm路径和非nii路径读取图像

        参数：
            参数1：非dcm路径和非nii路径
            参数2：想要转换成多大深度
            参数3：想要转换成多大通道数

        返回值：
            返回值1：读取到的数组图像
        """

        image = None

        if dtype == 'uint8':
            type = np.uint8
            if channels == 1:
                flag = 0
            elif channels == 3:
                flag = 1
            else:
                flag = -1
        else:
            type = np.uint16
            flag = -1

        try:
            image = cv2.imdecode(np.fromfile(path, dtype=type), flag)
            image = self.convert_image(image, dtype, channels)
            if image is None:
                image = np.array(Image.open(path))
                image = self.convert_image(image, dtype, channels, flag_pil=True)
            if image is None:
                image = cv2.imread(path.encode('gbk').decode(), flag)
                image = self.convert_image(image, dtype, channels)
        except:
            try:
                image = np.array(Image.open(path))
                image = self.convert_image(image, dtype, channels, flag_pil=True)
                if image is None:
                    image = cv2.imread(path.encode('gbk').decode(), flag)
                    image = self.convert_image(image, dtype, channels)
            except:
                try:
                    image = cv2.imread(path.encode('gbk').decode(), flag)
                    image = self.convert_image(image, dtype, channels)
                except:
                    win32api.MessageBox(0, '图像打开失败！', '提示', win32con.MB_ICONWARNING)

        return image

    def read_all(self, path, dtype='uint16', channels=1):
        """
        这个函数的作用是通过任意图像路径读取图像

        参数：
            参数1：任意图像路径
            参数2：想要转换成多大深度
            参数3：想要转换成多大通道数

        返回值：
            返回值1：读取到的数组图像
        """

        ext = os.path.splitext(path)[1].lower()
        if ext == '.dcm':
            image = self.read_dcm(path, dtype, channels)
        elif ext == '.nii':
            image = self.read_nii(path, dtype, channels)
        else:
            image = self.read_undcm(path, dtype, channels)

        return image

if __name__ == '__main__':
    readImage = ReadImage()
    image = readImage.read_all(path='difficult_image/nii/Label.nii')
    plt.imshow(image, cmap='gray')
    plt.show()