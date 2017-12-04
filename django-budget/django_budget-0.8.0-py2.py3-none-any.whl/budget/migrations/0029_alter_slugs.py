# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-20 23:30
from __future__ import unicode_literals


from django.db import IntegrityError
from django.db import migrations


from budget.utils import SLUG_MATCH_RE


def forward_func(apps, schema_editor):
    """TK."""
    Item = apps.get_model('budget', 'Item')

    for item in Item.objects.all():
        matched_slug = SLUG_MATCH_RE.match(item.slug)

        if matched_slug:
            slug_parts = matched_slug.groupdict()

            if item.primary_for_package:
                if slug_parts.get('suffix_letter', ''):
                    primary_slug = '{}--{}'.format(
                        slug_parts['slug_key'],
                        slug_parts['suffix_letter']
                    )
                else:
                    primary_slug = slug_parts['slug_key']

                package = item.primary_for_package

                preserved_slug = 'Migrated -- original slug "{}"'.format(
                    item.slug
                )

                package.slug_key = primary_slug
                package.notes = '{}\n{}'.format(package.notes, preserved_slug)
                package.save()

                item.slug_key = None

            elif item.additional_for_package:
                if slug_parts.get('additional_slug') is not None:
                    additional_slug = slug_parts['additional_slug']
                else:
                    raise IntegrityError(
                        ' '.join([
                            'The additional content item "{}" doesn\'t',
                            'have a slug.',
                            'Halting migration.',
                        ]).format(str(item))
                    )

                item.slug_key = additional_slug
            else:
                raise IntegrityError(
                    ' '.join([
                        'The budget item "{}" isn\'t connected as either the',
                        'primary piece of content in a package or as an',
                        'additional piece of content.',
                        'Halting migration.',
                        # ]).format(str(item))
                    ]).format(str(item.id))
                )

        else:
            raise IntegrityError(
                ' '.join([
                    'Couldn\'t parse slug from budget item "{}".',
                    'Halting migration.',
                ]).format(str(item))
            )

        item.save()


def backward_func(apps, schema_editor):
    """TK."""
    Item = apps.get_model('budget', 'Item')

    for item in Item.objects.all():
        if item.primary_for_package:
            package = item.primary_for_package

            slug_and_suffix = package.slug_key.split('--')

            if len(slug_and_suffix) > 1:
                suffix = slug_and_suffix[-1]

                item_slug = '{}.{}.{}{}'.format(
                    package.hub,
                    '--'.join(slug_and_suffix[:-1]),
                    package.slugified_date,
                    suffix
                )
            else:
                item_slug = '{}.{}.{}'.format(
                    package.hub,
                    package.slug_key,
                    package.slugified_date,
                )

            item.slug_key = package.slug_key

            package.slug_key = ''
            package.save()

        elif item.additional_for_package:
            package = item.additional_for_package

            slug_and_suffix = package.slug_key.split('--')

            if len(slug_and_suffix) > 1:
                suffix = slug_and_suffix[-1]

                item_slug = '{}.{}.{}{}.{}'.format(
                    package.hub,
                    '--'.join(slug_and_suffix[:-1]),
                    package.slugified_date,
                    suffix,
                    item.slug_key
                )
            else:
                item_slug = '{}.{}.{}.{}'.format(
                    package.hub,
                    package.slug_key,
                    package.slugified_date,
                    item.slug_key
                )

        else:
            raise IntegrityError(
                ' '.join([
                    'The budget item "{}" isn\'t connected as either the',
                    'primary piece of content in a package or as an',
                    'additional piece of content.',
                    'Halting migration.'
                ])
            )
        item.slug = item_slug

        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0028_auto_20170820_1830'),
    ]

    operations = [
        migrations.RunPython(forward_func, backward_func)
    ]
