import os
import unittest
from src.tokenreplace import load_config, load_mappings_from_csv, combine_mappings, process_file_or_directory

class TestTokenReplace(unittest.TestCase):

    def setUp(self):
        self.config_file = 'config/test_config.json'
        self.test_data_dir = 'tests/test_data'
        self.sample_mappings = {
            "#F8F8F8": "@color/ds_color_gray_05",
            "#4A4A4A": "@color/ds_color_dark"
        }
        self.sample_csv_path = 'config/example_mappings.csv'

    def test_load_config(self):
        config = load_config(self.config_file)
        self.assertIn('file_extensions', config)
        self.assertIn('mappings', config)
        self.assertIn('csv_file_path', config)
        self.assertIn('targets', config)

    def test_load_mappings_from_csv(self):
        mappings = load_mappings_from_csv(self.sample_csv_path)
        self.assertIn("#F8F8F8", mappings)
        self.assertEqual(mappings["#F8F8F8"], "@color/ds_color_gray_05")

    def test_combine_mappings(self):
        config_mappings = {"#FFFFFF": "@color/white"}
        csv_mappings = self.sample_mappings
        combined_mappings = combine_mappings(config_mappings, csv_mappings)
        self.assertIn("#FFFFFF", combined_mappings)
        self.assertIn("#F8F8F8", combined_mappings)

    def test_process_file_or_directory(self):
        config = load_config(self.config_file)
        mappings = combine_mappings(config['mappings'], load_mappings_from_csv(config['csv_file_path']))
        targets = config['targets']

        for target in targets:
            process_file_or_directory(
                path=target,
                mappings=mappings,
                file_extensions=config['file_extensions']
            )

        # Check XML file
        with open(os.path.join(self.test_data_dir, 'test_file.xml'), 'r') as file:
            content = file.read()
            self.assertIn('@color/ds_color_gray_05', content)
            self.assertIn('@color/ds_color_dark', content)

        # Check Swift file
        with open(os.path.join(self.test_data_dir, 'test_file.swift'), 'r') as file:
            content = file.read()
            self.assertIn('UIColor.dsColorGray05', content)
            self.assertIn('UIColor.dsColorDark', content)

        # Check HTML file
        with open(os.path.join(self.test_data_dir, 'test_file.html'), 'r') as file:
            content = file.read()
            self.assertIn('var(--ds-color-gray-05)', content)
            self.assertIn('var(--ds-color-dark)', content)

if __name__ == '__main__':
    unittest.main()
