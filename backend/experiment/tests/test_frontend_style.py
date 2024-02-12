import unittest

from experiment.actions.frontend_style import FrontendStyle


class TestFrontendStyle(unittest.TestCase):

    def test_init_with_valid_root_style(self):
        style = FrontendStyle(FrontendStyle.PRIMARY)
        self.assertEqual(style.get_style('root'), FrontendStyle.PRIMARY)

    def test_init_with_invalid_root_style(self):
        with self.assertRaises(ValueError):
            FrontendStyle("invalid-style")

    def test_init_with_valid_nested_styles(self):
        nested_style = FrontendStyle(FrontendStyle.SUCCESS)
        style = FrontendStyle(FrontendStyle.PRIMARY, nested=nested_style)
        self.assertIsInstance(style.get_style('nested'), FrontendStyle)

    def test_init_with_invalid_nested_styles(self):
        with self.assertRaises(ValueError):
            FrontendStyle(FrontendStyle.PRIMARY, nested="invalid-style")

    def test_get_style(self):
        style = FrontendStyle(FrontendStyle.SECONDARY)
        self.assertEqual(style.get_style('root'), FrontendStyle.SECONDARY)

    def test_get_style_non_existing_element(self):
        style = FrontendStyle(FrontendStyle.SECONDARY)
        self.assertIsNone(style.get_style('non-existing'))

    def test_apply_valid_style(self):
        style = FrontendStyle(FrontendStyle.EMPTY)
        style.apply_style('root', FrontendStyle.INFO)
        self.assertEqual(style.get_style('root'), FrontendStyle.INFO)

    def test_apply_invalid_style(self):
        style = FrontendStyle(FrontendStyle.EMPTY)
        with self.assertRaises(ValueError):
            style.apply_style('root', "invalid-style")

    def test_to_dict(self):
        nested_style = FrontendStyle(FrontendStyle.SUCCESS)
        style = FrontendStyle(FrontendStyle.NEUTRAL, nested=nested_style)
        expected_dict = {'root': FrontendStyle.NEUTRAL, 'nested': {'root': FrontendStyle.SUCCESS}}
        self.assertEqual(style.to_dict(), expected_dict)

    def test_to_dict_with_deep_nesting(self):
        nested_style_level_2 = FrontendStyle(FrontendStyle.WARNING)
        nested_style_level_1 = FrontendStyle(FrontendStyle.INFO, nested_lvl2=nested_style_level_2)
        style = FrontendStyle(FrontendStyle.NEUTRAL, nested_lvl1=nested_style_level_1)
        expected_dict = {
            'root': FrontendStyle.NEUTRAL,
            'nested_lvl1': {
                'root': FrontendStyle.INFO,
                'nested_lvl2': {
                    'root': FrontendStyle.WARNING
                }
            }
        }
        self.assertEqual(style.to_dict(), expected_dict)


if __name__ == '__main__':
    unittest.main()
