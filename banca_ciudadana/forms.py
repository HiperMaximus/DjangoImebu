from django.forms import ModelForm, DateField, DateInput, BooleanField, DecimalField, IntegerField
from .models import fase1, fase2
from django.core.validators import MinValueValidator, MaxValueValidator

class registroPersonaFase1Form(ModelForm):
    politicaTratamiento = BooleanField(required = True, label="Política de Tratamiento de Datos")
    aceptoTerminosCondiciones = BooleanField(required = True, label="Acepto Términos y Condiciones")
    field_order=['nombres','apellidos','tipoDocumento','numeroDocumento','email','telefono1','telefono2','direccion','tipoPersona','politicaTratamiento','aceptoTerminosCondiciones']
    class Meta:
        model = fase1
        fields = ('nombres','apellidos','tipoDocumento','numeroDocumento','email','telefono1','telefono2','direccion','tipoPersona','politicaTratamiento','aceptoTerminosCondiciones')

class registroPersonaFase2Form(ModelForm):
    fechaNacimiento = DateField(widget=DateInput(
        format=('%Y-%m-%d'),
        attrs={'class': 'form-control', 
               'placeholder': 'Elija una fecha',
               'type': 'date'
              }),
        label="Fecha de Nacimiento")
    montoSolicitado=DecimalField(validators=[MinValueValidator(0)], label="Monto Solicitado")
    estrato = IntegerField(validators=[MinValueValidator(0),MaxValueValidator(6)], label="Estrato")
    field_order=['montoSolicitado','genero','barrio','comuna','estrato','direccionComercial','fechaNacimiento','escolaridad','actividad','sector','formalidad','vulnerabilidad']
    class Meta:
        model = fase2
        fields = ('montoSolicitado','genero','barrio','comuna','estrato','direccionComercial','fechaNacimiento','escolaridad','actividad','sector','formalidad','vulnerabilidad')

