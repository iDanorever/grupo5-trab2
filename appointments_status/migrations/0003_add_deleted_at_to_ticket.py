# Generated manually for adding deleted_at field to Ticket model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments_status', '0002_auto_create_tickets'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de eliminación'),
        ),
        migrations.AddIndex(
            model_name='ticket',
            index=models.Index(fields=['appointment'], name='tickets_appointment_idx'),
        ),
    ]
