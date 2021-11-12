# Generated by Django 3.2.6 on 2021-11-12 00:56

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('account_id', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Account ID')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='Email')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('hide_email', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='analyticsUpload',
            fields=[
                ('file_id', models.AutoField(primary_key=True, serialize=False, verbose_name='File ID')),
                ('name', models.CharField(max_length=200, verbose_name='File Name')),
                ('file_type', models.CharField(max_length=200, verbose_name='File Extension')),
                ('file', models.FileField(upload_to='twitter/upload_file/', verbose_name='File')),
            ],
        ),
        migrations.CreateModel(
            name='ClassifierModels',
            fields=[
                ('id_model', models.AutoField(primary_key=True, serialize=False, verbose_name='model ID ')),
                ('correct', models.CharField(max_length=200, verbose_name='Correct')),
                ('incorrect', models.CharField(max_length=200, verbose_name='Incorrect')),
                ('accuracy', models.CharField(max_length=200, verbose_name='Accuracy')),
                ('recall', models.CharField(max_length=200, verbose_name='Recall')),
                ('precision', models.CharField(max_length=200, verbose_name='Precision')),
                ('f1_score', models.CharField(max_length=200, verbose_name='F1_Score')),
            ],
        ),
        migrations.CreateModel(
            name='ClassifierSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_size', models.CharField(max_length=200, verbose_name='Test Size')),
                ('rand_state', models.CharField(max_length=200, verbose_name='Random State')),
                ('average', models.CharField(max_length=200, verbose_name='Average')),
            ],
        ),
        migrations.CreateModel(
            name='Intents',
            fields=[
                ('id_tag', models.AutoField(primary_key=True, serialize=False, verbose_name='Tag ID')),
                ('tag', models.CharField(max_length=500, null=True, verbose_name='Tag')),
                ('pattern', models.CharField(max_length=3000, null=True, verbose_name='pattern')),
                ('response', models.CharField(max_length=3000, null=True, verbose_name='response')),
                ('context', models.CharField(blank=True, max_length=500, null=True, verbose_name='context')),
                ('context_set', models.CharField(blank=True, max_length=500, null=True, verbose_name='context')),
            ],
        ),
        migrations.CreateModel(
            name='linksModel',
            fields=[
                ('link_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Links ID')),
                ('link_name', models.CharField(max_length=200, verbose_name='Links Name')),
                ('links', models.CharField(max_length=500, verbose_name='Links')),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('twitter_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Twitter ID')),
                ('source_acct', models.CharField(max_length=250, verbose_name='Twitter Accounts')),
            ],
        ),
        migrations.CreateModel(
            name='Tweets',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Post ID')),
                ('source', models.CharField(max_length=500, verbose_name='Twitter Source')),
                ('posts', models.CharField(max_length=500, verbose_name='Raw tweet')),
                ('likes', models.CharField(max_length=10, verbose_name='Likes')),
                ('dates', models.CharField(max_length=30, verbose_name='Date Created')),
                ('time', models.CharField(max_length=30, verbose_name='Time Created')),
                ('tags', models.CharField(max_length=500, null=True, verbose_name='Hashtags')),
                ('links', models.CharField(max_length=200, null=True, verbose_name='Links')),
            ],
        ),
    ]
