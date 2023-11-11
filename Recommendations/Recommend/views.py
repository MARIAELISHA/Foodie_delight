from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from .forms import *
from django.http import Http404
from django.http import HttpResponse
from .models import Food
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Case, When
from django import forms
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import SignUpForm,RecommendForm


# Create your views here.

def index(request):
    food = Food.objects.all()
    query = request.GET.get('q')
    
    if query:
        food= Food.objects.filter(Q(title__icontains=query)).distinct()
        return render(request, 'home.html', {'foods': food})

    return render(request, 'home.html', {'foods': food})

def about(request):
    return render(request,'aboutus.html')


# Show details of the food
def detail(request, food_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    food = get_object_or_404(Food, id=food_id)
    food = Food.objects.get(id=food_id)
    
    temp = list(MyList.objects.all().values().filter(food_id=food_id,user=request.user))
    if temp:
        update = temp[0]['watch']
    else:
        update = False
    if request.method == "POST":

        # For my list
        if 'watch' in request.POST:
            watch_flag = request.POST['watch']
            if watch_flag == 'on':
                update = True
            else:
                update = False
            if MyList.objects.all().values().filter(food_id=food_id,user=request.user):
                MyList.objects.all().values().filter(food_id=food_id,user=request.user).update(watch=update)
            else:
                q=MyList(user=request.user,food=food,watch=update)
                q.save()
            if update:
                messages.success(request, "Food added to your list!")
            else:
                messages.success(request, "Food removed from your list!")

            
        # For rating
        else:
            rate = request.POST['rating']
            if Myrating.objects.all().values().filter(food_id=food_id,user=request.user):
                Myrating.objects.all().values().filter(food_id=food_id,user=request.user).update(rating=rate)
            else:
                q=Myrating(user=request.user,food=food,rating=rate)
                q.save()

            messages.success(request, "Rating has been submitted!")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    out = list(Myrating.objects.filter(user=request.user.id).values())

    # To display ratings in the movie detail page
    food_rating = 0
    rate_flag = False
    for each in out:
        if each['food_id'] == food_id:
            food_rating_rating = each['rating']
            rate_flag = True
            break

    context = {'food': food,'food_rating':food_rating,'rate_flag':rate_flag,'update':update}
    return render(request, 'review.html', context)


# MyList functionality
def watch(request):

    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404

    food = Food.objects.filter(mylist_watch=True,mylist_user=request.user)
    query = request.GET.get('q')

    if query:
        food = Food.objects.filter(Q(title__icontains=query)).distinct()
        return render(request, 'watch.html', {'food': food})

    return render(request, 'watch.html', {'food': food})


# To get similar food based on user rating
def get_similar(food_name,rating,corrMatrix):
    similar_ratings = corrMatrix[food_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings

class RecommendForm(forms.Form):
    pass

class CustomRecommendFood(RecommendForm):
    template='recommend.html'

# Recommendation Algorithm
# Recommendation Algorithm
    # Function to recommend based on user input


def recommend(request):
    return render(request,'recommend.html')

def recommend_result(request):
    new_food_item = request.POST.get('new_food_item')
    if new_food_item =='':
        return redirect('http://127.0.0.1:8000')
    else:
        data = pd.read_csv(r"C:\Users\Modern\Project\Recommendations\Food_preprocessed_1.csv", encoding='latin-1')
        label_encoder = LabelEncoder()
        data['Tokens'] = label_encoder.fit_transform(data['Tokens'])
        knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)  # You can adjust the number of neighbors (k) as neede
        X = data[['Tokens', 'Ratings']].values
        knn.fit(X)
    def recommend_food(new_food):
        try:
            # Transform the new food item into the same feature space
            new_food_encoded = label_encoder.transform([new_food])

            # For user rating, you can use a default value (e.g., the average rating from the dataset)
            user_rating = data['Ratings'].mean()

            # Find k-nearest neighbors based on both the new food item and the default user rating
            input_data = [[new_food_encoded[0], user_rating]]  # Create a list of lists
            distances, indices = knn.kneighbors(input_data)

            # Generate a recommendation list including restaurant information
            recommendation_list = []
            for i in indices[0]:
                recommended_food = label_encoder.inverse_transform([data.at[i, 'Tokens']])  # Change 'Labels' to 'Tokens'
                restaurant_id = data.at[i, 'Buisness_id']  # Use square brackets, not parentheses
                recommendation_list.append((recommended_food[0], restaurant_id))

            return recommendation_list

        except ValueError as e:
            # Handle the case where the label is not in the LabelEncoder's vocabulary
            print(f"Label not found: {e}")
            return []

    recommendations = recommend_food(new_food_item)
    #rows_ = recommendations.to_dict(orient='records')
    df = pd.DataFrame(recommendations,columns=['Food','Restaurant'])
    rows_= df.to_dict(orient='records')
    if df.shape[0]>0:
        print("-------------------Recommended food items with associated restaurants on the basis of Food and ratings:------------------------------")
        for i in range(df.shape[0]):
            print(f"Since you're looking for {new_food_item} you can look for :", df['Food'][i], " from this Restaurant:", df['Restaurant'][i])
    else:
        print("No recommendations available for this food item.")

    return render(request,'recommendation.html',{'rows':rows}) 


#Foodie Quiz
def foodiequiz(request):
    return render(request, 'foodiequiz.html')

def cocktail(request):
    return render(request, 'cocktail.html')

def cooking(request):
    return render(request, 'cooking.html')



# Register user
def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def profile(request):
    return render(request, 'profile.html') 

class CustomLoginView(LoginView):
    template_name = 'login.html'

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')  # Redirect to a dashboard or another page after successful login
                else:
                    return render(request, 'login.html', {'error_message': 'Your account is disabled'})
            else:
                return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# Login User
def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("index")
            else:
                return render(request, 'login.html', {'error_message': 'Your account disable'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid Login'})

    return render(request, 'login.html')


# Logout user
def Logout(request):
    logout(request)
    return redirect("login")

from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'dashboard.html', {'username': request.session.get('username', None)})


