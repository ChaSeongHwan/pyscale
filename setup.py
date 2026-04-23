"""PyScale 패키지 설치 스크립트"""

from setuptools import setup, find_packages
from pathlib import Path

readme = Path("README.md").read_text(encoding="utf-8")

setup(
    name="pyscale",
    version="1.0.0",
    author="PyScale Contributors",
    description="AI Image Upscaler with Advanced Resource Management",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/pyscale",
    
    packages=find_packages(),
    python_requires=">=3.9",
    
    install_requires=[
        "numpy>=1.24.0",
        "opencv-python>=4.8.0",
        "Pillow>=10.0.0",
        "psutil>=5.9.0",
    ],
    
    extras_require={
        "dev": ["pytest>=7.0", "black>=23.0"],
        "gpu": ["torch>=2.0.0", "realesrgan>=0.3.0"],
    },
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
