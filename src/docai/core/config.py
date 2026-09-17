"""
Cấu hình tập trung cho toàn bộ hệ thống DocAI Benchmark.

Cung cấp đường dẫn tuyệt đối an toàn tới các thư mục dữ liệu, mô hình và các tham số
môi trường mà không cần dùng các thủ thuật can thiệp sys.path.
"""

import os
from pathlib import Path
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """
    Cấu hình hệ thống DocAI Benchmark.
    """

    # Thư mục gốc của repository: src/docai/core/config.py -> 4 cấp parent là repo root
    repo_root: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parent.parent.parent.parent
    )

    # Cấu hình đường dẫn dữ liệu
    @property
    def data_dir(self) -> Path:
        return self.repo_root / "data"

    @property
    def raw_data_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def interim_data_dir(self) -> Path:
        return self.data_dir / "interim"

    @property
    def processed_data_dir(self) -> Path:
        return self.data_dir / "processed"

    @property
    def reports_dir(self) -> Path:
        return self.repo_root / "docs" / "reports"

    # Danh sách 4 bộ dữ liệu mục tiêu
    supported_datasets: list[str] = Field(
        default_factory=lambda: ["mcocr2021", "cord", "sroie", "cuad"]
    )

    # Cấu hình API Server
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)
    api_title: str = Field(default="DocAI Dual-Pipeline Benchmark API")
    api_version: str = Field(default="1.0.0")
    debug: bool = Field(default_factory=lambda: os.getenv("DOCAI_DEBUG", "0") == "1")

    def ensure_directories(self) -> None:
        """
        Đảm bảo các thư mục dữ liệu cần thiết tồn tại trên ổ đĩa.
        """
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.interim_data_dir.mkdir(parents=True, exist_ok=True)
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)


# Instance cấu hình mặc định dùng chung
settings = Settings()
