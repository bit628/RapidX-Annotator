import os
import cv2
import numpy as np
from libs.readimage import ReadImage

def get_num(image):
    divide_width = 2
    step_width = 2
    border_width = 20
    merge_threshold = 20

    ih, iw = image.shape[:2]

    rs = []
    for i in range(border_width, ih-border_width, step_width):
        img = image[i:i+divide_width,:,:]
        img_min = np.min(img)
        img_max = np.max(img)
        if img_min == 0 and img_max == 0:
            rs.append(i)
    merge_rs = []
    for i, r in enumerate(rs):
        if i == 0:
            merge_rs.append(r)
        else:
            if r - merge_rs[-1] < merge_threshold:
                merge_rs[-1] = r
            else:
                merge_rs.append(r)

    cs = []
    for i in range(border_width, iw-border_width, step_width):
        img = image[:,i:i+divide_width,:]
        img_min = np.min(img)
        img_max = np.max(img)
        if img_min == 0 and img_max == 0:
            cs.append(i)
    merge_cs = []
    for i, c in enumerate(cs):
        if i == 0:
            merge_cs.append(c)
        else:
            if c - merge_cs[-1] < merge_threshold:
                merge_cs[-1] = c
            else:
                merge_cs.append(c)

    rn = len(merge_rs)
    cn = len(merge_cs)
    if rn == 1 and cn == 0:
        num = 2
    elif rn == 2 and cn == 0:
        num = 3
    elif rn == 2 and cn == 1:
        num = 5
    elif rn == 3 and cn == 1:
        num = 7
    else:
        num = 1

    return num

def divede_image(image, num):
    h, w = image.shape[:2]

    if num == 1:
        images = [image]
        ps = [[0, 0]]

    elif num == 2:
        images = [
            image[:h // 2, :, :],
            image[h // 2:, :, :],
        ]
        ps = [
            [0, 0],
            [0, h // 2],
        ]

    elif num == 3:
        images = [
            image[:h // 3, :, :],
            image[h // 3:2 * h // 3, :, :],
            image[2 * h // 3:, :, :],
        ]
        ps = [
            [0, 0],
            [0, h // 3],
            [0, 2 * h // 3],
        ]

    elif num == 5:
        images = [
            image[:h // 3, :w // 2, :],
            image[h // 3:2 * h // 3, :w // 2, :],
            image[2 * h // 3:, :w // 2, :],
            image[:h // 3, w // 2:, :],
            image[h // 3:2 * h // 3, w // 2:, :],
        ]
        ps = [
            [0, 0],
            [0, h // 3],
            [0, 2 * h // 3],
            [w // 2, 0],
            [w // 2, h // 3],
        ]

    elif num == 7:
        images = [
            image[:h // 4, :w // 2, :],
            image[h // 4:2 * h // 4, :w // 2, :],
            image[2 * h // 4:3 * h // 4, :w // 2, :],
            image[3 * h // 4:, :w // 2, :],
            image[:h // 4, w // 2:, :],
            image[h // 4:2 * h // 4, w // 2:, :],
            image[2 * h // 4:3 * h // 4, w // 2:, :],
        ]
        ps = [
            [0, 0],
            [0, h // 4],
            [0, 2 * h // 4],
            [0, 3 * h // 4],
            [w // 2, 0],
            [w // 2, h // 4],
            [w // 2, 2 * h // 4],
        ]

    return images, ps

if __name__ == "__main__":
    img_path = "./images"
    img_save_path = "./images_divided"

    readImage = ReadImage()

    if not os.path.isdir(img_save_path):
        os.makedirs(img_save_path)

    for filename in os.listdir(img_path):
        filepath = os.path.join(img_path, filename)
        name, postfix = os.path.splitext(filename)
        if postfix.lower() in ['.tif', '.tiff', '.png', '.jpg', '.bmp']:
            img = readImage.read_all(filepath, dtype='uint16', channels=1)
            num = get_num(img)
            crop_imgs, _ = divede_image(img, num)
            for i, crop_img in enumerate(crop_imgs):
                crop_filepath = os.path.join(img_save_path, '{}-{}.tif'.format(name, i+1))
                cv2.imencode('.tif', crop_img, [cv2.IMWRITE_TIFF_COMPRESSION, 1])[1].tofile(crop_filepath)