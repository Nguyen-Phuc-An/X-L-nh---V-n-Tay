"""
Module so khớp ảnh vân tay
"""

import numpy as np
from scipy.spatial.distance import euclidean
import cv2


def tinh_khoang_cach_minutiae(minutiae1, minutiae2, max_distance=50, angle_tolerance=30):
    """
    Tính khoảng cách giữa hai minutiae points
    Xét cả vị trí và hướng
    
    Args:
        minutiae1 (dict): {'position': (i, j), 'orientation': angle}
        minutiae2 (dict): {'position': (i, j), 'orientation': angle}
        max_distance (float): Khoảng cách tối đa để coi là match
        angle_tolerance (float): Độ chịu nước cơn dành hướng (độ)
        
    Returns:
        float: Điểm tương đồng (0-100), 0 nếu không match
    """
    # Tính khoảng cách Euclidean
    pos1 = np.array(minutiae1['position'])
    pos2 = np.array(minutiae2['position'])
    dist = euclidean(pos1, pos2)
    
    # Kiểm tra khoảng cách
    if dist > max_distance:
        return 0.0
    
    # Tính chênh lệch hướng
    angle1 = minutiae1.get('orientation', 0)
    angle2 = minutiae2.get('orientation', 0)
    angle_diff = abs(angle1 - angle2)
    
    # Điều chỉnh angle_diff về [0, 180]
    if angle_diff > 180:
        angle_diff = 360 - angle_diff
    
    # Kiểm tra hướng
    if angle_diff > angle_tolerance:
        return 0.0
    
    # Tính điểm dựa trên khoảng cách
    distance_score = (max_distance - dist) / max_distance * 100
    
    # Tính điểm dựa trên hướng
    angle_score = (angle_tolerance - angle_diff) / angle_tolerance * 100
    
    # Trung bình hai điểm
    overall_score = (distance_score + angle_score) / 2
    
    return max(0, overall_score)


def so_khop_minutiae(minutiae1, minutiae2, max_distance=50, angle_tolerance=30, min_matches=5):
    """
    So khớp hai tập hợp minutiae
    
    Args:
        minutiae1 (dict): {'endings': [...], 'bifurcations': [...]}
        minutiae2 (dict): {'endings': [...], 'bifurcations': [...]}
        max_distance (float): Khoảng cách tối đa
        angle_tolerance (float): Độ chịu nước cơn về hướng
        min_matches (int): Số match tối thiểu
        
    Returns:
        dict: Kết quả so khớp với chi tiết
    """
    # Kết hợp tất cả minutiae từ cả hai tập hợp
    all_minutiae1 = minutiae1.get('endings', []) + minutiae1.get('bifurcations', [])
    all_minutiae2 = minutiae2.get('endings', []) + minutiae2.get('bifurcations', [])
    
    if not all_minutiae1 or not all_minutiae2:
        return {
            'match_count': 0,
            'total_minutiae1': len(all_minutiae1),
            'total_minutiae2': len(all_minutiae2),
            'similarity_score': 0.0,
            'matched_pairs': []
        }
    
    matched_pairs = []
    matched_indices2 = set()
    
    # Tìm matching cho mỗi minutiae từ tập 1
    for m1 in all_minutiae1:
        best_match = None
        best_score = 0
        best_index = -1
        
        for idx2, m2 in enumerate(all_minutiae2):
            if idx2 in matched_indices2:
                continue
            
            score = tinh_khoang_cach_minutiae(m1, m2, max_distance, angle_tolerance)
            
            if score > best_score:
                best_score = score
                best_match = m2
                best_index = idx2
        
        if best_score > 0:
            matched_pairs.append({
                'minutiae1': m1,
                'minutiae2': best_match,
                'score': best_score
            })
            matched_indices2.add(best_index)
    
    # Tính điểm tương đồng
    if matched_pairs:
        avg_score = np.mean([pair['score'] for pair in matched_pairs])
    else:
        avg_score = 0.0
    
    # Tính tỉ lệ so khớp
    max_minutiae = max(len(all_minutiae1), len(all_minutiae2))
    match_count = len(matched_pairs)
    match_percentage = (match_count / max_minutiae * 100) if max_minutiae > 0 else 0
    
    return {
        'match_count': match_count,
        'total_minutiae1': len(all_minutiae1),
        'total_minutiae2': len(all_minutiae2),
        'similarity_score': avg_score,
        'match_percentage': match_percentage,
        'matched_pairs': matched_pairs,
        'is_match': match_count >= min_matches and avg_score > 30
    }


def so_khop_anh_toan_phan(minutiae1, minutiae2, anh1=None, anh2=None, 
                          max_distance=50, angle_tolerance=30):
    """
    So khớp toàn phần giữa hai ảnh vân tay
    
    Args:
        minutiae1 (dict): Minutiae từ ảnh 1
        minutiae2 (dict): Minutiae từ ảnh 2
        anh1 (np.ndarray): Ảnh làm mảnh 1 (tuỳ chọn)
        anh2 (np.ndarray): Ảnh làm mảnh 2 (tuỳ chọn)
        max_distance (float): Khoảng cách tối đa
        angle_tolerance (float): Độ chịu nước cơn về hướng
        
    Returns:
        dict: Kết quả so khớp chi tiết
    """
    result = so_khop_minutiae(minutiae1, minutiae2, max_distance, angle_tolerance)
    
    # Thêm thông tin ảnh nếu có
    if anh1 is not None and anh2 is not None:
        result['fingerprint1_shape'] = anh1.shape
        result['fingerprint2_shape'] = anh2.shape
    
    return result


def tinh_diem_tuong_dong_tien_tien(minutiae1, minutiae2, 
                                  max_distance=50, angle_tolerance=30):
    """
    Tính điểm tương đồng nâng cao
    Xét thêm cấu trúc và mối quan hệ giữa các minutiae
    
    Args:
        minutiae1 (dict): Minutiae từ ảnh 1
        minutiae2 (dict): Minutiae từ ảnh 2
        max_distance (float): Khoảng cách tối đa
        angle_tolerance (float): Độ chịu nước cơn về hướng
        
    Returns:
        float: Điểm tương đồng cuối cùng (0-100)
    """
    result = so_khop_minutiae(minutiae1, minutiae2, max_distance, angle_tolerance)
    
    match_count = result['match_count']
    total = max(result['total_minutiae1'], result['total_minutiae2'])
    
    if total == 0:
        return 0.0
    
    # Điểm dựa trên số lượng match
    match_score = (match_count / total) * 50
    
    # Điểm dựa trên quality của match
    quality_score = result['similarity_score'] * 0.5
    
    # Điểm cuối cùng
    final_score = min(100, match_score + quality_score)
    
    return final_score


def phan_loai_match(similarity_score, match_percentage):
    """
    Phân loại kết quả so khớp
    
    Args:
        similarity_score (float): Điểm tương đồng (0-100)
        match_percentage (float): Tỉ lệ so khớp (%)
        
    Returns:
        str: Loại match ('match', 'possible_match', 'non_match')
    """
    if similarity_score >= 70 and match_percentage >= 50:
        return 'match'
    elif similarity_score >= 50 and match_percentage >= 30:
        return 'possible_match'
    else:
        return 'non_match'
