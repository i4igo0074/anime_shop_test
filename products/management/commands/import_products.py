import csv
import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.text import slugify
from products.models import Product, Category, Country  # Импортируйте ваши модели из приложения products
from decimal import Decimal

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(response.content)
        img_temp.flush()
        return img_temp
    else:
        return None

def clean_price(price):
    # Удаление символа валюты и пробелов
    cleaned_price = price.replace('₽', '').replace(' ', '').replace(',', '.')
    return Decimal(cleaned_price)

class Command(BaseCommand):
    help = 'Импортировать продукты из CSV'

    def handle(self, *args, **kwargs):
        csv_file_path = '/home/islambek/programming/parser/products.csv'  # путь к вашему CSV файлу

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Получаем или создаем категорию и страну
                    category, created = Category.objects.get_or_create(name='Одежда', defaults={'slug': slugify('Одежда')})
                    country, created = Country.objects.get_or_create(name='Казахстан', defaults={'slug': slugify('Казахстан')})
                    price = clean_price(row['price'])

                    # Создаем продукт
                    product = Product.objects.create(
                        name=row['name'],
                        description=row['description'],
                        price=price,
                        category=category,
                        country=country,
                        discount=0,
                        average_rating=0.00,
                    )

                    # Обработка изображения
                    image_url = row['base_image']
                    img_temp = download_image(image_url)
                    if img_temp:
                        product.base_image.save(os.path.basename(image_url), File(img_temp), save=True)

                    print(f"Продукт '{product.name}' успешно создан.")
        except FileNotFoundError:
            print(f"Ошибка: файл '{csv_file_path}' не найден.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
