from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('export_excel/', views.ExportExcelView.as_view(), name='export_excel'),

    # user
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    # reagent
    path('export_pdf/<int:pk>/', views.export_reagent_to_pdf, name='export_reagent_to_pdf'),
    path('reagent/<int:pk>', views.customer_reagent, name='reagent'),
    path('delete_reagent/<int:pk>', views.delete_reagent, name='delete_reagent'),
    path('add_reagent/', views.add_reagent, name='add_reagent'),
    path('update_reagent/<int:pk>', views.update_reagent, name='update_reagent'),

    # container
    path('container_numbers/<int:pk>', views.container_number, name='container_number'),
    path('container_numbers/<int:pk>/storage_location', views.storage_location, name='storage_location'),
    path('container_numbers/<int:pk>/storage_location/storage_chamber', views.storage_chamber, name='storage_chamber'),

    # types
    path('types/', views.types, name='types'),
    path('types/other_solution_type/', views.other_solution_type, name='other_solution_type'),
    path('types/buffer_solution_type/', views.buffer_solution_type, name='buffer_solution_type'),
    path('types/ferment_type/', views.ferment_type, name='ferment_type'),
    path('types/primer_type/', views.primer_type, name='primer_type'),
    path('types/restriction_enzyme_type/', views.restriction_enzyme_type, name='restriction_enzyme_type'),
    path('types/substance_solution_type/', views.substance_solution_type, name='substance_solution_type'),
    path('types/dry_substance_type/', views.dry_substance_type, name='dry_substance_type'),

]
