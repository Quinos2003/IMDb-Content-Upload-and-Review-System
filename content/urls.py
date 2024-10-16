from django.urls import path
from .views import UploadCSVView, MovieListView

urlpatterns = [
    path('upload/', UploadCSVView.as_view(), name='upload_csv'),
    path('movies/', MovieListView.as_view(), name='movie_list'),
]
