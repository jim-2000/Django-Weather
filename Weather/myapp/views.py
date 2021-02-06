from django.shortcuts import render,get_object_or_404,redirect
import requests
from .models import City
from .forms import CityForm
# Create your views here.
 
def HOME(request):
    url ="http://api.openweathermap.org/data/2.5/weather?q={}&appid=43bc0735ce7391cf78230441a0044f22"
    
    errmsg = ""
    msgclass =""
    msg = " "
    
    if request.method=='POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            city_count = City.objects.filter(name=new_city).count()
            if city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    errmsg = "This city is not in this world "              
            else:
                errmsg = " "
        if errmsg:
            msg = errmsg
            msgclass = "is-danger"
        else:
            msg = "this city is added by database "
            msgclass = "is-primary"
                
    form = CityForm()
    
    weather =[]
    city= City.objects.all()
    for p in city:
        r = requests.get(url.format(p)).json()     
        print(r)
        city_weather = {
            'city':p,
            'tempa':r['main']['temp'],
            'description':r['weather'][0]['description'],
            'icon':r['weather'][0]['icon'],
            'code':r['id'],
            'country':r['sys']['country']
            
            }
        weather.append(city_weather)
        print(weather)
    context ={
        'weather': weather,
        'form':form,
        'msg':msg,
        'msgclass':msgclass
        }
    return render(request, 'base.html',context)

def City_delete(request, city_name):
    city = get_object_or_404(City,name=city_name)
    city.delete()
    return redirect('myapp:City_weather')