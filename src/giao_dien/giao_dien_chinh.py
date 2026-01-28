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
from giao_dien.database_handler import DatabaseEventHandler
from giao_dien.giao_dien_dang_ky import GiaoDienDangKy
from giao_dien.giao_dien_tim_kiem import GiaoDienTimKiem


class GiaoDienChinh:
    """Lớp giao diện chính"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống nhận dạng vân tay - Fingerprint Recognition System")
        self.root.geometry("1600x950")
        self.root.minsize(1000, 600)
        
        # Thiết lập style
        self._setup_style()
        
        # Tạo header
        self._tao_header()
        
        # Tạo database handler
        self.db_handler = DatabaseEventHandler(self)
        
        # Tạo xử lý sự kiện
        self.hien_thi_ket_qua = None
        self.xu_ly_su_kien = XuLySuKien(self)
        self.db_handler.set_xu_ly_su_kien(self.xu_ly_su_kien)
        
        # Tạo toolbar
        self._tao_toolbar(root)
        
        # Tạo notebook (tabs) cho giao diện chính
        self.notebook_main = ttk.Notebook(root)
        self.notebook_main.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: So khớp 2 ảnh
        tab_so_khop = ttk.Frame(self.notebook_main)
        self.notebook_main.add(tab_so_khop, text="So Khớp 2 Ảnh")
        
        self.hien_thi_ket_qua = HienThiKetQua(tab_so_khop)
        
        # Gán lệnh cho các nút tải ảnh trong tab
        self.hien_thi_ket_qua.btn_anh_1.config(command=self.xu_ly_su_kien.chon_anh_1)
        self.hien_thi_ket_qua.btn_anh_2.config(command=self.xu_ly_su_kien.chon_anh_2)
        
        # Tab 2: Đăng ký người dùng
        tab_dang_ky = ttk.Frame(self.notebook_main)
        self.notebook_main.add(tab_dang_ky, text="Đăng Ký Người Dùng")
        
        self.giao_dien_dang_ky = GiaoDienDangKy(tab_dang_ky, self.db_handler)
        
        # Tab 3: Tìm kiếm/Nhận dạng
        tab_tim_kiem = ttk.Frame(self.notebook_main)
        self.notebook_main.add(tab_tim_kiem, text="Tìm Kiếm")
        
        self.giao_dien_tim_kiem = GiaoDienTimKiem(tab_tim_kiem, self.db_handler)
        
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
        title_label = tk.Label(header, text='HỆ THÔNG NHẬN DẠNG VÂN TAY', 
                               font=('Arial', 16, 'bold'), fg='white', bg='#1a1a1a')
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Subtitle
        subtitle_label = tk.Label(header, text='Nguyễn Phúc An (110122214) - Nguyễn Thiên Ân (110122030) - Hứa Khánh Đăng (110122046)', 
                                  font=('Arial', 10), fg='#cccccc', bg='#1a1a1a')
        subtitle_label.pack(side=tk.LEFT, padx=0, pady=10)
        
        # Status bar
        self.status_label = tk.Label(header, text='Chưa kết nối Database', 
                                     font=('Arial', 9), fg='#ff9999', bg='#1a1a1a')
        self.status_label.pack(side=tk.RIGHT, padx=20, pady=10)
    
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
        
        # Menu Database
        menu_db = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Database", menu=menu_db)
        menu_db.add_command(label="Kết Nối Database", command=self._ket_noi_database)
        menu_db.add_command(label="Xem Thống Kê", command=self._xem_thong_ke)
        menu_db.add_separator()
        menu_db.add_command(label="Lịch Sử So Khớp", command=self._xem_lich_su)
        
        # Menu Trợ giúp
        menu_help = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Trợ giúp", menu=menu_help)
        menu_help.add_command(label="Về chương trình", command=self._about)
    
    def _tao_toolbar(self, parent):
        """Tạo toolbar"""
        toolbar_frame = ttk.LabelFrame(parent, text="CÔNG CỤ", padding=10)
        toolbar_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.TOP)
        
        # Row 1: Database connection
        db_frame = ttk.Frame(toolbar_frame)
        db_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(db_frame, text="Database:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5)
        ttk.Button(db_frame, text="Kết Nối", width=15,
                  command=self._ket_noi_database).pack(side=tk.LEFT, padx=3)
        ttk.Button(db_frame, text="Thống Kê", width=15,
                  command=self._xem_thong_ke).pack(side=tk.LEFT, padx=3)
        
        ttk.Separator(db_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=15)
        
        # Row 2: Processing
        proc_frame = ttk.Frame(toolbar_frame)
        proc_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(proc_frame, text="Xử lý:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5)
        ttk.Button(proc_frame, text="Tiền xử lý", width=15,
                  command=self.xu_ly_su_kien.tien_xu_ly_anh).pack(side=tk.LEFT, padx=3)
        ttk.Button(proc_frame, text="Nhị phân hóa", width=15,
                  command=self.xu_ly_su_kien.nhi_phan_hoa_anh).pack(side=tk.LEFT, padx=3)
        ttk.Button(proc_frame, text="Làm mảnh", width=15,
                  command=self.xu_ly_su_kien.lam_manh_anh).pack(side=tk.LEFT, padx=3)
        ttk.Button(proc_frame, text="Trích đặc trưng", width=18,
                  command=self.xu_ly_su_kien.trich_dac_trung).pack(side=tk.LEFT, padx=3)
        
        ttk.Separator(proc_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=15)
        
        # Phương pháp so khớp
        ttk.Label(proc_frame, text="So khớp:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5)
        self.matching_method = tk.StringVar(value="minutiae")
        combo_matching = ttk.Combobox(proc_frame, textvariable=self.matching_method, 
                                      values=["minutiae", "feature", "lbp", "ridge", "frequency"],
                                      width=20, state='readonly')
        combo_matching.pack(side=tk.LEFT, padx=3)
        
        # Bind event để cập nhật UI khi thay đổi dropdown
        def on_matching_method_change(*args):
            phương_pháp = self.matching_method.get()
            self.hien_thi_ket_qua.cap_nhat_phuong_phap_so_khop(phương_pháp)
        
        self.matching_method.trace('w', on_matching_method_change)
        
        ttk.Button(proc_frame, text="Thực hiện", width=12,
                  command=self.xu_ly_su_kien.so_khop_anh).pack(side=tk.LEFT, padx=3)
        
        ttk.Button(proc_frame, text="So khớp tất cả", width=15,
                  command=self.xu_ly_su_kien.so_khop_tat_ca).pack(side=tk.LEFT, padx=3)
        
        ttk.Separator(proc_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=15)
        
        ttk.Button(proc_frame, text="Xóa dữ liệu", width=13,
                  command=self.xu_ly_su_kien.xoa_du_lieu).pack(side=tk.LEFT, padx=3)
    
    def _ket_noi_database(self):
        """Kết nối database"""
        if self.db_handler.ket_noi_database():
            self.status_label.config(text="Đã kết nối Database", fg='#99ff99')
    
    def _xem_thong_ke(self):
        """Xem thống kê database"""
        if not self.db_handler.kiểm_tra_kết_nối():
            return
        
        from tkinter import messagebox
        stats = self.db_handler.lay_thong_ke()
        
        message = f"""
        Thống Kê Hệ Thống:
        
        - Tổng người dùng: {stats.get('total_users', 0)}
        - Tổng vân tay: {stats.get('total_fingerprints', 0)}
        - Tổng lần so khớp: {stats.get('total_matches', 0)}
        - Lần thành công: {stats.get('successful_matches', 0)}
        - Tỉ lệ thành công: {stats.get('match_success_rate', 0):.2f}%
        """
        
        messagebox.showinfo("Thống Kê", message)
    
    def _xem_lich_su(self):
        """Xem lịch sử so khớp"""
        if not self.db_handler.kiểm_tra_kết_nối():
            return
        
        from tkinter import messagebox
        history = self.db_handler.lay_lich_su_so_khop(limit=10)
        
        if not history:
            messagebox.showinfo("Lịch Sử", "Không có lịch sử so khớp")
            return
        
        message = "Lịch Sử So Khớp (10 lần gần nhất):\n\n"
        for h in history:
            message += f"- {h.get('full_name', 'Unknown')} - {h.get('matching_method', 'N/A')} - {h.get('similarity_score', 0):.2f}\n"
        
        messagebox.showinfo("Lịch Sử", message)
    
    def _about(self):
        """Hiển thị thông tin về chương trình"""
        from tkinter import messagebox
        messagebox.showinfo("Về chương trình",
                          "Hệ thống nhận dạng vân tay\n"
                          "Phiên bản 3.0\n\n"
                          "Tính năng:\n"
                          "- 5 phương pháp so khớp\n"
                          "- Database MySQL\n"
                          "- Nhận dạng người dùng\n\n"
                          "Công nghệ:\n"
                          "- Python 3.x\n"
                          "- OpenCV\n"
                          "- NumPy\n"
                          "- MySQL")


def tao_giao_dien():
    """Hàm chính để tạo giao diện"""
    root = tk.Tk()
    app = GiaoDienChinh(root)
    root.mainloop()


if __name__ == "__main__":
    tao_giao_dien()

