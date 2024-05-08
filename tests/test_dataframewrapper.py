"""
Pytest for DataFrameWrapper class
"""
import pytest
import os
os.chdir('..')

from src.dataframewrapper import DataFrameWrapper


class TestDataFrameWrapper:
    @pytest.fixture(scope='class')
    def wrapper(self):
        return DataFrameWrapper()
    # @pytest.param()
    def test_top_handset_manufacturer(self, wrapper):
        assert len(wrapper.top_handset_manufacturer(5)) == 5
