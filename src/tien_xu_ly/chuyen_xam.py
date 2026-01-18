"""
Module chuyển ảnh sang ảnh xám (Grayscale)
"""

import cv2
import numpy as np


def chuyen_nh_xam(duong_dan_anh):
    """
    Chuyển ảnh từ RGB/BGR sang grayscale
    
    Args:
        duong_dan_anh (str): Đường dẫn tới file ảnh
        
    Returns:
        tuple: (ảnh gốc, ảnh xám)
    """
    # Đọc ảnh gốc
    anh_goc = cv2.imread(duong_dan_anh)
    
    if anh_goc is None:
        raise ValueError(f"Không thể đọc ảnh: {duong_dan_anh}")
    
    # Chuyển sang xám
    anh_xam = cv2.cvtColor(anh_goc, cv2.COLOR_BGR2GRAY)
    
    return anh_goc, anh_xam


def chuyen_xam_tu_mang(anh_goc):
    """
    Chuyển ảnh sang xám từ mảng numpy
    
    Args:
        anh_goc (np.ndarray): Mảng ảnh gốc
        
    Returns:
        np.ndarray: Ảnh xám
    """
    if len(anh_goc.shape) == 2:
        # Đã là ảnh xám
        return anh_goc
    
    anh_xam = cv2.cvtColor(anh_goc, cv2.COLOR_BGR2GRAY)
    return anh_xam
