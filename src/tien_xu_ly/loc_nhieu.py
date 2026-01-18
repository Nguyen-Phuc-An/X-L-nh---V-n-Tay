"""
Module lọc nhiễu ảnh
"""

import cv2
import numpy as np


def loc_nhieu_median(anh_xam, kernel_size=5):
    """
    Lọc nhiễu bằng Median Blur
    Tốt cho lọc nhiễu salt-and-pepper
    
    Args:
        anh_xam (np.ndarray): Ảnh xám đầu vào
        kernel_size (int): Kích thước kernel (phải là lẻ)
        
    Returns:
        np.ndarray: Ảnh sau lọc
    """
    anh_loc = cv2.medianBlur(anh_xam, kernel_size)
    return anh_loc


def loc_nhieu_bilateral(anh_xam, diameter=9, sigma_color=75, sigma_space=75):
    """
    Lọc nhiễu bằng Bilateral Filter
    Giữ lại các cạnh trong khi làm mịn ảnh
    
    Args:
        anh_xam (np.ndarray): Ảnh xám đầu vào
        diameter (int): Đường kính của từng vùng pixel
        sigma_color (float): Độ lệch chuẩn của các mẫu màu sắc
        sigma_space (float): Độ lệch chuẩn của các mẫu không gian
        
    Returns:
        np.ndarray: Ảnh sau lọc
    """
    anh_loc = cv2.bilateralFilter(anh_xam, diameter, sigma_color, sigma_space)
    return anh_loc


def loc_nhieu_gaussian(anh_xam, kernel_size=5, sigma=1.0):
    """
    Lọc nhiễu bằng Gaussian Blur
    
    Args:
        anh_xam (np.ndarray): Ảnh xám đầu vào
        kernel_size (int): Kích thước kernel (phải là lẻ)
        sigma (float): Độ lệch chuẩn
        
    Returns:
        np.ndarray: Ảnh sau lọc
    """
    anh_loc = cv2.GaussianBlur(anh_xam, (kernel_size, kernel_size), sigma)
    return anh_loc


def loc_nhieu_morphological(anh_xam, kernel_size=5):
    """
    Lọc nhiễu bằng Opening và Closing (Morphological)
    
    Args:
        anh_xam (np.ndarray): Ảnh xám đầu vào
        kernel_size (int): Kích thước kernel
        
    Returns:
        np.ndarray: Ảnh sau lọc
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    
    # Opening: Erosion -> Dilation (loại bỏ nhiễu nhỏ)
    anh_opening = cv2.morphologyEx(anh_xam, cv2.MORPH_OPEN, kernel)
    
    # Closing: Dilation -> Erosion (điền các lỗ nhỏ)
    anh_loc = cv2.morphologyEx(anh_opening, cv2.MORPH_CLOSE, kernel)
    
    return anh_loc
