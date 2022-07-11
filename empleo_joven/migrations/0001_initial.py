# Generated by Django 4.0.4 on 2022-06-03 06:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import empleo_joven.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gateway', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConvocatoriaEmpleoJoven',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField(default=False, verbose_name='Estado')),
                ('fechaInicio', models.DateField(verbose_name='Fecha Inicio')),
                ('fechaFin', models.DateField(verbose_name='Fecha Fin')),
            ],
            options={
                'verbose_name': 'Convocatoria Empleo Joven',
                'verbose_name_plural': 'Convocatorias Empleo Joven',
            },
        ),
        migrations.CreateModel(
            name='infoEmpleadosEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombresEmpleado', models.CharField(max_length=200, verbose_name='Nombres Empleado')),
                ('apellidosEmpleado', models.CharField(max_length=200, verbose_name='Apellidos Empleado')),
                ('numeroDocumento', models.CharField(max_length=100, verbose_name='Número de documento')),
                ('fechaNacimiento', models.DateField()),
                ('direccion', models.CharField(max_length=150, verbose_name='Direccion')),
                ('telefono1', models.CharField(max_length=50, verbose_name='Telefono')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('nombredocumentoFechaInicio', models.CharField(max_length=100, verbose_name='Nombre Documento Fecha Inicio')),
                ('documentoFechaInicio', models.FileField(max_length=1000, upload_to=empleo_joven.models.user_directory_path_empleadoJoven, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Documento Fecha Inicio')),
                ('nombredocumentoFechaFin', models.CharField(max_length=100, verbose_name='Nombre Documento Fecha Fin')),
                ('documentoFechaFin', models.FileField(max_length=1000, upload_to=empleo_joven.models.user_directory_path_empleadoJoven, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Documento Fecha Fin')),
                ('estado', models.CharField(choices=[('A', 'Aceptado'), ('ER', 'En revisión'), ('R', 'Rechazado')], default='ER', max_length=50, verbose_name='Estado')),
                ('observaciones', models.TextField(blank=True, default='Sin observaciones', null=True, verbose_name='Observaciones')),
                ('updated', models.DateField(auto_now=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('barrio', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='gateway.barriosfk', verbose_name='Barrio')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gateway.empresageneralperfil')),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='empleo_joven.convocatoriaempleojoven')),
                ('tipoDocumento', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='gateway.tipodocfk', verbose_name='Tipo de Documento')),
            ],
            options={
                'verbose_name': 'Informacion Empleado Empresa',
                'verbose_name_plural': 'Informacion Empleados Empresa',
            },
        ),
        migrations.CreateModel(
            name='DocumentosEmpresaJoven',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreDocumento', models.CharField(max_length=100, verbose_name='Nombre Documento')),
                ('documento', models.FileField(max_length=1000, upload_to=empleo_joven.models.user_directory_path_empresaJoven, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Documento')),
                ('estado', models.CharField(choices=[('A', 'Aceptado'), ('ER', 'En revisión'), ('R', 'Rechazado')], default='ER', max_length=50, verbose_name='Estado')),
                ('observaciones', models.TextField(blank=True, default='Sin observaciones', null=True, verbose_name='Observaciones')),
                ('updated', models.DateField(auto_now=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gateway.empresageneralperfil')),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='empleo_joven.convocatoriaempleojoven')),
            ],
            options={
                'verbose_name': 'Documento Empresa',
                'verbose_name_plural': 'Documentos Empresa',
            },
        ),
        migrations.AddConstraint(
            model_name='convocatoriaempleojoven',
            constraint=models.UniqueConstraint(fields=('fechaInicio', 'fechaFin'), name='periodoConvocatoriaJoven'),
        ),
        migrations.AddConstraint(
            model_name='infoempleadosempresa',
            constraint=models.UniqueConstraint(fields=('empresa', 'periodo', 'numeroDocumento'), name='empleadoEmpresaConvocatoria'),
        ),
        migrations.AddConstraint(
            model_name='documentosempresajoven',
            constraint=models.UniqueConstraint(fields=('documento', 'empresa'), name='id_documento_empresa_joven'),
        ),
        migrations.AddConstraint(
            model_name='documentosempresajoven',
            constraint=models.UniqueConstraint(fields=('nombreDocumento', 'empresa'), name='nombre_documento_empresa_joven'),
        ),
    ]
