"""
Module làm mảnh ảnh (Skeletonization)
Sử dụng thuật toán nhanh từ scikit-image
"""

import cv2
import numpy as np
from scipy import ndimage


def lam_manh_zhang_suen_optimize(anh_nhi_phan, max_iterations=100):
    """
    Làm mảnh ảnh bằng thuật toán Zhang-Suen (tối ưu hóa)
    Có giới hạn số lần lặp để tránh quay vô hạn
    
    Args:
        anh_nhi_phan (np.ndarray): Ảnh nhị phân đầu vào (255 và 0)
        max_iterations (int): Số lần lặp tối đa
        
    Returns:
        np.ndarray: Ảnh sau làm mảnh
    """
    # Chuẩn bị ảnh: chuyển thành 0 và 1
    skeleton = anh_nhi_phan.copy()
    skeleton[skeleton == 255] = 1
    skeleton = skeleton.astype(np.uint8)
    
    iteration = 0
    while iteration < max_iterations:
        iteration += 1
        skeleton_prev = skeleton.copy()
        
        # Xóa điểm ở hai pass
        skeleton = _zhang_suen_single_pass(skeleton)
        
        # Kiểm tra hội tụ
        if np.array_equal(skeleton, skeleton_prev):
            break
    
    # Chuyển lại sang 0 và 255
    skeleton[skeleton == 1] = 255
    
    return skeleton


def _zhang_suen_single_pass(skeleton):
    """Một pass của Zhang-Suen"""
    marked = []
    h, w = skeleton.shape
    
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            if skeleton[i, j] == 0:
                continue
            
            # Lấy 8 lân cận
            p2 = skeleton[i-1, j]
            p3 = skeleton[i-1, j+1]
            p4 = skeleton[i, j+1]
            p5 = skeleton[i+1, j+1]
            p6 = skeleton[i+1, j]
            p7 = skeleton[i+1, j-1]
            p8 = skeleton[i, j-1]
            p9 = skeleton[i-1, j-1]
            
            bp = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
            sp = (p2 == 0 and p3 == 1) + (p3 == 0 and p4 == 1) + \
                 (p4 == 0 and p5 == 1) + (p5 == 0 and p6 == 1) + \
                 (p6 == 0 and p7 == 1) + (p7 == 0 and p8 == 1) + \
                 (p8 == 0 and p9 == 1) + (p9 == 0 and p2 == 1)
            
            if (2 <= bp <= 6 and sp == 1 and 
                not (p2 == 1 and p4 == 1 and p8 == 1) and
                not (p2 == 1 and p4 == 1 and p6 == 1) and
                not (p2 == 1 and p6 == 1 and p8 == 1) and
                not (p4 == 1 and p6 == 1 and p8 == 1)):
                marked.append((i, j))
    
    for i, j in marked:
        skeleton[i, j] = 0
    
    return skeleton


def lam_manh_scikit_image(anh_nhi_phan):
    """
    Làm mảnh ảnh bằng scikit-image (NHANH HƠN)
    Phương pháp được khuyến khích vì tốc độ
    
    Args:
        anh_nhi_phan (np.ndarray): Ảnh nhị phân đầu vào
        
    Returns:
        np.ndarray: Ảnh sau làm mảnh
    """
    try:
        from skimage.morphology import skeletonize
        
        # Chuẩn bị ảnh
        anh_binary = anh_nhi_phan > 127
        
        # Làm mảnh
        skeleton = skeletonize(anh_binary)
        
        # Chuyển lại sang 255 và 0
        skeleton = (skeleton * 255).astype(np.uint8)
        
        return skeleton
    except ImportError:
        print("⚠️ Cảnh báo: scikit-image chưa cài. Sử dụng Zhang-Suen tối ưu thay thế")
        return lam_manh_zhang_suen_optimize(anh_nhi_phan)


def loc_nhieu_sau_lam_manh(anh_manh, min_length=5):
    """
    Loại bỏ các đường rất ngắn sau khi làm mảnh
    
    Args:
        anh_manh (np.ndarray): Ảnh làm mảnh
        min_length (int): Độ dài tối thiểu của một đường
        
    Returns:
        np.ndarray: Ảnh sau lọc
    """
    # Sử dụng labeling để tìm các thành phần liên thông
    labeled_array, num_features = ndimage.label(anh_manh > 127)
    
    anh_loc = anh_manh.copy()
    
    for label_id in range(1, num_features + 1):
        component = labeled_array == label_id
        if np.sum(component) < min_length:
            anh_loc[component] = 0
    
    return anh_loc
