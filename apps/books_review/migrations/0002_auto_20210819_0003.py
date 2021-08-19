# Generated by Django 2.2.4 on 2021-08-19 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books_review', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='users_review',
        ),
        migrations.AlterField(
            model_name='userbook',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_book', to='books_review.Book'),
        ),
        migrations.AlterField(
            model_name='userbook',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_user', to='books_review.User'),
        ),
    ]