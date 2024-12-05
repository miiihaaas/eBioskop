from datetime import datetime, timedelta, date
from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_mail import Message, Mail
from sqlalchemy import desc, func
from ebioskop import app, db, cache
from ebioskop.main.functions import get_cinema_week, get_empty_totals, validate_week_param, validate_year_param, update_box_office_data, format_box_office_data, calculate_totals
from ebioskop.models import CinemaHall, Movie, Projection, BoxOfficeWeekly, Distributor
import os
import json
import logging

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    route_name = request.endpoint
    return render_template('home.html', route_name=route_name)


@main.route('/faq', methods=['GET', 'POST'])
def faq():
    route_name = request.endpoint
    return render_template('faq.html', route_name=route_name)




@main.route('/box_office', methods=['GET'])
# @cache.cached(timeout=300)  # Privremeno isključujemo keširanje
def box_office():
    # Postavljanje log level-a na DEBUG za trenutni request
    app.logger.setLevel(logging.DEBUG)
    
    route_name = request.endpoint
    app.logger.info("Pristup box_office ruti")
    app.logger.info(f"URL argumenti: {request.args}")
    
    try:
        # Validacija parametara
        app.logger.info("Dobavljanje trenutne bioskopske nedelje")
        current_week, current_year = get_cinema_week()
        app.logger.info(f"Trenutna nedelja: {current_week}, godina: {current_year}")
        
        # Logovanje raw parametara
        raw_week = request.args.get('week')
        raw_year = request.args.get('year')
        app.logger.debug(f"Raw parametri iz URL-a: week={raw_week}, year={raw_year}")
        
        selected_week = validate_week_param(request.args.get('week', type=int, default=current_week))
        selected_year = validate_year_param(request.args.get('year', type=int, default=current_year))
        app.logger.info(f"Izabrana nedelja: {selected_week}, godina: {selected_year}")
        
        # Provera da li postoje box office podaci za izabranu nedelju
        app.logger.info("Provera postojanja box office podataka")
        box_office_exists = BoxOfficeWeekly.query.filter_by(
            year=selected_year, 
            week=selected_week
        ).first() is not None
        app.logger.info(f"Box office podaci postoje: {box_office_exists}")

        # Ako ne postoje podaci, ažuriramo ih
        if not box_office_exists:
            app.logger.info("Nema podataka, pokretanje ažuriranja")
            success = update_box_office_data(selected_week, selected_year)
            app.logger.info(f"Rezultat ažuriranja: {success}")
            if not success:
                app.logger.warning(f'Nema podataka za nedelju {selected_week} u {selected_year}. godini')
                flash(f'Nema podataka za nedelju {selected_week} u {selected_year}. godini', 'info')
                return render_template('box_office.html',
                                    route_name=route_name,
                                    movies=[],
                                    totals=get_empty_totals(),
                                    years=range(2020, datetime.now().year + 1),
                                    current_year=selected_year,
                                    current_week=selected_week)

        # Paginacija
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        app.logger.info(f"Paginacija: strana {page}, po strani {per_page}")
        
        # Dobavljanje box office podataka
        app.logger.info("Dobavljanje box office podataka")
        box_office_data = BoxOfficeWeekly.query.options(db.joinedload(BoxOfficeWeekly.movie)).filter_by(year=selected_year, week=selected_week)\
            .order_by(BoxOfficeWeekly.position)\
            .paginate(page=page, per_page=per_page, error_out=False)
            
        app.logger.info(f"Broj pronađenih zapisa: {len(box_office_data.items) if box_office_data.items else 0}")
            
        if not box_office_data.items:
            app.logger.warning(f'Nema podataka za nedelju {selected_week} u {selected_year}. godini')
            flash(f'Nema podataka za nedelju {selected_week} u {selected_year}. godini', 'info')
            return render_template('box_office.html',
                                route_name=route_name,
                                movies=[],
                                totals=get_empty_totals(),
                                years=range(2020, datetime.now().year + 1),
                                current_year=selected_year,
                                current_week=selected_week)
        
        # Formatiranje podataka za prikaz
        app.logger.info("Formatiranje podataka za prikaz")
        movies_data = format_box_office_data(box_office_data.items)
        totals = calculate_totals(box_office_data.items)
        app.logger.info(f"Formatirano {len(movies_data)} filmova")
        app.logger.debug("Movies data:")
        for movie in movies_data:
            app.logger.debug(f"Movie: {movie}")
        
        return render_template('box_office.html',
                            route_name=route_name,
                            movies=movies_data,
                            totals=totals,
                            pagination=box_office_data,
                            years=range(2020, datetime.now().year + 1),
                            current_year=selected_year,
                            current_week=selected_week)
                            
    except ValueError as e:
        app.logger.error(f"ValueError u box_office ruti: {str(e)}")
        flash(str(e), 'error')
        return redirect(url_for('main.box_office'))
    except Exception as e:
        app.logger.error(f"Neočekivana greška u box_office ruti: {str(e)}")
        app.logger.exception(e)  # Ovo će ispisati kompletan stack trace
        flash('Došlo je do greške prilikom učitavanja podataka', 'error')
        return redirect(url_for('main.home'))

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    route_name = request.endpoint
    return render_template('contact.html', route_name=route_name)