# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from .electricity import get_predicted_kwh, get_actual_kwh, get_predicted_cf, get_actual_cf, get_actual_liter, get_predicted_liter
from flask import jsonify
from .asset import *

"""
add predicted_kwh from electricity.py to the render_template so it can be used in building-data.html
"""

@blueprint.route('/building-data/<building>')
@login_required
def building_data(building):
    predicted_kwh = get_predicted_kwh(building)
    actual_kwh = get_actual_kwh(building)
    predicted_liter = get_predicted_liter(building)
    actual_liter = get_actual_liter(building)
    predicted_cf = get_predicted_cf(building)
    actual_cf = get_actual_cf(building)
    return jsonify(predicted_kwh=predicted_kwh, actual_kwh=actual_kwh, predicted_liter=predicted_liter, actual_liter=actual_liter, predicted_cf=predicted_cf, actual_cf=actual_cf)

@blueprint.route('/category_data/<category>')
@login_required
def category_data(category):
    category_details = get_category_details(category)
    return jsonify(category_details=category_details)

@blueprint.route('/tabel_form/<year>/<category>')
@login_required
def table_form(year, category):
    tabel_form_predicted = get_tabel_form_predicted(year, category)
    return jsonify(tabel_form_predicted=tabel_form_predicted)

@blueprint.route('/init/<year>/<category>')
@login_required
def init_future(year, category):
    initiative = initiatives(year, category)
    return jsonify(initiative=initiative)

@blueprint.route('/asset_data_pie/<category>/<target>')
@login_required
def category_data_pie(category, target):
    subcategory_array, target_array = pie_get_category(category, target)
    return jsonify(subcategory_array=subcategory_array, target_array=target_array)

@blueprint.route('/asset_data_pie_predicted/<year>/<category>/<target>')
@login_required
def category_data_pie_predicted(year, category, target):
    subcategory_array, target_array = pie_get_category_predicted(year, category, target)
    return jsonify(subcategory_array=subcategory_array, target_array=target_array)

@blueprint.route('/asset')
@login_required
def asset():
    counts = stacked_count_category()
    return jsonify(counts)


@blueprint.route('/donut-data')
def pie_data():
    data = pie_count_category()
    return jsonify(data)

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
