from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from .forms import ProductForm
from django.db.models import Q
from .utils import is_valid_ticker
from .models import Product, Historical
from django.views.decorators.csrf import csrf_exempt


def product_list(request):
    """
    Handles the display of the product list with optional search and pagination.

    Args:
        request (HttpRequest): The request object containing HTTP metadata.

    Returns:
        HttpResponse: Rendered HTML page with the list of products and pagination details.
    """
    search_query = request.GET.get('query', '')

    # Filter products based on search query if it exists, otherwise fetch all products
    if search_query:
        products = Product.objects.filter(Q(name__icontains=search_query) | Q(ticker__icontains=search_query)).order_by(
            'id')
    else:
        products = Product.objects.all().order_by('id')

    # Paginate the product list
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the product list page with pagination and search details
    return render(request, 'products_app/product_list.html', {
        'page_obj': page_obj,
        'total_products': products.count(),
        'search_query': search_query
    })


def product_update(request, pk):
    """
    Handles the updating of a product.

    Args:
        request (HttpRequest): The request object containing HTTP metadata.
        pk (int): Primary key of the product to be updated.

    Returns:
        JsonResponse: JSON response with updated product details on success.
        HttpResponseBadRequest: Bad request response with form errors on failure.
        HttpResponse: Rendered HTML form for updating the product on GET request.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            return JsonResponse({'id': product.id, 'ticker': product.ticker, 'name': product.name})
        else:
            return HttpResponseBadRequest(form.errors.as_json())
    else:
        form = ProductForm(instance=product)
        return render(request, 'products_app/product_update.html', {'form': form, 'product': product})


def product_create(request):
    """
    Handles the creation of a new product.

    Args:
        request (HttpRequest): The request object containing HTTP metadata.

    Returns:
        JsonResponse: JSON response with created product details on success.
        HttpResponseBadRequest: Bad request response with error message on failure.
    """
    ticker = request.POST.get('ticker')

    if not ticker:
        return HttpResponseBadRequest("Ticker is required")

    ticker = ticker.upper()

    if not is_valid_ticker(ticker):
        return HttpResponseBadRequest("Invalid ticker")

    request.POST = request.POST.copy()
    request.POST['ticker'] = ticker

    form = ProductForm(request.POST)
    if form.is_valid():
        product = form.save()
        return JsonResponse({'id': product.id, 'ticker': product.ticker, 'name': product.name})
    else:
        return HttpResponseBadRequest(form.errors.as_json())


def product_delete(request, pk):
    """
    Handles the deletion of a product.

    Args:
        request (HttpRequest): The request object containing HTTP metadata.
        pk (int): Primary key of the product to be deleted.

    Returns:
        JsonResponse: JSON response confirming the deletion on success.
        HttpResponseBadRequest: Bad request response if the request method is invalid.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return JsonResponse({'id': pk})

    return HttpResponseBadRequest("Invalid request method.")


def home(request):
    """
    Renders the home page.

    Args:
        request (HttpRequest): The request object containing HTTP metadata.

    Returns:
        HttpResponse: Rendered HTML home page.
    """
    return render(request, 'products_app/home.html')


def get_historical_data(request, product_id):
    """
    Retrieves historical data for a specific product.

    Args:
        request (HttpRequest): The request object containing HTTP metadata.
        product_id (int): The ID of the product to retrieve historical data for.

    Returns:
        JsonResponse: JSON response containing historical data.
    """
    data = list(Historical.objects.filter(product_id=product_id).values('timestamp', 'open', 'high', 'low', 'close'))
    return JsonResponse(data, safe=False)


def price_history(request):
    """
    Renders the price history page with all products.

    Args:
        request (HttpRequest): The request object containing HTTP metadata.

    Returns:
        HttpResponse: Rendered HTML page with product price history.
    """
    products = Product.objects.all()
    return render(request, 'products_app/price_history.html', {
        'products': products
    })



@csrf_exempt
def product_update_name(request):
    if request.method == 'POST':
        ticker = request.POST.get('ticker')
        new_name = request.POST.get('name')

        if not ticker or not new_name:
            return HttpResponseBadRequest("Ticker and new name must be provided")

        try:
            product = Product.objects.get(ticker=ticker.upper())
            product.name = new_name
            product.save()
            return JsonResponse({'message': 'Product name updated successfully', 'id': product.id, 'ticker': product.ticker, 'name': product.name})
        except Product.DoesNotExist:
            return HttpResponseBadRequest("Product not found")

    return HttpResponseBadRequest("Invalid request method")
