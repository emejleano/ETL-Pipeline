"""
Unit test untuk module extract.py
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from utils.extract import scrape_page, scrape_all_pages, extract_data
import requests


class TestExtract:
    """Test class untuk fungsi-fungsi di extract.py"""
    
    @patch('utils.extract.requests.get')
    def test_scrape_page_success(self, mock_get):
        """Test scraping satu halaman berhasil"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'''
        <html>
            <div class="card">
                <h5 class="card-title">Test Product</h5>
                <p class="card-text">$50</p>
                <span class="rating">4.5 / 5</span>
                <span class="colors">3 Colors</span>
                <span class="size">Size: M, L, XL</span>
                <span class="gender">Gender: Male</span>
            </div>
        </html>
        '''
        mock_get.return_value = mock_response
        
        # Test
        result = scrape_page(1)
        
        # Assert
        assert len(result) > 0
        assert result[0]['Title'] == 'Test Product'
        assert result[0]['Price'] == '$50'
        assert 'timestamp' in result[0]
    
    @patch('utils.extract.requests.get')
    def test_scrape_page_request_error(self, mock_get):
        """Test error saat request"""
        mock_get.side_effect = requests.RequestException("Connection error")
        
        with pytest.raises(requests.RequestException):
            scrape_page(1)
    
    @patch('utils.extract.requests.get')
    def test_scrape_page_no_products(self, mock_get):
        """Test halaman tanpa produk"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'<html><body></body></html>'
        mock_get.return_value = mock_response
        
        with pytest.raises(Exception):
            scrape_page(1)
    
    @patch('utils.extract.scrape_page')
    def test_scrape_all_pages_success(self, mock_scrape_page):
        """Test scraping semua halaman berhasil"""
        # Mock scrape_page untuk return 2 produk per halaman
        mock_scrape_page.return_value = [
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
                'Price': '$60',
                'Rating': '4.0 / 5',
                'Colors': '2 Colors',
                'Size': 'Size: L',
                'Gender': 'Gender: Female',
                'timestamp': '2025-01-01 00:00:00'
            }
        ]
        
        # Test dengan 3 halaman saja
        result = scrape_all_pages(1, 3)
        
        # Assert
        assert len(result) == 6  # 2 produk x 3 halaman
        assert mock_scrape_page.call_count == 3
    
    @patch('utils.extract.scrape_page')
    def test_scrape_all_pages_no_data(self, mock_scrape_page):
        """Test scraping semua halaman tidak menghasilkan data"""
        mock_scrape_page.side_effect = Exception("No data")
        
        with pytest.raises(Exception):
            scrape_all_pages(1, 2)
    
    @patch('utils.extract.scrape_all_pages')
    def test_extract_data_success(self, mock_scrape_all):
        """Test fungsi extract_data berhasil"""
        mock_scrape_all.return_value = [
            {'Title': 'Product 1', 'Price': '$50'}
        ]
        
        result = extract_data()
        
        assert len(result) > 0
        assert mock_scrape_all.called
    
    @patch('utils.extract.scrape_all_pages')
    def test_extract_data_error(self, mock_scrape_all):
        """Test fungsi extract_data error"""
        mock_scrape_all.side_effect = Exception("Scraping failed")
        
        with pytest.raises(Exception):
            extract_data()
    
    def test_scrape_page_with_invalid_page(self):
        """Test scrape_page dengan nomor halaman invalid"""
        # Test akan menghasilkan error karena halaman tidak ada
        with pytest.raises(Exception):
            scrape_page(-1)
    
    @patch('utils.extract.requests.get')
    def test_scrape_page_timeout(self, mock_get):
        """Test timeout saat scraping"""
        mock_get.side_effect = requests.Timeout("Request timeout")
        
        with pytest.raises(requests.RequestException):
            scrape_page(1)
