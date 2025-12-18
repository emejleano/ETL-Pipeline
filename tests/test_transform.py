"""
Unit test untuk module transform.py
"""
import pytest
import pandas as pd
from utils.transform import (
    convert_price_to_rupiah,
    clean_rating,
    clean_colors,
    clean_size,
    clean_gender,
    remove_invalid_data,
    transform_data
)


class TestTransform:
    """Test class untuk fungsi-fungsi di transform.py"""
    
    def test_convert_price_to_rupiah_valid(self):
        """Test konversi harga valid"""
        assert convert_price_to_rupiah("$50") == 800000.0
        assert convert_price_to_rupiah("$100") == 1600000.0
        assert convert_price_to_rupiah("50") == 800000.0
    
    def test_convert_price_to_rupiah_unavailable(self):
        """Test konversi harga unavailable"""
        assert convert_price_to_rupiah("Price Unavailable") is None
        assert convert_price_to_rupiah("Unavailable") is None
    
    def test_convert_price_to_rupiah_null(self):
        """Test konversi harga null"""
        assert convert_price_to_rupiah(None) is None
        assert convert_price_to_rupiah("") is None
    
    def test_convert_price_to_rupiah_custom_rate(self):
        """Test konversi harga dengan rate custom"""
        assert convert_price_to_rupiah("$50", 15000) == 750000.0
    
    def test_clean_rating_valid(self):
        """Test clean rating valid"""
        assert clean_rating("4.5 / 5") == 4.5
        assert clean_rating("4.0 / 5") == 4.0
        assert clean_rating("5") == 5.0
    
    def test_clean_rating_invalid(self):
        """Test clean rating invalid"""
        assert clean_rating("Invalid Rating") is None
        assert clean_rating(None) is None
    
    def test_clean_colors_valid(self):
        """Test clean colors valid"""
        assert clean_colors("3 Colors") == 3
        assert clean_colors("5 Colors") == 5
        assert clean_colors("1") == 1
    
    def test_clean_colors_invalid(self):
        """Test clean colors invalid"""
        assert clean_colors(None) is None
        assert clean_colors("") is None
    
    def test_clean_size_valid(self):
        """Test clean size valid"""
        assert clean_size("Size: M, L, XL") == "M, L, XL"
        assert clean_size("Size: S") == "S"
    
    def test_clean_size_invalid(self):
        """Test clean size invalid"""
        assert clean_size(None) is None
        assert clean_size("") is None
    
    def test_clean_gender_valid(self):
        """Test clean gender valid"""
        assert clean_gender("Gender: Male") == "Male"
        assert clean_gender("Gender: Female") == "Female"
    
    def test_clean_gender_invalid(self):
        """Test clean gender invalid"""
        assert clean_gender(None) is None
        assert clean_gender("") is None
    
    def test_remove_invalid_data(self):
        """Test remove invalid data"""
        df = pd.DataFrame({
            'Title': ['Product 1', 'Unknown Product', 'Product 3'],
            'Price': [100, 200, 300]
        })
        
        result = remove_invalid_data(df)
        
        assert len(result) == 2
        assert 'Unknown Product' not in result['Title'].values
    
    def test_transform_data_success(self):
        """Test transformasi data berhasil"""
        raw_data = [
            {
                'Title': 'Product 1',
                'Price': '$50',
                'Rating': '4.5 / 5',
                'Colors': '3 Colors',
                'Size': 'Size: M, L',
                'Gender': 'Gender: Male',
                'timestamp': '2025-01-01 00:00:00'
            },
            {
                'Title': 'Product 2',
                'Price': '$60',
                'Rating': '4.0 / 5',
                'Colors': '2 Colors',
                'Size': 'Size: L, XL',
                'Gender': 'Gender: Female',
                'timestamp': '2025-01-01 00:00:00'
            }
        ]
        
        result = transform_data(raw_data)
        
        assert len(result) > 0
        assert result['Price'].dtype == float
        assert result['Rating'].dtype == float
        assert result['Colors'].dtype == int
        assert result['Size'].dtype == object
        assert result['Gender'].dtype == object
    
    def test_transform_data_removes_duplicates(self):
        """Test transformasi menghapus duplikat"""
        raw_data = [
            {
                'Title': 'Product 1',
                'Price': '$50',
                'Rating': '4.5 / 5',
                'Colors': '3 Colors',
                'Size': 'Size: M',
                'Gender': 'Gender: Male',
                'timestamp': '2025-01-01 00:00:00'
            },
            {
                'Title': 'Product 1',
                'Price': '$50',
                'Rating': '4.5 / 5',
                'Colors': '3 Colors',
                'Size': 'Size: M',
                'Gender': 'Gender: Male',
                'timestamp': '2025-01-01 00:00:00'
            }
        ]
        
        result = transform_data(raw_data)
        
        assert len(result) == 1
    
    def test_transform_data_removes_null(self):
        """Test transformasi menghapus null"""
        raw_data = [
            {
                'Title': 'Product 1',
                'Price': '$50',
                'Rating': '4.5 / 5',
                'Colors': '3 Colors',
                'Size': 'Size: M',
                'Gender': 'Gender: Male',
                'timestamp': '2025-01-01 00:00:00'
            },
            {
                'Title': 'Product 2',
                'Price': 'Price Unavailable',
                'Rating': 'Invalid Rating',
                'Colors': '2 Colors',
                'Size': 'Size: L',
                'Gender': 'Gender: Female',
                'timestamp': '2025-01-01 00:00:00'
            }
        ]
        
        result = transform_data(raw_data)
        
        # Data ke-2 akan dihapus karena Price dan Rating menjadi None
        assert len(result) == 1
    
    def test_convert_price_error_handling(self):
        """Test error handling pada convert_price_to_rupiah"""
        # Test dengan data yang tidak bisa dikonversi
        assert convert_price_to_rupiah("invalid_price") is None
    
    def test_clean_rating_error_handling(self):
        """Test error handling pada clean_rating"""
        # Test dengan data yang tidak bisa dikonversi
        assert clean_rating("not_a_rating") is None
    
    def test_transform_data_with_empty_list(self):
        """Test transformasi dengan list kosong"""
        with pytest.raises(Exception):
            transform_data([])
