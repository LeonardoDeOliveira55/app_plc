# Generated by Django 4.2.3 on 2025-01-22 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plc_address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_io', models.CharField(choices=[('DI', 'Digital Input'), ('DO', 'Digital Output'), ('AI', 'Analog Input'), ('AO', 'Analog Output'), ('RTD', 'RTD')], max_length=3)),
                ('direccion_et', models.CharField(max_length=50)),
                ('numero_modulo', models.IntegerField()),
                ('numero_entrada', models.IntegerField()),
                ('slot', models.IntegerField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='entradasalida',
            name='registro',
        ),
        migrations.RemoveField(
            model_name='registro',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='empresas',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='user',
        ),
        migrations.DeleteModel(
            name='Empresa',
        ),
        migrations.DeleteModel(
            name='EntradaSalida',
        ),
        migrations.DeleteModel(
            name='Registro',
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
        migrations.AddField(
            model_name='direccion',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='direcciones', to='plc_address.tag'),
        ),
    ]
