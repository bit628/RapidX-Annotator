import cv2
import time
import numpy as np
from scipy import signal

def enhance1(image, blur_size=3, gamma=0.4, gamma_times=1, center_value=4.2, times=8):
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if image.dtype == 'uint8':
        max_value = 255
        image_dtype = np.uint8
    else:
        max_value = 65535
        image_dtype = np.uint16

    image = cv2.medianBlur(image, blur_size)

    image = image.astype(np.float64)

    image_max = np.max(image)
    image = np.power(image, gamma) / np.power(image_max, gamma) * image_max * gamma_times
    image[image > max_value] = max_value
    image[image < 0] = 0

    kernel_sharpen = np.array([[0, -1, 0], [-1, center_value, -1], [0, -1, 0]])
    image = signal.convolve2d(image, kernel_sharpen, 'same', boundary='fill', fillvalue=0) # dtype为int32
    image[image > max_value] = max_value
    image[image < 0] = 0

    median = np.median(image)
    image = (image - median) * times + median
    image[image > max_value] = max_value
    image[image < 0] = 0

    return image.astype(image_dtype)

def enhance2(image, blur_size=3, gamma=0.5, gamma_times=1, block_size=3, bias=600,
             d=20, sigmaColor=75, sigmaSpace=75, clipLimit=5, k1=0.2, dde=2):
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if image.dtype == 'uint8':
        target = 255
        max_value = 255
        image_dtype = np.uint8
    else:
        target = 65535
        max_value = 65535
        image_dtype = np.uint16

    image = cv2.medianBlur(image, blur_size)

    image = image.astype(np.float64)

    image_max = np.max(image)
    image = np.power(image, gamma) / np.power(image_max, gamma) * image_max * gamma_times
    image[image > max_value] = max_value
    image[image < 0] = 0

    h, w = image.shape[:2]

    r = image.shape[0]
    num = r % block_size
    if num > 0:
        r_stack_num = block_size - num
        image_r_stack = np.repeat(image[-1:,:], r_stack_num, axis=0)
        image_r_stack = np.vstack((image, image_r_stack))
    else:
        image_r_stack = image

    c = image_r_stack.shape[1]
    num = c % block_size
    if num > 0:
        c_stack_num = block_size - num
        image_rc_stack = np.repeat(image_r_stack[:,-1:], c_stack_num, axis=1)
        image_rc_stack = np.hstack((image_r_stack, image_rc_stack))
    else:
        image_rc_stack = image_r_stack

    kernel = np.ones((block_size, block_size)) / (block_size**2)
    image_avg = signal.convolve2d(image_rc_stack, kernel, 'same', boundary='fill', fillvalue=0)
    block_avg = image_avg[block_size//2:, block_size//2:][::block_size, ::block_size]

    image_avg = np.repeat(block_avg, block_size, axis=0) # 扩展行
    image_avg = np.repeat(image_avg, block_size, axis=1) # 扩展列
    image_std = np.square(image_rc_stack - image_avg)
    kernel = np.ones((block_size, block_size))
    image_std = signal.convolve2d(image_std, kernel, 'same', boundary='fill', fillvalue=0)
    block_std = np.sqrt(image_std[block_size // 2:, block_size // 2:][::block_size, ::block_size])/(block_size**2)

    # block_avg = []
    # block_std = []
    # for i in range(0, h, block_size):
    #     block_avg_col = []
    #     block_std_col = []
    #     for j in range(0, w, block_size):
    #         block = image[i:i+block_size, j:j+block_size]
    #         avg = np.average(block)
    #         std = np.sqrt(np.sum(np.square(block-avg)))/(block_size**2)
    #         block_avg_col.append(avg)
    #         block_std_col.append(std)
    #     block_avg.append(block_avg_col)
    #     block_std.append(block_std_col)
    # block_avg = np.array(block_avg)
    # block_std = np.array(block_std)

    block_str = target / (block_std + bias)

    bh, bw = block_avg.shape[:2]
    target_size = (bw * block_size, bh * block_size)
    nblock_avg = cv2.resize(block_avg, target_size, interpolation=cv2.INTER_LINEAR)[:h, :w]
    nblock_str = cv2.resize(block_str, target_size, interpolation=cv2.INTER_LINEAR)[:h, :w]

    image_base = cv2.bilateralFilter(image.astype(np.float32), d=d, sigmaColor=sigmaColor, sigmaSpace=sigmaSpace)

    image_detail = image - image_base

    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=(8, 8))
    image_base = clahe.apply(image_base.astype(image_dtype))

    image_base = k1 * nblock_str * (image - nblock_avg) + image_base

    image = image_base + dde * image_detail

    image[image > max_value] = max_value
    image[image < 0] = 0

    return image.astype(image_dtype)

def enhance3(image, sigma=4.0, alpha=6.0):
    if image.dtype == 'uint8':
        max_value = 255
        image_dtype = np.uint8
    else:
        max_value = 65535
        image_dtype = np.uint16

    log_image = np.log(image.astype(np.float64) + 1)

    blurred_log_image = cv2.GaussianBlur(log_image, (0, 0), sigma)

    detail_log_image = log_image - blurred_log_image

    enhanced_log_image = np.exp(blurred_log_image + alpha * detail_log_image) - 1

    enhanced_log_image[enhanced_log_image > max_value] = max_value

    enhanced_log_image = enhanced_log_image.astype(image_dtype)

    return enhanced_log_image

if __name__ == '__main__':
    image = cv2.imread('source.tif', -1)
    image = enhance3(image, sigma=4, alpha=6)
    cv2.imwrite('source_enhanced.tif', image)