"""
Module chuẩn hóa ảnh (Normalization)
"""

import cv2
import numpy as np


def chuan_hoa_anh(anh_xam):
    """
    Chuẩn hóa ảnh để cải thiện độ tương phản
    Sử dụng histogram equalization
    
    Args:
        anh_xam (np.ndarray): Ảnh xám đầu vào
        
    Returns:
        np.ndarray: Ảnh sau chuẩn hóa
    """
    # CLAHE - Contrast Limited Adaptive Histogram Equalization
    # Tốt hơn histogram equalization bình thường
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    anh_chuan_hoa = clahe.apply(anh_xam)
    
    return anh_chuan_hoa


def chuan_hoa_tuyến_tính(anh_xam):
    """
    Chuẩn hóa tuyến tính: (pixel - min) / (max - min) * 255
    
    Args:
        anh_xam (np.ndarray): Ảnh xám đầu vào
        
    Returns:
        np.ndarray: Ảnh sau chuẩn hóa
    """
    min_val = np.min(anh_xam)
    max_val = np.max(anh_xam)
    
    if max_val == min_val:
        return anh_xam
    
    anh_chuan_hoa = 255 * (anh_xam - min_val) / (max_val - min_val)
    anh_chuan_hoa = anh_chuan_hoa.astype(np.uint8)
    
    return anh_chuan_hoa


def chuan_hoa_z_score(anh_xam):
    """
    Chuẩn hóa Z-score: (pixel - mean) / std
    
    Args:
        anh_xam (np.ndarray): Ảnh xám đầu vào
        
    Returns:
        np.ndarray: Ảnh sau chuẩn hóa
    """
    mean = np.mean(anh_xam)
    std = np.std(anh_xam)
    
    if std == 0:
        return anh_xam
    
    anh_chuan_hoa = (anh_xam - mean) / std
    # Chuẩn hóa lại về [0, 255]
    anh_chuan_hoa = ((anh_chuan_hoa - anh_chuan_hoa.min()) / 
                     (anh_chuan_hoa.max() - anh_chuan_hoa.min()) * 255)
    anh_chuan_hoa = anh_chuan_hoa.astype(np.uint8)
    
    return anh_chuan_hoa
