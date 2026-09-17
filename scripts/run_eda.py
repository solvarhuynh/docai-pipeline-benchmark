"""
CLI Script chạy khảo sát và khám phá dữ liệu (EDA).

Cách chạy:
    python scripts/run_eda.py --dataset all
    python scripts/run_eda.py --dataset mcocr2021
"""

import argparse
import json
from docai.core.config import settings
from docai.data.eda import analyze_dataset
from docai.data.loaders import list_available_datasets


def main():
    parser = argparse.ArgumentParser(description="Khảo sát dữ liệu thô cho DocAI Product & Research")
    parser.add_argument(
        "--dataset",
        type=str,
        default="all",
        choices=["all", "mcocr2021", "cord", "sroie", "cuad"],
        help="Tên bộ dữ liệu cần khảo sát (mặc định: all)"
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=50,
        help="Số lượng mẫu tối đa để phân tích độ phân giải (mặc định: 50)"
    )
    args = parser.parse_args()

    print("==================================================")
    print("DOCAI PRODUCT & RESEARCH - EDA SURVEY")
    print("==================================================")
    print(f"Thư mục dữ liệu thô: {settings.raw_data_dir}\n")

    datasets_to_check = (
        settings.supported_datasets if args.dataset == "all" else [args.dataset]
    )

    for ds_name in datasets_to_check:
        print(f"--- Đang phân tích bộ dữ liệu: {ds_name} ---")
        res = analyze_dataset(ds_name, max_samples=args.max_samples)
        print(f"Trạng thái: {res.get('status')}")
        print(f"Tổng số file: {res.get('total_files', 0)}")
        if res.get("extensions_breakdown"):
            print(f"Phân loại định dạng: {res.get('extensions_breakdown')}")
        if res.get("resolution_analysis"):
            print(f"Phân tích độ phân giải:\n{json.dumps(res['resolution_analysis'], indent=2, ensure_ascii=False)}")
        print()


if __name__ == "__main__":
    main()
