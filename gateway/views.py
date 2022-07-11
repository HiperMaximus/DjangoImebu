from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache
from .models import EmpresaGeneralPerfil, PersonaGeneralPerfil, User
from django.contrib.auth import authenticate, login, logout
from .forms import registroEmpresaForm, registroPersonaForm, userForm, registroDocumentoEmpresaForm
from empleo_joven.models import ConvocatoriaEmpleoJoven

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('gateway:mainDashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,'Se ha producido un error')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            if qs:=EmpresaGeneralPerfil.objects.filter(user__email=email):
                roleUser='empresaGeneral'
                nombre = qs.values('nombreEmpresa')[0]['nombreEmpresa']
            elif qs:=PersonaGeneralPerfil.objects.filter(user__email=email):
                roleUser='personaGeneral'
                nombre = qs.values('nombres')[0]['nombres'].split(' ')[0]
            else:
                roleUser='noAsignado'
            login(request,user)
            request.session['roleUser'] = roleUser
            request.session['nombre']=nombre
            
            if roleUser!='noAsignado':
                return redirect('gateway:mainDashboard')

        else:
            messages.error(request,'El usuario o la contraseña no existen')
    context = {'page':page}
    return render(request,'gateway/login_register.html',context)

@login_required(login_url='gateway:login')
def logoutUser(request):
    logout(request)
    return redirect('gateway:login')

def registerPageEmpresa(request):
    page='registerEmpresa'
    if request.user.is_authenticated:
        return redirect('gateway:mainDashboard')
    formUser = userForm()
    form = registroEmpresaForm()
    formDocument = registroDocumentoEmpresaForm()
    if request.method == 'POST':
        form = registroEmpresaForm(request.POST)
        formUser = userForm(request.POST)
        formDocument = registroDocumentoEmpresaForm(request.POST,request.FILES)
        if form.is_valid() and formUser.is_valid() and formDocument.is_valid():
            user = formUser.save()
            profile=form.save(commit=False)
            profile.user = user
            profile.save()
            request.FILES['documento'].name = 'RUT.pdf'
            formDocument = registroDocumentoEmpresaForm(request.POST,request.FILES)
            documentoRut = formDocument.save(commit=False)
            documentoRut.empresa = profile
            documentoRut.nombreDocumento = 'RUT.pdf'
            documentoRut.save()
            return redirect('gateway:login')
        else:
            messages.error(request, 'Ocurrio un error inesperado, intentelo de nuevo en un momento')
    context = {'form':form,'formUser':formUser,'formDocument':formDocument,'page':page}
    return render(request, 'gateway/login_register.html',context)

def registerPagePersona(request):
    if request.user.is_authenticated:
        return redirect('gateway:mainDashboard')
    formUser = userForm()
    form = registroPersonaForm()
    if request.method == 'POST':
        form = registroPersonaForm(request.POST)
        formUser = userForm(request.POST)
        if form.is_valid() and formUser.is_valid():
            user = formUser.save()
            profile=form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('gateway:login')
        else:
            messages.error(request, 'Ocurrio un error inesperado, intentelo de nuevo en un momento')
    context = {'form':form,'formUser':formUser}
    return render(request, 'gateway/login_register.html',context)

#@login_required(login_url='gateway:login')
def home(request):
    if request.user.is_authenticated:
        return redirect('gateway:mainDashboard')
    return render(request, 'gateway/home.html')
    
@login_required(login_url='gateway:login')
def mainDashboard(request):
    periodo = ConvocatoriaEmpleoJoven.objects.filter(activo=True)
    context = {'periodo':periodo}
    return render(request, 'gateway/mainDashboard.html',context)