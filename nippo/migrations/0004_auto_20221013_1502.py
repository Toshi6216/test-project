# Generated by Django 3.2.15 on 2022-10-13 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nippo', '0003_contentscard'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentscard',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images', verbose_name='イメージ画像'),
        ),
        migrations.AlterField(
            model_name='contentscard',
            name='content',
            field=models.TextField(verbose_name='本文'),
        ),
        migrations.AlterField(
            model_name='contentscard',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contentscard', to='nippo.post', verbose_name='紐づく記事'),
        ),
        migrations.AlterField(
            model_name='contentscard',
            name='subtitle',
            field=models.CharField(max_length=100, verbose_name='サブタイトル'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100, verbose_name='タイトル'),
        ),
    ]