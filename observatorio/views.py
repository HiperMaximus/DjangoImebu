from django.shortcuts import render

# Create your views here.
def observatorioDashboard(request):
    return render(request, 'observatorio/observatorioDashboard.html')

def indicadorMercadoLaboral(request):
    return render(request, 'observatorio/indicadorMercLaboral.html')

def indicadorMacroeconomico(request):
    return render(request, 'observatorio/indicadorMacroeconomico.html')

def indicadorPulsoSocial(request):
    return render(request, 'observatorio/indicadorPulsoSocial.html')

def indicadorEmpresarial(request):
    return render(request, 'observatorio/indicadorEmpresarial.html')
