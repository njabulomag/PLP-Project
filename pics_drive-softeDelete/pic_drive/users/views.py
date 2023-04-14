from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm 
from django.views.generic.edit import FormView

class RegisterPage(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('pics-home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            username = form.cleaned_data.get('username')
            messages.info(self.request, f'Account created for {username}!')
            return redirect('login')
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('pics-home')
        return super(RegisterPage, self).get(*args, **kwargs)

# functional view for user registration
# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.info(request, f'Account created for {username}!')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})

