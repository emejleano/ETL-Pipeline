"""
Module untuk transformasi dan pembersihan data
"""
import pandas as pd
import re


def convert_price_to_rupiah(price_str, exchange_rate=16000):
    """
    Konversi harga dari dolar ke rupiah
    
    Args:
        price_str (str): String harga dalam format "$xxx" atau "Price Unavailable"
        exchange_rate (int): Nilai tukar dolar ke rupiah
        
    Returns:
        float or None: Harga dalam rupiah atau None jika tidak valid
        
    Raises:
        ValueError: Jika terjadi error konversi
    """
    try:
        if not price_str or pd.isna(price_str):
            return None
            
        if "Price Unavailable" in str(price_str) or "Unavailable" in str(price_str):
            return None
        
        # Extract angka dari string menggunakan regex
        price_match = re.search(r'\$?\s*(\d+\.?\d*)', str(price_str))
        if price_match:
            price_usd = float(price_match.group(1))
            return price_usd * exchange_rate
        
        return None
        
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Error konversi price: {e}")


def clean_rating(rating_str):
    """
    Membersihkan kolom rating
    
    Args:
        rating_str (str): String rating dalam format "4.8 / 5" atau "Invalid Rating"
        
    Returns:
        float or None: Nilai rating atau None jika tidak valid
        
    Raises:
        ValueError: Jika terjadi error konversi
    """
    try:
        if not rating_str or pd.isna(rating_str):
            return None
            
        if "Invalid" in str(rating_str):
            return None
        
        # Extract angka rating menggunakan regex
        rating_match = re.search(r'(\d+\.?\d*)', str(rating_str))
        if rating_match:
            return float(rating_match.group(1))
        
        return None
        
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Error clean rating: {e}")


def clean_colors(colors_str):
    """
    Membersihkan kolom colors
    
    Args:
        colors_str (str): String colors dalam format "3 Colors"
        
    Returns:
        int or None: Jumlah warna atau None jika tidak valid
        
    Raises:
        ValueError: Jika terjadi error konversi
    """
    try:
        if not colors_str or pd.isna(colors_str):
            return None
        
        # Extract angka dari string
        colors_match = re.search(r'(\d+)', str(colors_str))
        if colors_match:
            return int(colors_match.group(1))
        
        return None
        
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Error clean colors: {e}")


def clean_size(size_str):
    """
    Membersihkan kolom size
    
    Args:
        size_str (str): String size dalam format "Size: M, L, XL"
        
    Returns:
        str or None: Ukuran tanpa prefix atau None jika tidak valid
        
    Raises:
        ValueError: Jika terjadi error konversi
    """
    try:
        if not size_str or pd.isna(size_str):
            return None
        
        # Hapus prefix "Size: "
        clean = str(size_str).replace("Size:", "").strip()
        
        if clean:
            return clean
        
        return None
        
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Error clean size: {e}")


def clean_gender(gender_str):
    """
    Membersihkan kolom gender
    
    Args:
        gender_str (str): String gender dalam format "Gender: Male"
        
    Returns:
        str or None: Jenis kelamin tanpa prefix atau None jika tidak valid
        
    Raises:
        ValueError: Jika terjadi error konversi
    """
    try:
        if not gender_str or pd.isna(gender_str):
            return None
        
        # Hapus prefix "Gender: "
        clean = str(gender_str).replace("Gender:", "").strip()
        
        if clean:
            return clean
        
        return None
        
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Error clean gender: {e}")


def remove_invalid_data(df):
    """
    Hapus data yang tidak valid seperti "Unknown Product"
    
    Args:
        df (pd.DataFrame): DataFrame yang akan dibersihkan
        
    Returns:
        pd.DataFrame: DataFrame yang sudah dibersihkan
        
    Raises:
        Exception: Jika terjadi error saat menghapus data invalid
    """
    try:
        # Hapus data dengan title "Unknown Product" atau mengandung "Unknown"
        df = df[~df['Title'].str.contains('Unknown', case=False, na=False)]
        
        return df
        
    except Exception as e:
        raise Exception(f"Error menghapus invalid data: {e}")


def transform_data(raw_data):
    """
    Fungsi utama untuk transformasi data
    
    Args:
        raw_data (list): List of dictionaries dari hasil scraping
        
    Returns:
        pd.DataFrame: DataFrame yang sudah dibersihkan dan ditransformasi
        
    Raises:
        Exception: Jika terjadi error saat transformasi
    """
    try:
        # Konversi ke DataFrame
        df = pd.DataFrame(raw_data)
        
        print(f"Data awal: {len(df)} baris")
        
        # Transformasi setiap kolom
        df['Price'] = df['Price'].apply(convert_price_to_rupiah)
        df['Rating'] = df['Rating'].apply(clean_rating)
        df['Colors'] = df['Colors'].apply(clean_colors)
        df['Size'] = df['Size'].apply(clean_size)
        df['Gender'] = df['Gender'].apply(clean_gender)
        
        # Hapus data invalid
        df = remove_invalid_data(df)
        print(f"Setelah hapus invalid data: {len(df)} baris")
        
        # Hapus duplikat
        df = df.drop_duplicates()
        print(f"Setelah hapus duplikat: {len(df)} baris")
        
        # Hapus baris dengan nilai null
        df = df.dropna()
        print(f"Setelah hapus null: {len(df)} baris")
        
        # Konversi tipe data
        df['Price'] = df['Price'].astype(float)
        df['Rating'] = df['Rating'].astype(float)
        df['Colors'] = df['Colors'].astype(int)
        df['Size'] = df['Size'].astype(str)
        df['Gender'] = df['Gender'].astype(str)
        df['Title'] = df['Title'].astype(str)
        df['timestamp'] = df['timestamp'].astype(str)
        
        print(f"Data final: {len(df)} baris")
        print("\nTipe data:")
        print(df.dtypes)
        
        return df
        
    except Exception as e:
        raise Exception(f"Error transformasi data: {e}")
