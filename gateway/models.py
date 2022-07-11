from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


class TipoDocFk(models.Model):
    nombreTipoDoc= models.CharField(verbose_name="Tipo de Documento",max_length=100, unique=True)
    class Meta: 
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"
    def __str__(self):
        return self.nombreTipoDoc

class BarriosFk(models.Model):
    nombreBarrios= models.CharField(("Barrio"),max_length=100, unique=True)
    class Meta:
        verbose_name = "Barrio"
        verbose_name_plural = "Barrios"
    def __str__(self):
        return self.nombreBarrios

class User(AbstractUser):
    username= models.CharField(("Número de documento"),max_length=100)
    tipoDocumento= models.ForeignKey(TipoDocFk,on_delete=models.PROTECT, default=1, verbose_name="Tipo de Documento")
    direccion= models.CharField(("Direccion"),max_length=150)
    barrio= models.ForeignKey(BarriosFk,on_delete=models.PROTECT, default=1, verbose_name="Barrio")
    email = models.EmailField(("Email"),unique=True)
    telefono1 = models.CharField(("Telefono 1"),max_length=50)
    telefono2 = models.CharField(("Telefono 2"),max_length=50,null=True,blank=True)
    politicaTratamiento= models.BooleanField(blank=False)
    aceptoTerminosCondiciones= models.BooleanField(blank=False)
    first_name = None #models.CharField(("Nombre"), max_length=150, blank=True,null=True,default='')
    last_name = None #models.CharField(("Apellidos"), max_length=150, blank=True,null=True,default='')
    USERNAME_FIELD= 'email'
    EMAIL_FIELD='email'
    REQUIRED_FIELDS=['username','direccion','telefono1','telefono2','politicaTratamiento','aceptoTerminosCondiciones']
    class Meta:
        constraints=[models.UniqueConstraint(fields=['username','tipoDocumento'],name='id_general')]
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    def __str__(self):
        return str(self.tipoDocumento) + ' ' + self.username
    
class CiuuFk(models.Model):
    nombreCiuu=models.CharField(("CIUU"),max_length=300, unique=True)
    class Meta: 
        verbose_name = "CIUU"
        verbose_name_plural = "CIUU"
    def __str__(self):
        return self.nombreCiuu

class VulnerabilidadFk(models.Model):
    nombreVulnerabilidad= models.CharField(("Vulnerabilidad"),max_length=150, unique=True)
    class Meta: 
        verbose_name = "Vulnerabilidad"
        verbose_name_plural = "Vulnerabilidades"
    def __str__(self):
        return self.nombreVulnerabilidad
    
class NacionalidadFk(models.Model):
    nombreNacionalidad= models.CharField(("Nacionalidad"),max_length=100, unique=True)
    class Meta: 
        verbose_name = "Nacionalidad"
        verbose_name_plural = "Nacionalidades"
    def __str__(self):
        return self.nombreNacionalidad
    
class EstadoCivilFk(models.Model):
    nombreEstadoCivil= models.CharField(("Estado Civil"),max_length=50, unique=True)
    class Meta: 
        verbose_name = "Estado Civil"
        verbose_name_plural = "Estados Civiles"
    def __str__(self):
        return self.nombreEstadoCivil
    
class EtniaFK(models.Model):
    nombreEtnia= models.CharField(("Etnia"),max_length=100, unique=True)
    class Meta: 
        verbose_name = "Etnia"
        verbose_name_plural = "Etnias"
    def __str__(self):
        return self.nombreEtnia
    
class EmpresaGeneralPerfil(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    nombreEmpresa=models.CharField(("Nombre de Empresa"),max_length=200)
    nombreRepresentante= models.CharField(("Nombre de Representante"),max_length=200)
    CIIU = models.ForeignKey(CiuuFk,on_delete=models.PROTECT,blank=False, default=1)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)
    class Meta: 
        constraints=[models.UniqueConstraint(fields=['user','nombreEmpresa'],name='id_dueñoEmpresa')]
        verbose_name = "Empresa General Perfil"
        verbose_name_plural = "Empresas General Perfil"
    def __str__(self):
        return self.nombreEmpresa + ' ' + self.nombreRepresentante

def user_directory_path_empresa(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'protected/gateway/docsGeneralEmpresa/user_{0}/{1}'.format(instance.empresa.pk, filename)

class DocumentosEmpresa(models.Model):
    empresa = models.ForeignKey(
        EmpresaGeneralPerfil,
        on_delete=models.CASCADE
    )
    nombreDocumento = models.CharField(("Nombre Documento"),max_length=100)
    documento= models.FileField(("Documento"),upload_to=user_directory_path_empresa, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    estado= models.CharField(("Estado"),max_length=50,choices=[('A','Aceptado'),('ER','En revisión'),('R','Rechazado')], default='ER')
    observaciones=models.TextField(("Observaciones"),default='Sin observaciones',null=True,blank=True)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['empresa','documento'],name='id_documento_empresa'),
        models.UniqueConstraint(fields=['empresa','nombreDocumento'],name='nombre_documento_empresa')]
        verbose_name = "Documento Empresa"
        verbose_name_plural = "Documentos Empresa"
    def __str__(self):
        return self.nombreDocumento
    
    def save(self, *args, **kwargs):
        #try:
        #    this = DocumentosEmpresa.objects.get(id=self.id)
        #    if this.documento:
        #        os.remove(this.documento.path)   
        #except ObjectDoesNotExist: 
        #    pass
        # delete old file when replacing by updating the file
        try:
            this = DocumentosEmpresa.objects.get(id=self.id)
            if this.documento != self.documento:
                this.documento.delete(save=False)
                self.estado='ER'
        except: pass # when new photo then we do nothing, normal case          
        super(DocumentosEmpresa, self).save(*args, **kwargs)

class PersonaGeneralPerfil(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    nombres= models.CharField(("Nombres"),max_length=200)
    apellidos= models.CharField(("Apellidos"),max_length=200)
    fechaNacimiento= models.DateField()
    genero= models.CharField(("Genero"),max_length=50,choices=[('F','Femenino'),('M','Masculino'),('O','Otros')], default='F')
    etnia= models.ForeignKey(EtniaFK,null=True,on_delete=models.SET_NULL,blank=False, default=1, verbose_name="Etnia")
    vulnerabilidad = models.ManyToManyField(VulnerabilidadFk)
    nacionalidad = models.ForeignKey(NacionalidadFk,null=True ,on_delete=models.SET_NULL,blank=False, default=1, verbose_name="Nacionalidad")
    estadoCivil= models.ForeignKey(EstadoCivilFk,null=True ,on_delete=models.SET_NULL,blank=False, default=1, verbose_name="Estado Civil")
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)
    class Meta: 
        verbose_name = "Persona General Perfil"
        verbose_name_plural = "Personas General Perfil"
    def __str__(self):
        return self.nombres + ' ' +self.apellidos

def user_directory_path_persona(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'protected/gateway/docsPersonaGeneral/user_{0}/{1}'.format(instance.persona.pk, filename)

class DocumentosPersonas(models.Model):
    persona = models.ForeignKey(
        PersonaGeneralPerfil,
        on_delete=models.CASCADE
    )
    nombreDocumento = models.CharField(("Nombre Documento"),max_length=100)
    documento= models.FileField(("Documento"),upload_to=user_directory_path_persona, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    estado= models.CharField(("Estado"),max_length=50,choices=[('A','Aceptado'),('ER','En revisión'),('R','Rechazado')], default='ER')
    observaciones=models.TextField(("Observaciones"),default='Sin observaciones',null=True,blank=True)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['persona','documento'],name='id_documento_persona'),
        models.UniqueConstraint(fields=['persona','nombreDocumento'],name='nombre_documento_persona')]
        verbose_name = "Documento Persona"
        verbose_name_plural = "Documentos Persona"
    def __str__(self):
        return self.nombreDocumento

    def save(self, *args, **kwargs):
        #try:
        #    this = DocumentosEmpresa.objects.get(id=self.id)
        #    if this.documento:
        #        os.remove(this.documento.path)   
        #except ObjectDoesNotExist: 
        #    pass
        # delete old file when replacing by updating the file
        try:
            this = DocumentosPersonas.objects.get(id=self.id)
            if this.documento != self.documento:
                this.documento.delete(save=False)
                self.estado='ER'
        except: pass # when new photo then we do nothing, normal case          
        super(DocumentosPersonas, self).save(*args, **kwargs)

class DependenciasFK(models.Model):
    nombreDependencia= models.CharField(("Dependencia"),max_length=100, unique=True)
    class Meta: 
        verbose_name = "Dependencia"
        verbose_name_plural = "Dependencias"
    def __str__(self):
        return self.nombreDependencia

class FuncionarioImebuPerfil(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    nombres= models.CharField(("Nombres"),max_length=200)
    apellidos= models.CharField(("Apellidos"),max_length=200)
    fechaNacimiento= models.DateField(("Fecha de Nacimiento"))
    genero= models.CharField(("Genero"),max_length=50,choices=[('F','Femenino'),('M','Masculino'),('O','Otros')], default='F')
    cargo=models.CharField(("Cargo"),max_length=200, default=1)
    contrato=models.CharField(("Contrato"), max_length=200)
    Dependencia=models.ForeignKey(DependenciasFK,on_delete=models.PROTECT, default=1)
    etnia= models.ForeignKey(EtniaFK,null=True ,on_delete=models.SET_NULL, default=1)
    vulnerabilidad = models.ManyToManyField(VulnerabilidadFk)
    nacionalidad = models.ForeignKey(NacionalidadFk,null=True ,on_delete=models.SET_NULL, default=1)
    estadoCivil= models.ForeignKey(EstadoCivilFk,null=True ,on_delete=models.SET_NULL, default=1)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)
    class Meta: 
        verbose_name = "Funcionario Imebu"
        verbose_name_plural = "Funcionarios Imebu"
    def __str__(self):
        return self.nombres + ' ' + self.apellidos