
from django.shortcuts import redirect, render
import requests
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6b26b64684e52cd1eb38d72ea7f80564'
    cities = City.objects.all()
    form = CityForm()
    weather_data = []
    
    for city in cities:
        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)
      
    if request.method == 'POST': # only true if form is submitte
        form = CityForm(request.POST) # add actual request data to form for processing
        if form.is_valid():
            data = form.cleaned_data['name']
            city_weather = requests.get(url.format(data)).json()
            if city_weather['cod'] == '404':
                return redirect('index')
            else:
                form.save() # will validate and save if validate    
                return redirect('index')
   
    context = {
        'weather_data':weather_data,
        'form' : form,
    }
    return render(request, 'weather/index.html', context) #returns the index.html template