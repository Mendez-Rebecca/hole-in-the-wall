from django.shortcuts import render, redirect, reverse
from .models import Restaurant, Day
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def restaurants_index(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/index.html', {
        'restaurants': restaurants
    })

def restaurants_detail(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return render(request, 'restaurants/detail.html', {
        'restaurant': restaurant
    })

class RestaurantCreate(LoginRequiredMixin, CreateView):
    model = Restaurant
    fields = ['name', 'address', 'city', 'state', 'zip_code', 'cuisine', 'dine_in', 'take_out', 'delivery', 'drive_thru']

    def form_valid(self, form):
        # Assign the logged-in user to the restaurant
        form.instance.user = self.request.user
        return super().form_valid(form)

class RestaurantUpdate(UpdateView):
    model = Restaurant
    fields = ['dine_in', 'take_out', 'delivery', 'drive_thru']

class RestaurantDelete(DeleteView):
    model = Restaurant
    success_url = '/restaurants'

class DayCreate(CreateView):
    model = Day
    fields = ['opening_time', 'closing_time']

class DayDetail(DetailView):
    model = Day

class DayUpdate(UpdateView):
    model = Day
    fields = ['opening_time', 'closing_time']

class DayDelete(DeleteView):
    model = Day

    def get_success_url(self):
        pk = self.kwargs['pk']
        restaurant_id = Day.objects.filter(pk = pk).first().restaurant_id
        return reverse('detail', restaurant_id = restaurant_id)

def assoc_day(request, restaurant_id, day_id):
    Restaurant.objects.get(id=restaurant_id).days.add(day_id)
    return redirect('detail', restaurant_id=restaurant_id)

def unassoc_day(request, restaurant_id, day_id):
    Restaurant.objects.get(id=restaurant_id).days.remove(day_id)
    return redirect('detail', restaurant_id=restaurant_id)

def add_review(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.restaurant_id = restaurant_id
        new_review.save()
    else:
        form = ReviewForm()

    return render(request, 'restaurants/detail.html', {
        'restaurant': restaurant,
        'review_form': form,
    })

# @login_required
# def reviews_index(request):
#   reviews = Review.objects.filter(user=request.user)
#   # You could also retrieve the logged in user's reviews
#   return render(request, 'reviews/index.html', { 'reviews': reviews })
