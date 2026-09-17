"""
Khung ứng dụng Dashboard trực quan hoá dựa trên Plotly Dash.

Stack công nghệ chính thức:
Python -> pandas -> Plotly -> Dash

Mục đích kiến trúc:
Cung cấp ba khu vực frontend tương tác: Invoice Workspace, Contract Workspace và Research Lab.
Product workspace hiển thị kết quả trích xuất, risk flags, evidence và JSON; Research Lab
hiển thị comparison/benchmark khi có kết quả thực nghiệm.

Cam kết kiến trúc:
Không sử dụng Power BI, không phụ thuộc file .pbix hay công cụ BI độc quyền bên ngoài.
"""

from docai.core.config import settings


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
        title="DocAI Document Intelligence Platform",
        suppress_callback_exceptions=True
    )

    app.layout = html.Div(
        children=[
            html.H1("DocAI Document Intelligence Platform", style={"textAlign": "center"}),
            html.P(
                "Invoice Workspace + Contract Workspace + Research Lab "
                "(Stack: Python -> pandas -> Plotly -> Dash).",
                style={"textAlign": "center"}
            ),
            dcc.Tabs(
                id="dashboard-tabs",
                value="tab-invoice",
                children=[
                    dcc.Tab(label="Invoice Workspace", value="tab-invoice"),
                    dcc.Tab(label="Contract Workspace", value="tab-contract"),
                    dcc.Tab(label="Research Lab", value="tab-research"),
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
        dash_app.run(debug=settings.debug, port=8050)
    else:
        print("Vui lòng cài đặt dash và plotly để chạy dashboard: pip install dash plotly")
