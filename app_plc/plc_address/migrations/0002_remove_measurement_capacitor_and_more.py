# Generated by Django 4.2.7 on 2025-01-27 23:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plc_address', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measurement',
            name='capacitor',
        ),
        migrations.RemoveField(
            model_name='measurement',
            name='measured_current',
        ),
        migrations.AddField(
            model_name='measurement',
            name='contactor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='plc_address.contactor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='measurement',
            name='current_r',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Corriente R (A)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='measurement',
            name='current_s',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Corriente S (A)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='measurement',
            name='current_t',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Corriente T (A)'),
            preserve_default=False,
        ),
    ]
