from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='gateway:login')
#@cache_control(no_store=True)
def empleoDashboard(request):
    return render(request, 'empleo/empleoDashboard.html')
