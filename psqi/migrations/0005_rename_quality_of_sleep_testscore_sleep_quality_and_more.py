# Generated by Django 5.1.1 on 2024-09-21 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psqi', '0004_rename_psqiquestionnaire_questionnaire'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testscore',
            old_name='quality_of_sleep',
            new_name='sleep_quality',
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='evaluation_date',
            field=models.TextField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='partner_presence',
            field=models.IntegerField(choices=[(0, 'Não'), (1, 'Parceiro ou colega, mas em outro quarto'), (1, 'Parceiro no mesmo quarto, mas em outra cama'), (1, 'Parceiro na mesma cama')], verbose_name='10. Você tem um(a) parceiro [esposo(a)] ou colega de quarto?'),
        ),
    ]