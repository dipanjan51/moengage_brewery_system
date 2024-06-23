import requests
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review

from django.db.models import Avg


# Create your views here.
@login_required(login_url='login')
def home_view(request):
    if request.user.is_authenticated:
        context = {'username': request.user.username, 'results': 'blank'}
        query = request.GET.get('query')
        search_type = request.GET.get('type')
        if query and search_type:
            try:
                response = requests.get(f'https://api.openbrewerydb.org/v1/breweries?{search_type}={query}&per_page=3')
            
                if response.status_code == 200:
                    results = response.json()

                    for brewery_data in results:
                        reviews = Review.objects.filter(brewery_id=brewery_data['id'])
                        if reviews.exists():
                            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
                            if average_rating is not None:
                                average_rating = round(average_rating, 1)
                        else:
                            average_rating = "No rating yet"
                        brewery_data['average_rating'] = average_rating
                else:
                    messages.error(request, "Error fetching data. Try Again")
            
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Request failed: {e}")

            context = {'username': request.user.username,
                   'results': results}

    return render (request,'breweries/home.html', context)


@login_required(login_url='login')
def search_view(request):
    print("helo")
    query = request.GET.get('query')
    search_type = request.GET.get('type')

    if query and search_type:
        try:
            response = requests.get(f'https://api.openbrewerydb.org/v1/breweries?{search_type}={query}&per_page=3')
        
            if response.status_code == 200:
                results = response.json()
            else:
                messages.error(request, "Error fetching data. Try Again")
        
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Request failed: {e}")
    
    context = {'username': request.user.username, 
               'results': results}

    return render(request, 'breweries/home.html', context)


@login_required(login_url='login')
def brewery_details(request, id):
    url = f"https://api.openbrewerydb.org/v1/breweries/{id}"
    response = requests.get(url)
    result = response.json()

    if request.method == "POST":
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        if rating and review:
            try:
                rating = int(rating)
                if 1 <= rating <= 5:
                    review = Review.objects.create(
                        brewery_id=id,
                        user=request.user,
                        rating=rating,
                        review=review)
                    return redirect('brewery_details', id=id)
                else:
                    error_message = "Rating must be between 1 and 5"
            except ValueError:
                error_message = "Rating must be between 1 and 5"
        else:
            error_message = "All fields are required"
    else:
        error_message = None

    reviews = Review.objects.filter(brewery_id=id).order_by('-created_at')


    context = {'result': result,
               'reviews': reviews,
               'error_message': error_message,
               }
    # pprint(context)
    return render(request, 'breweries/brewery_details.html', context)