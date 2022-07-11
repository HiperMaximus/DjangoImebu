from django.contrib import admin
from .models import fase1,fase2,operador,funcionarioOperador,tipologias,opcionesOperador,proceso,eventos, sectores, actividades
from gateway.models import User
from gateway.admin import CustomUserAdmin

# Register your models here.
class fase1Admin(admin.ModelAdmin):
    list_display = ('nombres','apellidos','numeroDocumento','email','telefono1','telefono2','direccion','tipoPersona','politicaTratamiento','aceptoTerminosCondiciones')
    list_filter = ('tipoPersona',)
    search_fields = ('nombres','apellidos','numeroDocumento','email')

class fase2Admin(admin.ModelAdmin):
    list_display = ('persona','montoSolicitado','genero','barrio','comuna','estrato','direccionComercial','escolaridad','actividad','sector','formalidad')
    list_filter = ('genero','estrato','escolaridad','actividad','sector','formalidad')
    search_fields = ('persona','montoSolicitado','numeroDocumento','email','direccionComercial')

class funcionarioOperadorAdmin(admin.ModelAdmin):
    list_display = ('user','operador','nombres','apellidos','fechaNacimiento','genero')
    list_filter = ('operador','genero')
    search_fields = ('user','operador','nombres','apellidos')

class tipologiasAdmin(admin.ModelAdmin):
    list_display = ('nombreTipologia',)
    #list_filter = ('nombreTipologia',)
    search_fields = ('nombreTipologia',)

class opcionesOperadorAdmin(admin.ModelAdmin):
    list_display = ('persona','operador','observaciones')
    list_filter = ('operador',)
    search_fields = ('persona','operador','observaciones')

class procesoAdmin(admin.ModelAdmin):
    list_display = ('persona','funcionarioOperador','observaciones','estado')
    list_filter = ('funcionarioOperador','estado')
    search_fields = ('persona','funcionarioOperador','observaciones','estado')

class eventosAdmin(admin.ModelAdmin):
    list_display = ('proceso','observaciones')
    list_filter = ('proceso',)
    search_fields = ('proceso','observaciones')

class sectoresAdmin(admin.ModelAdmin):
    list_display = ('nombreSector',)
    list_filter = ('nombreSector',)

class actividadesAdmin(admin.ModelAdmin):
    list_display = ('nombreActividad',)
    list_filter = ('nombreActividad',)

#custom models
class OperadorFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('Operador')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'operador'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        operadores=[op[0] for op in operador.objects.filter().values_list('nombre')]
        return tuple(zip(operadores,operadores))

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() is None:
            operadores=[op[0] for op in operador.objects.filter().values_list('user')]
        else:
            operadores=[op[0] for op in operador.objects.filter(nombre=self.value()).values_list('user')]
        return  queryset.filter(pk__in=operadores)

class UserOperador(User):
    class Meta:
        proxy = True
        verbose_name = "Usuario Operador"
        verbose_name_plural = "Usuarios Operador"

class UserOperadorInline(admin.StackedInline):
    model = operador

class UserOperadorAdmin(CustomUserAdmin):
    inlines = [
        UserOperadorInline,
    ]
    list_filter= (OperadorFilter,)


admin.site.register(fase1,fase1Admin)
admin.site.register(fase2,fase2Admin)
admin.site.register(funcionarioOperador,funcionarioOperadorAdmin)
admin.site.register(tipologias,tipologiasAdmin)
admin.site.register(opcionesOperador,opcionesOperadorAdmin)
admin.site.register(proceso,procesoAdmin)
admin.site.register(eventos,eventosAdmin)
admin.site.register(sectores,sectoresAdmin)
admin.site.register(actividades,actividadesAdmin)
admin.site.register(UserOperador,UserOperadorAdmin)


#class operadorAdmin(admin.ModelAdmin):
    #list_display = ('user','nombre','direccion')
    #list_filter = ('user',)
    #search_fields = ('user','nombre','direccion')
#admin.site.register(operador,operadorAdmin)
