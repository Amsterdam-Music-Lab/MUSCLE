import unittest

from experiment.actions.frontend_style import FrontendStyle, EFrontendStyle


class TestFrontendStyle(unittest.TestCase):

    def test_init_with_valid_root_style(self):
        style = FrontendStyle(EFrontendStyle.PRIMARY)
        self.assertEqual(style.get_style('root'), EFrontendStyle.PRIMARY)

    def test_init_with_invalid_root_style(self):
        with self.assertRaises(ValueError):
            FrontendStyle("invalid-style")

    def test_init_with_valid_nested_styles(self):
        nested_style = FrontendStyle(EFrontendStyle.SUCCESS)
        style = FrontendStyle(EFrontendStyle.PRIMARY, nested=nested_style)
        self.assertIsInstance(style.get_style('nested'), FrontendStyle)

    def test_init_with_invalid_nested_styles(self):
        with self.assertRaises(ValueError):
            FrontendStyle(EFrontendStyle.PRIMARY, nested="invalid-style")

    def test_get_style(self):
        style = FrontendStyle(EFrontendStyle.SECONDARY)
        self.assertEqual(style.get_style('root'), EFrontendStyle.SECONDARY)

    def test_get_style_non_existing_element(self):
        style = FrontendStyle(EFrontendStyle.SECONDARY)
        self.assertIsNone(style.get_style('non-existing'))

    def test_apply_valid_style(self):
        style = FrontendStyle(EFrontendStyle.EMPTY)
        style.apply_style('root', EFrontendStyle.INFO)
        self.assertEqual(style.get_style('root'), EFrontendStyle.INFO)

    def test_apply_invalid_style(self):
        style = FrontendStyle(EFrontendStyle.EMPTY)
        with self.assertRaises(ValueError):
            style.apply_style('root', "invalid-style")

    def test_to_dict(self):
        nested_style = FrontendStyle(EFrontendStyle.SUCCESS)
        style = FrontendStyle(EFrontendStyle.NEUTRAL, nested=nested_style)
        expected_dict = {'root': EFrontendStyle.NEUTRAL.value, 'nested': {'root': EFrontendStyle.SUCCESS.value}}
        self.assertEqual(style.to_dict(), expected_dict)

    def test_to_dict_with_deep_nesting(self):
        nested_style_level_2 = FrontendStyle(EFrontendStyle.WARNING)
        nested_style_level_1 = FrontendStyle(EFrontendStyle.INFO, nested_lvl2=nested_style_level_2)
        style = FrontendStyle(EFrontendStyle.NEUTRAL, nested_lvl1=nested_style_level_1)
        expected_dict = {
            'root': EFrontendStyle.NEUTRAL.value,
            'nested_lvl1': {
                'root': EFrontendStyle.INFO.value,
                'nested_lvl2': {
                    'root': EFrontendStyle.WARNING.value
                }
            }
        }
        self.assertEqual(style.to_dict(), expected_dict)


if __name__ == '__main__':
    unittest.main()
