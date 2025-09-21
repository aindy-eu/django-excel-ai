from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_migrate_names_to_profile"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="user",
            name="last_name",
        ),
    ]
