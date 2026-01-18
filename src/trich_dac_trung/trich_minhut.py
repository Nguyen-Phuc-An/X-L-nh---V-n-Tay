"""
Module trích chọn đặc trưng Minutiae
Sử dụng thuật toán Crossing Number
"""

import numpy as np
import cv2
from scipy import ndimage


def tinh_crossing_number(anh_manh, i, j):
    """
    Tính Crossing Number tại vị trí (i, j)
    Crossing Number = số lần chuyển đổi từ nền đến tiền cảnh trong 8 lân cận
    
    Args:
        anh_manh (np.ndarray): Ảnh làm mảnh nhị phân
        i (int): Tọa độ hàng
        j (int): Tọa độ cột
        
    Returns:
        int: Giá trị Crossing Number
    """
    try:
        neighbors = np.array([
            anh_manh[i-1, j-1], anh_manh[i-1, j],   anh_manh[i-1, j+1],
            anh_manh[i, j-1],                        anh_manh[i, j+1],
            anh_manh[i+1, j-1], anh_manh[i+1, j],   anh_manh[i+1, j+1]
        ], dtype=np.float32)
    except IndexError:
        return 0
    
    # Bình thường hóa thành 0 và 1 (sử dụng ngưỡng 100 thay vì 127)
    neighbors = (neighbors > 100).astype(np.int32)
    
    # Sắp xếp theo vòng tròn để tính CN
    # p2 p3 p4 p5 p6 p7 p8 p9 p2
    p = np.array([neighbors[1], neighbors[2], neighbors[4], 
                  neighbors[7], neighbors[6], neighbors[5], 
                  neighbors[3], neighbors[0], neighbors[1]], dtype=np.int32)
    
    # Đếm số chuyển đổi từ 0->1
    cn = 0
    for k in range(8):
        cn += abs(int(p[k+1]) - int(p[k]))
    
    cn = cn // 2
    return cn


def phan_loai_minutiae(anh_manh):
    """
    Phân loại các điểm minutiae thành ending và bifurcation
    Cải tiến: Crossing Number + Neighbor count method
    
    Args:
        anh_manh (np.ndarray): Ảnh làm mảnh nhị phân
        
    Returns:
        tuple: (danh sách ending, danh sách bifurcation)
    """
    endings = []
    bifurcations = []
    
    h, w = anh_manh.shape
    
    # Debug: Đếm số điểm foreground
    foreground_count = np.sum(anh_manh > 100)
    print(f"[DEBUG] Tổng điểm foreground: {foreground_count}")
    
    # Phương pháp 1: Crossing Number (CN)
    print(f"[DEBUG] Đang phân tích bằng Crossing Number...")
    cn_endings = []
    cn_bifurcations = []
    
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            if anh_manh[i, j] > 100:
                cn = tinh_crossing_number(anh_manh, i, j)
                
                if cn == 1:
                    cn_endings.append((i, j))
                elif cn == 3 or cn == 5:
                    cn_bifurcations.append((i, j))
    
    print(f"[DEBUG] CN: Ending={len(cn_endings)}, Bifurcation={len(cn_bifurcations)}")
    
    # Phương pháp 2: Đếm hàng xóm (Alternative)
    print(f"[DEBUG] Đang phân tích bằng Neighbor Count...")
    neighbor_endings = []
    neighbor_bifurcations = []
    
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            if anh_manh[i, j] > 100:
                # Đếm foreground hàng xóm (8-connected)
                neighbors = anh_manh[i-1:i+2, j-1:j+2] > 100
                neighbor_count = np.sum(neighbors) - 1  # Trừ chính nó
                
                if neighbor_count == 1:  # Endpoint (ending)
                    neighbor_endings.append((i, j))
                elif neighbor_count >= 3 and neighbor_count <= 4:  # Bifurcation
                    neighbor_bifurcations.append((i, j))
    
    print(f"[DEBUG] Neighbor: Ending={len(neighbor_endings)}, Bifurcation={len(neighbor_bifurcations)}")
    
    # Chọn phương pháp tốt hơn
    if len(cn_endings) + len(cn_bifurcations) > 0:
        endings = cn_endings
        bifurcations = cn_bifurcations
        print(f"[DEBUG] Sử dụng kết quả Crossing Number")
    elif len(neighbor_endings) + len(neighbor_bifurcations) > 0:
        endings = neighbor_endings
        bifurcations = neighbor_bifurcations
        print(f"[DEBUG] Sử dụng kết quả Neighbor Count (CN không có kết quả)")
    
    print(f"[DEBUG] Final: Ending={len(endings)}, Bifurcation={len(bifurcations)}")
    
    return endings, bifurcations


def tinh_huong_minutiae(anh_manh, point, window_size=11):
    """
    Tính hướng của minutiae point
    Cải tiến: Tăng window_size và xử lý lỗi tốt hơn
    
    Args:
        anh_manh (np.ndarray): Ảnh làm mảnh
        point (tuple): Tọa độ (i, j)
        window_size (int): Kích thước cửa sổ tính hướng
        
    Returns:
        float: Hướng tính bằng độ (0-360)
    """
    i, j = point
    h, w = anh_manh.shape
    
    # Lấy vùng xung quanh point
    y1 = max(0, i - window_size // 2)
    y2 = min(h, i + window_size // 2 + 1)
    x1 = max(0, j - window_size // 2)
    x2 = min(w, j + window_size // 2 + 1)
    
    region = anh_manh[y1:y2, x1:x2] > 100  # Giảm ngưỡng
    
    if np.sum(region) == 0:
        return 0  # Nếu không có điểm, trả về 0
    
    # Tính gradient
    gy, gx = np.gradient(region.astype(float))
    
    # Tính hướng từ gradient
    mean_gy = np.mean(gy)
    mean_gx = np.mean(gx)
    
    if mean_gx == 0 and mean_gy == 0:
        return 0
    
    huong = np.arctan2(mean_gy, mean_gx)
    huong = np.degrees(huong) % 360
    
    return huong


def trich_minutiae_chi_tiet(anh_manh):
    """
    Trích chọn minutiae với chi tiết đầy đủ
    
    Args:
        anh_manh (np.ndarray): Ảnh làm mảnh nhị phân
        
    Returns:
        dict: Dictionary chứa danh sách ending và bifurcation với hướng
    """
    endings, bifurcations = phan_loai_minutiae(anh_manh)
    
    minutiae = {
        'endings': [],
        'bifurcations': []
    }
    
    # Tính hướng cho các ending points
    for point in endings:
        huong = tinh_huong_minutiae(anh_manh, point)
        minutiae['endings'].append({
            'position': point,
            'orientation': huong,
            'type': 'ending'
        })
    
    # Tính hướng cho các bifurcation points
    for point in bifurcations:
        huong = tinh_huong_minutiae(anh_manh, point)
        minutiae['bifurcations'].append({
            'position': point,
            'orientation': huong,
            'type': 'bifurcation'
        })
    
    return minutiae


def loc_nhieu_minutiae(endings, bifurcations, min_distance=2):
    """
    Loại bỏ các minutiae giả (nhiễu)
    bằng cách xóa những điểm quá gần nhau
    
    Args:
        endings (list): Danh sách ending points
        bifurcations (list): Danh sách bifurcation points
        min_distance (float): Khoảng cách tối thiểu cho phép (mặc định=2)
        
    Returns:
        tuple: (endings đã lọc, bifurcations đã lọc)
    """
    def loc_nhieu_danh_sach(points, min_dist):
        if not points:
            return []
        
        points = sorted(points)
        filtered = [points[0]]
        
        for point in points[1:]:
            # Tính khoảng cách với tất cả điểm đã chọn
            min_dist_to_selected = min(
                np.sqrt((point[0] - p[0])**2 + (point[1] - p[1])**2)
                for p in filtered
            )
            
            if min_dist_to_selected >= min_dist:
                filtered.append(point)
        
        return filtered
    
    endings_filtered = loc_nhieu_danh_sach(endings, min_distance)
    bifurcations_filtered = loc_nhieu_danh_sach(bifurcations, min_distance)
    
    return endings_filtered, bifurcations_filtered
