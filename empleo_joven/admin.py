from django.contrib import admin
from .models import infoEmpleadosEmpresa, ConvocatoriaEmpleoJoven, DocumentosEmpresaJoven
from gateway.models import BarriosFk

# Register your models here.
#admin.site.register(DocumentosEmpresaJoven)

class ConvocatoriaEmpleoJovenAdmin(admin.ModelAdmin):
    list_display = ('fechaInicio','fechaFin','activo')
    list_filter = ('activo',)

class infoEmpleadosEmpresaAdmin(admin.ModelAdmin):
    list_display = ('empresa','periodo','nombresEmpleado','apellidosEmpleado','numeroDocumento','telefono1','email','nombredocumentoFechaInicio','documentoFechaInicio','nombredocumentoFechaFin','documentoFechaFin','estado','observaciones')
    list_editable = ('estado','observaciones')
    search_fields = ('empresa','nombredocumentoFechaInicio','nombredocumentoFechaFin','estado','observaciones')
    list_filter = ('estado','barrio')

class DocuEmpresaJovenAdmin(admin.ModelAdmin):
    list_display = ('empresa','periodo','nombreDocumento','documento','estado','observaciones')
    readonly_fields = ('empresa','periodo','nombreDocumento','documento')
    list_editable = ('estado','observaciones')
    search_fields = ('empresa','estado','observaciones','nombreDocumento')
    list_filter = ('estado',)
    #list_display_links = (None)


admin.site.register(DocumentosEmpresaJoven,DocuEmpresaJovenAdmin)
admin.site.register(ConvocatoriaEmpleoJoven,ConvocatoriaEmpleoJovenAdmin)
admin.site.register(infoEmpleadosEmpresa,infoEmpleadosEmpresaAdmin)




#class EmpresaGeneralPerfilAdmin(admin.ModelAdmin):
#    model=EmpresaGeneralPerfil
#    list_display=('user','nombreEmpresa','get_estado')
#    readonly_fields=('user','nombreEmpresa','nombreRepresentante','CIIU')
#    inlines = [
#        CustomDocuEmpresaAdmin,
#    ]
#    @display(ordering='estado',description='Estado')
#    def get_estado(self, obj):
#        return 'No aceptado' if len(DocumentosEmpresaJoven.objects.filter(Q(estado='ER') | Q(estado='R'),empresa=obj.pk).values_list('estado')) else 'Aceptado'

