"""djangoflix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from playlists.views import(
    MovieListView,
    MovieDetailView,
    PlaylistDetailView,
    SearchView, 
    signup_view,
    signin_view,
    signout_view,
    TVShowListView,
    TVShowDetailView, 
    TVShowSeasonDetailView,
    FeaturedPlaylistListView,
    # register_request
)
from videos.views import(
    VideoLandingPageView,
    CreateCheckoutSessionView,
    SuccessView,
    CancelledView,
    stripe_webhook,
    StripeIntentView
)
from ratings.views import rate_object_view

urlpatterns = [
    path('', FeaturedPlaylistListView.as_view()),
    path('admin/', admin.site.urls),
    path('cancelled/', CancelledView.as_view(), name="cancelled"),
    path('success/', SuccessView.as_view(), name="success"),
    path('category/', include('categories.urls'), name="category"),
    path('config/', VideoLandingPageView.stripe_config),
    path('categories/', include('categories.urls'), name="categories"),
    path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('post/<pk>/', CreateCheckoutSessionView.as_view(), name="post"),
    path('movies/<slug:slug>/', MovieDetailView.as_view(), name="movies"),
    path('movies/', MovieListView.as_view(), name="movies"),
    path('media/<int:pk>', PlaylistDetailView.as_view(), name="media"),
    # path("register/", register_request, name="register"),
    path('search/', SearchView.as_view()),
    path('signup/', signup_view, name="signup"),
    path('signin/', signin_view, name="signin"),
    path('signout/', signout_view, name="signout"),
    path('shows/<slug:showSlug>/seasons/<slug:seasonSlug>/', TVShowSeasonDetailView.as_view()),
    path('shows/<slug:slug>/seasons/', TVShowDetailView.as_view(), name="shows"),
    path('shows/<slug:slug>/', TVShowDetailView.as_view(), name="shows"),
    path('shows/', TVShowListView.as_view(), name="shows"),
    path('stripe/', VideoLandingPageView.as_view(), name="stripe"),
    path('tags/', include('tags.urls')),
    path('webhook-stripe/', stripe_webhook, name="stripe-webhook"),
    path('object-rate/', rate_object_view)
]
