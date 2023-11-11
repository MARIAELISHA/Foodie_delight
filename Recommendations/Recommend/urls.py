from django.urls import path
from . import views
from .views import CustomLoginView,custom_login,dashboard_view,CustomRecommendFood
from .views import signUp



urlpatterns = [
    path('recommend/', views.recommend, name='recommend'),
    path('', views.index, name='index'),
    path('signUp/', signUp, name='signUp'),
    #path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('<int:food_id>/', views.detail, name='review'),
    path('watch/', views.watch, name='watch'),
    path('about/', views.about, name='about'),
  #  path('recommendation/', views.recommendation, name='Recommendation'),
    path('foodiequiz/',views.foodiequiz,name='foodie'),
    path('cocktail/',views.cocktail,name='cocktail'),
    path('cooking/', views.cooking,name='Cooking Class'),
    path('RecommendForm/',views.RecommendForm,name='RecommendForm'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('login/', custom_login, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('profile/',views.profile,name='profile'),
    path('recommend/Recommend_result/',views.recommend_result,name='recommend_result')
    #path('recommendation/', views.recommend, name='recommend'),
   # path('recommending/',views.recommend_food,name='recommend_food'),

]