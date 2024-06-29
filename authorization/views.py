from django.shortcuts import render, redirect
from .forms import CustomerUserCreationForm, CustomerAuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout

# Create your views here.
def home(request): 
    context = {
        'user': request.user, 
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomerUserCreationForm()
    return render(request, 'register.html', {'form': form})    


class CustomerLoginView(LoginView):
    authentication_form = CustomerAuthenticationForm
    template_name = 'login.html'
    redirect_field_name = 'home'
    redirect_authenticated_user = True

def logout_view(request):
    logout(request)
    return redirect('login')