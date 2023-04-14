from django.urls import path
from . import views 
from .views import (
                    CategoryListView, 
                    PictureListView, 
                    PictureDetailView, 
                    CategoryFolderCreateView,
                    CategoryFolderUpdateView,
                    CategoryFolderSoftDeleteView,
                    PictureCreateView,
                    PictureUpdateView,
                    PictureSoftDeleteView,
                    SoftDeletedCategoryListView,
                    SoftDeletedPictureListView,
                    SoftDeletedPictureDetailView,
                    PictureRestoreView,
                    CategoryFolderRestoreView,
                    PicturePermanentDeleteView,
                    CategoryFolderPermanentDeleteView
                    )

urlpatterns = [
  
   path('', CategoryListView.as_view(), name='pics-home'),
   path('bin/', SoftDeletedCategoryListView.as_view(), name='bin-pics'),

   path('folder/picture/<str:name>/', PictureListView.as_view(), name='category-pics'),
   path('bin/picture/<str:name>/', SoftDeletedPictureListView.as_view(), name='bin-category'),

   
   path('folder/picture/<int:pk>/detail/', PictureDetailView.as_view(), name='detail-pics'),
   path('bin/picture/<int:pk>/detail/', SoftDeletedPictureDetailView.as_view(), name='bin-detail'),


   path('folder/new', CategoryFolderCreateView.as_view(), name='new-folder'),
   path('folder/<str:name>/update/', CategoryFolderUpdateView.as_view(), name='update-folder'),
   path('folder/<str:name>/delete/', CategoryFolderSoftDeleteView.as_view(), name='delete-folder'),
   path('folder/<str:name>/delete/permanent/', CategoryFolderPermanentDeleteView.as_view(), name='perm-delete-folder'),
   path('bin/<str:name>/restore/', CategoryFolderRestoreView.as_view(), name='restore-folder'),

   
   path('folder/picture/<str:name>/new/picture/', PictureCreateView.as_view(), name='new-picture'),
   path('folder/picture/<int:pk>/update/', PictureUpdateView.as_view(), name='update-picture'),
   path('folder/picture/<int:pk>/delete/', PictureSoftDeleteView.as_view(), name='delete-picture'),
   path('folder/picture/<int:pk>/delete/permanent/', PicturePermanentDeleteView.as_view(), name='perm-delete-picture'),
   path('bin/picture/<int:pk>/restore/', PictureRestoreView.as_view(), name='restore-picture'),









   
  
]
