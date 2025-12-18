"""
Module untuk ekstraksi data dari website fashion-studio.dicoding.dev
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


def scrape_page(page_number):
    """
    Scrape data dari satu halaman website
    
    Args:
        page_number (int): Nomor halaman yang akan di-scrape
        
    Returns:
        list: List of dictionaries berisi data produk
        
    Raises:
        requests.RequestException: Jika terjadi error saat request
        Exception: Jika terjadi error saat parsing data
    """
    try:
        # Halaman 1 adalah root URL, halaman lainnya menggunakan page{nomor}
        if page_number == 1:
            url = "https://fashion-studio.dicoding.dev/"
        else:
            url = f"https://fashion-studio.dicoding.dev/page{page_number}"
        
        # Menambahkan headers untuk menghindari blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []
        
        # Mencari semua card produk dengan class 'collection-card'
        product_cards = soup.find_all('div', class_='collection-card')
        
        if not product_cards:
            raise Exception(f"Tidak ditemukan produk di halaman {page_number}")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for card in product_cards:
            try:
                # Extract title dari h3 class='product-title'
                title_elem = card.find('h3', class_='product-title')
                title = title_elem.text.strip() if title_elem else None
                
                # Extract price dari span class='price'
                price_elem = card.find('span', class_='price')
                price = price_elem.text.strip() if price_elem else None
                
                # Extract rating, colors, size, gender dari paragraf
                # Semua ada di dalam <p> tags
                paragraphs = card.find_all('p', style="font-size: 14px; color: #777;")
                
                rating = None
                colors = None
                size = None
                gender = None
                
                for p in paragraphs:
                    text = p.text.strip()
                    if 'Rating:' in text:
                        rating = text.replace('Rating:', '').replace('⭐', '').strip()
                    elif 'Colors' in text:
                        colors = text.strip()
                    elif 'Size:' in text:
                        size = text.strip()
                    elif 'Gender:' in text:
                        gender = text.strip()
                
                product = {
                    'Title': title,
                    'Price': price,
                    'Rating': rating,
                    'Colors': colors,
                    'Size': size,
                    'Gender': gender,
                    'timestamp': timestamp
                }
                
                products.append(product)
                
            except Exception as e:
                print(f"Error parsing product card: {e}")
                continue
        
        return products
        
    except requests.RequestException as e:
        raise requests.RequestException(f"Error melakukan request ke halaman {page_number}: {e}")
    except Exception as e:
        raise Exception(f"Error scraping halaman {page_number}: {e}")


def scrape_all_pages(start_page=1, end_page=50):
    """
    Scrape data dari semua halaman website
    
    Args:
        start_page (int): Halaman awal
        end_page (int): Halaman akhir
        
    Returns:
        list: List of dictionaries berisi semua data produk
        
    Raises:
        Exception: Jika terjadi error saat scraping
    """
    try:
        all_products = []
        
        print(f"Memulai scraping dari halaman {start_page} sampai {end_page}...")
        
        for page in range(start_page, end_page + 1):
            try:
                print(f"Scraping halaman {page}...")
                products = scrape_page(page)
                all_products.extend(products)
                
                # Delay untuk menghindari rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error di halaman {page}: {e}")
                continue
        
        print(f"Scraping selesai. Total produk: {len(all_products)}")
        
        if not all_products:
            raise Exception("Tidak ada data yang berhasil di-scrape")
        
        return all_products
        
    except Exception as e:
        raise Exception(f"Error saat scraping semua halaman: {e}")


def extract_data():
    """
    Fungsi utama untuk ekstraksi data
    
    Returns:
        list: List of dictionaries berisi semua data produk
    """
    try:
        return scrape_all_pages(1, 50)
    except Exception as e:
        print(f"Error ekstraksi data: {e}")
        raise
