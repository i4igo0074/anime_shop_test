from products import Product  
import random

def apply_discounts_to_products():
    # Получаем все продукты
    products = Product.objects.all()
    total_products = len(products)
    
    # Вычисляем количество товаров для каждой категории скидок
    discount_5_percent_count = int(total_products * 0.7)
    discount_10_percent_count = int(total_products * 0.25)
    discount_15_percent_count = int(total_products * 0.05)
    
    # Получаем случайные товары для каждой категории скидок
    discount_5_percent_products = random.sample(list(products), discount_5_percent_count)
    discount_10_percent_products = random.sample(list(products.difference(discount_5_percent_products)), discount_10_percent_count)
    discount_15_percent_products = random.sample(list(products.difference(discount_5_percent_products).difference(discount_10_percent_products)), discount_15_percent_count)
    
    # Применяем скидки к товарам
    for product in discount_5_percent_products:
        product.discount = 5
        product.save()
    
    for product in discount_10_percent_products:
        product.discount = 10
        product.save()
    
    for product in discount_15_percent_products:
        product.discount = 15
        product.save()


