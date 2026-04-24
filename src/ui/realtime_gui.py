"""
src/ui/realtime_gui.py - 실시간 GUI

tkinter 기반, 실시간 화면 표시
"""

import tkinter as tk
from tkinter import ttk
import threading
import cv2
import numpy as np
from PIL import Image, ImageTk
import logging

from ..config.settings import AppConfig, ResourceProfile, SystemInfo
from ..capture.realtime import RealtimeCapture, CaptureRegion
from ..algorithms.hybrid import SmartHybrid
from ..core.realtime_processor import RealtimeProcessor

logger = logging.getLogger(__name__)

THEME = {
    "bg": "#0a0e27",
    "panel": "#1a1f3a",
    "accent": "#7c3aed",
    "text": "#e0e7ff",
    "muted": "#6b7280",
}


class RealtimeGUI(tk.Tk):
    """실시간 업스케일 GUI"""
    
    def __init__(self):
        super().__init__()
        self.title("🎮 PyScale Realtime")
        self.geometry("1200x800")
        self.configure(bg=THEME["bg"])
        
        self.config = AppConfig()
        self.config.print_config()
        
        self.running = False
        self.processor = None
        
        self._build_ui()
    
    def _build_ui(self):
        """UI 구축"""
        # 상단: 타이틀
        title = tk.Label(
            self, text="🎮 PyScale Realtime",
            bg=THEME["bg"], fg=THEME["accent"],
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)
        
        # 메인 프레임
        main = tk.Frame(self, bg=THEME["bg"])
        main.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 왼쪽: 설정
        left = tk.Frame(main, bg=THEME["panel"], width=280)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)
        
        # 프로필 선택
        tk.Label(left, text="리소스 프로필", bg=THEME["panel"],
                fg=THEME["text"], font=("Arial", 10, "bold")).pack(pady=10)
        
        self.profile_var = tk.StringVar(value=self.config.profile.value)
        for profile in ResourceProfile:
            tk.Radiobutton(left, text=profile.value,
                          variable=self.profile_var,
                          value=profile.value,
                          bg=THEME["panel"], fg=THEME["text"],
                          selectcolor=THEME["accent"],
                          command=self._on_profile_change).pack(anchor="w", padx=20)
        
        # 배율
        tk.Label(left, text="배율", bg=THEME["panel"],
                fg=THEME["text"], font=("Arial", 10, "bold")).pack(pady=(20, 10))
        
        self.scale_var = tk.DoubleVar(value=self.config.get_default_scale())
        tk.Scale(left, from_=1.0, to=4.0, resolution=0.5,
                variable=self.scale_var, orient="horizontal",
                bg=THEME["panel"], fg=THEME["text"]).pack(fill="x", padx=10)
        
        # 알고리즘
        tk.Label(left, text="알고리즘", bg=THEME["panel"],
                fg=THEME["text"], font=("Arial", 10, "bold")).pack(pady=(20, 10))
        
        self.algo_var = tk.StringVar(value="smart")
        algos = ["smart", "bicubic", "lanczos", "fsr", "nis"]
        for algo in algos:
            tk.Radiobutton(left, text=algo,
                          variable=self.algo_var,
                          value=algo,
                          bg=THEME["panel"], fg=THEME["text"],
                          selectcolor=THEME["accent"]).pack(anchor="w", padx=20)
        
        # FPS
        tk.Label(left, text="FPS 제한", bg=THEME["panel"],
                fg=THEME["text"], font=("Arial", 10, "bold")).pack(pady=(20, 10))
        
        self.fps_var = tk.IntVar(value=self.config.get_target_fps())
        tk.Scale(left, from_=30, to=144, resolution=15,
                variable=self.fps_var, orient="horizontal",
                bg=THEME["panel"], fg=THEME["text"]).pack(fill="x", padx=10)
        
        # 버튼
        tk.Button(left, text="▶ 시작",
                 command=self._start,
                 bg=THEME["accent"], fg="white",
                 relief="flat", padx=10, pady=8,
                 font=("Arial", 11, "bold")).pack(fill="x", padx=10, pady=5)
        
        tk.Button(left, text="⏹ 중지",
                 command=self._stop,
                 bg="#ff4444", fg="white",
                 relief="flat", padx=10, pady=8,
                 font=("Arial", 11, "bold")).pack(fill="x", padx=10, pady=5)
        
        # 통계
        self.stats_label = tk.Label(left, text="",
                                   bg=THEME["panel"], fg=THEME["muted"],
                                   font=("Arial", 9), justify="left")
        self.stats_label.pack(fill="x", padx=10, pady=20)
        
        # 오른쪽: 미리보기
        right = tk.Frame(main, bg=THEME["bg"])
        right.pack(side="left", fill="both", expand=True)
        
        tk.Label(right, text="원본", bg=THEME["bg"],
                fg=THEME["muted"], font=("Arial", 9)).pack()
        
        self.canvas_input = tk.Canvas(right, bg="#000", height=300)
        self.canvas_input.pack(fill="both", expand=True, pady=5)
        
        tk.Label(right, text="업스케일됨", bg=THEME["bg"],
                fg=THEME["muted"], font=("Arial", 9)).pack()
        
        self.canvas_output = tk.Canvas(right, bg="#000", height=300)
        self.canvas_output.pack(fill="both", expand=True, pady=5)
        
        # 업데이트 루프
        self._update_stats()
    
    def _on_profile_change(self):
        """프로필 변경"""
        for profile in ResourceProfile:
            if profile.value == self.profile_var.get():
                self.config = AppConfig(profile)
                logger.info(f"Profile changed: {profile.value}")
                break
    
    def _display_frame(self, frame, canvas):
        """프레임 표시"""
        if frame is None:
            return
        
        cw = canvas.winfo_width()
        ch = canvas.winfo_height()
        if cw < 2 or ch < 2:
            return
        
        h, w = frame.shape[:2]
        ratio = min(cw / w, ch / h)
        nw, nh = int(w * ratio), int(h * ratio)
        
        resized = cv2.resize(frame, (nw, nh))
        img_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        photo = ImageTk.PhotoImage(pil_img)
        
        canvas.delete("all")
        canvas.create_image(cw//2, ch//2, image=photo)
        canvas.image = photo
    
    def _on_output_frame(self, frame):
        """출력 프레임 콜백"""
        self.after(0, lambda f=frame: self._display_frame(f, self.canvas_output))
    
    def _start(self):
        """시작"""
        if self.running:
            logger.warning("Already running")
            return
        
        self.running = True
        
        # 캡처 및 업스케일러 설정
        capture = RealtimeCapture(target_fps=self.fps_var.get())
        upscaler = SmartHybrid(scale=self.scale_var.get())
        
        # 프로세서 시작
        self.processor = RealtimeProcessor(
            capture, upscaler,
            output_callback=self._on_output_frame,
            target_fps=self.fps_var.get()
        )
        self.processor.start()
        
        # 캡처 시작
        def capture_loop():
            while self.running:
                frame = capture.get_latest_frame()
                if frame is not None:
                    self.after(0, lambda f=frame: self._display_frame(f, self.canvas_input))
                import time
                time.sleep(0.033)  # ~30fps
        
        t = threading.Thread(target=capture_loop, daemon=True)
        t.start()
        
        logger.info("Started")
    
    def _stop(self):
        """중지"""
        if not self.running:
            return
        
        self.running = False
        if self.processor:
            self.processor.stop()
        
        logger.info("Stopped")
    
    def _update_stats(self):
        """통계 업데이트"""
        if self.processor:
            stats = self.processor.get_stats()
            text = f"""FPS: {stats.total_fps:.1f}
처리: {stats.upscale_time_ms:.1f}ms
업스케일: {stats.upscale_fps:.1f}FPS"""
            self.stats_label.config(text=text)
        
        self.after(500, self._update_stats)


def main():
    """메인"""
    logging.basicConfig(level=logging.INFO)
    SystemInfo.print_info()
    app = RealtimeGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
