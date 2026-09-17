"""
Module Dashboard trực quan hoá dựa trên Plotly Dash cho DocAI Benchmark.

Khẳng định kiến trúc: Sử dụng Plotly Dash (Python -> pandas -> Plotly -> Dash),
tuyệt đối không sử dụng Power BI hoặc các định dạng đóng .pbix.
"""

from docai.dashboard.app import create_dashboard_app

__all__ = [
    "create_dashboard_app",
]
