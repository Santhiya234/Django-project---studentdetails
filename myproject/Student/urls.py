from django.urls import path
from Student.views import StudentListView, StudentuniqueView, StudentmarksView, ExportExcelView

urlpatterns = [
    path('list/', StudentListView.as_view(), name='student-list'),
    path('<int:pk>/', StudentuniqueView.as_view(), name='student-unique'),
    path('mark/<int:id>/', StudentmarksView.as_view(), name='student-mark'),  
    path('export/', ExportExcelView.as_view(), name='export-student')
]

# from django.urls import path
# from Student.views import StudentListView, StudentuniqueView, StudentmarksView

# urlpatterns = [
#     path('list/', StudentListView.as_view(), name='student-list'),
#     path('<int:pk>/',StudentuniqueView.as_view(), name='student-unique'),
#     path('mark/<int:id>/',StudentmarksView.as_view(), name='student-mark')
# ]

