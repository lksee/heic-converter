import os
import threading
import concurrent.futures
import subprocess
import platform
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import logging

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
from pillow_heif import register_heif_opener

# HEIF 형식 지원 등록
register_heif_opener()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ImageFormat:
    """이미지 형식 정보를 담는 데이터 클래스"""
    name: str
    extension: str
    pil_format: str

class HEICConverter:
    """HEIC 이미지 변환기 메인 클래스"""
    
    # 지원하는 이미지 형식들
    SUPPORTED_FORMATS = {
        "JPEG": ImageFormat("JPEG", "jpg", "JPEG"),
        "PNG": ImageFormat("PNG", "png", "PNG"),
        "WEBP": ImageFormat("WEBP", "webp", "WEBP")
    }
    
    # 지원하는 HEIC 확장자들
    HEIC_EXTENSIONS = {'.heic', '.heif', '.HEIC', '.HEIF'}
    
    def __init__(self):
        self.source_directory: Optional[Path] = None
        self.output_directory: Optional[Path] = None
        self.heic_files: List[str] = []
        self.setup_ui()
        self.setup_styles()
        
    def setup_styles(self):
        """UI 스타일 설정"""
        style = ttk.Style()
        
        # 테마 설정
        style.theme_use('clam')
        
        # 커스텀 스타일 정의
        style.configure('Title.TLabel', font=('맑은 고딕', 18, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('맑은 고딕', 11, 'bold'), foreground='#34495e')
        style.configure('Info.TLabel', font=('맑은 고딕', 9), foreground='#7f8c8d')
        style.configure('Success.TLabel', foreground='#27ae60', font=('맑은 고딕', 10, 'bold'))
        style.configure('Error.TLabel', foreground='#e74c3c', font=('맑은 고딕', 10))
        style.configure('Warning.TLabel', foreground='#f39c12', font=('맑은 고딕', 10))
        
        # 버튼 스타일
        style.configure('Primary.TButton', 
                       font=('맑은 고딕', 10, 'bold'),
                       foreground='white')
        style.map('Primary.TButton',
                  background=[('active', '#3498db'), ('pressed', '#2980b9'), ('!active', '#3498db')])
        
        style.configure('Success.TButton', 
                       font=('맑은 고딕', 10, 'bold'),
                       foreground='white')
        style.map('Success.TButton',
                  background=[('active', '#27ae60'), ('pressed', '#229954'), ('!active', '#2ecc71')])
        
        style.configure('Secondary.TButton', 
                       font=('맑은 고딕', 9))
        
        # 프레임 스타일
        style.configure('Card.TLabelframe', relief='solid', borderwidth=1)
        style.configure('Card.TLabelframe.Label', font=('맑은 고딕', 10, 'bold'), foreground='#2c3e50')
        
    def setup_ui(self):
        """UI 구성 요소 설정"""
        self.root = tk.Tk()
        self.root.title("HEIC 이미지 변환기 v1.0")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # 아이콘 설정 시도
        try:
            # Windows에서 기본 아이콘 사용
            if platform.system() == 'Windows':
                self.root.iconbitmap(default='')
        except:
            pass
        
        # 메인 스타일
        self.root.configure(bg='#ecf0f1')
        
        self.create_widgets()
        self.create_layout()
        
    def create_widgets(self):
        """UI 위젯들 생성"""
        # 메인 프레임
        self.main_frame = ttk.Frame(self.root, padding="15")
        
        # 제목 프레임
        self.title_frame = ttk.Frame(self.main_frame)
        self.title_label = ttk.Label(
            self.title_frame, 
            text="🔄 HEIC 이미지 변환기", 
            style='Title.TLabel'
        )
        self.version_label = ttk.Label(
            self.title_frame,
            text="v1.0 - 고성능 배치 변환",
            style='Info.TLabel'
        )
        
        # 상단 컨트롤 프레임
        self.control_frame = ttk.Frame(self.main_frame)
        
        # 파일 선택 섹션
        self.file_section = ttk.LabelFrame(
            self.control_frame, 
            text=" 📁 파일 선택 ", 
            style='Card.TLabelframe',
            padding="15"
        )
        
        self.select_button = ttk.Button(
            self.file_section,
            text="📂 HEIC 파일 폴더 선택",
            command=self.select_directory,
            style='Primary.TButton',
            width=25
        )
        
        self.directory_frame = ttk.Frame(self.file_section)
        ttk.Label(self.directory_frame, text="선택된 폴더:", style='Header.TLabel').pack(anchor='w')
        self.directory_label = ttk.Label(
            self.directory_frame,
            text="아직 선택되지 않음",
            style='Info.TLabel',
            wraplength=350
        )
        
        # 설정 섹션
        self.settings_section = ttk.LabelFrame(
            self.control_frame, 
            text=" ⚙️ 변환 설정 ", 
            style='Card.TLabelframe',
            padding="15"
        )
        
        # 출력 형식
        self.format_frame = ttk.Frame(self.settings_section)
        ttk.Label(self.format_frame, text="출력 형식:", style='Header.TLabel').pack(anchor='w')
        self.format_combo = ttk.Combobox(
            self.format_frame,
            values=list(self.SUPPORTED_FORMATS.keys()),
            state='readonly',
            width=12,
            font=('맑은 고딕', 10)
        )
        self.format_combo.set("JPEG")
        
        # 품질 설정
        self.quality_frame = ttk.Frame(self.settings_section)
        ttk.Label(self.quality_frame, text="품질 설정:", style='Header.TLabel').pack(anchor='w')
        
        self.quality_control_frame = ttk.Frame(self.quality_frame)
        self.quality_var = tk.IntVar(value=95)
        self.quality_scale = ttk.Scale(
            self.quality_control_frame,
            from_=50,
            to=100,
            variable=self.quality_var,
            orient='horizontal',
            length=150
        )
        self.quality_label = ttk.Label(
            self.quality_control_frame, 
            text="95%", 
            style='Info.TLabel',
            width=5
        )
        
        # 품질 라벨 업데이트 함수
        def update_quality_label(*args):
            self.quality_label.config(text=f"{self.quality_var.get()}%")
        
        self.quality_var.trace('w', update_quality_label)
        
        # 메인 컨텐츠 프레임 (3열 레이아웃)
        self.content_frame = ttk.Frame(self.main_frame)
        
        # 왼쪽: 파일 목록
        self.file_list_section = ttk.LabelFrame(
            self.content_frame, 
            text=" 📋 HEIC 파일 목록 ", 
            style='Card.TLabelframe',
            padding="10"
        )
        
        self.file_list_frame = ttk.Frame(self.file_list_section)
        self.file_listbox = tk.Listbox(
            self.file_list_frame,
            selectmode=tk.SINGLE,
            font=('맑은 고딕', 9),
            height=15,
            activestyle='dotbox',
            selectbackground='#3498db'
        )
        
        self.file_scrollbar = ttk.Scrollbar(
            self.file_list_frame,
            orient='vertical',
            command=self.file_listbox.yview
        )
        self.file_listbox.config(yscrollcommand=self.file_scrollbar.set)
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        self.file_info_frame = ttk.Frame(self.file_list_section)
        self.file_count_label = ttk.Label(
            self.file_info_frame,
            text="파일 개수: 0",
            style='Info.TLabel'
        )
        self.file_size_label = ttk.Label(
            self.file_info_frame,
            text="총 용량: 0 MB",
            style='Info.TLabel'
        )
        
        # 가운데: 미리보기
        self.preview_section = ttk.LabelFrame(
            self.content_frame, 
            text=" 🖼️ 이미지 미리보기 ", 
            style='Card.TLabelframe',
            padding="10"
        )
        
        self.canvas = tk.Canvas(
            self.preview_section,
            width=400,
            height=300,
            bg='#ffffff',
            relief='solid',
            borderwidth=1,
            highlightthickness=0
        )
        
        # 오른쪽: 이미지 정보
        self.info_section = ttk.LabelFrame(
            self.content_frame, 
            text=" 📊 이미지 정보 ", 
            style='Card.TLabelframe',
            padding="10"
        )
        
        self.info_frame = ttk.Frame(self.info_section)
        self.exif_text = tk.Text(
            self.info_frame,
            height=18,
            width=35,
            wrap=tk.WORD,
            font=('맑은 고딕', 9),
            state='disabled',
            relief='solid',
            borderwidth=1,
            bg='#ffffff'
        )
        
        self.info_scrollbar = ttk.Scrollbar(
            self.info_frame,
            orient='vertical',
            command=self.exif_text.yview
        )
        self.exif_text.config(yscrollcommand=self.info_scrollbar.set)
        
        # 하단: 변환 섹션
        self.convert_section = ttk.LabelFrame(
            self.main_frame, 
            text=" 🚀 변환 실행 ", 
            style='Card.TLabelframe',
            padding="15"
        )
        
        # 진행률 표시
        self.progress_frame = ttk.Frame(self.convert_section)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=500,
            style='TProgressbar'
        )
        
        self.progress_label = ttk.Label(
            self.progress_frame,
            text="변환 대기 중...",
            style='Info.TLabel'
        )
        
        # 버튼 프레임
        self.button_frame = ttk.Frame(self.convert_section)
        
        self.convert_button = ttk.Button(
            self.button_frame,
            text="🔄 변환 시작",
            command=self.start_conversion,
            style='Success.TButton',
            width=15
        )
        
        self.open_folder_button = ttk.Button(
            self.button_frame,
            text="📁 결과 폴더 열기",
            command=self.open_output_folder,
            style='Secondary.TButton',
            width=15,
            state='disabled'
        )
        
        self.reset_button = ttk.Button(
            self.button_frame,
            text="🔄 초기화",
            command=self.reset_all,
            style='Secondary.TButton',
            width=12
        )
        
        # 상태 표시
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_label = ttk.Label(
            self.status_frame,
            text="📍 프로그램이 준비되었습니다. HEIC 파일이 있는 폴더를 선택해주세요.",
            style='Info.TLabel'
        )
        
    def create_layout(self):
        """개선된 레이아웃 구성"""
        self.main_frame.pack(fill='both', expand=True)
        
        # 제목 영역
        self.title_frame.pack(fill='x', pady=(0, 20))
        self.title_label.pack()
        self.version_label.pack(pady=(5, 0))
        
        # 상단 컨트롤 영역 (2열)
        self.control_frame.pack(fill='x', pady=(0, 15))
        
        # 파일 선택 섹션 (왼쪽)
        self.file_section.pack(side='left', fill='both', expand=True, padx=(0, 10))
        self.select_button.pack(pady=(0, 15))
        self.directory_frame.pack(fill='x')
        self.directory_label.pack(anchor='w')
        
        # 설정 섹션 (오른쪽)
        self.settings_section.pack(side='right', fill='y')
        
        # 출력 형식
        self.format_frame.pack(fill='x', pady=(0, 15))
        self.format_combo.pack(anchor='w', pady=(5, 0))
        
        # 품질 설정
        self.quality_frame.pack(fill='x')
        self.quality_control_frame.pack(anchor='w', pady=(5, 0))
        self.quality_scale.pack(side='left')
        self.quality_label.pack(side='left', padx=(10, 0))
        
        # 메인 컨텐츠 영역 (3열, 고정 크기 지정)
        self.content_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # 파일 목록 (왼쪽, 300px 고정)
        self.file_list_section.pack(side='left', fill='y', padx=(0, 10))
        self.file_list_section.configure(width=300)
        self.file_list_section.pack_propagate(False)  # 크기 고정
        
        self.file_list_frame.pack(fill='both', expand=True)
        self.file_listbox.pack(side='left', fill='both', expand=True)
        self.file_scrollbar.pack(side='right', fill='y')
        
        self.file_info_frame.pack(fill='x', pady=(10, 0))
        self.file_count_label.pack(anchor='w')
        self.file_size_label.pack(anchor='w')
        
        # 미리보기 (가운데, 확장 가능)
        self.preview_section.pack(side='left', fill='both', expand=True, padx=(0, 10))
        self.canvas.pack(expand=True, fill='both')
        
        # 이미지 정보 (오른쪽, 350px 고정)
        self.info_section.pack(side='right', fill='y')
        self.info_section.configure(width=350)
        self.info_section.pack_propagate(False)  # 크기 고정
        
        self.info_frame.pack(fill='both', expand=True)
        self.exif_text.pack(side='left', fill='both', expand=True)
        self.info_scrollbar.pack(side='right', fill='y')
        
        # 변환 섹션 (하단)
        self.convert_section.pack(fill='x', pady=(0, 15))
        
        # 진행률
        self.progress_frame.pack(fill='x', pady=(0, 15))
        self.progress_bar.pack(fill='x')
        self.progress_label.pack(pady=(10, 0))
        
        # 버튼들
        self.button_frame.pack()
        self.convert_button.pack(side='left', padx=(0, 10))
        self.open_folder_button.pack(side='left', padx=(0, 10))
        self.reset_button.pack(side='left')
        
        # 상태 표시
        self.status_frame.pack(fill='x')
        self.status_label.pack()
        
    def select_directory(self):
        """디렉토리 선택 및 HEIC 파일 스캔"""
        directory = filedialog.askdirectory(title="HEIC 파일이 있는 폴더를 선택하세요")
        
        if directory:
            self.source_directory = Path(directory)
            self.directory_label.config(text=str(self.source_directory))
            self.scan_heic_files()
            self.update_status("✅ 폴더 선택 완료", "success")
        
    def scan_heic_files(self):
        """HEIC 파일 스캔"""
        if not self.source_directory:
            return
            
        try:
            self.heic_files.clear()
            self.file_listbox.delete(0, tk.END)
            
            total_size = 0
            # HEIC 파일 찾기
            for file_path in self.source_directory.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in self.HEIC_EXTENSIONS:
                    self.heic_files.append(file_path.name)
                    self.file_listbox.insert(tk.END, file_path.name)
                    total_size += file_path.stat().st_size
            
            # 파일 정보 업데이트
            count = len(self.heic_files)
            size_mb = total_size / (1024 * 1024)
            
            self.file_count_label.config(text=f"파일 개수: {count:,}개")
            self.file_size_label.config(text=f"총 용량: {size_mb:.1f} MB")
            
            if count == 0:
                self.update_status("⚠️ HEIC 파일을 찾을 수 없습니다", "warning")
                self.clear_preview_and_info()
            else:
                self.update_status(f"📋 {count:,}개의 HEIC 파일을 발견했습니다 ({size_mb:.1f} MB)", "success")
                
        except Exception as e:
            logger.error(f"파일 스캔 중 오류: {e}")
            self.update_status("❌ 파일 스캔 중 오류가 발생했습니다", "error")
            
    def on_file_select(self, event):
        """파일 선택 시 미리보기 및 EXIF 정보 표시"""
        selection = self.file_listbox.curselection()
        if not selection:
            return
            
        try:
            selected_file = self.heic_files[selection[0]]
            file_path = self.source_directory / selected_file
            
            # 이미지 미리보기 로드
            self.load_preview(file_path)
            
            # EXIF 정보 표시
            self.display_exif_info(file_path)
            
            self.update_status(f"🖼️ {selected_file} 미리보기를 표시했습니다", "info")
            
        except Exception as e:
            logger.error(f"파일 선택 처리 중 오류: {e}")
            self.update_status("❌ 파일 정보 로드 중 오류가 발생했습니다", "error")
            
    def load_preview(self, file_path: Path):
        """이미지 미리보기 로드"""
        try:
            with Image.open(file_path) as image:
                # 캔버스 크기 가져오기
                self.canvas.update_idletasks()
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                
                if canvas_width <= 1 or canvas_height <= 1:
                    canvas_width, canvas_height = 400, 300
                
                # 이미지 비율 유지하면서 리사이즈
                img_ratio = image.width / image.height
                canvas_ratio = canvas_width / canvas_height
                
                margin = 20
                if img_ratio > canvas_ratio:
                    # 이미지가 더 넓음
                    new_width = canvas_width - margin
                    new_height = int(new_width / img_ratio)
                else:
                    # 이미지가 더 높음
                    new_height = canvas_height - margin
                    new_width = int(new_height * img_ratio)
                
                resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(resized_image)
                
                # 캔버스 초기화 및 이미지 표시
                self.canvas.delete("all")
                self.canvas.create_image(
                    canvas_width // 2,
                    canvas_height // 2,
                    image=photo,
                    anchor='center'
                )
                
                # 이미지 정보 표시
                info_text = f"{image.width} × {image.height} px"
                self.canvas.create_text(
                    10, canvas_height - 20,
                    text=info_text,
                    anchor='sw',
                    fill='#7f8c8d',
                    font=('맑은 고딕', 9)
                )
                
                # 이미지 참조 유지
                self.canvas.image = photo
                
        except Exception as e:
            logger.error(f"이미지 미리보기 로드 오류: {e}")
            self.canvas.delete("all")
            self.canvas.create_text(
                200, 150,
                text="❌ 미리보기를 불러올 수 없습니다",
                fill="#e74c3c",
                font=('맑은 고딕', 12),
                anchor='center'
            )
            
    def display_exif_info(self, file_path: Path):
        """EXIF 정보 표시"""
        try:
            with Image.open(file_path) as image:
                exif_data = image.getexif()
                file_stat = file_path.stat()
                
                # 기본 파일 정보
                info_lines = []
                info_lines.append("📁 파일 정보")
                info_lines.append("─" * 30)
                info_lines.append(f"파일명: {file_path.name}")
                info_lines.append(f"크기: {image.width:,} × {image.height:,} px")
                info_lines.append(f"모드: {image.mode}")
                info_lines.append(f"용량: {file_stat.st_size / (1024*1024):.2f} MB")
                info_lines.append("")
                
                # EXIF 정보
                if exif_data:
                    info_lines.append("📷 촬영 정보")
                    info_lines.append("─" * 30)
                    
                    # 주요 EXIF 태그들
                    exif_tags = {
                        271: ("제조사", "🏢"),
                        272: ("카메라 모델", "📸"),
                        306: ("촬영 일시", "📅"),
                        315: ("소프트웨어", "💻"),
                        33434: ("노출 시간", "⏱️"),
                        33437: ("F-Stop", "🔍"),
                        34855: ("ISO", "🌟"),
                        36867: ("원본 촬영 일시", "📅"),
                        36868: ("디지털화 일시", "💾"),
                        40961: ("색공간", "🎨"),
                        40962: ("가로 해상도", "📐"),
                        40963: ("세로 해상도", "📐")
                    }
                    
                    for tag_id, (tag_name, emoji) in exif_tags.items():
                        if tag_id in exif_data:
                            value = exif_data[tag_id]
                            if isinstance(value, tuple) and len(value) == 2:
                                if tag_id == 33434:  # 노출 시간
                                    value = f"1/{int(value[1]/value[0])}" if value[0] != 0 else "N/A"
                                elif tag_id == 33437:  # F-Stop
                                    value = f"f/{value[0]/value[1]:.1f}" if value[1] != 0 else "N/A"
                                else:
                                    value = f"{value[0]}/{value[1]}"
                            elif tag_id == 34855:  # ISO
                                value = f"ISO {value}"
                            
                            info_lines.append(f"{emoji} {tag_name}: {value}")
                    
                    # GPS 정보 확인
                    gps_info = image.getexif().get_ifd(0x8825)
                    if gps_info:
                        info_lines.append("")
                        info_lines.append("🌍 위치 정보")
                        info_lines.append("─" * 30)
                        info_lines.append("📍 GPS 데이터 있음")
                else:
                    info_lines.append("📷 촬영 정보")
                    info_lines.append("─" * 30)
                    info_lines.append("EXIF 정보가 없습니다.")
                
                # 텍스트 위젯에 정보 표시
                self.exif_text.config(state='normal')
                self.exif_text.delete(1.0, tk.END)
                self.exif_text.insert(1.0, '\n'.join(info_lines))
                self.exif_text.config(state='disabled')
                
        except Exception as e:
            logger.error(f"EXIF 정보 표시 오류: {e}")
            self.exif_text.config(state='normal')
            self.exif_text.delete(1.0, tk.END)
            self.exif_text.insert(1.0, "❌ 이미지 정보를 불러올 수 없습니다.")
            self.exif_text.config(state='disabled')
            
    def clear_preview_and_info(self):
        """미리보기와 정보 초기화"""
        self.canvas.delete("all")
        self.canvas.create_text(
            200, 150,
            text="📁 파일을 선택하면 미리보기가 표시됩니다",
            fill="#95a5a6",
            font=('맑은 고딕', 12),
            anchor='center'
        )
        
        self.exif_text.config(state='normal')
        self.exif_text.delete(1.0, tk.END)
        self.exif_text.insert(1.0, "🖼️ 이미지를 선택하면\n정보가 표시됩니다.")
        self.exif_text.config(state='disabled')
            
    def convert_single_file(self, file_name: str, output_format: ImageFormat, quality: int) -> bool:
        """단일 파일 변환"""
        try:
            input_path = self.source_directory / file_name
            
            # 출력 디렉토리 생성
            output_dir = self.source_directory / output_format.extension
            output_dir.mkdir(exist_ok=True)
            self.output_directory = output_dir
            
            # 출력 파일명 생성
            output_filename = f"{input_path.stem}.{output_format.extension}"
            output_path = output_dir / output_filename
            
            # 이미지 변환
            with Image.open(input_path) as image:
                # 원본 메타데이터 보존
                exif_data = image.getexif()
                icc_profile = image.info.get("icc_profile")
                
                # 변환 옵션 설정
                save_kwargs = {
                    'format': output_format.pil_format,
                    'exif': exif_data if exif_data else None,
                    'icc_profile': icc_profile
                }
                
                # JPEG의 경우 품질 설정
                if output_format.pil_format == 'JPEG':
                    save_kwargs['quality'] = quality
                    save_kwargs['optimize'] = True
                
                # PNG의 경우 최적화 설정
                elif output_format.pil_format == 'PNG':
                    save_kwargs['optimize'] = True
                    
                # WEBP의 경우 품질 설정
                elif output_format.pil_format == 'WEBP':
                    save_kwargs['quality'] = quality
                    save_kwargs['method'] = 6  # 최고 압축률
                
                # 파일 저장
                image.save(output_path, **save_kwargs)
                
            return True
            
        except Exception as e:
            logger.error(f"파일 변환 오류 ({file_name}): {e}")
            return False
            
    def start_conversion(self):
        """변환 프로세스 시작"""
        if not self.validate_conversion():
            return
            
        # 버튼 상태 변경
        self.convert_button.config(state='disabled', text="🔄 변환 중...")
        self.open_folder_button.config(state='disabled')
        
        # 별도 스레드에서 변환 실행
        thread = threading.Thread(target=self.run_conversion)
        thread.daemon = True
        thread.start()
        
    def validate_conversion(self) -> bool:
        """변환 전 유효성 검사"""
        if not self.source_directory:
            messagebox.showwarning("경고", "먼저 HEIC 파일이 있는 폴더를 선택해주세요.")
            return False
            
        if not self.heic_files:
            messagebox.showwarning("경고", "변환할 HEIC 파일이 없습니다.")
            return False
            
        return True
        
    def run_conversion(self):
        """변환 실행 (별도 스레드)"""
        try:
            output_format = self.SUPPORTED_FORMATS[self.format_combo.get()]
            quality = self.quality_var.get()
            total_files = len(self.heic_files)
            
            # 진행률 초기화
            self.progress_var.set(0)
            self.update_progress_label("🚀 변환을 시작합니다...")
            
            successful_conversions = 0
            failed_conversions = 0
            
            # 동시 처리를 위한 ThreadPoolExecutor 사용
            max_workers = min(4, os.cpu_count() or 1)  # 최대 4개 스레드 사용
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # 모든 변환 작업 제출
                future_to_file = {
                    executor.submit(self.convert_single_file, file_name, output_format, quality): file_name
                    for file_name in self.heic_files
                }
                
                # 완료된 작업들 처리
                for future in concurrent.futures.as_completed(future_to_file):
                    file_name = future_to_file[future]
                    
                    try:
                        success = future.result()
                        if success:
                            successful_conversions += 1
                        else:
                            failed_conversions += 1
                    except Exception as e:
                        logger.error(f"변환 작업 오류 ({file_name}): {e}")
                        failed_conversions += 1
                    
                    # 진행률 업데이트
                    completed = successful_conversions + failed_conversions
                    progress = (completed / total_files) * 100
                    
                    self.root.after(0, lambda p=progress: self.progress_var.set(p))
                    self.root.after(0, lambda c=completed, t=total_files, name=file_name: 
                                  self.update_progress_label(f"⚡ 변환 중... ({c}/{t}) - {name}"))
            
            # 변환 완료 처리
            self.root.after(0, self.conversion_completed, successful_conversions, failed_conversions)
            
        except Exception as e:
            logger.error(f"변환 프로세스 오류: {e}")
            self.root.after(0, lambda: self.conversion_error(str(e)))
            
    def conversion_completed(self, successful: int, failed: int):
        """변환 완료 처리"""
        self.convert_button.config(state='normal', text="🔄 변환 시작")
        self.open_folder_button.config(state='normal')
        self.progress_var.set(100)
        
        if failed == 0:
            message = f"🎉 모든 파일이 성공적으로 변환되었습니다!\n\n✅ 성공: {successful:,}개 파일\n📁 저장 위치: {self.output_directory}"
            self.update_status("✅ 모든 파일 변환 완료!", "success")
            self.update_progress_label("🎉 변환 완료!")
            
            # 성공 메시지와 함께 폴더 열기 옵션 제공
            result = messagebox.askquestion(
                "변환 완료", 
                f"{message}\n\n📂 결과 폴더를 바로 열어보시겠습니까?",
                icon='question'
            )
            if result == 'yes':
                self.open_output_folder()
        else:
            message = f"⚠️ 변환이 완료되었습니다 (일부 오류 발생)\n\n✅ 성공: {successful:,}개\n❌ 실패: {failed:,}개\n📁 저장 위치: {self.output_directory}"
            self.update_status(f"⚠️ 변환 완료 (실패: {failed:,}개)", "warning")
            self.update_progress_label(f"⚠️ 변환 완료 (실패: {failed:,}개)")
            messagebox.showwarning("변환 완료", message)
            
    def conversion_error(self, error_message: str):
        """변환 오류 처리"""
        self.convert_button.config(state='normal', text="🔄 변환 시작")
        self.progress_var.set(0)
        self.update_status("❌ 변환 중 오류 발생", "error")
        self.update_progress_label("❌ 변환 실패")
        messagebox.showerror("오류", f"변환 중 심각한 오류가 발생했습니다:\n\n{error_message}")
        
    def open_output_folder(self):
        """변환된 파일이 있는 폴더 열기"""
        if not self.output_directory or not self.output_directory.exists():
            messagebox.showwarning("경고", "아직 변환된 파일이 없습니다.")
            return
            
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(self.output_directory)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", str(self.output_directory)])
            else:  # Linux
                subprocess.run(["xdg-open", str(self.output_directory)])
                
            self.update_status(f"📂 결과 폴더를 열었습니다: {self.output_directory}", "info")
            
        except Exception as e:
            logger.error(f"폴더 열기 오류: {e}")
            messagebox.showerror("오류", f"폴더를 열 수 없습니다:\n{e}")
            
    def reset_all(self):
        """모든 설정 초기화"""
        result = messagebox.askquestion(
            "초기화", 
            "모든 설정을 초기화하시겠습니까?\n\n• 선택된 폴더 정보\n• 파일 목록\n• 미리보기\n• 진행률",
            icon='question'
        )
        
        if result == 'yes':
            self.source_directory = None
            self.output_directory = None
            self.heic_files.clear()
            
            # UI 초기화
            self.directory_label.config(text="아직 선택되지 않음")
            self.file_listbox.delete(0, tk.END)
            self.file_count_label.config(text="파일 개수: 0")
            self.file_size_label.config(text="총 용량: 0 MB")
            
            self.clear_preview_and_info()
            
            self.progress_var.set(0)
            self.update_progress_label("변환 대기 중...")
            self.open_folder_button.config(state='disabled')
            
            self.format_combo.set("JPEG")
            self.quality_var.set(95)
            
            self.update_status("🔄 모든 설정이 초기화되었습니다", "info")
        
    def update_progress_label(self, text: str):
        """진행률 라벨 업데이트"""
        self.progress_label.config(text=text)
        
    def update_status(self, message: str, status_type: str = "info"):
        """상태 표시 업데이트"""
        if status_type == "success":
            self.status_label.config(text=message, style='Success.TLabel')
        elif status_type == "error":
            self.status_label.config(text=message, style='Error.TLabel')
        elif status_type == "warning":
            self.status_label.config(text=message, style='Warning.TLabel')
        else:
            self.status_label.config(text=message, style='Info.TLabel')
            
    def run(self):
        """애플리케이션 실행"""
        try:
            # 초기 캔버스 텍스트
            self.clear_preview_and_info()
            
            # 창 최소화/최대화 이벤트 바인딩
            self.root.bind('<Configure>', self.on_window_configure)
            
            self.root.mainloop()
            
        except Exception as e:
            logger.error(f"애플리케이션 실행 오류: {e}")
            messagebox.showerror("오류", f"애플리케이션 실행 중 오류가 발생했습니다:\n{e}")
            
    def on_window_configure(self, event):
        """창 크기 변경 시 캔버스 업데이트"""
        if event.widget == self.root:
            # 현재 선택된 파일이 있으면 미리보기 다시 로드
            selection = self.file_listbox.curselection()
            if selection and self.heic_files:
                try:
                    selected_file = self.heic_files[selection[0]]
                    file_path = self.source_directory / selected_file
                    # 짧은 지연 후 미리보기 업데이트 (레이아웃 안정화 대기)
                    self.root.after(100, lambda: self.load_preview(file_path))
                except:
                    pass

def main():
    """메인 함수"""
    try:
        app = HEICConverter()
        app.run()
    except Exception as e:
        logger.error(f"애플리케이션 초기화 오류: {e}")
        messagebox.showerror("오류", f"애플리케이션을 시작할 수 없습니다:\n{e}")

if __name__ == "__main__":
    main()