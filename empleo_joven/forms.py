from django.forms import ModelForm, FileField, DateField, DateInput
from .models import infoEmpleadosEmpresa, DocumentosEmpresaJoven
from django.core.validators import FileExtensionValidator

class registroEmpleadosEmpresaForm(ModelForm):
    fechaNacimiento = DateField(widget=DateInput(
        format=('%Y-%m-%d'),
        attrs={'class': 'form-control', 
               'placeholder': 'Elija una fecha',
               'type': 'date'
              }),
        label="Fecha de Nacimiento")
    documentoFechaInicio = FileField(validators=[FileExtensionValidator(allowed_extensions=['pdf'])], label="Documento Fecha Inicio")
    documentoFechaFin = FileField(validators=[FileExtensionValidator(allowed_extensions=['pdf'])],label="Documento Fecha Fin")
    field_order=['nombresEmpleado','apellidosEmpleado','tipoDocumento','numeroDocumento','fechaNacimiento','barrio','direccion','telefono1','email','documentoFechaInicio','documentoFechaFin']
    class Meta:
        model = infoEmpleadosEmpresa
        fields = ('nombresEmpleado','apellidosEmpleado','tipoDocumento','numeroDocumento','fechaNacimiento','barrio','direccion','telefono1','email','documentoFechaInicio','documentoFechaFin')

class registroDocumentoEmpresaJovenForm(ModelForm):
    documento = FileField(validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    class Meta:
        model = DocumentosEmpresaJoven
        fields = ('documento',)