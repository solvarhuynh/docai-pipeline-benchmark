"""
Module Dashboard trực quan hoá dựa trên Plotly Dash cho DocAI Benchmark.

Khẳng định kiến trúc: Sử dụng Plotly Dash (Python -> pandas -> Plotly -> Dash),
tuyệt đối không sử dụng Power BI hoặc các định dạng đóng .pbix.
"""

def create_dashboard_app(*args, **kwargs):
    """
    Lazy re-export để `python -m docai.dashboard.app` không nạp module hai lần.
    """
    from docai.dashboard.app import create_dashboard_app as _create_dashboard_app

    return _create_dashboard_app(*args, **kwargs)

__all__ = [
    "create_dashboard_app",
]
