from django.urls import path
from . import views

urlpatterns = [
    path('api/tests/', views.PatientTestResultsView.as_view(), name='patient_tests'),
    path('api/tests/create/', views.TestResultCreateView.as_view(), name='create_test'),
    path('api/tests/stats/', views.TestStatsView.as_view(), name='test_stats'),
]

