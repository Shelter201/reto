# Generated by Django 2.1.3 on 2018-11-29 03:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('name', models.CharField(blank=True, default='', max_length=100)),
            ],
            options={
                'verbose_name': 'Poll',
                'verbose_name_plural': 'Polls',
                'db_table': 'poll',
            },
        ),
        migrations.CreateModel(
            name='PollOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('option_name', models.CharField(blank=True, default='', max_length=100)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='poll', to='poll.Poll')),
            ],
            options={
                'verbose_name': 'Option',
                'verbose_name_plural': 'Options',
                'db_table': 'poll_option',
            },
        ),
        migrations.CreateModel(
            name='PollVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='option', to='poll.PollOption')),
            ],
            options={
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Votes',
                'db_table': 'poll_vote',
            },
        ),
    ]