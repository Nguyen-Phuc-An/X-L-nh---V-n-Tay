"""
Module nhị phân hóa ảnh
"""

import cv2
import numpy as np


def nhi_phan_hoa_otsu(anh_xam):
    """
    Nhị phân hóa ảnh bằng phương pháp Otsu
    Tự động tìm ngưỡng tối ưu
    
    Args:
        anh_xam (np.ndarray): Ảnh xám đầu vào
        
    Returns:
        tuple: (ảnh nhị phân, ngưỡng được chọn)
    """
    # Otsu auto tìm ngưỡng
    threshold_value, anh_nhi_phan = cv2.threshold(anh_xam, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return anh_nhi_phan, threshold_value


def nhi_phan_hoa_adaptive(anh_xam, block_size=11, constant=2):
    """
    Nhị phân hóa ảnh bằng Adaptive Threshold
    Tốt cho ảnh có điều kiện ánh sáng không đều
    
    Args:
        anh_xam (np.ndarray): Ảnh xám đầu vào
        block_size (int): Kích thước vùng lân cận (phải là lẻ)
        constant (float): Hằng số trừ từ trung bình
        
    Returns:
        np.ndarray: Ảnh nhị phân
    """
    anh_nhi_phan = cv2.adaptiveThreshold(
        anh_xam,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        block_size,
        constant
    )
    return anh_nhi_phan


def nhi_phan_hoa_custom(anh_xam, threshold=127):
    """
    Nhị phân hóa ảnh với ngưỡng tuỳ chỉnh
    
    Args:
        anh_xam (np.ndarray): Ảnh xám đầu vào
        threshold (int): Giá trị ngưỡng (0-255)
        
    Returns:
        np.ndarray: Ảnh nhị phân
    """
    anh_nhi_phan = cv2.threshold(anh_xam, threshold, 255, cv2.THRESH_BINARY)[1]
    return anh_nhi_phan


def nhi_phan_hoa_binary_inverse(anh_xam):
    """
    Nhị phân hóa ảnh với ngược lại (đảo màu)
    
    Args:
        anh_xam (np.ndarray): Ảnh xám đầu vào
        
    Returns:
        np.ndarray: Ảnh nhị phân (ngược)
    """
    _, anh_nhi_phan = cv2.threshold(anh_xam, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return anh_nhi_phan


def lam_sach_anh_nhi_phan(anh_nhi_phan, kernel_size=5):
    """
    Làm sạch ảnh nhị phân bằng morphological operations
    
    Args:
        anh_nhi_phan (np.ndarray): Ảnh nhị phân đầu vào
        kernel_size (int): Kích thước kernel
        
    Returns:
        np.ndarray: Ảnh nhị phân sau làm sạch
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    
    # Opening: loại bỏ nhiễu nhỏ
    anh_opening = cv2.morphologyEx(anh_nhi_phan, cv2.MORPH_OPEN, kernel)
    
    # Closing: điền các lỗ nhỏ
    anh_closing = cv2.morphologyEx(anh_opening, cv2.MORPH_CLOSE, kernel)
    
    return anh_closing
