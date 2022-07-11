
from django.forms import FileField, ModelForm, BooleanField, PasswordInput, DateField, DateInput, CharField, Select, TextInput, ModelChoiceField, CheckboxInput, FileInput
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator
from .models import EmpresaGeneralPerfil, PersonaGeneralPerfil, DocumentosEmpresa, DocumentosPersonas, User, CiuuFk, TipoDocFk, BarriosFk

class userForm(UserCreationForm):
    tipoDocumento = ModelChoiceField(queryset=TipoDocFk.objects.all(),
                        widget=Select(
                            attrs={'class': 'form-select',
                            'style':'border: 1px solid #DBE2EA;'
                            },
                        ),
                        initial='1')
    username = CharField(widget=TextInput(
        attrs={'class': 'form-control', 
               'placeholder': 'Número de documento',
               'type': 'text',
               'style':'border: 1px solid #DBE2EA;'
              }),
              label="Número de documento")
    direccion = CharField(widget=TextInput(
        attrs={'class': 'form-control', 
               'placeholder': 'Dirección',
               'type': 'text',
               'style':'border: 1px solid #DBE2EA;'
              }),
              label="Dirección")
    barrio = ModelChoiceField(queryset=BarriosFk.objects.all(),
                        widget=Select(
                            attrs={'class': 'form-select',
                            'style':'border: 1px solid #DBE2EA;'
                            },
                        ),
                        initial='1')
    email = CharField(widget=TextInput(
        attrs={'class': 'form-control', 
               'placeholder': 'Email',
               'type': 'email',
               'style':'border: 1px solid #DBE2EA;'
              }),
              label="Email")
    telefono1 = CharField(widget=TextInput(
        attrs={'class': 'form-control', 
               'placeholder': 'Teléfono 1',
               'type': 'text',
               'style':'border: 1px solid #DBE2EA;'
              }),
              label="Teléfono 1")
    telefono2 = CharField(widget=TextInput(
        attrs={'class': 'form-control', 
               'placeholder': 'Teléfono 2',
               'type': 'text',
               'style':'border: 1px solid #DBE2EA;'
              }),
              label="Teléfono 2")
    password1 = CharField(widget=PasswordInput(
        attrs={'class': 'form-control',
                'placeholder': 'Contraseña',
                'type': 'password',
                'style':'border: 1px solid #DBE2EA;'
                }),
                label="Contraseña")
    password2 = CharField(widget=PasswordInput(
        attrs={'class': 'form-control',
                'placeholder': 'Confirmar contraseña',
                'type': 'password',
                'style':'border: 1px solid #DBE2EA;'
                }),
                label="Confirmar contraseña")
    politicaTratamiento = BooleanField(widget=CheckboxInput(
        attrs={'class': 'form-check-input',
                'style':'border: 1px solid #DBE2EA;',
                'type': 'checkbox'
                }),
                label="Acepto la política de tratamiento de datos",
                required=True)
    aceptoTerminosCondiciones = BooleanField(widget=CheckboxInput(
        attrs={'class': 'form-check-input',
                'style':'border: 1px solid #DBE2EA;',
                'type': 'checkbox'
                }),
                label="Acepto los términos y condiciones",
                required=True)

    field_order=['tipoDocumento','username','direccion','barrio','email','telefono1','telefono2','password1','password2','politicaTratamiento','aceptoTerminosCondiciones']
    class Meta:
        model = User
        fields = ('tipoDocumento','username','direccion','barrio','email','telefono1','telefono2','password1','password2','politicaTratamiento','aceptoTerminosCondiciones')
        widgets = {
            'password': PasswordInput(),
        }
        
class registroEmpresaForm(ModelForm):
    nombreEmpresa = CharField(widget=TextInput(
        attrs={'class': 'form-control', 
               'placeholder': 'Nombre de la empresa',
               'type': 'text',
               'style':'border: 1px solid #DBE2EA;'
              }),
              label="Nombre de la empresa")
    nombreRepresentante = CharField(widget=TextInput(
        attrs={'class': 'form-control', 
               'placeholder': 'Nombre del representante',
               'type': 'text',
               'style':'border: 1px solid #DBE2EA;'
              }),
              label="Nombre del representante")
    CIIU = ModelChoiceField(queryset=CiuuFk.objects.all(),
                            widget=Select(
                                attrs={'class': 'form-select',
                                'style':'border: 1px solid #DBE2EA;'
                                },
                            ),
                            initial='1')
    class Meta:
        model = EmpresaGeneralPerfil
        fields = ('nombreEmpresa','nombreRepresentante','CIIU')

class registroPersonaForm(ModelForm):
    fechaNacimiento = DateField(widget=DateInput(
        format=('%Y-%m-%d'),
        attrs={'class': 'form-control', 
               'placeholder': 'Elija una fecha',
               'type': 'date'
              }),
              label="Fecha de Nacimiento")
    class Meta:
        model = PersonaGeneralPerfil
        fields = ('nombres','apellidos','fechaNacimiento','genero','etnia','vulnerabilidad','nacionalidad','estadoCivil')

class registroDocumentoEmpresaForm(ModelForm):
    documento = FileField(validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
        ,widget=FileInput(
        attrs={'class': 'form-control',
                'type': 'file',
                'style':'border: 1px solid #DBE2EA;'
                }),
        label="Documento")
    class Meta:
        model = DocumentosEmpresa
        fields = ('documento',)

class registroDocumentoPersonaForm(ModelForm):
    documento = FileField(validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    class Meta:
        model = DocumentosPersonas
        fields = ('documento',)