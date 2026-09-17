"""
Integration test kiểm tra các route của FastAPI Service (docai.api.main).
"""

import unittest

try:
    from docai.api.main import app
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False


class TestAPIRoutes(unittest.TestCase):
    """
    Kiểm tra cấu hình router, endpoint và phương thức HTTP của FastAPI service.
    """

    @unittest.skipUnless(FASTAPI_AVAILABLE, "FastAPI chưa được cài đặt trong môi trường này")
    def test_routes_registered(self):
        registered_paths = {route.path for route in app.routes}
        self.assertIn("/health", registered_paths)
        self.assertIn("/parse/classic", registered_paths)
        self.assertIn("/parse/vlm", registered_paths)
        self.assertIn("/compare", registered_paths)
        self.assertIn("/explain", registered_paths)

    @unittest.skipUnless(FASTAPI_AVAILABLE, "FastAPI chưa được cài đặt trong môi trường này")
    def test_health_route_methods(self):
        health_route = next((r for r in app.routes if r.path == "/health"), None)
        self.assertIsNotNone(health_route)
        self.assertIn("GET", health_route.methods)

    @unittest.skipUnless(FASTAPI_AVAILABLE, "FastAPI chưa được cài đặt trong môi trường này")
    def test_parsing_routes_methods(self):
        classic_route = next((r for r in app.routes if r.path == "/parse/classic"), None)
        vlm_route = next((r for r in app.routes if r.path == "/parse/vlm"), None)
        compare_route = next((r for r in app.routes if r.path == "/compare"), None)
        explain_route = next((r for r in app.routes if r.path == "/explain"), None)

        self.assertIsNotNone(classic_route)
        self.assertIn("POST", classic_route.methods)

        self.assertIsNotNone(vlm_route)
        self.assertIn("POST", vlm_route.methods)

        self.assertIsNotNone(compare_route)
        self.assertIn("POST", compare_route.methods)

        self.assertIsNotNone(explain_route)
        self.assertIn("POST", explain_route.methods)


if __name__ == "__main__":
    unittest.main()
