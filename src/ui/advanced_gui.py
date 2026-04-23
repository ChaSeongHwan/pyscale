"""
src/ui/advanced_gui.py - 고급 GUI

tkinter 기반, 리소스 할당 기능 포함
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import cv2
import numpy as np
from PIL import Image, ImageTk
import logging

from ..config.config import AppConfig, ResourceProfile, SystemInfo
from ..algorithms.hybrid import IntelligentHybrid
from ..core.performance_monitor import PerformanceMonitor

logger = logging.getLogger(__name__)

THEME = {
    "bg": "#0a0e27",
    "panel": "#1a1f3a",
    "accent": "#7c3aed",
    "text": "#e0e7ff",
    "muted": "#6b7280",
}


class AdvancedGUI(tk.Tk):
    """고급 GUI"""
    
    def __init__(self):
        super().__init__()
        self.title("⬆ PyScale Pro")
        self.geometry("1000x700")
        self.configure(bg=THEME["bg"])
        
        self.config = AppConfig()
        self.monitor = PerformanceMonitor()
        self.upscaler = IntelligentHybrid(sharpness=0.3)
        
        self.current_image = None
        self.result_image = None
        
        self._build_ui()
    
    def _build_ui(self):
        """UI 빌드"""
        # 타이틀
        title = tk.Label(self, text="⬆ PyScale Pro",
                        bg=THEME["bg"], fg=THEME["accent"],
                        font=("Arial", 18, "bold"))
        title.pack(pady=10)
        
        # 메인 프레임
        main = tk.Frame(self, bg=THEME["bg"])
        main.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 왼쪽: 설정
        left = tk.Frame(main, bg=THEME["panel"], width=250)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)
        
        tk.Label(left, text="리소스 프로필", bg=THEME["panel"],
                fg=THEME["text"], font=("Arial", 10, "bold")).pack(pady=10)
        
        profiles = [p.value for p in ResourceProfile]
        self.profile_var = tk.StringVar(value=self.config.profile.value)
        for profile in profiles:
            tk.Radiobutton(left, text=profile,
                          variable=self.profile_var,
                          value=profile,
                          bg=THEME["panel"], fg=THEME["text"],
                          selectcolor=THEME["accent"]).pack(anchor="w", padx=20)
        
        # 배율
        tk.Label(left, text="배율", bg=THEME["panel"],
                fg=THEME["text"], font=("Arial", 10, "bold")).pack(pady=(20, 10))
        
        self.scale_var = tk.DoubleVar(value=2.0)
        tk.Scale(left, from_=1.0, to=8.0, resolution=0.5,
                variable=self.scale_var, orient="horizontal",
                bg=THEME["panel"], fg=THEME["text"]).pack(fill="x", padx=10)
        
        # 버튼
        tk.Button(left, text="📂 열기",
                 command=self._open_image,
                 bg=THEME["accent"], fg="white",
                 relief="flat", padx=10, pady=5).pack(fill="x", padx=10, pady=5)
        
        tk.Button(left, text="▶ 업스케일",
                 command=self._run_upscale,
                 bg=THEME["accent"], fg="white",
                 relief="flat", padx=10, pady=5).pack(fill="x", padx=10, pady=5)
        
        tk.Button(left, text="💾 저장",
                 command=self._save_image,
                 bg=THEME["accent"], fg="white",
                 relief="flat", padx=10, pady=5).pack(fill="x", padx=10, pady=5)
        
        # 진행 바
        self.progress = ttk.Progressbar(left, mode="indeterminate")
        self.progress.pack(fill="x", padx=10, pady=10)
        
        # 오른쪽: 미리보기
        right = tk.Frame(main, bg=THEME["bg"])
        right.pack(side="left", fill="both", expand=True)
        
        tk.Label(right, text="원본", bg=THEME["bg"],
                fg=THEME["muted"], font=("Arial", 9)).pack()
        
        self.canvas_before = tk.Canvas(right, bg="#000", height=250)
        self.canvas_before.pack(fill="both", expand=True, padx=(0, 5), pady=5)
        
        tk.Label(right, text="결과", bg=THEME["bg"],
                fg=THEME["muted"], font=("Arial", 9)).pack()
        
        self.canvas_after = tk.Canvas(right, bg="#000", height=250)
        self.canvas_after.pack(fill="both", expand=True, padx=(0, 5), pady=5)
    
    def _open_image(self):
        """이미지 열기"""
        path = filedialog.askopenfilename(
            filetypes=[("Image", "*.jpg *.png *.bmp")]
        )
        if not path:
            return
        
        self.current_image = cv2.imread(path)
        if self.current_image is None:
            messagebox.showerror("오류", "이미지 로드 실패")
            return
        
        self._display_image(self.current_image, self.canvas_before)
        logger.info(f"이미지 로드: {path}")
    
    def _display_image(self, img, canvas):
        """이미지 표시"""
        cw = canvas.winfo_width()
        ch = canvas.winfo_height()
        if cw < 2 or ch < 2:
            return
        
        h, w = img.shape[:2]
        ratio = min(cw / w, ch / h)
        nw, nh = int(w * ratio), int(h * ratio)
        
        resized = cv2.resize(img, (nw, nh))
        img_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        photo = ImageTk.PhotoImage(pil_img)
        
        canvas.delete("all")
        canvas.create_image(cw//2, ch//2, image=photo)
        canvas.image = photo
    
    def _run_upscale(self):
        """업스케일 실행"""
        if self.current_image is None:
            messagebox.showwarning("알림", "먼저 이미지를 로드하세요")
            return
        
        self.progress.start(10)
        t = threading.Thread(target=self._upscale_task, daemon=True)
        t.start()
    
    def _upscale_task(self):
        """업스케일 작업"""
        try:
            scale = self.scale_var.get()
            result, metrics = self.upscaler.upscale_safe(
                self.current_image, scale
            )
            self.result_image = result
            
            self.after(0, lambda: self._display_image(result, self.canvas_after))
            self.after(0, lambda: logger.info(
                f"완료: {metrics.output_size} ({metrics.processing_time_ms:.1f}ms)"
            ))
        
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("오류", str(e)))
        finally:
            self.after(0, self.progress.stop)
    
    def _save_image(self):
        """이미지 저장"""
        if self.result_image is None:
            messagebox.showwarning("알림", "먼저 업스케일을 실행하세요")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPG", "*.jpg")]
        )
        if not path:
            return
        
        cv2.imwrite(path, self.result_image)
        logger.info(f"저장: {path}")


def main():
    """메인 함수"""
    app = AdvancedGUI()
    app.mainloop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
