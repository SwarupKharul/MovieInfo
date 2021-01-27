from django.shortcuts import render
import requests

# Create your views here.


def home(request):
    url = "https://api.themoviedb.org/3/movie/popular?api_key=de8f28fe9542059df82d3faa0485ce94"
    response = requests.request("GET", url).json()
    response = response["results"]
    unwanted = ['genre_ids', 'backdrop_path',
                'title', 'adult', 'vote_count']
    for key in unwanted:
        for result in response:
            del result[key]
            if 'release_date' in result:
                st = result['release_date']
                st = st[0:4]
                result['release_date'] = st

    image = "http://image.tmdb.org/t/p/w185/"
    return render(request, "home.html", {"response": response, 'image_url': image})


def search(request):
    find = request.GET.get('search')
    url = "https://api.themoviedb.org/3/search/movie?api_key=de8f28fe9542059df82d3faa0485ce94&language=en-US&query=" + find
    result = requests.request(
        "GET", url).json()
    results = result["results"]
    unwanted = ['genre_ids', 'backdrop_path',
                'title', 'adult', 'vote_count']
    for key in unwanted:
        for result in results:
            del result[key]
            if 'release_date' in result:
                st = result['release_date']
                st = st[0:4]
                result['release_date'] = st

    image = "http://image.tmdb.org/t/p/w185/"

    return render(request, "search.html", {'image_url': image, 'results': results,'find':find})


def details(request, title, overview, rating, image, id):
    img = "http://image.tmdb.org/t/p/w185/"
    image = image.strip()
    print(image)
    details = {"title": title, "overview": overview,
               "rating": rating, "image_url": image, 'id': id}

    url = "https://api.themoviedb.org/3/movie/{{id}}/similar?api_key=de8f28fe9542059df82d3faa0485ce94"
    response = requests.request("GET", url).json()

    return render(request, "details.html", {"details": details, 'image_url': img, 'r': response})
