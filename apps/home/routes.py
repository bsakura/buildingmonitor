# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from sqlalchemy import func
from apps.home import blueprint
from flask import redirect, render_template, request, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound
from .electricity import get_predicted_kwh, get_actual_kwh, get_predicted_cf, get_actual_cf, get_actual_liter, get_predicted_liter
from flask import jsonify
from .asset import *
from .leedsdata import *
from .buildingdata import *
from datetime import datetime
from .electricitydata import *
import logging


"""
add predicted_kwh from electricity.py to the render_template so it can be used in building-data.html
"""
# add logger
LOG = logging.getLogger(__name__)



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


# Route to get all Leed entries
@blueprint.route('/leed', methods=['GET'])
def get_leed():
    leed = Leed.query.all()
    results = []
    for entry in leed:
        result = {
            'building_id': entry.building_id,
            'location_transportation': entry.location_transportation,
            'sustainable_sites': entry.sustainable_sites,
            'water_efficiency': entry.water_efficiency,
            'energy_atmosphere': entry.energy_atmosphere,
            'materials_resources': entry.materials_resources,
            'indoor_environmental_quality': entry.indoor_environmental_quality,
            'innovation': entry.innovation,
            'total_leed': entry.total_leed
        }
        results.append(result)
    return jsonify(results)

# Route to get a specific Leed entry by building ID
@blueprint.route('/leed/<int:building_id>', methods=['GET'])
def get_leed_by_id(building_id):
    entry = Leed.query.filter_by(building_id=building_id).first()
    if not entry:
        return jsonify({'message': 'Leed entry not found'})
    result = {
        'building_id': entry.building_id,
        'location_transportation': entry.location_transportation,
        'sustainable_sites': entry.sustainable_sites,
        'water_efficiency': entry.water_efficiency,
        'energy_atmosphere': entry.energy_atmosphere,
        'materials_resources': entry.materials_resources,
        'indoor_environmental_quality': entry.indoor_environmental_quality,
        'innovation': entry.innovation,
        'total_leed': entry.total_leed
    }
    return jsonify(result)

# Route to add data input from a form
@blueprint.route('/submit_electricity', methods=['POST'])
def submit_electricity():
    building_id = request.form['building_id']
    date_str = request.form['date']
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    electricity_usage = int(request.form['electricity_usage'])
    new_electricity = Electricity(building_id=building_id, date=date_obj, electricity_usage=electricity_usage)
    db.session.add(new_electricity)
    db.session.commit()
    return redirect('/')

@blueprint.route('/electricity_usage/<int:building_id>')
def show_electricity_usage_for_building(building_id):
    electricity_usage = Electricity.query.filter_by(building_id=building_id).all()
    return render_template('electricity_usage.html', electricity_usage=electricity_usage)

@blueprint.route('/electricity_usage/recent/<int:building_id>')
def show_electricity_usage_for_recent_date(building_id):
    latest_date = db.session.query(func.max(Electricity.date)).filter_by(building_id=building_id).scalar()
    LOG.info("latest_date: %s", latest_date)
    electricity_usage = Electricity.query.filter_by(building_id=building_id, date=latest_date).first()
    LOG.info("ASD")
    LOG.info(electricity_usage)

    if electricity_usage is None:
        return jsonify(error="No data found for building")

    # Create a dictionary containing the relevant information
    data = {
        # "building_id": electricity_usage.building_id,
        # "date": electricity_usage.date.isoformat(),
        "electricity_usage": int(electricity_usage.electricity_usage)
    }

    # jsonify electricity_usage
    LOG.info("fsa")
    LOG.info((data))
    LOG.info("bbb")
    LOG.info((data['electricity_usage']))


    # LOG.info("data: %s", data)

    return (jsonify(data))




@blueprint.route('/submit_leed', methods=['POST'])
def submit_leed():
    building_id = request.form['building_id']
    location_transportation = int(request.form['location_transportation'])
    sustainable_sites = int(request.form['sustainable_sites_1']) + int(request.form['sustainable_sites_2'])
    water_efficiency = int(request.form['water_efficiency'])
    energy_atmosphere = int(request.form['energy_atmosphere'])
    materials_resources = int(request.form['materials_resources'])
    indoor_environmental_quality = int(request.form['indoor_environmental_quality'])
    innovation = int(request.form['innovation'])
    total_leed = location_transportation + sustainable_sites + water_efficiency + energy_atmosphere + materials_resources + indoor_environmental_quality + innovation
    date_str = request.form['date']
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    leed = Leed(building_id=building_id,
                location_transportation=location_transportation,
                sustainable_sites=sustainable_sites,
                water_efficiency=water_efficiency,
                energy_atmosphere=energy_atmosphere,
                materials_resources=materials_resources,
                indoor_environmental_quality=indoor_environmental_quality,
                innovation=innovation,
                total_leed=total_leed,
                date=date_obj)
    print(leed)
    db.session.add(leed)
    db.session.commit()
    
    return redirect('/')


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
