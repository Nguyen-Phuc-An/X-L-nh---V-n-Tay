"""
Module giao diện chính Tkinter
Hệ thống nhận dạng vân tay
"""

import tkinter as tk
from tkinter import ttk
import os
import sys

# Thêm đường dẫn để import các module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from giao_dien.hien_thi_ket_qua import HienThiKetQua
from giao_dien.xu_ly_su_kien import XuLySuKien


class GiaoDienChinh:
    """Lớp giao diện chính"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống nhận dạng vân tay - Fingerprint Recognition System")
        self.root.geometry("1500x900")
        self.root.minsize(1000, 600)
        
        # Thiết lập style
        self._setup_style()
        
        # Tạo header
        self._tao_header()
        
        # Tạo xử lý sự kiện trước (để dùng cho toolbar và menu bar)
        self.hien_thi_ket_qua = None
        self.xu_ly_su_kien = XuLySuKien(self)
        
        # Tạo toolbar (thanh công cụ) - ở trên cùng trước main_frame
        self._tao_toolbar(root)
        
        # Tạo main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tạo hiển thị kết quả
        self.hien_thi_ket_qua = HienThiKetQua(main_frame)
        
        # Tạo menu bar
        self._tao_menu_bar()
    
    def _setup_style(self):
        """Cấu hình style toàn cục"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cấu hình màu sắc
        bg_color = '#f0f0f0'
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color)
        style.configure('TButton', font=('Arial', 9))
    
    def _tao_header(self):
        """Tạo header với logo và tiêu đề"""
        header = tk.Frame(self.root, bg='#1a1a1a', height=60)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        # Tiêu đề
        title_label = tk.Label(header, text='🔐 FINGERPRINT RECOGNITION SYSTEM', 
                               font=('Arial', 16, 'bold'), fg='white', bg='#1a1a1a')
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Subtitle
        subtitle_label = tk.Label(header, text='Hệ thống nhận dạng vân tay thông minh', 
                                  font=('Arial', 10), fg='#cccccc', bg='#1a1a1a')
        subtitle_label.pack(side=tk.LEFT, padx=0, pady=10)
    
    def _tao_menu_bar(self):
        """Tạo menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu File
        menu_file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=menu_file)
        menu_file.add_command(label="Chọn ảnh 1", command=self.xu_ly_su_kien.chon_anh_1)
        menu_file.add_command(label="Chọn ảnh 2", command=self.xu_ly_su_kien.chon_anh_2)
        menu_file.add_separator()
        menu_file.add_command(label="Thoát", command=self.root.quit)
        
        # Menu Xử lý
        menu_xu_ly = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Xử lý", menu=menu_xu_ly)
        menu_xu_ly.add_command(label="Tiền xử lý", command=self.xu_ly_su_kien.tien_xu_ly_anh)
        menu_xu_ly.add_command(label="Nhị phân hóa", command=self.xu_ly_su_kien.nhi_phan_hoa_anh)
        menu_xu_ly.add_command(label="Làm mảnh", command=self.xu_ly_su_kien.lam_manh_anh)
        menu_xu_ly.add_command(label="Trích đặc trưng", command=self.xu_ly_su_kien.trich_dac_trung)
        menu_xu_ly.add_command(label="So khớp", command=self.xu_ly_su_kien.so_khop_anh)
        
        # Menu Trợ giúp
        menu_help = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Trợ giúp", menu=menu_help)
        menu_help.add_command(label="Về chương trình", command=self._about)
    
    def _tao_toolbar(self, parent):
        """Tạo toolbar"""
        toolbar_frame = ttk.LabelFrame(parent, text="🛠️ CÔNG CỤ", padding=10)
        toolbar_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.TOP)
        
        # Row 1: File selection
        file_frame = ttk.Frame(toolbar_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_frame, text="Tải ảnh:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="📁 Ảnh 1", width=12,
                  command=self.xu_ly_su_kien.chon_anh_1).pack(side=tk.LEFT, padx=3)
        ttk.Button(file_frame, text="📁 Ảnh 2", width=12,
                  command=self.xu_ly_su_kien.chon_anh_2).pack(side=tk.LEFT, padx=3)
        
        ttk.Separator(file_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=15)
        
        # Row 2: Processing
        proc_frame = ttk.Frame(toolbar_frame)
        proc_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(proc_frame, text="Xử lý:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5)
        ttk.Button(proc_frame, text="🔧 Tiền xử lý", width=15,
                  command=self.xu_ly_su_kien.tien_xu_ly_anh).pack(side=tk.LEFT, padx=3)
        ttk.Button(proc_frame, text="⚫ Nhị phân hóa", width=15,
                  command=self.xu_ly_su_kien.nhi_phan_hoa_anh).pack(side=tk.LEFT, padx=3)
        ttk.Button(proc_frame, text="✏️ Làm mảnh", width=15,
                  command=self.xu_ly_su_kien.lam_manh_anh).pack(side=tk.LEFT, padx=3)
        ttk.Button(proc_frame, text="🔍 Trích đặc trưng", width=18,
                  command=self.xu_ly_su_kien.trich_dac_trung).pack(side=tk.LEFT, padx=3)
        ttk.Button(proc_frame, text="⚖️ So khớp", width=12,
                  command=self.xu_ly_su_kien.so_khop_anh).pack(side=tk.LEFT, padx=3)
        
        ttk.Separator(proc_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=15)
        
        ttk.Button(proc_frame, text="🗑️ Xóa dữ liệu", width=13,
                  command=self.xu_ly_su_kien.xoa_du_lieu).pack(side=tk.LEFT, padx=3)
    
    def _about(self):
        """Hiển thị thông tin về chương trình"""
        from tkinter import messagebox
        messagebox.showinfo("Về chương trình",
                          "Hệ thống nhận dạng vân tay\n"
                          "Phiên bản 1.0\n\n"
                          "Công nghệ:\n"
                          "- Python 3.x\n"
                          "- OpenCV\n"
                          "- NumPy\n"
                          "- Tkinter")


def tao_giao_dien():
    """Hàm chính để tạo giao diện"""
    root = tk.Tk()
    app = GiaoDienChinh(root)
    root.mainloop()


if __name__ == "__main__":
    tao_giao_dien()
