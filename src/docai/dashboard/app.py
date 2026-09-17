"""
Khung ứng dụng Dashboard trực quan hoá dựa trên Plotly Dash.

Stack công nghệ chính thức:
Python -> pandas -> Plotly -> Dash

Mục đích kiến trúc:
Cung cấp giao diện trực quan tương tác phục vụ:
1. Hiển thị kết quả trích xuất tài liệu và độ tin cậy (confidence) của từng trường.
2. So sánh đối đầu song song giữa Track A (Classic) và Track B (VLM-native).
3. Hiển thị cờ cảnh báo gian lận số liệu và rủi ro điều khoản (fraud/risk flags).
4. Minh hoạ bản đồ nhiệt giải thích (Explainability Heatmap Overlay).
5. Theo dõi các chỉ số benchmark thực nghiệm (F1 field-level, độ trễ, chi phí GPU).

Cam kết kiến trúc:
Không sử dụng Power BI, không phụ thuộc file .pbix hay công cụ BI độc quyền bên ngoài.
"""

from typing import Any, Dict, Optional


def create_dashboard_app():
    """
    Khởi tạo và cấu hình ứng dụng Plotly Dash.
    Hàm này chuẩn bị khung layout và callbacks kết nối với pipeline DocAI.
    """
    try:
        import dash
        from dash import html, dcc
    except ImportError:
        # Nếu Dash chưa được cài đặt trong môi trường hiện tại
        return None

    app = dash.Dash(
        __name__,
        title="DocAI Dual-Pipeline Benchmark Dashboard",
        suppress_callback_exceptions=True
    )

    app.layout = html.Div(
        children=[
            html.H1("DocAI Dual-Pipeline Benchmark Dashboard", style={"textAlign": "center"}),
            html.P(
                "Khung trực quan hoá so sánh pipeline Document AI cổ điển và VLM-native "
                "(Stack: Python -> pandas -> Plotly -> Dash).",
                style={"textAlign": "center"}
            ),
            dcc.Tabs(
                id="dashboard-tabs",
                value="tab-extraction",
                children=[
                    dcc.Tab(label="Kết quả trích xuất & Confidence", value="tab-extraction"),
                    dcc.Tab(label="So sánh Track A vs Track B", value="tab-comparison"),
                    dcc.Tab(label="Cảnh báo Gian lận & Rủi ro", value="tab-fraud"),
                    dcc.Tab(label="Bản đồ nhiệt Giải thích (Explainability)", value="tab-explain"),
                    dcc.Tab(label="Chỉ số Benchmark & Chi phí GPU", value="tab-benchmark"),
                ]
            ),
            html.Div(id="tab-content", style={"padding": "20px"}),
        ],
        style={"fontFamily": "sans-serif", "margin": "20px"}
    )

    return app


if __name__ == "__main__":
    dash_app = create_dashboard_app()
    if dash_app is not None:
        dash_app.run(debug=True, port=8050)
    else:
        print("Vui lòng cài đặt dash và plotly để chạy dashboard: pip install dash plotly")
