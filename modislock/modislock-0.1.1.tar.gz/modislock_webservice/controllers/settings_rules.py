# coding: utf-8

# Flask
from flask import render_template, Blueprint, request, redirect, url_for, current_app
from flask_security import login_required
from modislock_webservice.forms import GlobalTimeSettingsForm

# Database
from modislock_webservice.models import db, SettingsValues, Settings
from sqlalchemy import or_
from sqlalchemy.exc import InternalError, IntegrityError

# OS
from datetime import datetime


bp = Blueprint('settings_rules', __name__)


def save_glob_rules_settings(form):
    """Saves various global rule(s) settings to database

    :param form form:
    """

    old_settings = get_glob_rules_settings()
    keys = set(old_settings.keys())

    new_settings = dict()
    new_settings['GLOBAL_DAYS'] = 0b00000001 if form.glob_mon.data == 1 else 0b00000000
    new_settings['GLOBAL_DAYS'] = new_settings.get('GLOBAL_DAYS') | (1 << 1) if form.glob_tue.data == 1 else new_settings.get('GLOBAL_DAYS') & ~(1 << 1)
    new_settings['GLOBAL_DAYS'] = new_settings.get('GLOBAL_DAYS') | (1 << 2) if form.glob_wed.data == 1 else new_settings.get('GLOBAL_DAYS') & ~(1 << 2)
    new_settings['GLOBAL_DAYS'] = new_settings.get('GLOBAL_DAYS') | (1 << 3) if form.glob_thr.data == 1 else new_settings.get('GLOBAL_DAYS') & ~(1 << 3)
    new_settings['GLOBAL_DAYS'] = new_settings.get('GLOBAL_DAYS') | (1 << 4) if form.glob_fri.data == 1 else new_settings.get('GLOBAL_DAYS') & ~(1 << 4)
    new_settings['GLOBAL_DAYS'] = new_settings.get('GLOBAL_DAYS') | (1 << 5) if form.glob_sat.data == 1 else new_settings.get('GLOBAL_DAYS') & ~(1 << 5)
    new_settings['GLOBAL_DAYS'] = new_settings.get('GLOBAL_DAYS') | (1 << 6) if form.glob_sun.data == 1 else new_settings.get('GLOBAL_DAYS') & ~(1 << 6)

    # start_time = datetime.strptime("2017-07-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    # new_settings['GLOBAL_START_TIME'] = str(datetime(2000, 7, 1, form.glob_start_hour.data, form.glob_start_min.data, 00))
    new_settings['GLOBAL_START_TIME'] = str('{:02d}'.format(form.glob_start_hour.data))+':'+str('{:02d}'.format(form.glob_start_min.data))+":00"

    # stop_time = datetime.strptime(old_settings.get('GLOBAL_END_TIME', "2017-07-01 03:04:05"), "%Y-%m-%d %H:%M:%S")
    # new_stop_time = stop_time.replace(hour=form.glob_stop_hour.data, minute=form.glob_stop_min.data)
    new_settings['GLOBAL_END_TIME'] = str('{:02d}'.format(form.glob_stop_hour.data))+':'+str('{:02d}'.format(form.glob_stop_min.data))+":00"

    for key in keys:
        try:
            new_value = new_settings[key]
            record = Settings.query.filter(Settings.settings_name == key).first()
            record = SettingsValues.query.filter(SettingsValues.settings_id_settings == record.id_settings).first()

            if record is not None:
                record.value = new_value
                db.session.commit()
        except KeyError:
            continue


def get_glob_rules_settings():
    """Retrieves the global rule(s) settings from database

    :return dict glob_rules_settings:
    """

    glob_rules_settings = dict()

    # DEFAULT VALUES
    # glob_rules_settings['GLOBAL_DAYS'] = 0b01010101
    # glob_rules_settings['GLOBAL_START_TIME'] = "02:03:04"
    # glob_rules_settings['GLOBAL_END_TIME'] = "05:06:07"

    _glob_rules = Settings.query \
        .join(SettingsValues, Settings.id_settings == SettingsValues.settings_id_settings) \
        .filter(Settings.settings_name.like('GLOBAL%')) \
        .with_entities(Settings.settings_name, Settings.units, SettingsValues.value) \
        .all()

    for setting in _glob_rules:
        name = setting[0]

        if setting[1] == 'time':
            value= str(setting[2])
        elif setting[1] == 'integer':
            value = int(setting[2])

        glob_rules_settings[name] = value

    return glob_rules_settings


@bp.route('/settings/rules', methods=['GET', 'POST'])
@login_required
def rules_settings():
    """Route to rule settings

    :return html settings_rules.html:
    """
    form = GlobalTimeSettingsForm()

    if request.method == 'POST':
        if form.validate():
            save_glob_rules_settings(form)

    # Global Rule(s) Settings
    try:
        settings = get_glob_rules_settings()
    except Exception as e:
        current_app.logger.error(e)
    else:
        weekdays = settings.get('GLOBAL_DAYS')

        form.glob_mon.data = True if ((weekdays & (1 << 0)) >> 0) else False
        form.glob_tue.data = True if ((weekdays & (1 << 1)) >> 1) else False
        form.glob_wed.data = True if ((weekdays & (1 << 2)) >> 2) else False
        form.glob_thr.data = True if ((weekdays & (1 << 3)) >> 3) else False
        form.glob_fri.data = True if ((weekdays & (1 << 4)) >> 4) else False
        form.glob_sat.data = True if ((weekdays & (1 << 5)) >> 5) else False
        form.glob_sun.data = True if ((weekdays & (1 << 6)) >> 6) else False

        # start_time = datetime.strptime( glob_rules_settings.get('GLOBAL_START_TIME'), "%Y-%m-%d %H:%M:%S")
        start_time = datetime.strptime(settings.get('GLOBAL_START_TIME'), "%H:%M:%S")
        form.glob_start_hour.data = start_time.hour
        form.glob_start_min.data = start_time.minute

        # stop_time = datetime.strptime( glob_rules_settings.get('GLOBAL_END_TIME'), "%Y-%m-%d %H:%M:%S")
        stop_time = datetime.strptime(settings.get('GLOBAL_END_TIME'), "%H:%M:%S")
        form.glob_stop_hour.data = stop_time.hour
        form.glob_stop_min.data = stop_time.minute

    return render_template('settings_rules/settings_rules.html', form=form)
