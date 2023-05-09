# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from apps.home import blueprint
from flask import redirect, render_template, request, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound
from .electricity import *
from flask import jsonify
from .asset import *
from .leedsdata import *
from .buildingdata import *
from datetime import datetime
from .electricitydata import *
from .waterdata import *
from .carbondata import *
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
            'material_resources': entry.material_resources,
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
        'material_resources': entry.material_resources,
        'indoor_environmental_quality': entry.indoor_environmental_quality,
        'innovation': entry.innovation,
        'total_leed': entry.total_leed
    }
    return jsonify(result)

# Route to add data input from a form
@blueprint.route('/submit_electricity', methods=['POST'])
def submit_electricity():
    building_id = int(request.form['building_id'])
    date_str = request.form['date']
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    date_obj = date_obj.replace(day=1)
    electricity_usage = int(request.form['electricity_usage'])
    new_electricity = Electricity(building_id=building_id, date=date_obj, electricity_usage=electricity_usage)
    db.session.add(new_electricity)
    db.session.commit()
    return redirect('/')

@blueprint.route('/submit_water', methods=['POST'])
def submit_water():
    building_id = int(request.form['building_id'])
    date_str = request.form['date']
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    date_obj = date_obj.replace(day=1)
    water_usage = int(request.form['water_usage'])
    new_water = Water(building_id=building_id, date=date_obj, water_usage=water_usage)
    db.session.add(new_water)
    db.session.commit()
    return redirect('/')

@blueprint.route('/electricity_usage/<int:building_id>')
def show_electricity_usage_for_building(building_id):
    electricity_usage = Electricity.query.filter_by(building_id=building_id).all()
    return render_template('electricity_usage.html', electricity_usage=electricity_usage)

@blueprint.route('/electricity_usage/recent/<int:building_id>')
def show_electricity_usage_for_recent_date(building_id):
    latest_date = db.session.query(func.max(Electricity.date)).filter_by(building_id=building_id).scalar()
    electricity_usage = Electricity.query.filter_by(building_id=building_id, date=latest_date).first()
 
    if electricity_usage is None:
        return jsonify(error="No data found for building")

    data = {
        "electricity_usage": int(electricity_usage.electricity_usage)
    }

    return (jsonify(data))

#show water usage for building most recent
@blueprint.route('/water_usage/recent/<int:building_id>')
def show_water_usage_for_recent_date(building_id):
    latest_date = db.session.query(func.max(Water.date)).filter_by(building_id=building_id).scalar()
    water_usage = Water.query.filter_by(building_id=building_id, date=latest_date).first()
 
    if water_usage is None:
        return jsonify(error="No data found for building")

    data = {
        "water_usage": int(water_usage.water_usage)
    }

    return (jsonify(data))

#show carbon usage for most recent building
@blueprint.route('/carbon_usage/recent/<int:building_id>')
def show_carbon_usage_for_recent_date(building_id):
    latest_date = db.session.query(func.max(Carbon.date)).filter_by(building_id=building_id).scalar()
    carbon_footprint = Carbon.query.filter_by(building_id=building_id, date=latest_date).first()
 
    if carbon_footprint is None:
        return jsonify(error="No data found for building")

    data = {
        "carbon_footprint": int(carbon_footprint.carbon_footprint)
    }

    return (jsonify(data))

@blueprint.route('/submit_leed', methods=['POST'])
def submit_leed():
    building_id = int(request.form['building_id'])
    location_transportation = int(request.form['location_transportation_1']) + int(request.form['location_transportation_2']) + int(request.form['location_transportation_3'])
    sustainable_sites = int(request.form['sustainable_sites_1']) + int(request.form['sustainable_sites_2']) + int(request.form['sustainable_sites_3']) + int(request.form['sustainable_sites_4']) + int(request.form['sustainable_sites_5']) + int(request.form['sustainable_sites_6']) + int(request.form['sustainable_sites_7'])
    water_efficiency = int(request.form['water_efficiency_1']) + int(request.form['water_efficiency_2']) + int(request.form['water_efficiency_3']) + int(request.form['water_efficiency_4']) + int(request.form['water_efficiency_5'])
    energy_atmosphere = int(request.form['energy_atmosphere_1']) + int(request.form['energy_atmosphere_2']) + int(request.form['energy_atmosphere_3']) + int(request.form['energy_atmosphere_4']) + int(request.form['energy_atmosphere_5']) + int(request.form['energy_atmosphere_6']) + int(request.form['energy_atmosphere_7']) + int(request.form['energy_atmosphere_8']) + int(request.form['energy_atmosphere_9']) + int(request.form['energy_atmosphere_10']) + int(request.form['energy_atmosphere_11']) + int(request.form['energy_atmosphere_12'])
    material_resources = int(request.form['material_resources_1']) + int(request.form['material_resources_2']) + int(request.form['material_resources_3']) + int(request.form['material_resources_4'])+ int(request.form['material_resources_5'])
    indoor_environmental_quality = int(request.form['indoor_environmental_quality_1']) + int(request.form['indoor_environmental_quality_2']) + int(request.form['indoor_environmental_quality_3']) + int(request.form['indoor_environmental_quality_4']) + int(request.form['indoor_environmental_quality_5']) + int(request.form['indoor_environmental_quality_6']) + int(request.form['indoor_environmental_quality_7']) + int(request.form['indoor_environmental_quality_8']) + int(request.form['indoor_environmental_quality_9']) + int(request.form['indoor_environmental_quality_10']) + int(request.form['indoor_environmental_quality_11']) + int(request.form['indoor_environmental_quality_12']) + int(request.form['indoor_environmental_quality_13'])
    innovation = int(request.form['innovation_1']) + int(request.form['innovation_2']) 
    total_leed = location_transportation + sustainable_sites + water_efficiency + energy_atmosphere + material_resources + indoor_environmental_quality + innovation
    date_str = request.form['date']
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    date_obj = date_obj.replace(day=1)
    
    leed = Leed(building_id=building_id,
                location_transportation=location_transportation,
                sustainable_sites=sustainable_sites,
                water_efficiency=water_efficiency,
                energy_atmosphere=energy_atmosphere,
                materials_resources=material_resources,
                indoor_environmental_quality=indoor_environmental_quality,
                innovation=innovation,
                total_leed=total_leed,
                date=date_obj)
    print(leed)
    try:
        db.session.add(leed)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_info = str(e.__dict__.get('orig', e))
        return render_template('home/leeds.html', show_warning=True)
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
