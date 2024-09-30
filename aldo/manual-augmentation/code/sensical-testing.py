import unittest
#>>>>>>>>>>>>>>>ADDED THIS<<<<<<<<<<<<<<<<<<
import pandas as pd
from unittest.mock import patch
import matplotlib
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
from sensical_edc import sage_data_client, plot_pressure_and_hist, plot_temperature_and_hist

# class TestIntegration(unittest.TestCase):
#     def setUp(self):
#         self.pressure_df = pd.DataFrame({'timestamp': ['2022-01-01'], 'value': [100000]})
#         self.temperature_df = pd.DataFrame({'timestamp': ['2022-01-01'], 'value': [200000]})

#     def test_plot_pressure_and_temperature(self):
#         sage_data_client.query.return_value = self.pressure_df
#         plot_pressure_and_hist()
#         plot_temperature_and_hist()

#         # Check that the plots were created correctly
#         # assert matplotlib.pyplot.show.called


class TestPlotFunctions(unittest.TestCase):
    def setUp(self):
        self.pressure_df = pd.DataFrame({'timestamp': ['2022-01-01'], 'value': [100]})
        self.temperature_df = pd.DataFrame({'timestamp': ['2022-01-01'], 'value': [20]})

    def test_plot_pressure_and_hist(self):
        with unittest.mock.patch('matplotlib.pyplot.show') as mock_show:
            plot_pressure_and_hist()
            # mock_show.assert_called_once()

    def test_plot_temperature_and_hist(self):
        with unittest.mock.patch('matplotlib.pyplot.show') as mock_show:
            plot_temperature_and_hist()
            # mock_show.assert_called_once()

    def test_plot_pressure_and_hist_with_data(self):
        with unittest.mock.patch('matplotlib.pyplot.show') as mock_show:
            plot_pressure_and_hist()
            # mock_show.assert_called_once()

    def test_plot_temperature_and_hist_with_data(self):
        with unittest.mock.patch('matplotlib.pyplot.show') as mock_show:
            plot_temperature_and_hist()
            # mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()

