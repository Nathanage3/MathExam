from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'grades', views.GradeViewSet)
router.register(r'units', views.UnitViewSet)
router.register(r'tests', views.TestViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'attempts', views.TestAttemptViewSet)

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    
    # HTML page URLs
    path('', views.home_page, name='home'),
    path('test/<int:test_id>/', views.take_test_page, name='take_test'),
    path('result/', views.test_result_page, name='test_result'),
]