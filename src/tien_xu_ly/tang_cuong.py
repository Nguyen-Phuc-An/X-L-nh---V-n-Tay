"""
Module tăng cường ảnh bằng Gabor Filter
"""

import cv2
import numpy as np


def tao_gabor_kernel(kernel_size=21, lambda_=10, gamma=0.5, psi=0, sigma=3, theta=0):
    """
    Tạo kernel Gabor filter
    
    Args:
        kernel_size (int): Kích thước kernel
        lambda_ (float): Bước sóng của sóng sin
        gamma (float): Tỷ lệ co dãn không gian (spatial aspect ratio)
        psi (float): Độ dốc pha
        sigma (float): Độ lệch chuẩn của Gaussian
        theta (float): Hướng (radian)
        
    Returns:
        np.ndarray: Kernel Gabor
    """
    kernel = np.zeros((kernel_size, kernel_size))
    
    for x in range(kernel_size):
        for y in range(kernel_size):
            # Chuyển đổi sang tọa độ tâm
            px = x - kernel_size // 2
            py = y - kernel_size // 2
            
            # Xoay tọa độ
            x_prime = px * np.cos(theta) + py * np.sin(theta)
            y_prime = -px * np.sin(theta) + py * np.cos(theta)
            
            # Gabor function
            gauss = np.exp(-(x_prime**2 + gamma**2 * y_prime**2) / (2 * sigma**2))
            sinusoid = np.cos(2 * np.pi * x_prime / lambda_ + psi)
            kernel[y, x] = gauss * sinusoid
    
    # Chuẩn hóa kernel
    kernel = kernel / np.sum(np.abs(kernel))
    
    return kernel


def ap_dung_gabor_filter(anh_xam, kernel_size=21, num_orientations=6):
    """
    Áp dụng Gabor filter với nhiều hướng khác nhau
    
    Args:
        anh_xam (np.ndarray): Ảnh xám đầu vào
        kernel_size (int): Kích thước kernel
        num_orientations (int): Số hướng để lọc
        
    Returns:
        np.ndarray: Ảnh được tăng cường
    """
    anh_tang_cuong = np.zeros_like(anh_xam, dtype=np.float32)
    
    # Tạo Gabor filter cho các hướng khác nhau
    for i in range(num_orientations):
        theta = (i * np.pi) / num_orientations
        kernel = tao_gabor_kernel(kernel_size=kernel_size, theta=theta)
        
        # Áp dụng filter
        filtered = cv2.filter2D(anh_xam.astype(np.float32), -1, kernel)
        
        # Lấy max response
        anh_tang_cuong = np.maximum(anh_tang_cuong, np.abs(filtered))
    
    # Chuẩn hóa về [0, 255]
    anh_tang_cuong = np.uint8(255 * anh_tang_cuong / np.max(anh_tang_cuong + 1e-8))
    
    return anh_tang_cuong


def tang_cuong_anh_histogram(anh_xam):
    """
    Tăng cường ảnh bằng histogram equalization
    
    Args:
        anh_xam (np.ndarray): Ảnh xám đầu vào
        
    Returns:
        np.ndarray: Ảnh được tăng cường
    """
    anh_tang_cuong = cv2.equalizeHist(anh_xam)
    return anh_tang_cuong


def tang_cuong_unsharp_mask(anh_xam, kernel_size=5, sigma=1.0, strength=1.5):
    """
    Tăng cường ảnh bằng Unsharp Mask
    
    Args:
        anh_xam (np.ndarray): Ảnh xám đầu vào
        kernel_size (int): Kích thước kernel Gaussian
        sigma (float): Độ lệch chuẩn Gaussian
        strength (float): Độ mạnh của unsharp mask
        
    Returns:
        np.ndarray: Ảnh được tăng cường
    """
    # Làm mờ ảnh
    anh_blur = cv2.GaussianBlur(anh_xam, (kernel_size, kernel_size), sigma)
    
    # Tính unsharp mask
    anh_tang_cuong = cv2.addWeighted(anh_xam, 1 + strength, anh_blur, -strength, 0)
    
    # Clamp giá trị về [0, 255]
    anh_tang_cuong = np.clip(anh_tang_cuong, 0, 255).astype(np.uint8)
    
    return anh_tang_cuong
