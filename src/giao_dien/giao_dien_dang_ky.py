"""
Module giao diện đăng ký người dùng mới
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tien_xu_ly.chuyen_xam import chuyen_nh_xam
from tien_xu_ly.chuan_hoa import chuan_hoa_anh
from tien_xu_ly.tang_cuong import ap_dung_gabor_filter
from phan_doan.nhi_phan_hoa import nhi_phan_hoa_otsu
from lam_manh.lam_manh_anh import lam_manh_scikit_image
from trich_dac_trung.trich_dac_trung_chi_tiet import trich_minutiae_chi_tiet


class GiaoDienDangKy:
    """Giao diện đăng ký người dùng mới"""
    
    def __init__(self, parent_frame, database_handler):
        """
        Khởi tạo giao diện đăng ký
        
        Args:
            parent_frame: Frame cha
            database_handler: Instance DatabaseEventHandler
        """
        self.parent = parent_frame
        self.db_handler = database_handler
        
        # Biến lưu trữ
        self.anh_duong_dan = None
        self.anh_goc = None
        self.anh_xam = None
        self.anh_nhi_phan = None
        self.anh_manh = None
        self.minutiae = None
        self.feature_data = None
        self.lbp_data = None
        self.ridge_data = None
        self.frequency_data = None
        
        self._tao_giao_dien()
    
    def _tao_giao_dien(self):
        """Tạo giao diện đăng ký"""
        # Frame chính
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame chính sử dụng PanedWindow cho 3 cột
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # ===== CỘT TRÁI: Thông tin người dùng =====
        info_frame = ttk.Frame(paned_window)
        paned_window.add(info_frame, weight=1)
        
        # Label cho phần thông tin
        ttk.Label(info_frame, text="THÔNG TIN NGƯỜI DÙNG", 
                 font=('Arial', 10, 'bold')).pack(pady=15)
        
        # Scrollable frame cho form
        canvas = tk.Canvas(info_frame, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Username
        frame_username = ttk.Frame(scrollable_frame)
        frame_username.pack(fill=tk.X, padx=10, pady=8)
        ttk.Label(frame_username, text="Username:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.var_username = tk.StringVar()
        ttk.Entry(frame_username, textvariable=self.var_username, width=30).pack(fill=tk.X, pady=4)
        
        # Full Name
        frame_fullname = ttk.Frame(scrollable_frame)
        frame_fullname.pack(fill=tk.X, padx=10, pady=8)
        ttk.Label(frame_fullname, text="Họ và Tên:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.var_fullname = tk.StringVar()
        ttk.Entry(frame_fullname, textvariable=self.var_fullname, width=30).pack(fill=tk.X, pady=4)
        
        # Email
        frame_email = ttk.Frame(scrollable_frame)
        frame_email.pack(fill=tk.X, padx=10, pady=8)
        ttk.Label(frame_email, text="Email:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.var_email = tk.StringVar()
        ttk.Entry(frame_email, textvariable=self.var_email, width=30).pack(fill=tk.X, pady=4)
        
        # Phone
        frame_phone = ttk.Frame(scrollable_frame)
        frame_phone.pack(fill=tk.X, padx=10, pady=8)
        ttk.Label(frame_phone, text="Số điện thoại:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.var_phone = tk.StringVar()
        ttk.Entry(frame_phone, textvariable=self.var_phone, width=30).pack(fill=tk.X, pady=4)
        
        # ID Number
        frame_idnumber = ttk.Frame(scrollable_frame)
        frame_idnumber.pack(fill=tk.X, padx=10, pady=8)
        ttk.Label(frame_idnumber, text="CCCD/Hộ chiếu:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.var_idnumber = tk.StringVar()
        ttk.Entry(frame_idnumber, textvariable=self.var_idnumber, width=30).pack(fill=tk.X, pady=4)
        
        # Position
        frame_position = ttk.Frame(scrollable_frame)
        frame_position.pack(fill=tk.X, padx=10, pady=8)
        ttk.Label(frame_position, text="Chức vụ:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.var_position = tk.StringVar()
        ttk.Entry(frame_position, textvariable=self.var_position, width=30).pack(fill=tk.X, pady=4)
        
        # Department
        frame_department = ttk.Frame(scrollable_frame)
        frame_department.pack(fill=tk.X, padx=10, pady=8)
        ttk.Label(frame_department, text="Phòng ban:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.var_department = tk.StringVar()
        ttk.Entry(frame_department, textvariable=self.var_department, width=30).pack(fill=tk.X, pady=4)
        
        # ===== CỘT GIỮA: Ảnh xem trước =====
        image_frame = ttk.Frame(paned_window)
        paned_window.add(image_frame, weight=1)
        
        ttk.Label(image_frame, text="HÌNH ẢNH XEM TRƯỚC", 
                 font=('Arial', 10, 'bold')).pack(pady=10)
        
        # Canvas hiển thị ảnh
        self.canvas_image = tk.Canvas(image_frame, bg='#e0e0e0')
        self.canvas_image.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ===== CỘT PHẢI: Xử lý ảnh và nút thao tác =====
        action_frame = ttk.Frame(paned_window)
        paned_window.add(action_frame, weight=1)
        
        ttk.Label(action_frame, text="TÙYỂN ĐỘC & THAO TÁC", 
                 font=('Arial', 10, 'bold')).pack(pady=10)
        
        # Upload button frame
        button_top_frame = ttk.Frame(action_frame)
        button_top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_top_frame, text="Chọn Ảnh", 
                  command=self._chon_anh).pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
        
        ttk.Button(button_top_frame, text="Xóa Ảnh", 
                  command=self._xoa_anh).pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
        
        # Finger name
        ttk.Label(action_frame, text="Ngón tay:", font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=5, pady=(10, 3))
        self.var_finger = tk.StringVar(value="Thumb")
        combo_finger = ttk.Combobox(action_frame, textvariable=self.var_finger,
                                    values=["Thumb", "Index", "Middle", "Ring", "Pinky"],
                                    state='readonly', width=30)
        combo_finger.pack(pady=5, fill=tk.X, padx=5)
        
        # Hand
        ttk.Label(action_frame, text="Tay:", font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=5, pady=(10, 3))
        self.var_hand = tk.StringVar(value="Right")
        combo_hand = ttk.Combobox(action_frame, textvariable=self.var_hand,
                                 values=["Right", "Left"],
                                 state='readonly', width=30)
        combo_hand.pack(pady=5, fill=tk.X, padx=5)
        
        # Separator
        ttk.Separator(action_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10, padx=5)
        
        # ===== Phần thông tin xử lý =====
        ttk.Label(action_frame, text="Trạng thái xử lý:", font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=5)
        
        self.text_status = tk.Text(action_frame, height=6, width=35, state=tk.DISABLED, wrap=tk.WORD)
        self.text_status.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ===== Buttons =====
        button_bottom_frame = ttk.Frame(action_frame)
        button_bottom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_bottom_frame, text="✅ Đăng Ký",
                  command=self._dang_ky).pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
        
        ttk.Button(button_bottom_frame, text="Làm Mới",
                  command=self._lam_moi).pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
    
    def _chon_anh(self):
        """Chọn ảnh vân tay"""
        duong_dan = filedialog.askopenfilename(
            title="Chọn ảnh vân tay",
            filetypes=[("Ảnh", "*.jpg *.jpeg *.png *.bmp"), ("Tất cả", "*.*")]
        )
        
        if not duong_dan:
            return
        
        try:
            self.anh_duong_dan = duong_dan
            
            # Đọc ảnh
            self.anh_goc, self.anh_xam = chuyen_nh_xam(duong_dan)
            
            # Hiển thị ảnh toàn màn hình
            # Lấy kích thước canvas
            canvas_width = self.canvas_image.winfo_width()
            canvas_height = self.canvas_image.winfo_height()
            
            # Nếu canvas chưa có kích thước, dùng mặc định
            if canvas_width <= 1:
                canvas_width = 400
            if canvas_height <= 1:
                canvas_height = 400
            
            # Resize ảnh để vừa canvas
            aspect_ratio = self.anh_xam.shape[1] / self.anh_xam.shape[0]
            if (canvas_width / canvas_height) > aspect_ratio:
                # Canvas rộng hơn
                display_height = canvas_height
                display_width = int(display_height * aspect_ratio)
            else:
                # Canvas cao hơn
                display_width = canvas_width
                display_height = int(display_width / aspect_ratio)
            
            anh_display = cv2.resize(self.anh_xam, (display_width, display_height))
            anh_pil = Image.fromarray(anh_display)
            anh_tk = ImageTk.PhotoImage(anh_pil)
            
            # Xóa ảnh cũ
            self.canvas_image.delete("all")
            
            # Vẽ ảnh ở giữa canvas
            self.canvas_image.create_image(canvas_width // 2, canvas_height // 2, 
                                          image=anh_tk)
            self.canvas_image.image = anh_tk
            
            self._cap_nhat_trang_thai(f"Đã chọn ảnh: {os.path.basename(duong_dan)}")
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi chọn ảnh: {str(e)}")
            self._cap_nhat_trang_thai(f"Lỗi: {str(e)}")
    
    def _xoa_anh(self):
        """Xóa ảnh đã chọn"""
        self.anh_duong_dan = None
        self.anh_goc = None
        self.anh_xam = None
        self.anh_nhi_phan = None
        self.anh_manh = None
        self.minutiae = None
        self.feature_data = None
        self.lbp_data = None
        self.ridge_data = None
        self.frequency_data = None
        
        self.canvas_image.delete("all")
        self._cap_nhat_trang_thai("Ảnh đã được xóa")
    
    def _xu_ly_anh(self):
        """Xử lý ảnh tự động"""
        if self.anh_xam is None:
            return False
        
        try:
            self._cap_nhat_trang_thai("Đang xử lý ảnh...")
            
            # Chuẩn hóa
            self._cap_nhat_trang_thai("Đang chuẩn hóa...")
            anh_chuan_hoa = chuan_hoa_anh(self.anh_xam)
            
            # Tăng cường
            self._cap_nhat_trang_thai("Đang tăng cường...")
            anh_tang_cuong = ap_dung_gabor_filter(anh_chuan_hoa)
            
            # Nhị phân hóa
            self._cap_nhat_trang_thai("Đang nhị phân hóa...")
            anh_nhi_phan, _ = nhi_phan_hoa_otsu(anh_tang_cuong)
            
            # Lưu ảnh nhị phân
            self.anh_nhi_phan = anh_nhi_phan
            
            # Làm mảnh
            self._cap_nhat_trang_thai("Đang làm mảnh ảnh...")
            self.anh_manh = lam_manh_scikit_image(anh_nhi_phan)
            
            # Lưu ảnh tiền xử lý (cho Feature/LBP/Ridge/Frequency)
            self.anh_xu_ly = anh_nhi_phan  # Ảnh nhị phân trước thinning
            
            # Trích tất cả đặc trưng từ ảnh tiền xử lý (anh_nhi_phan)
            self._cap_nhat_trang_thai("Đang trích tất cả đặc trưng...")
            
            # Minutiae (từ ảnh làm mảnh)
            self.minutiae = trich_minutiae_chi_tiet(self.anh_manh)
            
            # Feature (SIFT)
            try:
                sift = cv2.SIFT_create()
                kp, des = sift.detectAndCompute(anh_nhi_phan, None)
                self.feature_data = {
                    'keypoints': [(int(k.pt[0]), int(k.pt[1]), float(k.size), float(k.angle)) for k in kp],
                    'descriptors': des.tolist() if des is not None else []
                }
            except:
                self.feature_data = None
            
            # LBP
            try:
                from skimage.feature import local_binary_pattern
                lbp = local_binary_pattern(anh_nhi_phan, 8, 1)
                hist, _ = np.histogram(lbp.ravel(), bins=256, range=(0, 256))
                self.lbp_data = {
                    'histogram': hist.tolist(),
                    'shape': anh_nhi_phan.shape
                }
            except:
                self.lbp_data = None
            
            # Ridge Orientation
            try:
                gy, gx = np.gradient(anh_nhi_phan.astype(float))
                orientation = np.arctan2(gy, gx)
                step = 10
                sampled_orientation = orientation[::step, ::step]
                self.ridge_data = {
                    'orientation': sampled_orientation.tolist(),
                    'step': step,
                    'shape': anh_nhi_phan.shape
                }
            except:
                self.ridge_data = None
            
            # Frequency Domain
            try:
                wavelengths = [5, 10, 15]
                orientations = [0, 45, 90, 135]
                responses = []
                
                for wl in wavelengths:
                    for angle in orientations:
                        kernel = cv2.getGaborKernel((21, 21), wl, np.radians(angle), 10, 0.5, 0)
                        response = cv2.filter2D(anh_nhi_phan, -1, kernel)
                        responses.append(float(np.mean(np.abs(response))))
                
                self.frequency_data = {
                    'gabor_responses': responses,
                    'wavelengths': wavelengths,
                    'orientations': orientations
                }
            except:
                self.frequency_data = None
            
            # Summary
            minutiae_count = len(self.minutiae.get('endings', [])) + len(self.minutiae.get('bifurcations', [])) if self.minutiae else 0
            
            self._cap_nhat_trang_thai(
                f"Xử lý hoàn tất!\n"
                f"  - Minutiae: {minutiae_count}\n"
                f"  - Feature: {'Đã trích' if self.feature_data else 'Không'}\n"
                f"  - LBP: {'Đã trích' if self.lbp_data else 'Không'}\n"
                f"  - Ridge: {'Đã trích' if self.ridge_data else 'Không'}\n"
                f"  - Frequency: {'Đã trích' if self.frequency_data else 'Không'}"
            )
            return True
        
        except Exception as e:
            self._cap_nhat_trang_thai(f"Lỗi xử lý: {str(e)}")
            messagebox.showerror("Lỗi", f"Lỗi xử lý ảnh: {str(e)}")
            return False
    
    def _dang_ky(self):
        """Đăng ký người dùng"""
        # Kiểm tra thông tin
        if not self.var_username.get():
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập username!")
            return
        
        if not self.var_fullname.get():
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập họ và tên!")
            return
        
        if self.anh_xam is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh vân tay!")
            return
        
        # Kiểm tra kết nối database
        if not self.db_handler.kiểm_tra_kết_nối():
            return
        
        try:
            # Xử lý ảnh
            if not self._xu_ly_anh():
                return
            
            # Thêm người dùng
            self._cap_nhat_trang_thai("Đang lưu người dùng...")
            user_id = self.db_handler.them_nguoi_dung_moi(
                username=self.var_username.get(),
                full_name=self.var_fullname.get(),
                email=self.var_email.get() or None,
                phone=self.var_phone.get() or None,
                address=None,
                date_of_birth=None,
                gender=None,
                identification_number=self.var_idnumber.get() or None,
                position=self.var_position.get() or None,
                department=self.var_department.get() or None,
                notes="Đăng ký lần đầu"
            )
            
            if not user_id:
                return
            
            # Lưu vân tay (lưu ảnh nhị phân)
            self._cap_nhat_trang_thai("Đang lưu vân tay...")
            fingerprint_id = self.db_handler.luu_van_tay(
                user_id=user_id,
                finger_name=self.var_finger.get(),
                hand=self.var_hand.get(),
                anh_xu_ly=self.anh_nhi_phan,
                minutiae_data=self.minutiae,
                quality_score=85.0
            )
            
            if not fingerprint_id:
                return
            
            self._cap_nhat_trang_thai(
                f"Đăng ký thành công!\n"
                f"  - User ID: {user_id}\n"
                f"  - Fingerprint ID: {fingerprint_id}"
            )
            
            messagebox.showinfo("Thành công", 
                              f"Đăng ký thành công!\n\n"
                              f"User ID: {user_id}\n"
                              f"Fingerprint ID: {fingerprint_id}")
            
            self._lam_moi()
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi đăng ký: {str(e)}")
            self._cap_nhat_trang_thai(f"Lỗi: {str(e)}")
    
    def _lam_moi(self):
        """Làm mới form"""
        self.var_username.set("")
        self.var_fullname.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_idnumber.set("")
        self.var_position.set("")
        self.var_department.set("")
        self.var_finger.set("Thumb")
        self.var_hand.set("Right")
        
        self._xoa_anh()
        self._cap_nhat_trang_thai("Form đã được làm mới")
    
    def _cap_nhat_trang_thai(self, message):
        """Cập nhật trạng thái"""
        self.text_status.config(state=tk.NORMAL)
        self.text_status.insert(tk.END, message + "\n")
        self.text_status.see(tk.END)
        self.text_status.config(state=tk.DISABLED)
