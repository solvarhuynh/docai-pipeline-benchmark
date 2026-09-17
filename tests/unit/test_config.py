"""
Unit test kiểm tra module cấu hình hệ thống (docai.core.config).
"""

import unittest
from docai.core.config import Settings, settings


class TestConfig(unittest.TestCase):
    """
    Kiểm tra cấu hình đường dẫn và tham số hệ thống.
    """

    def test_settings_instance(self):
        self.assertIsInstance(settings, Settings)
        self.assertTrue(settings.repo_root.exists(), "Thư mục gốc của repository phải tồn tại")

    def test_data_paths(self):
        self.assertEqual(settings.data_dir, settings.repo_root / "data")
        self.assertEqual(settings.raw_data_dir, settings.repo_root / "data" / "raw")
        self.assertEqual(settings.interim_data_dir, settings.repo_root / "data" / "interim")
        self.assertEqual(settings.processed_data_dir, settings.repo_root / "data" / "processed")

    def test_supported_datasets(self):
        datasets = settings.supported_datasets
        self.assertIn("mcocr2021", datasets)
        self.assertIn("cord", datasets)
        self.assertIn("sroie", datasets)
        self.assertIn("cuad", datasets)


if __name__ == "__main__":
    unittest.main()
