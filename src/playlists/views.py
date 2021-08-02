from django.http import Http404
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, get_user_model, logout
# from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, SignInForm

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from djangoflix.db.models import PublishStateOptions

from .mixins import PlaylistMixin
from .models import Playlist, MovieProxy, TVShowProxy, TVShowSeasonProxy


User = get_user_model()

def signup_view(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(username=username, email=email, password=password)
        if new_user:
            return HttpResponseRedirect('/movies')
    return render(request, 'signup.html', {'form': form})

def signin_view(request):
    form = SignInForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        new_user = authenticate(username=username, password=password)
        if new_user is not None:
            
            login(request, new_user)
            # print(user)
            # Redirect to a success page.
            # context["form"] = LoginForm()
            return HttpResponseRedirect('/shows')
    return render(request, 'signin.html', {'form': form})

def signout_view(request):
    logout(request)
    return HttpResponseRedirect("/signin")


class SearchView(PlaylistMixin, ListView):
    def get_context_data(self):
        context = super().get_context_data()
        query = self.request.GET.get("q")
        if query is not None:
            context['title'] = f"Searched for {query}"
        else:
            context['title'] = 'Perform a search'
        return context
    
    def get_queryset(self):
        query = self.request.GET.get("q") # request.GET = {}
        return Playlist.objects.all().movie_or_show().search(query=query)


class MovieListView(LoginRequiredMixin, PlaylistMixin, ListView):
    login_url = '/'
    redirect_field_name = 'redirect_to'
    queryset = MovieProxy.objects.all()
    title = "Movies"


class MovieDetailView(LoginRequiredMixin, PlaylistMixin, DetailView):
    template_name = 'playlists/movie_detail.html'
    queryset = MovieProxy.objects.all()
    

class PlaylistDetailView(LoginRequiredMixin, PlaylistMixin, DetailView):
    login_url = '/'
    redirect_field_name = 'redirect_to'
    template_name = 'playlists/playlist_detail.html'
    queryset = Playlist.objects.all()


class TVShowListView(LoginRequiredMixin, PlaylistMixin, ListView):
    login_url = '/'
    redirect_field_name = 'redirect_to'
    queryset = TVShowProxy.objects.all()
    title = "TV Shows"


class TVShowDetailView(LoginRequiredMixin, PlaylistMixin, DetailView):
    template_name = 'playlists/tvshow_detail.html'
    queryset = TVShowProxy.objects.all()


class TVShowSeasonDetailView(LoginRequiredMixin, PlaylistMixin, DetailView):
    template_name = 'playlists/season_detail.html'
    queryset = TVShowSeasonProxy.objects.all()

    def get_object(self):
        kwargs = self.kwargs
        show_slug = kwargs.get("showSlug")
        season_slug = kwargs.get("seasonSlug")
        now = timezone.now()
        try:
            obj = TVShowSeasonProxy.objects.get(
                state=PublishStateOptions.PUBLISH,
                publish_timestamp__lte=now,
                parent__slug__iexact=show_slug,
                slug__iexact=season_slug
            )
        except TVShowSeasonProxy.MultipleObjectsReturned:
            qs = TVShowSeasonProxy.objects.filter(
                parent__slug__iexact=show_slug,
                slug__iexact=season_slug
            ).published()
            obj = qs.first()
            # log this
        except:
            raise Http404
        return obj


        # qs = self.get_queryset().filter(parent__slug__iexact=show_slug, slug__iexact=season_slug)
        # if not qs.count() == 1:
        #     raise Http404
        # return qs.first()

class FeaturedPlaylistListView(PlaylistMixin, ListView):
    template_name = 'playlists/featured_list.html'
    queryset = Playlist.objects.featured_playlists()
    title = "Featured"