from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("random/", views.randomPage, name="random"),
    path("newpage/", views.createNewPage, name="newPage"),
    path("editpage/<str:title>", views.editPage, name="editPage")
]
