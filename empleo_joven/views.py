from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from gateway.models import DocumentosEmpresa, EmpresaGeneralPerfil
from .models import DocumentosEmpresaJoven, ConvocatoriaEmpleoJoven, infoEmpleadosEmpresa 
from django.contrib import messages
from gateway.forms import registroDocumentoEmpresaForm
from .forms import registroDocumentoEmpresaJovenForm, registroEmpleadosEmpresaForm
from django.views.decorators.cache import cache_control
from django.db.models import Q

# Create your views here.
@login_required(login_url='gateway:login')
def empleoJovenDashboard(request):
    return render(request, 'empleo_joven/empleoJovenDashboard.html')

@cache_control(no_store=True)
@login_required(login_url='gateway:login')
def empleoJovenRegistroEmpresa(request):
    formDocument = registroDocumentoEmpresaForm()
    formEmpresaJovenDocument = registroDocumentoEmpresaJovenForm()
    periodo = ConvocatoriaEmpleoJoven.objects.filter(activo=True)[0]
    periodoFront = ConvocatoriaEmpleoJoven.objects.filter(activo=True).values()[0]
    if rut:= DocumentosEmpresa.objects.filter(empresa_id=str(request.user.pk),documento__contains='user_'+str(request.user.pk)+'/RUT.pdf',nombreDocumento='RUT.pdf'):
        rut=rut.values()[0]
    else:
        rut=None
    if registroMercantil:= DocumentosEmpresa.objects.filter(empresa_id=str(request.user.pk),documento__contains='user_'+str(request.user.pk)+'/RegistroMercantil.pdf',nombreDocumento='RegistroMercantil.pdf'):
        registroMercantil=registroMercantil.values()[0]
    else:
        registroMercantil=None
    if certificacionBancaria:= DocumentosEmpresa.objects.filter(empresa_id=str(request.user.pk),documento__contains='user_'+str(request.user.pk)+'/CertificacionBancaria.pdf',nombreDocumento='CertificacionBancaria.pdf'):
        certificacionBancaria=certificacionBancaria.values()[0]
    else:
        certificacionBancaria=None
    if industriaComercio:= DocumentosEmpresaJoven.objects.filter(
        Q(documento__contains=f"user_{str(request.user.pk)}/")&
        Q(documento__contains="empresa/IndustriaComercio.pdf"),
        empresa_id=str(request.user.pk),nombreDocumento='IndustriaComercio.pdf').order_by('-updated'):
            industriaComercio=industriaComercio.values()[0]
    else:
        industriaComercio=None
    if certificacionPagosNomina:= DocumentosEmpresaJoven.objects.filter(
        Q(empresa_id=str(request.user.pk)) &
        Q(documento__contains=f"user_{str(request.user.pk)}/")&
        Q(documento__contains="empresa/CertificacionPagosNomina.pdf") &
        Q(nombreDocumento='CertificacionPagosNomina.pdf')).order_by('-updated'):
            certificacionPagosNomina=certificacionPagosNomina.values()[0]
    else:
        certificacionPagosNomina=None
    if declaracionJuramentada:= DocumentosEmpresaJoven.objects.filter(
        Q(documento__contains=f"user_{str(request.user.pk)}/")&
        Q(documento__contains="empresa/DeclaracionJuramentada.pdf"),
        empresa_id=str(request.user.pk),
        nombreDocumento='DeclaracionJuramentada.pdf').order_by('-updated'):
            declaracionJuramentada=declaracionJuramentada.values()[0]
    else:
        declaracionJuramentada=None
    context = {'formDocument':formDocument,'formEmpresaJovenDocument':formEmpresaJovenDocument,'periodoFront':periodoFront,'rut':rut,'registroMercantil':registroMercantil,'certificacionBancaria':certificacionBancaria,'industriaComercio':industriaComercio,'certificacionPagosNomina':certificacionPagosNomina,'declaracionJuramentada':declaracionJuramentada}
    return render(request, 'empleo_joven/registroDocumentosEmpresa.html', context)

@cache_control(no_store=True)
@login_required(login_url='gateway:login')
def empleoJovenAddDocumentGeneral(request, nombre_documento):
    formDocument = registroDocumentoEmpresaForm()
    if request.method == 'POST':
        formDocument = registroDocumentoEmpresaForm(request.POST,request.FILES)
        if formDocument.is_valid():
            profile = EmpresaGeneralPerfil.objects.filter(user_id=str(request.user.pk))[0]
            request.FILES['documento'].name = nombre_documento+'.pdf'
            formDocument = registroDocumentoEmpresaForm(request.POST,request.FILES)
            documento = formDocument.save(commit=False)
            documento.empresa = profile
            documento.nombreDocumento = nombre_documento+'.pdf'
            documento.save()
            return redirect('empleoJoven:empleoJovenRegistroEmpresa')
        else:
            messages.error(request, 'Ocurrio un error inesperado, intentelo de nuevo en un momento')
            return redirect('empleoJoven:empleoJovenRegistroEmpresa')

@cache_control(no_store=True)
@login_required(login_url='gateway:login')
def empleoJovenAddDocumentJoven(request, nombre_documento):
    formEmpresaJovenDocument = registroDocumentoEmpresaJovenForm()
    if request.method == 'POST':
        formEmpresaJovenDocument = registroDocumentoEmpresaJovenForm(request.POST,request.FILES)
        if formEmpresaJovenDocument.is_valid():
            profile = EmpresaGeneralPerfil.objects.filter(user_id=str(request.user.pk))[0]
            periodo = ConvocatoriaEmpleoJoven.objects.filter(activo=True)[0]
            request.FILES['documento'].name = nombre_documento+'.pdf'
            formEmpresaJovenDocument = registroDocumentoEmpresaJovenForm(request.POST,request.FILES)
            documento = formEmpresaJovenDocument.save(commit=False)
            documento.empresa = profile
            documento.periodo = periodo
            documento.nombreDocumento = nombre_documento+'.pdf'
            documento.save()
            return redirect('empleoJoven:empleoJovenRegistroEmpresa')
        else:
            messages.error(request, 'Ocurrio un error inesperado, intentelo de nuevo en un momento')
            return redirect('empleoJoven:empleoJovenRegistroEmpresa')

@cache_control(no_store=True)
@login_required(login_url='gateway:login')
def empleoJovenUpdateDocumentGeneral(request,pk,nombre_documento):
    formDocument = DocumentosEmpresa.objects.get(id=pk)
    formUpdated = registroDocumentoEmpresaForm(instance=formDocument)
    if request.method == 'POST':
        formUpdated = registroDocumentoEmpresaForm(request.POST,request.FILES, instance=formDocument)
        if formUpdated.is_valid():
            request.FILES['documento'].name = nombre_documento+'.pdf'
            formUpdated = registroDocumentoEmpresaForm(request.POST,request.FILES, instance=formDocument)
            formUpdated.save()
            return redirect('empleoJoven:empleoJovenRegistroEmpresa')
    return render(request, 'empleo_joven/registroDocumentosEmpresa.html')

@cache_control(no_store=True)
@login_required(login_url='gateway:login')
def empleoJovenUpdateDocumentJoven(request,pk,nombre_documento):
    formDocument = DocumentosEmpresaJoven.objects.get(id=pk)
    formUpdated = registroDocumentoEmpresaJovenForm(instance=formDocument)
    if request.method == 'POST':
        formUpdated = registroDocumentoEmpresaJovenForm(request.POST,request.FILES, instance=formDocument)
        if formUpdated.is_valid():
            request.FILES['documento'].name = nombre_documento+'.pdf'
            formUpdated = registroDocumentoEmpresaJovenForm(request.POST,request.FILES, instance=formDocument)
            formUpdated.save()
            return redirect('empleoJoven:empleoJovenRegistroEmpresa')
    return render(request, 'empleo_joven/registroDocumentosEmpresa.html')

@cache_control(no_store=True)
@login_required(login_url='gateway:login')
def empleoJovenDeleteDocumentJoven(request,pk):
    documento=DocumentosEmpresaJoven.objects.filter(id=pk,empresa_id=str(request.user.pk))
    if documento:
        if request.method == 'POST':
                documento.delete()
                return redirect('empleoJoven:empleoJovenRegistroEmpresa')
    else:
        messages.error(request, 'Ocurrio un error, por favor intentelo de nuevo en unos momentos')
        return render(request, 'empleo_joven/registroDocumentosEmpresa.html')

@cache_control(no_store=True)
@login_required(login_url='gateway:login')
def empleoJovenRegistroEmpleados(request):
    formEmpleado = registroEmpleadosEmpresaForm()
    periodoFront = ConvocatoriaEmpleoJoven.objects.filter(activo=True).values()[0]
    if empleados:=infoEmpleadosEmpresa.objects.filter(empresa_id=str(request.user.pk)):
        formEmpleados = {em.id:registroEmpleadosEmpresaForm(instance=em) for em in empleados}
        empleados=empleados.values()
        for em in empleados:
            em['form']=formEmpleados[em['id']]
    else:
        empleados=None
        formEmpleados=None
    context = {'formEmpleado':formEmpleado,'periodoFront':periodoFront,'empleados':empleados}
    return render(request, 'empleo_joven/registroEmpleadosEmpresa.html', context)

@cache_control(no_store=True)
@login_required(login_url='gateway:login')
def empleoJovenAddEmpleado(request):
    formEmpleado = registroEmpleadosEmpresaForm()
    if request.method == 'POST':
        formEmpleado = registroEmpleadosEmpresaForm(request.POST,request.FILES)
        if formEmpleado.is_valid():
            empresa = EmpresaGeneralPerfil.objects.filter(user_id=str(request.user.pk))[0]
            periodo = ConvocatoriaEmpleoJoven.objects.filter(activo=True)
            nombreInicio=str(periodo.values()[0]['fechaInicio'])+'.pdf'
            nombreFin=str(periodo.values()[0]['fechaFin'])+'.pdf'
            request.FILES['documentoFechaInicio'].name = nombreInicio
            request.FILES['documentoFechaFin'].name = nombreFin
            formEmpleado = registroEmpleadosEmpresaForm(request.POST,request.FILES)
            documento = formEmpleado.save(commit=False)
            documento.empresa = empresa
            documento.periodo=periodo[0]
            documento.nombredocumentoFechaInicio = nombreInicio
            documento.nombredocumentoFechaFin = nombreFin
            documento.save()
            return redirect('empleoJoven:empleoJovenRegistroEmpleados')
        else:
            print(formEmpleado.errors.as_data())
            messages.error(request, 'Ocurrio un error inesperado, intentelo de nuevo en un momento')
            return redirect('empleoJoven:empleoJovenRegistroEmpleados')

@cache_control(no_store=True)
@login_required(login_url='gateway:login')
def empleoJovenDeleteEmpleado(request,pk):
    empleado=infoEmpleadosEmpresa.objects.filter(id=pk,empresa_id=str(request.user.pk))
    if empleado:
        if request.method == 'POST':
            empleado.delete()
            return redirect('empleoJoven:empleoJovenRegistroEmpleados')
    else:
        messages.error(request, 'Ocurrio un error, por favor intentelo de nuevo en unos momentos')
        return render(request, 'empleo_joven/registroEmpleadosEmpresa.html')

@cache_control(no_store=True)
@login_required(login_url='gateway:login')
def empleoJovenUpdateEmpleado(request,pk):
    formEmpleado = infoEmpleadosEmpresa.objects.get(id=pk)
    formUpdated = registroEmpleadosEmpresaForm(instance=formEmpleado)
    if request.method == 'POST':
        formUpdated = registroEmpleadosEmpresaForm(request.POST,request.FILES, instance=formEmpleado)
        if formUpdated.is_valid():
            periodo = ConvocatoriaEmpleoJoven.objects.filter(activo=True)
            nombreInicio=str(periodo.values()[0]['fechaInicio'])+'.pdf'
            nombreFin=str(periodo.values()[0]['fechaFin'])+'.pdf'
            request.FILES['documentoFechaInicio'].name = nombreInicio
            request.FILES['documentoFechaFin'].name = nombreFin
            formUpdated = registroEmpleadosEmpresaForm(request.POST,request.FILES,instance=formEmpleado)
            formUpdated.save()
            return redirect('empleoJoven:empleoJovenRegistroEmpleados')
    context={'formUpdated':formUpdated}
    return render(request, 'empleo_joven/registroEmpleadosEmpresa.html',context)
