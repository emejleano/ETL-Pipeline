"""
Module untuk loading data ke berbagai repositori data
"""
import pandas as pd
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from sqlalchemy import create_engine, text
import json


def load_to_csv(df, filename='products.csv'):
    """
    Simpan DataFrame ke file CSV
    
    Args:
        df (pd.DataFrame): DataFrame yang akan disimpan
        filename (str): Nama file CSV
        
    Returns:
        str: Path file yang disimpan
        
    Raises:
        Exception: Jika terjadi error saat menyimpan
    """
    try:
        # Simpan ke CSV
        df.to_csv(filename, index=False)
        
        print(f"Data berhasil disimpan ke {filename}")
        
        return os.path.abspath(filename)
        
    except Exception as e:
        raise Exception(f"Error menyimpan ke CSV: {e}")


def load_to_google_sheets(df, credentials_file='google-sheets-api.json', spreadsheet_id=None):
    """
    Simpan DataFrame ke Google Sheets
    
    Args:
        df (pd.DataFrame): DataFrame yang akan disimpan
        credentials_file (str): Path ke file credentials JSON
        spreadsheet_id (str): ID spreadsheet (optional, akan membuat baru jika None)
        
    Returns:
        str: URL Google Sheets
        
    Raises:
        Exception: Jika terjadi error saat menyimpan
    """
    try:
        # Load credentials
        if not os.path.exists(credentials_file):
            raise FileNotFoundError(f"File credentials tidak ditemukan: {credentials_file}")
        
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
                  'https://www.googleapis.com/auth/drive']
        
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES)
        
        service = build('sheets', 'v4', credentials=credentials)
        drive_service = build('drive', 'v3', credentials=credentials)
        
        # Jika tidak ada spreadsheet_id, buat spreadsheet baru
        if not spreadsheet_id:
            spreadsheet = {
                'properties': {
                    'title': 'Fashion Studio Products'
                }
            }
            spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                        fields='spreadsheetId').execute()
            spreadsheet_id = spreadsheet.get('spreadsheetId')
            
            # Set permission untuk "Anyone with the link" sebagai EDITOR
            permission = {
                'type': 'anyone',
                'role': 'writer'
            }
            drive_service.permissions().create(
                fileId=spreadsheet_id,
                body=permission
            ).execute()
            
            print(f"Spreadsheet baru dibuat: {spreadsheet_id}")
        else:
            print(f"Menggunakan spreadsheet yang sudah ada: {spreadsheet_id}")
        
        # Konversi DataFrame ke list of lists
        values = [df.columns.tolist()] + df.values.tolist()
        
        # Clear existing data
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range='Sheet1'
        ).execute()
        
        # Update data
        body = {
            'values': values
        }
        
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range='Sheet1!A1',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
        print(f"Data berhasil disimpan ke Google Sheets: {url}")
        
        return url
        
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except Exception as e:
        raise Exception(f"Error menyimpan ke Google Sheets: {e}")


def load_to_postgresql(df, connection_string=None):
    """
    Simpan DataFrame ke PostgreSQL
    
    Args:
        df (pd.DataFrame): DataFrame yang akan disimpan
        connection_string (str): Connection string PostgreSQL
                                Format: postgresql://user:password@host:port/database
        
    Returns:
        bool: True jika berhasil
        
    Raises:
        Exception: Jika terjadi error saat menyimpan
    """
    try:
        if not connection_string:
            # Default connection string untuk testing lokal
            connection_string = os.getenv('POSTGRESQL_CONNECTION_STRING', 
                                         'postgresql://postgres:postgres@localhost:5432/fashion_db')
        
        # Create engine
        engine = create_engine(connection_string)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        # Simpan ke database
        table_name = 'products'
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        print(f"Data berhasil disimpan ke PostgreSQL table: {table_name}")
        
        return True
        
    except Exception as e:
        raise Exception(f"Error menyimpan ke PostgreSQL: {e}")


def load_data(df, to_csv=True, to_google_sheets=False, to_postgresql=False,
              csv_filename='products.csv', credentials_file='google-sheets-api.json',
              spreadsheet_id=None, postgres_connection=None):
    """
    Fungsi utama untuk loading data ke berbagai repositori
    
    Args:
        df (pd.DataFrame): DataFrame yang akan disimpan
        to_csv (bool): Simpan ke CSV
        to_google_sheets (bool): Simpan ke Google Sheets
        to_postgresql (bool): Simpan ke PostgreSQL
        csv_filename (str): Nama file CSV
        credentials_file (str): Path ke file credentials Google Sheets
        spreadsheet_id (str): ID Google Sheets (optional)
        postgres_connection (str): Connection string PostgreSQL
        
    Returns:
        dict: Dictionary berisi status dan informasi hasil loading
        
    Raises:
        Exception: Jika semua loading gagal
    """
    results = {
        'csv': None,
        'google_sheets': None,
        'postgresql': None
    }
    
    errors = []
    
    try:
        # Load ke CSV
        if to_csv:
            try:
                csv_path = load_to_csv(df, csv_filename)
                results['csv'] = {'status': 'success', 'path': csv_path}
            except Exception as e:
                error_msg = f"CSV Error: {e}"
                print(error_msg)
                errors.append(error_msg)
                results['csv'] = {'status': 'failed', 'error': str(e)}
        
        # Load ke Google Sheets
        if to_google_sheets:
            try:
                sheets_url = load_to_google_sheets(df, credentials_file, spreadsheet_id)
                results['google_sheets'] = {'status': 'success', 'url': sheets_url}
            except Exception as e:
                error_msg = f"Google Sheets Error: {e}"
                print(error_msg)
                errors.append(error_msg)
                results['google_sheets'] = {'status': 'failed', 'error': str(e)}
        
        # Load ke PostgreSQL
        if to_postgresql:
            try:
                load_to_postgresql(df, postgres_connection)
                results['postgresql'] = {'status': 'success'}
            except Exception as e:
                error_msg = f"PostgreSQL Error: {e}"
                print(error_msg)
                errors.append(error_msg)
                results['postgresql'] = {'status': 'failed', 'error': str(e)}
        
        # Jika semua loading yang diminta gagal
        if all(results[k] and results[k].get('status') == 'failed' 
               for k in results if results[k] is not None):
            raise Exception(f"Semua loading gagal: {'; '.join(errors)}")
        
        return results
        
    except Exception as e:
        raise Exception(f"Error loading data: {e}")
