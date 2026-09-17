"""
Modal deployment script cho DocAI Dual-Pipeline Benchmark.

Thuộc: Giai đoạn 2 (Hạ tầng) và Giai đoạn 10 (FastAPI Service & Tài liệu hoá).
Nhiệm vụ:
- Cung cấp hàm test GPU đơn giản chạy thật để xác nhận tài khoản Modal, GPU T4 và billing hoạt động ngay từ đầu.
- Định nghĩa khung triển khai FastAPI service và các hàm tính toán GPU cho Track A và Track B trên Modal Serverless.
"""

import subprocess
import modal

app = modal.App("docai-pipeline-benchmark")

# Image cơ bản cho worker GPU
image = (
    modal.Image.debian_slim()
    .apt_install("libgl1", "libglib2.0-0")
    .pip_install(
        "torch>=2.2.0",
        "pydantic>=2.6.0",
        "fastapi>=0.110.0"
    )
)


@app.function(image=image, gpu="T4", timeout=120)
def test_gpu_billing():
    """
    Function test GPU đơn giản để kiểm tra billing và xác nhận GPU T4 hoạt động.
    Có thể chạy thật ngay bằng lệnh: modal run modal_app/deploy.py
    """
    res = subprocess.run(["nvidia-smi"], capture_output=True, text=True, check=True)
    return {
        "status": "success",
        "gpu_info": res.stdout.strip(),
        "message": "Modal GPU T4 allocation and billing confirmed."
    }


# TODO: Giai đoạn 4 - Định nghĩa function fine-tune LayoutLMv3 trên Modal GPU A10G/T4
# @app.function(image=image, gpu="A10G", timeout=3600)
# def run_finetune_layoutlmv3():
#     pass


# TODO: Giai đoạn 10 - Deploy FastAPI service lên Modal web endpoint
# @app.function(image=image, gpu="T4")
# @modal.asgi_app()
# def fastapi_app():
#     from api.main import app as web_app
#     return web_app


@app.local_entrypoint()
def main():
    """
    Entrypoint local để test GPU trên Modal qua CLI.
    """
    print("Testing Modal GPU billing...")
    result = test_gpu_billing.remote()
    print("Status:", result["status"])
    print("GPU Info:\n", result["gpu_info"])
