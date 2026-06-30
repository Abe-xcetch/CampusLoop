from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listingapproval',
            name='reviewed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
