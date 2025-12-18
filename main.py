"""
Main script untuk menjalankan ETL Pipeline
"""
from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import load_data
import sys


def main():
    """
    Fungsi utama untuk menjalankan ETL Pipeline
    """
    try:
        print("="*60)
        print("MEMULAI ETL PIPELINE - Fashion Studio Products")
        print("="*60)
        
        # EXTRACT
        print("\n[1/3] EXTRACT - Scraping data dari website...")
        raw_data = extract_data()
        print(f"✓ Extract selesai: {len(raw_data)} produk")
        
        # TRANSFORM
        print("\n[2/3] TRANSFORM - Membersihkan dan transformasi data...")
        clean_df = transform_data(raw_data)
        print(f"✓ Transform selesai: {len(clean_df)} produk (setelah cleaning)")
        
        # LOAD
        print("\n[3/3] LOAD - Menyimpan data...")
        
        # Konfigurasi: tentukan ke mana data akan disimpan
        
        results = load_data(
            df=clean_df,
            to_csv=True,                    # Simpan ke CSV
            to_google_sheets=True,          # Simpan ke Google Sheets
            csv_filename='products.csv',
            credentials_file='google-sheets-api.json',
            spreadsheet_id='19_1wpy7ZUWtQWd9fJj9xsqTUScHEezpffWqMAvlst4A',  # Spreadsheet yang sudah ada
            postgres_connection=None        
        )
        
        print("\n✓ Load selesai!")
        print("\n" + "="*60)
        print("RINGKASAN HASIL:")
        print("="*60)
        
        for target, result in results.items():
            if result:
                if result['status'] == 'success':
                    print(f"✓ {target.upper()}: Berhasil")
                    if 'path' in result:
                        print(f"  Path: {result['path']}")
                    if 'url' in result:
                        print(f"  URL: {result['url']}")
                else:
                    print(f"✗ {target.upper()}: Gagal - {result['error']}")
        
        print("\n" + "="*60)
        print("ETL PIPELINE SELESAI")
        print("="*60)
        
        # Preview data
        print("\nPreview 5 baris pertama:")
        print(clean_df.head())
        print("\nInfo DataFrame:")
        print(clean_df.info())
        
    except KeyboardInterrupt:
        print("\n\nETL Pipeline dibatalkan oleh user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
