from django.shortcuts import render,get_object_or_404, redirect
from .models import fase1,fase2 
from django.contrib import messages
#from .forms import registroDocumentoEmpresaJovenForm, registroEmpleadosEmpresaForm
from django.views.decorators.cache import cache_control
from django.db.models import Q
from .forms import registroPersonaFase1Form, registroPersonaFase2Form

@cache_control(no_store=True)
def bancaPostulacionFase1(request):
    formFase1 = registroPersonaFase1Form()
    if request.method == 'POST':
        formPostuladoFase1 = registroPersonaFase1Form(request.POST)
        if formPostuladoFase1.is_valid():
            PostuladoFase1=formPostuladoFase1.save()
            formFase2 = registroPersonaFase2Form()
            context={'idFase1':PostuladoFase1.id, 'formFase2':formFase2}
            return render(request, 'banca_ciudadana/registroFase2.html',context)
        else:
            context={"formFase1":formPostuladoFase1}
            return render(request,'banca_ciudadana/registroFase1.html',context)
    context={'formFase1':formFase1}
    return render(request,'banca_ciudadana/registroFase1.html',context)

@cache_control(no_store=True)
def bancaPostulacionFase2(request):
    if request.method == 'POST':
        formPostuladoFase2 = registroPersonaFase2Form(request.POST)
        if formPostuladoFase2.is_valid():
            if (idFase1:= fase1.objects.get(id=request.POST['idFase1'])) and not (fase2.objects.filter(persona=request.POST['idFase1'])):
                form2=formPostuladoFase2.save(commit=False)
                form2.persona=idFase1
                form2.save()
                messages.success(request, 'Gracias por postularte, te contactaremos pronto')
                return redirect('gateway:home')
            else:
                context={'idFase1':request.POST['idFase1'],"formFase2":formPostuladoFase2}
                render(request, 'banca_ciudadana/registroFase2.html',context)
        else:
            #for error in formPostuladoFase2.errors:
            #    messages.error(request, 'Ocurrio un error inesperado en el campo: ' +str(error))
            context = {'formFase2':formPostuladoFase2,'idFase1':request.POST['idFase1']}
            return render(request,'banca_ciudadana/registroFase2.html',context)
    return redirect('gateway:login')
