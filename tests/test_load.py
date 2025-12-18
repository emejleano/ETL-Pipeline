"""
Unit test untuk module load.py
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock, mock_open
from utils.load import (
    load_to_csv,
    load_to_google_sheets,
    load_to_postgresql,
    load_data
)
import os


class TestLoad:
    """Test class untuk fungsi-fungsi di load.py"""
    
    def test_load_to_csv_success(self, tmp_path):
        """Test simpan ke CSV berhasil"""
        # Create sample DataFrame
        df = pd.DataFrame({
            'Title': ['Product 1', 'Product 2'],
            'Price': [800000.0, 960000.0],
            'Rating': [4.5, 4.0]
        })
        
        # Create temporary file path
        csv_file = tmp_path / "test_products.csv"
        
        # Test
        result = load_to_csv(df, str(csv_file))
        
        # Assert
        assert os.path.exists(csv_file)
        assert csv_file.read_text().startswith('Title,Price,Rating')
    
    def test_load_to_csv_error(self):
        """Test error saat simpan ke CSV"""
        df = pd.DataFrame({'col': [1, 2, 3]})
        
        # Test dengan path yang invalid
        with pytest.raises(Exception):
            load_to_csv(df, '/invalid/path/file.csv')
    
    @patch('utils.load.service_account.Credentials.from_service_account_file')
    @patch('utils.load.build')
    def test_load_to_google_sheets_success(self, mock_build, mock_creds):
        """Test simpan ke Google Sheets berhasil"""
        # Mock credentials
        mock_creds.return_value = Mock()
        
        # Mock Google Sheets service
        mock_sheets_service = MagicMock()
        mock_drive_service = MagicMock()
        
        # Mock create spreadsheet
        mock_sheets_service.spreadsheets().create().execute.return_value = {
            'spreadsheetId': 'test123'
        }
        
        # Mock clear and update
        mock_sheets_service.spreadsheets().values().clear().execute.return_value = {}
        mock_sheets_service.spreadsheets().values().update().execute.return_value = {}
        
        # Mock drive permission
        mock_drive_service.permissions().create().execute.return_value = {}
        
        # Setup build to return different services
        def build_side_effect(service, version, credentials):
            if service == 'sheets':
                return mock_sheets_service
            elif service == 'drive':
                return mock_drive_service
        
        mock_build.side_effect = build_side_effect
        
        # Create sample DataFrame
        df = pd.DataFrame({
            'Title': ['Product 1'],
            'Price': [800000.0]
        })
        
        # Test dengan mock credentials file
        with patch('os.path.exists', return_value=True):
            result = load_to_google_sheets(df)
        
        # Assert
        assert 'https://docs.google.com/spreadsheets/d/test123' in result
    
    @patch('utils.load.service_account.Credentials.from_service_account_file')
    def test_load_to_google_sheets_no_credentials(self, mock_creds):
        """Test Google Sheets tanpa credentials file"""
        df = pd.DataFrame({'col': [1, 2, 3]})
        
        with pytest.raises(FileNotFoundError):
            load_to_google_sheets(df, 'nonexistent.json')
    
    @patch('utils.load.create_engine')
    def test_load_to_postgresql_success(self, mock_create_engine):
        """Test simpan ke PostgreSQL berhasil"""
        # Mock engine and connection
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_create_engine.return_value = mock_engine
        
        # Create sample DataFrame
        df = pd.DataFrame({
            'Title': ['Product 1'],
            'Price': [800000.0]
        })
        
        # Mock to_sql
        with patch.object(pd.DataFrame, 'to_sql'):
            result = load_to_postgresql(df, 'postgresql://user:pass@localhost/db')
        
        # Assert
        assert result is True
    
    @patch('utils.load.create_engine')
    def test_load_to_postgresql_connection_error(self, mock_create_engine):
        """Test error koneksi PostgreSQL"""
        mock_create_engine.side_effect = Exception("Connection failed")
        
        df = pd.DataFrame({'col': [1, 2, 3]})
        
        with pytest.raises(Exception):
            load_to_postgresql(df, 'postgresql://invalid')
    
    @patch('utils.load.load_to_csv')
    def test_load_data_csv_only(self, mock_csv):
        """Test load_data hanya ke CSV"""
        mock_csv.return_value = '/path/to/products.csv'
        
        df = pd.DataFrame({'col': [1, 2, 3]})
        
        result = load_data(df, to_csv=True, to_google_sheets=False, to_postgresql=False)
        
        assert result['csv']['status'] == 'success'
        assert mock_csv.called
    
    @patch('utils.load.load_to_csv')
    @patch('utils.load.load_to_google_sheets')
    def test_load_data_multiple_targets(self, mock_sheets, mock_csv):
        """Test load_data ke multiple targets"""
        mock_csv.return_value = '/path/to/products.csv'
        mock_sheets.return_value = 'https://sheets.google.com/test'
        
        df = pd.DataFrame({'col': [1, 2, 3]})
        
        result = load_data(df, to_csv=True, to_google_sheets=True, to_postgresql=False)
        
        assert result['csv']['status'] == 'success'
        assert result['google_sheets']['status'] == 'success'
        assert mock_csv.called
        assert mock_sheets.called
    
    @patch('utils.load.load_to_csv')
    def test_load_data_csv_error(self, mock_csv):
        """Test error saat load ke CSV"""
        mock_csv.side_effect = Exception("CSV Error")
        
        df = pd.DataFrame({'col': [1, 2, 3]})
        
        # Seharusnya masih berjalan tapi dengan status failed
        result = load_data(df, to_csv=True, to_google_sheets=False, to_postgresql=False)
        
        assert result['csv']['status'] == 'failed'
    
    @patch('utils.load.load_to_csv')
    @patch('utils.load.load_to_google_sheets')
    @patch('utils.load.load_to_postgresql')
    def test_load_data_all_failed(self, mock_pg, mock_sheets, mock_csv):
        """Test semua loading gagal"""
        mock_csv.side_effect = Exception("CSV Error")
        mock_sheets.side_effect = Exception("Sheets Error")
        mock_pg.side_effect = Exception("PG Error")
        
        df = pd.DataFrame({'col': [1, 2, 3]})
        
        with pytest.raises(Exception):
            load_data(df, to_csv=True, to_google_sheets=True, to_postgresql=True)
    
    def test_load_to_csv_with_special_characters(self, tmp_path):
        """Test simpan CSV dengan karakter special"""
        df = pd.DataFrame({
            'Title': ['Product "Special"', 'Product, with comma'],
            'Price': [800000.0, 960000.0]
        })
        
        csv_file = tmp_path / "special_test.csv"
        
        result = load_to_csv(df, str(csv_file))
        
        assert os.path.exists(csv_file)
        
        # Baca kembali dan verify
        df_read = pd.read_csv(csv_file)
        assert len(df_read) == 2
