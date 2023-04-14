from django.shortcuts import redirect, render, get_object_or_404, reverse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Picture, Category
from django.db.models import Q

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    ordering = ['-date_created']
    template_name = 'pics/home.html'    
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['categories'] = context['categories'].filter(Q(author=self.request.user) & 
                                                             Q(deleted_at=None))
        return context
    

class PictureListView(ListView):
    model = Picture
    context_object_name = 'pictures'
    ordering = ['-date_posted']
    template_name = 'pics/pictures_list.html'   
    
    def get_queryset(self):
        tag = get_object_or_404(Category, name=self.kwargs.get('name'))
        return Picture.objects.filter(Q(category=tag) & Q(deleted_at=None)).order_by('-date_posted') 
    
    def get_context_data(self, **kwargs):
        context = super(PictureListView, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('name')
        return context
    

# recycle bin logic ------------------------------------------
class SoftDeletedCategoryListView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    ordering = ['-date_created']
    template_name = 'pics/deleted_folder_list.html'    
    
    def get_context_data(self, **kwargs):
        context = super(SoftDeletedCategoryListView, self).get_context_data(**kwargs)
        context['categories'] = context['categories'].filter(Q(author=self.request.user) & 
                                                             ~Q(deleted_at=None))
        
        context['deleted_pictures'] = Picture.objects.filter(~Q(deleted_at=None))
        return context
    
class SoftDeletedPictureListView(ListView):
    model = Picture
    context_object_name = 'pictures'
    ordering = ['-date_posted']
    template_name = 'pics/deleted_pictures_list.html'   
    
    def get_queryset(self):
        tag = get_object_or_404(Category, name=self.kwargs.get('name'))
        return Picture.objects.filter(Q(category=tag) & ~Q(deleted_at =None)).order_by('-date_posted') 
    
    def get_context_data(self, **kwargs):
        context = super(SoftDeletedPictureListView, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('name')
        return context

class SoftDeletedPictureDetailView(DetailView):
    model = Picture
    context_object_name = 'picture'
    template_name = 'pics/deleted_picture_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(SoftDeletedPictureDetailView, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('name')
        return context
    

# ----------------------------------------------------------------
class PictureDetailView(DetailView):
    model = Picture
    context_object_name = 'picture'
    template_name = 'pics/picture_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(PictureDetailView, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('name')
        return context
class CategoryFolderCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'pics/new_folder.html'
    fields = ['name']
    success_url = '/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CategoryFolderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name']
    template_name = 'pics/new_folder.html'
    success_url = '/'

    # https://stackoverflow.com/a/62978825
    def get_object(self, queryset=None):
        return Category.objects.get(name=self.kwargs['name']) # instead of self.request.GET or self.request.POST

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        category = self.get_object()
        if self.request.user == category.author:
            return True
        return False
    
class CategoryFolderSoftDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'pics/category_confirm_delete.html'
    success_url = '/'    

    def delete(self, request, *args, **kwargs):
       """
       Call the delete() method on the fetched object and then redirect to the
       success URL.
       """
       self.object = self.get_object()
       success_url = self.get_success_url()
       self.object.soft_delete()
       return HttpResponseRedirect(success_url)

    def test_func(self):
        category = self.get_object()
        if self.request.user == category.author:
            return True
        return False
    
    # https://stackoverflow.com/a/62978825
    def get_object(self, queryset=None):
        return Category.objects.get(name=self.kwargs['name']) # instead of self.request.GET or self.request.POST

class CategoryFolderPermanentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'pics/category_confirm_delete.html'
    success_url = '/'    

    def test_func(self):
        category = self.get_object()
        if self.request.user == category.author:
            return True
        return False
    
    # https://stackoverflow.com/a/62978825
    def get_object(self, queryset=None):
        return Category.objects.get(name=self.kwargs['name']) # instead of self.request.GET or self.request.POST


class CategoryFolderRestoreView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'pics/category_confirm_restore.html'
    success_url = '/'    

    def delete(self, request, *args, **kwargs):
       """
       Call the delete() method on the fetched object and then redirect to the
       success URL.
       """
       self.object = self.get_object()
       success_url = self.get_success_url()
       self.object.restore()
       return HttpResponseRedirect(success_url)

    def test_func(self):
        category = self.get_object()
        if self.request.user == category.author:
            return True
        return False
    
    # https://stackoverflow.com/a/62978825
    def get_object(self, queryset=None):
        return Category.objects.get(name=self.kwargs['name']) # instead of self.request.GET or self.request.POST

class PictureCreateView(LoginRequiredMixin,CreateView):
    model = Picture
    template_name = 'pics/new_picture.html'
    fields = ['image']
    success_url = '/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        name = self.kwargs.get('name')
        form.instance.category = Category.objects.get(name=name)
        return super().form_valid(form)
    
    # https://stackoverflow.com/a/62978825
    def get_object(self, queryset=None):
        return Category.objects.get(name=self.kwargs['name']) # instead of self.request.GET or self.request.POST

class PictureUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
   model = Picture
   template_name = 'pics/new_picture.html'
   fields = ['image']
   success_url = '/'

   def form_valid(self, form):
       form.instance.owner = self.request.user
       name = self.kwargs.get('name')
       form.instance.category = Category.objects.get(name=name)
       return super().form_valid(form)
    
   def test_func(self):
        category = self.get_object()
        if self.request.user == category.owner:
            return True
        return False
    
class PictureSoftDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Picture
    template_name = 'pics/picture_confirm_delete.html'
    success_url = '/'    
    
    def delete(self, request, *args, **kwargs):
       """
       Call the delete() method on the fetched object and then redirect to the
       success URL.
       """
       self.object = self.get_object()
       success_url = self.get_success_url()
       self.object.soft_delete()
       return HttpResponseRedirect(success_url)

    def test_func(self):
        category = self.get_object()
        if self.request.user == category.owner:
            return True
        return False
    
class PictureRestoreView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Picture
    template_name = 'pics/picture_confirm_restore.html'
    success_url = '/'    
    
    def delete(self, request, *args, **kwargs):
       """
       Call the delete() method on the fetched object and then redirect to the
       success URL.
       """
       self.object = self.get_object()
       success_url = self.get_success_url()
       self.object.restore()
       return HttpResponseRedirect(success_url)

    def test_func(self):
        category = self.get_object()
        if self.request.user == category.owner:
            return True
        return False
    
class PicturePermanentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Picture
    template_name = 'pics/picture_confirm_delete.html'
    success_url = '/'    
    
    def test_func(self):
        category = self.get_object()
        if self.request.user == category.owner:
            return True
        return False
    
