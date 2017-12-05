# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-22 02:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0006_auto_20171005_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballotmeasurecontest',
            name='division',
            field=models.ForeignKey(help_text="Reference to the Division that defines the political geography of the contest, e.g., a specific Congressional or State Senate district. Should be a subdivision of the Division referenced by the contest's Election.", on_delete=django.db.models.deletion.PROTECT, related_name='ballotmeasurecontests', related_query_name='ballotmeasurecontests', to='core.Division'),
        ),
        migrations.AlterField(
            model_name='ballotmeasurecontest',
            name='runoff_for_contest',
            field=models.OneToOneField(help_text='If this contest is a runoff to determine the outcome of a previously undecided contest, reference to that BallotMeasureContest.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='runoff_contest', to='elections.BallotMeasureContest'),
        ),
        migrations.AlterField(
            model_name='candidacy',
            name='post',
            field=models.ForeignKey(help_text='Reference to Post representing the public office for which the candidate is seeking election.', on_delete=django.db.models.deletion.PROTECT, related_name='candidacies', to='core.Post'),
        ),
        migrations.AlterField(
            model_name='candidacy',
            name='top_ticket_candidacy',
            field=models.ForeignKey(help_text='If the candidate is running as part of ticket, e.g., a Vice Presidential candidate running with a Presidential candidate, reference to candidacy at the top of the ticket.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ticket', to='elections.Candidacy'),
        ),
        migrations.AlterField(
            model_name='candidatecontest',
            name='division',
            field=models.ForeignKey(help_text="Reference to the Division that defines the political geography of the contest, e.g., a specific Congressional or State Senate district. Should be a subdivision of the Division referenced by the contest's Election.", on_delete=django.db.models.deletion.PROTECT, related_name='candidatecontests', related_query_name='candidatecontests', to='core.Division'),
        ),
        migrations.AlterField(
            model_name='candidatecontest',
            name='runoff_for_contest',
            field=models.OneToOneField(help_text='If this contest is a runoff to determine the outcome of a previously undecided contest, reference to that CandidateContest.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='runoff_contest', to='elections.CandidateContest'),
        ),
        migrations.AlterField(
            model_name='partycontest',
            name='division',
            field=models.ForeignKey(help_text="Reference to the Division that defines the political geography of the contest, e.g., a specific Congressional or State Senate district. Should be a subdivision of the Division referenced by the contest's Election.", on_delete=django.db.models.deletion.PROTECT, related_name='partycontests', related_query_name='partycontests', to='core.Division'),
        ),
        migrations.AlterField(
            model_name='partycontest',
            name='runoff_for_contest',
            field=models.OneToOneField(help_text='If this contest is a runoff to determine the outcome of a previously undecided contest, reference to that PartyContest.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='elections.PartyContest'),
        ),
        migrations.AlterField(
            model_name='retentioncontest',
            name='division',
            field=models.ForeignKey(help_text="Reference to the Division that defines the political geography of the contest, e.g., a specific Congressional or State Senate district. Should be a subdivision of the Division referenced by the contest's Election.", on_delete=django.db.models.deletion.PROTECT, related_name='retentioncontests', related_query_name='retentioncontests', to='core.Division'),
        ),
        migrations.AlterField(
            model_name='retentioncontest',
            name='membership',
            field=models.ForeignKey(help_text='Reference to the Membership that represents the tenure of a person in a specific public office.', on_delete=django.db.models.deletion.PROTECT, to='core.Membership'),
        ),
        migrations.AlterField(
            model_name='retentioncontest',
            name='runoff_for_contest',
            field=models.OneToOneField(help_text='If this contest is a runoff to determine the outcome of a previously undecided contest, reference to that RetentionContest.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='runoff_contest', to='elections.RetentionContest'),
        ),
    ]
