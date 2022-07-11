from pyexpat import model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import EmpresaGeneralPerfil, DocumentosEmpresa, PersonaGeneralPerfil, DocumentosPersonas, User, TipoDocFk, BarriosFk, CiuuFk, VulnerabilidadFk, NacionalidadFk, EstadoCivilFk, EtniaFK, DependenciasFK, FuncionarioImebuPerfil
from .forms import userForm

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = userForm
    form=userForm
    model = User
    list_display = ('username','email','telefono1','telefono2','politicaTratamiento','aceptoTerminosCondiciones')
    #list_filter = ()
    fieldsets = (
        ('Información de usuario',{'fields': (('username','direccion','email')),
                'classes':('extrapretty','wide'),
                'description':'<h1><strong>olacarebola</strong></h1>'}),
        ('Información de contacto',{'fields':('telefono1','telefono2')}),
        ('Politica de tratamiento de datos',{'fields':('politicaTratamiento','aceptoTerminosCondiciones')}),
        ('Grupos', {'fields': ('groups',)}),
        ('Permisos individuales', {'fields': ('user_permissions',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        ('Información de usuario',{'fields': (('username','direccion','email')),
                'classes':('extrapretty','wide'),
                'description':'<h1><strong>olacarebola</strong></h1>'}),
        ('Información de contacto',{'fields':('telefono1','telefono2')}),
        ('Politica de tratamiento de datos',{'fields':('politicaTratamiento','aceptoTerminosCondiciones')}),
        ('Contraseña', {'fields': ('password1', 'password2')}),
        ('Grupos', {'fields': ('groups',)}),
        ('Permisos individuales', {'fields': ('user_permissions',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    search_fields = ('email','username','telefono1')
    ordering = ('email',)

class TipoDocFkAdmin(admin.ModelAdmin):
    list_display = ('nombreTipoDoc',)
    list_filter = ('nombreTipoDoc',)

class BarriosFkAdmin(admin.ModelAdmin):
    list_display = ('nombreBarrios',)
    list_filter = ('nombreBarrios',)

class CiuuFkAdmin(admin.ModelAdmin):
    list_display = ('nombreCiuu',)
    list_filter = ('nombreCiuu',)
    search_fields = ('nombreCiuu',)

class VulnerabilidadFkAdmin(admin.ModelAdmin):
    list_display = ('nombreVulnerabilidad',)
    list_filter = ('nombreVulnerabilidad',)

class NacionalidadFkAdmin(admin.ModelAdmin):
    list_display = ('nombreNacionalidad',)
    list_filter = ('nombreNacionalidad',)

class EstadoCivilFkAdmin(admin.ModelAdmin):
    list_display = ('nombreEstadoCivil',)
    list_filter = ('nombreEstadoCivil',)

class EtniaFKAdmin(admin.ModelAdmin):
    list_display = ('nombreEtnia',)
    list_filter = ('nombreEtnia',)

class DocumentosEmpresaAdmin(admin.ModelAdmin):
    list_display = ('empresa','nombreDocumento','documento','estado','observaciones')
    list_filter = ('empresa','nombreDocumento','estado')
    list_editable = ('estado','observaciones')

class EmpresaGeneralPerfilAdmin(admin.ModelAdmin):
    list_display = ('user','nombreEmpresa','nombreRepresentante','CIIU')
    list_filter = ('CIIU',)
    search_fields = ('user','nombreEmpresa','nombreRepresentante','CIIU')

class PersonaGeneralPerfilAdmin(admin.ModelAdmin):
    list_display = ('user','nombres','apellidos','fechaNacimiento','genero')
    list_filter = ('genero',)
    search_fields = ('user','nombres','apellidos','genero')

class DocumentosPersonasAdmin(admin.ModelAdmin):
    list_display = ('persona','nombreDocumento','documento','estado','observaciones')
    list_filter = ('persona','nombreDocumento','estado')
    list_editable = ('estado','observaciones')

class DependenciasFKAdmin(admin.ModelAdmin):
    list_display = ('nombreDependencia',)
    list_filter = ('nombreDependencia',)

#custom models
class FuncionarioFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('Dependencia')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'dependencia'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        dependencias=[dep[0] for dep in DependenciasFK.objects.filter().values_list('nombreDependencia')]
        return tuple(zip(dependencias,dependencias))

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() is None:
            funcionarios=[func[0] for func in FuncionarioImebuPerfil.objects.filter().values_list('user')]
        else:
            funcionarios=[func[0] for func in FuncionarioImebuPerfil.objects.filter(Dependencia__nombreDependencia=self.value()).values_list('user')]
        return  queryset.filter(pk__in=funcionarios)

class UserFuncionario(User):
    class Meta:
        proxy = True
        verbose_name = "Usuario Funcionario"
        verbose_name_plural = "Usuarios Funcionarios"

class UserFuncionarioInline(admin.StackedInline):
    model = FuncionarioImebuPerfil

class UserFuncionarioAdmin(CustomUserAdmin):
    inlines = [
        UserFuncionarioInline,
    ]
    list_filter= (FuncionarioFilter,)


admin.site.register(User, CustomUserAdmin)
admin.site.register(TipoDocFk, TipoDocFkAdmin)
admin.site.register(BarriosFk, BarriosFkAdmin)
admin.site.register(CiuuFk, CiuuFkAdmin)
admin.site.register(VulnerabilidadFk, VulnerabilidadFkAdmin)
admin.site.register(NacionalidadFk, NacionalidadFkAdmin)
admin.site.register(EstadoCivilFk, EstadoCivilFkAdmin)
admin.site.register(EtniaFK, EtniaFKAdmin)
admin.site.register(DocumentosEmpresa, DocumentosEmpresaAdmin)
admin.site.register(EmpresaGeneralPerfil, EmpresaGeneralPerfilAdmin)
admin.site.register(PersonaGeneralPerfil, PersonaGeneralPerfilAdmin)
admin.site.register(DocumentosPersonas, DocumentosPersonasAdmin)
admin.site.register(DependenciasFK, DependenciasFKAdmin)
admin.site.register(UserFuncionario,UserFuncionarioAdmin)


#class FuncionarioImebuPerfilAdmin(admin.ModelAdmin):
    #list_display = ('user','nombres','apellidos','cargo','Dependencia')
    #list_filter = ('Dependencia',)
    #search_fields = ('user','nombres','apellidos','cargo','Dependencia','genero')

#admin.site.register(FuncionarioImebuPerfil, FuncionarioImebuPerfilAdmin)


#    fieldsets = (
#        (None, {'fields': ('email', 'password')}),
#        ('Personal info', {'fields': ('first_name', 'last_name')}),
#        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#        ('Important dates', {'fields': ('last_login', 'date_joined')}),
#        ('Contact info', {'fields': ('contact_no',)}),)

#    add_fieldsets = (
#        (None, {
#            'classes': ('wide',),
#            'fields': ('email', 'password1', 'password2'),}),)

#class PersonAdmin(admin.ModelAdmin):
#    form = userForm

#admin.site.register(User)