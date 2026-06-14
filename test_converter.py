import unittest
from converter import UnitConverter

class DummyConverter(UnitConverter):
    def __init__(self):
        # Skip Tkinter GUI setup to allow headless testing
        pass

class TestConverterLogic(unittest.TestCase):
    def setUp(self):
        self.converter = DummyConverter()

    def test_parse_feet_input_decimal(self):
        self.assertEqual(self.converter.parse_feet_input("7.25"), 7.25)
        self.assertEqual(self.converter.parse_feet_input("-7.25"), -7.25)
        self.assertEqual(self.converter.parse_feet_input("0"), 0.0)
        self.assertEqual(self.converter.parse_feet_input(""), 0.0)

    def test_parse_feet_input_feet_fraction_inches(self):
        # 7' 3 1/2" -> 7 + (3.5 / 12) = 7.291666...
        self.assertAlmostEqual(self.converter.parse_feet_input("7' 3 1/2\""), 7.2916667, places=6)
        self.assertAlmostEqual(self.converter.parse_feet_input("-7' 3 1/2\""), -7.2916667, places=6)
        # 7' 3/4" -> 7 + (0.75 / 12) = 7.0625
        self.assertAlmostEqual(self.converter.parse_feet_input("7' 3/4\""), 7.0625, places=6)
        self.assertAlmostEqual(self.converter.parse_feet_input("-7' 3/4\""), -7.0625, places=6)

    def test_parse_feet_input_feet_decimal_inches(self):
        # 7' 3.5" -> 7.291666...
        self.assertAlmostEqual(self.converter.parse_feet_input("7' 3.5\""), 7.2916667, places=6)
        self.assertAlmostEqual(self.converter.parse_feet_input("-7' 3.5\""), -7.2916667, places=6)

    def test_parse_feet_input_feet_only(self):
        self.assertEqual(self.converter.parse_feet_input("7'"), 7.0)
        self.assertEqual(self.converter.parse_feet_input("-7'"), -7.0)

    def test_parse_feet_input_fraction_only(self):
        # 3 1/2" -> 3.5 / 12 = 0.291666...
        self.assertAlmostEqual(self.converter.parse_feet_input("3 1/2\""), 0.2916667, places=6)
        # 1/2" -> 0.5 / 12 = 0.041666...
        self.assertAlmostEqual(self.converter.parse_feet_input("1/2\""), 0.0416667, places=6)
        # 1/2 (feet) -> 0.5
        self.assertEqual(self.converter.parse_feet_input("1/2"), 0.5)

    def test_parse_feet_input_invalid(self):
        # Division by zero should not crash, it should return None
        self.assertIsNone(self.converter.parse_feet_input("7' 3 1/0\""))
        self.assertIsNone(self.converter.parse_feet_input("1/0"))
        # Invalid format
        self.assertIsNone(self.converter.parse_feet_input("invalid"))
        self.assertIsNone(self.converter.parse_feet_input("7' 3a\""))

    def test_format_feet_fractional(self):
        self.assertEqual(self.converter.format_feet_fractional(0.0), "0'")
        self.assertEqual(self.converter.format_feet_fractional(7.2916667), "7' 3 1/2\"")
        self.assertEqual(self.converter.format_feet_fractional(-7.2916667), "-7' 3 1/2\"")
        # 7.0625 ft -> 7 feet, 0.75 inches -> 7' 3/4"
        self.assertEqual(self.converter.format_feet_fractional(7.0625), "7' 3/4\"")
        self.assertEqual(self.converter.format_feet_fractional(-7.0625), "-7' 3/4\"")

if __name__ == "__main__":
    unittest.main()
