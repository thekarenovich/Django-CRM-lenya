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

    # magazine
    path('get_magazines', views.get_magazines, name='get_magazines'),
    path('add_magazine', views.add_magazine, name='add_magazine'),

    # container
    path('container_numbers/<str:container_number>', views.container_number, name='container_number'),
    path('container_numbers/<str:container_number>/storage_location', views.storage_location, name='storage_location'),
    path('container_numbers/<str:container_number>/storage_location/storage_chamber', views.storage_chamber,
         name='storage_chamber'),

    # types
    path('types/', views.types, name='types'),
    path('types/other_solution_type/', views.other_solution_type, name='other_solution_type'),
    path('types/buffer_solution_type/', views.buffer_solution_type, name='buffer_solution_type'),
    path('types/ferment_type/', views.ferment_type, name='ferment_type'),
    path('types/primer_type/', views.primer_type, name='primer_type'),
    path('types/restriction_enzyme_type/', views.restriction_enzyme_type, name='restriction_enzyme_type'),
    path('types/substance_solution_type/', views.substance_solution_type, name='substance_solution_type'),
    path('types/dry_substance_type/', views.dry_substance_type, name='dry_substance_type'),

    # add to db
    path('add_storage_chamber/', views.add_storage_chamber),
    path('add_storage_location/', views.add_storage_location),
    path('add_container_type/', views.add_container_type),
    path('add_container/', views.add_container),
    path('add_reagent_type/', views.add_reagent_type),
    path('add_reagents/', views.add_reagents),
    path('add_other_solutions/', views.add_other_solutions),
    path('add_buffer_solutions/', views.add_buffer_solutions),
    path('add_ferment_types/', views.add_ferment_types),
    path('add_dry_substance_types/', views.add_dry_substance_types),
    path('add_primer_types/', views.add_primer_types),
    path('add_restriction_enzyme_types/', views.add_restriction_enzyme_types),
    path('add_substance_solution_types/', views.add_substance_solution_types),
]
