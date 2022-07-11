from django.db import models
from django.core.validators import FileExtensionValidator

from gateway.models import EmpresaGeneralPerfil, TipoDocFk, BarriosFk

class ConvocatoriaEmpleoJoven(models.Model):
    activo=models.BooleanField(("Estado"),default=False)
    fechaInicio=models.DateField(("Fecha Inicio"),)
    fechaFin=models.DateField(("Fecha Fin"),)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['fechaInicio','fechaFin'],name='periodoConvocatoriaJoven')]
        verbose_name = "Convocatoria Empleo Joven"
        verbose_name_plural = "Convocatorias Empleo Joven"
    def __str__(self):
        return 'Convocatoria: ' + str(self.fechaInicio) + ' - ' + str(self.fechaFin)

def user_directory_path_empleadoJoven(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    path='protected/empleoJoven/docsEmpresaJoven/user_{0}/{1}_{2}/empleados/CCREEMPLAZAR{3}/{4}'.format(instance.empresa.pk,instance.periodo.fechaInicio,instance.periodo.fechaFin,instance.numeroDocumento,filename)
    return path 

class infoEmpleadosEmpresa(models.Model):
    empresa = models.ForeignKey(
        EmpresaGeneralPerfil,
        on_delete=models.CASCADE
    )
    periodo=models.ForeignKey(
        ConvocatoriaEmpleoJoven,
        on_delete=models.PROTECT
    )
    nombresEmpleado=models.CharField(("Nombres Empleado"),max_length=200)
    apellidosEmpleado=models.CharField(("Apellidos Empleado"),max_length=200)
    tipoDocumento= models.ForeignKey(TipoDocFk,on_delete=models.PROTECT, default=1, verbose_name="Tipo de Documento")
    numeroDocumento= models.CharField(("Número de documento"),max_length=100)
    fechaNacimiento= models.DateField()
    barrio = models.ForeignKey(BarriosFk,on_delete=models.PROTECT, default=1, verbose_name="Barrio")
    direccion= models.CharField(("Direccion"),max_length=150)
    telefono1 = models.CharField(("Telefono"),max_length=50)
    email = models.EmailField(("Email"),)
    nombredocumentoFechaInicio=models.CharField(("Nombre Documento Fecha Inicio"),max_length=100)
    documentoFechaInicio= models.FileField(("Documento Fecha Inicio"),upload_to=user_directory_path_empleadoJoven,validators=[FileExtensionValidator(allowed_extensions=['pdf'])],max_length=1000)
    nombredocumentoFechaFin=models.CharField(("Nombre Documento Fecha Fin"),max_length=100)
    documentoFechaFin= models.FileField(("Documento Fecha Fin"),upload_to=user_directory_path_empleadoJoven, validators=[FileExtensionValidator(allowed_extensions=['pdf'])],max_length=1000)
    estado= models.CharField(("Estado"),max_length=50,choices=[('A','Aceptado'),('ER','En revisión'),('R','Rechazado')], default='ER')
    observaciones=models.TextField(("Observaciones"),default='Sin observaciones',null=True,blank=True)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['empresa','periodo','numeroDocumento'],name='empleadoEmpresaConvocatoria')]
        verbose_name = "Informacion Empleado Empresa"
        verbose_name_plural = "Informacion Empleados Empresa"
    def __str__(self):
        return self.nombresEmpleado + ' ' + self.apellidosEmpleado

    def save(self, *args, **kwargs):
        try:
            this = infoEmpleadosEmpresa.objects.get(id=self.id)
            if this.documentoFechaInicio != self.documentoFechaInicio:
                this.documentoFechaInicio.delete(save=False)
                self.estado='ER'
            if this.documentoFechaFin != self.documentoFechaFin:
                this.documentoFechaFin.delete(save=False)
                self.estado='ER'    
        except: pass # when new photo then we do nothing, normal case          
        super(infoEmpleadosEmpresa, self).save(*args, **kwargs)


def user_directory_path_empresaJoven(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'protected/empleoJoven/docsEmpresaJoven/user_{0}/{1}_{2}/empresa/{3}'.format(instance.empresa.pk,instance.periodo.fechaInicio,instance.periodo.fechaFin, filename)

class DocumentosEmpresaJoven(models.Model):
    empresa=models.ForeignKey(
        EmpresaGeneralPerfil,
        on_delete=models.CASCADE
    )
    periodo=models.ForeignKey(
        ConvocatoriaEmpleoJoven,
        on_delete=models.PROTECT
    )
    nombreDocumento=models.CharField(("Nombre Documento"),max_length=100)
    documento= models.FileField(("Documento"),upload_to=user_directory_path_empresaJoven, validators=[FileExtensionValidator(allowed_extensions=['pdf'])],max_length=1000)
    estado= models.CharField(("Estado"),max_length=50,choices=[('A','Aceptado'),('ER','En revisión'),('R','Rechazado')], default='ER')
    observaciones=models.TextField(("Observaciones"),default='Sin observaciones',null=True,blank=True)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['documento','empresa'],name='id_documento_empresa_joven'),
        models.UniqueConstraint(fields=['nombreDocumento','empresa'],name='nombre_documento_empresa_joven')]
        verbose_name = "Documento Empresa"
        verbose_name_plural = "Documentos Empresa"

    def save(self, *args, **kwargs):
        #try:
        #    this = DocumentosEmpresa.objects.get(id=self.id)
        #    if this.documento:
        #        os.remove(this.documento.path)   
        #except ObjectDoesNotExist: 
        #    pass
        # delete old file when replacing by updating the file
        try:
            this = DocumentosEmpresaJoven.objects.get(id=self.id)
            if this.documento != self.documento:
                this.documento.delete(save=False)
                self.estado='ER'
        except: pass # when new photo then we do nothing, normal case          
        super(DocumentosEmpresaJoven, self).save(*args, **kwargs)