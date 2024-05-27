from django.db import migrations


def insert_initial_data(apps, schema_editor):
    BloodGroup = apps.get_model("bloodbank", "BloodGroup")
    BloodGroup.objects.create(group_name="o+")
    BloodGroup.objects.create(group_name="o-")
    BloodGroup.objects.create(group_name="ab+")
    BloodGroup.objects.create(group_name="ab-")
    BloodGroup.objects.create(group_name="a+")
    BloodGroup.objects.create(group_name="a-")
    BloodGroup.objects.create(group_name="b+")
    BloodGroup.objects.create(group_name="b-")


class Migration(migrations.Migration):

    dependencies = [
        ("bloodbank", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(insert_initial_data),
    ]
