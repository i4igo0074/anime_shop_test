from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Country, ProductReview, Favorite, Collection
from django.contrib.auth.decorators import login_required



def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.user.is_authenticated:
        # Проверка, отзыв оставлен пользователем или нет
        user_review = ProductReview.objects.filter(product=product, author=request.user).first()
    else:
        user_review = 0
            
    if request.method == 'POST':
        stars = request.POST.get('stars', 1)
        ProductReview.objects.update_or_create(
            product=product,
            author=request.user,
            defaults={'rating': stars}
        )
        return redirect('product_detail', product_id=product_id)
    
    product_in_favorites = Favorite.objects.filter(user=request.user, product=product).exists()
    context = {
        'product': product,
        'user_review': user_review,
        'product_in_favorites': product_in_favorites
    }
    return render(request, 'product_detail.html', context)



def catalog(request):
    products = Product.objects.all()  # Получаем все продукты

    # Получаем все категории и страны для фильтрации
    categories = Category.objects.all()
    countries = Country.objects.all()

    # Получаем параметры фильтра из GET-запроса
    selected_category = request.GET.get('category')
    selected_country = request.GET.get('country')

    # Применяем фильтрацию, если выбраны категория или страна
    if selected_category:
        products = products.filter(category__slug=selected_category)
    if selected_country:
        products = products.filter(country__slug=selected_country)

    context = {
        'products': products,  # Все продукты (для отладки)
        'filtered_products': products,  # Отфильтрованные продукты
        'categories': categories,
        'countries': countries,
        'selected_category': selected_category,
        'selected_country': selected_country,
        'cart_count': 0,  # Замените на реальный подсчет количества товаров в корзине
    }

    return render(request, 'catalog.html', context)




@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True

    return redirect('product_detail', product_id=product_id)
    # return JsonResponse({'is_favorite': is_favorite})

def favorites(request):
    products = Product.objects.filter(favorites__user=request.user).all()
    context = {
        'products': products,
    }
    return render(request, 'favorites.html', context)

def collection(request):
    collections = Collection.objects.all()

    context = {
        'collections': collections,
    }
    return render(request, 'collection.html', context)

def collection_detail(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    products = collection.products.all()

    context = {
        'collection': collection,
        'products': products,
    }
    return render(request, 'collection_detail.html', context)