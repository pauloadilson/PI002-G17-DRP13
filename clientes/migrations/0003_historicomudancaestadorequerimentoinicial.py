# Generated by Django 5.1.1 on 2024-10-22 01:42

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_estadoexigencia_estadorequerimentoinicial_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricoMudancaEstadoRequerimentoInicial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('observacao', models.TextField(blank=True, null=True)),
                ('data_mudanca', models.DateTimeField(default=datetime.date(2024, 10, 21))),
                ('estado_anterior', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='estado_anterior', to='clientes.estadorequerimentoinicial')),
                ('estado_novo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='estado_novo', to='clientes.estadorequerimentoinicial')),
                ('requerimento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='historico_estado_requerimento', to='clientes.requerimentoinicial')),
            ],
        ),
    ]