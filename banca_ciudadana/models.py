from django.db import models
from gateway.models import User, TipoDocFk, VulnerabilidadFk, BarriosFk
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class sectores(models.Model):
    nombreSector = models.CharField(("Sector"),max_length=150)
    class Meta: 
        verbose_name = "Sector"
        verbose_name_plural = "Sectores"
    def __str__(self):
        return self.nombreSector

class actividades(models.Model):
    nombreActividad = models.CharField(("Actividad"),max_length=150)
    class Meta: 
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"
    def __str__(self):
        return self.nombreActividad

class fase1(models.Model):
    nombres = models.CharField(("Nombres"),max_length=150)
    apellidos =models.CharField(("Apellidos"),max_length=150)
    tipoDocumento= models.ForeignKey(TipoDocFk,on_delete=models.PROTECT, blank=False, default=1,verbose_name="Tipo de Documento")
    numeroDocumento =models.CharField(("Número de Documento"),max_length=150)
    email = models.EmailField(("Email"))
    telefono1 = models.CharField(("Telefono 1"),max_length=50)
    telefono2 = models.CharField(("Telefono 2"),max_length=50, null=True, blank=True)
    direccion= models.CharField(("Direccion"),max_length=150)
    tipoPersona=models.CharField(("Tipo de Persona"),max_length=150, blank=False,default='EmpresaEmprendedor',choices=[('EmpresaEmprendedor','Empresa (Emprendedor)'),('Microempresario','Micro empresario'),('Independiente','Independiente o persona con idea de negocio'),('Empresa','Empresa')])
    politicaTratamiento= models.BooleanField(blank=False)
    aceptoTerminosCondiciones= models.BooleanField(blank=False)
    class Meta: 
        verbose_name = "Informacion Fase 1"
        verbose_name_plural = "Informacion Fase 1"
    def __str__(self):
        return self.nombres + ' ' + self.apellidos

class fase2(models.Model):
    persona = models.OneToOneField(fase1,on_delete=models.CASCADE)
    montoSolicitado= models.DecimalField(("Monto Solicitado"),max_digits=11, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    genero = models.CharField(("Genero"),max_length=50,choices=[('F','Femenino'),('M','Masculino'),('O','Otros')], default='F')
    barrio= models.ForeignKey(BarriosFk,on_delete=models.PROTECT, default=1, verbose_name="Barrio")
    comuna = models.CharField(("Comuna"),max_length=50)
    estrato = models.IntegerField(("Estrato"),validators=[MinValueValidator(0),MaxValueValidator(6)])
    direccionComercial = models.CharField(("Direccion Comercial"),max_length=100)
    fechaNacimiento = models.DateField()
    escolaridad = models.CharField(("Escolaridad"),max_length=50, blank=False,default='Primaria',choices=[('Primaria','Primaria'),('Bachiller','Bachiller'),('Pregrado','Pregrado'),('Especialidad','Especialidad'),('Maestria','Maestria'),('Doctorado','Doctorado')])
    actividad = models.ForeignKey(actividades,on_delete=models.PROTECT, blank=False, default=1, verbose_name="Actividad")
    sector = models.ForeignKey(sectores,on_delete=models.PROTECT, blank=False, default=1, verbose_name="Sector")
    formalidad = models.CharField(("Formalidad"),max_length=50, blank=False,default='Rut',choices=
                [('Rut','Rut'),('Cedula','Cedula'),('ICA','ICA'),('Informal','Informal')])
    vulnerabilidad = models.ManyToManyField(VulnerabilidadFk)
    class Meta: 
        verbose_name = "Informacion Fase 2"
        verbose_name_plural = "Informacion Fase 2"
    def __str__(self):
        return self.persona.nombres + ' ' + self.persona.apellidos
    
class operador(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    nombre= models.CharField(("Nombre del Operador"),max_length=200)
    direccion= models.CharField(("Direccion"),max_length=200)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)
    class Meta: 
        verbose_name = "Operador"
        verbose_name_plural = "Operadores"
    def __str__(self):
        return self.nombre

class funcionarioOperador(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    operador = models.ForeignKey(operador,on_delete=models.CASCADE, verbose_name="Operador")
    nombres= models.CharField(("Nombres"),max_length=200)
    apellidos= models.CharField(("Apellidos"),max_length=200)
    fechaNacimiento= models.DateField()
    genero= models.CharField(("Genero"),max_length=50,choices=[('F','Femenino'),('M','Masculino'),('O','Otros')], default='F')
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)
    class Meta: 
        verbose_name = "Funcionario Operador"
        verbose_name_plural = "Funcionarios Operador"
    def __str__(self):
        return self.nombres + ' ' + self.apellidos + ' ' + self.operador.nombre

class tipologias(models.Model):
    nombreTipologia=models.CharField(("Tipologia"),max_length=100)
    class Meta: 
        verbose_name = "Tipologia"
        verbose_name_plural = "Tipologias"
    def __str__(self):
        return self.nombreTipologia

class opcionesOperador(models.Model):
    persona = models.ForeignKey(fase2,on_delete=models.CASCADE, verbose_name="Persona")
    operador = models.ForeignKey(operador,on_delete=models.PROTECT, verbose_name="Operador")
    observaciones = models.TextField(("Observaciones"),)
    tipologias = models.ManyToManyField(tipologias)
    class Meta: 
        verbose_name = "Opcion del Operador"
        verbose_name_plural = "Opciones del Operador"
    def __str__(self):
        return self.persona.nombres + ' ' + self.persona.apellidos + ' ' + self.operador

class proceso(models.Model):
    persona = models.ForeignKey(fase2,on_delete=models.CASCADE, verbose_name="Persona")
    funcionarioOperador=models.ForeignKey(funcionarioOperador,on_delete=models.PROTECT, verbose_name="Funcionario Operador")
    observaciones = models.TextField(("Observadores"),)
    tipologias = models.ManyToManyField(tipologias)
    estado=models.CharField(("Estado"),max_length=100,choices=[('A','ACEPTADO'),('R','RECHAZADO'),('EP','En PROCESO')])
    class Meta: 
        verbose_name = "Proceso"
        verbose_name_plural = "Procesos"
    def __str__(self):
        return self.persona.nombres + ' ' + self.persona.apellidos + ' ' + self.funcionarioOperador.nombres + ' ' + self.funcionarioOperador.apellidos

class eventos(models.Model):
    proceso = models.ForeignKey(proceso,on_delete=models.CASCADE, verbose_name="Proceso")
    observaciones = models.TextField(("Observaciones"),)
    tipologias = models.ManyToManyField(tipologias)
    class Meta: 
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
    def __str__(self):
        return 'Proceso: ' +self.proceso.id
