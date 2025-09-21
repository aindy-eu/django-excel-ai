from django.db import migrations


def migrate_names_to_profile(apps, schema_editor):
    """
    Move first_name and last_name from User to UserProfile.
    """
    User = apps.get_model("users", "User")
    UserProfile = apps.get_model("users", "UserProfile")

    for user in User.objects.all():
        profile, created = UserProfile.objects.get_or_create(user=user)

        # Migrate the names if they exist
        if user.first_name or user.last_name:
            profile.first_name = user.first_name
            profile.last_name = user.last_name
            profile.save()

        # Migrate phone if it exists
        if hasattr(user, "phone") and user.phone:
            profile.phone_number = user.phone
            profile.save()


def reverse_migration(apps, schema_editor):
    """
    Move names back from UserProfile to User (for rollback).
    """
    User = apps.get_model("users", "User")
    UserProfile = apps.get_model("users", "UserProfile")

    for profile in UserProfile.objects.all():
        user = profile.user
        if profile.first_name or profile.last_name:
            user.first_name = profile.first_name
            user.last_name = profile.last_name
            user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_remove_user_phone_userprofile_first_name_and_more"),
    ]

    operations = [
        migrations.RunPython(migrate_names_to_profile, reverse_migration),
    ]
