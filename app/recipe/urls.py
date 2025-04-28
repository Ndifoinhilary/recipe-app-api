from  rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import  views
app_name = 'recipe'

router = DefaultRouter()

router.register('recipe', views.RecipeViewSet, basename='recipe')
router.register('tag', views.TagViewSet, basename='tag')
urlpatterns = [
    path('', include(router.urls))
]


urlpatterns = [
    path('', include(router.urls))
]