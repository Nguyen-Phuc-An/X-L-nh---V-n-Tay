"""
Module vẽ các đặc trưng minutiae lên ảnh
"""

import cv2
import numpy as np


def ve_minutiae_tren_anh(anh_goc, endings, bifurcations):
    """
    Vẽ các minutiae points lên ảnh gốc
    
    Args:
        anh_goc (np.ndarray): Ảnh gốc (grayscale hoặc color)
        endings (list): Danh sách ending points (i, j)
        bifurcations (list): Danh sách bifurcation points (i, j)
        
    Returns:
        np.ndarray: Ảnh với minutiae được vẽ
    """
    # Chuyển sang color nếu là grayscale
    if len(anh_goc.shape) == 2:
        anh_ve = cv2.cvtColor(anh_goc, cv2.COLOR_GRAY2BGR)
    else:
        anh_ve = anh_goc.copy()
    
    # Vẽ ending points (xanh lá cây)
    for point in endings:
        i, j = point
        cv2.circle(anh_ve, (j, i), 3, (0, 255, 0), -1)  # BGR: xanh lá
        cv2.circle(anh_ve, (j, i), 5, (0, 255, 0), 1)
    
    # Vẽ bifurcation points (đỏ)
    for point in bifurcations:
        i, j = point
        cv2.circle(anh_ve, (j, i), 3, (0, 0, 255), -1)  # BGR: đỏ
        cv2.circle(anh_ve, (j, i), 5, (0, 0, 255), 1)
    
    return anh_ve


def ve_minutiae_chi_tiet(anh_goc, minutiae):
    """
    Vẽ minutiae với hướng
    
    Args:
        anh_goc (np.ndarray): Ảnh gốc
        minutiae (dict): Dictionary chứa endings và bifurcations với chi tiết
        
    Returns:
        np.ndarray: Ảnh với minutiae được vẽ
    """
    # Chuyển sang color nếu là grayscale
    if len(anh_goc.shape) == 2:
        anh_ve = cv2.cvtColor(anh_goc, cv2.COLOR_GRAY2BGR)
    else:
        anh_ve = anh_goc.copy()
    
    # Vẽ ending points
    for item in minutiae.get('endings', []):
        i, j = item['position']
        huong = item['orientation']
        
        # Vẽ vòng tròn (xanh lá)
        cv2.circle(anh_ve, (j, i), 3, (0, 255, 0), -1)
        cv2.circle(anh_ve, (j, i), 5, (0, 255, 0), 1)
        
        # Vẽ mũi tên hướng
        dx = 7 * np.cos(np.radians(huong))
        dy = 7 * np.sin(np.radians(huong))
        cv2.arrowedLine(anh_ve, (j, i), 
                       (int(j + dx), int(i + dy)), 
                       (0, 255, 0), 1, tipLength=0.3)
    
    # Vẽ bifurcation points
    for item in minutiae.get('bifurcations', []):
        i, j = item['position']
        huong = item['orientation']
        
        # Vẽ vòng tròn (đỏ)
        cv2.circle(anh_ve, (j, i), 3, (0, 0, 255), -1)
        cv2.circle(anh_ve, (j, i), 5, (0, 0, 255), 1)
        
        # Vẽ mũi tên hướng
        dx = 7 * np.cos(np.radians(huong))
        dy = 7 * np.sin(np.radians(huong))
        cv2.arrowedLine(anh_ve, (j, i), 
                       (int(j + dx), int(i + dy)), 
                       (0, 0, 255), 1, tipLength=0.3)
    
    return anh_ve


def tao_anh_minutiae_che_do(anh_manh):
    """
    Tạo ảnh hiển thị chế độ minutiae (chỉ hiển thị skeleton)
    Dùng cho hiển thị
    
    Args:
        anh_manh (np.ndarray): Ảnh làm mảnh
        
    Returns:
        np.ndarray: Ảnh color
    """
    anh_color = cv2.cvtColor(anh_manh, cv2.COLOR_GRAY2BGR)
    return anh_color


def tao_heatmap_minutiae(anh_manh, endings, bifurcations, radius=10):
    """
    Tạo heatmap hiển thị mật độ minutiae
    
    Args:
        anh_manh (np.ndarray): Ảnh làm mảnh
        endings (list): Danh sách ending points
        bifurcations (list): Danh sách bifurcation points
        radius (int): Bán kính của Gaussian kernel
        
    Returns:
        np.ndarray: Ảnh heatmap
    """
    h, w = anh_manh.shape
    heatmap = np.zeros((h, w), dtype=np.float32)
    
    # Tạo Gaussian kernel
    kernel = cv2.getGaussianKernel(2*radius+1, radius/2)
    kernel = kernel @ kernel.T
    
    # Thêm ending points
    for i, j in endings:
        y1 = max(0, i - radius)
        y2 = min(h, i + radius + 1)
        x1 = max(0, j - radius)
        x2 = min(w, j + radius + 1)
        
        ky1 = max(0, radius - i)
        ky2 = ky1 + (y2 - y1)
        kx1 = max(0, radius - j)
        kx2 = kx1 + (x2 - x1)
        
        heatmap[y1:y2, x1:x2] += kernel[ky1:ky2, kx1:kx2].flatten().reshape(y2-y1, x2-x1)
    
    # Thêm bifurcation points
    for i, j in bifurcations:
        y1 = max(0, i - radius)
        y2 = min(h, i + radius + 1)
        x1 = max(0, j - radius)
        x2 = min(w, j + radius + 1)
        
        ky1 = max(0, radius - i)
        ky2 = ky1 + (y2 - y1)
        kx1 = max(0, radius - j)
        kx2 = kx1 + (x2 - x1)
        
        heatmap[y1:y2, x1:x2] += kernel[ky1:ky2, kx1:kx2].flatten().reshape(y2-y1, x2-x1)
    
    # Chuẩn hóa và áp dụng colormap
    heatmap = np.uint8(255 * heatmap / (np.max(heatmap) + 1e-8))
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    return heatmap_color
