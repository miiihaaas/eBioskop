import datetime
import json
from flask import Blueprint, render_template, request, url_for, flash, redirect, jsonify
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload
from ebioskop import app, db
from ebioskop.models import Cinema, CinemaHall, CinemaProperties, Movie, Projection
from ebioskop.projections.forms import AddProjectionForm


projections = Blueprint('projections', __name__)


from flask import request, jsonify
from sqlalchemy import extract

@projections.route('/projections_list', methods=['GET'])
@login_required
def projections_list():
    route_name = request.endpoint
    
    # Dobijanje filter parametara
    movie_id = request.args.get('film')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    filter_format = request.args.get('filter_format')
    version = request.args.get('verzija')
    
    # Kreiranje osnovnog upita
    query = Projection.query
    
    if current_user.user_type == 'cinema':
        query = query.join(CinemaHall).filter(
            CinemaHall.cinema_properties_id == current_user.cinema_properties_id
        )
    
    # Primena filtera
    if movie_id:
        query = query.filter(Projection.movie_id == movie_id)
    if date_from:
        year, month = map(int, date_from.split('-'))
        query = query.filter(extract('year', Projection.date) >= year,
                            extract('month', Projection.date) >= month)
    if date_to:
        year, month = map(int, date_to.split('-'))
        query = query.filter(extract('year', Projection.date) <= year,
                            extract('month', Projection.date) <= month)
    if filter_format:
        query = query.filter(Projection.format == filter_format)
    if version:
        query = query.filter(Projection.version == version)
    
    projections_list = query.options(joinedload(Projection.movie)).all()
    
    movies = Movie.query.filter(Movie.release_date <= datetime.date.today()).all()
    movies_data = [{
        'id': movie.id,
        'versions': movie.versions,
        'projection_formats': movie.projection_formats
    } for movie in movies]
    
    add_form = AddProjectionForm()
    add_form.movie_id.choices = [(movie.id, movie.local_title) for movie in movies]
    add_form.cinema_hall_id.choices = [(hall.id, hall.hall_name) for hall in CinemaHall.query.filter_by(cinema_properties_id=current_user.cinema_properties_id).all()]
    
    return render_template('projections_list.html', 
                            route_name=route_name,
                            projections_list=projections_list,
                            add_form=add_form,
                            movies_data=movies_data,
                            movies=movies,
                            filters={
                                'movie_id': movie_id,
                                'date_from': date_from,
                                'date_to': date_to,
                                'filter_format': filter_format,
                                'version': version
                            })


@projections.route('/projections/add_projection', methods=['POST'])
@login_required
def add_projection():
    movies = Movie.query.all()
    add_form = AddProjectionForm()
    add_form.movie_id.choices = [(movie.id, movie.local_title) for movie in movies]
    add_form.cinema_hall_id.choices = [(hall.id, hall.hall_name) for hall in CinemaHall.query.filter_by(cinema_properties_id=current_user.cinema_properties_id).all()]
    
    print(f'{add_form.data=}')
    
    existing_projection = Projection.query.filter_by(
        date=add_form.date.data,
        time=add_form.time.data,
        version=add_form.version.data,
        format=add_form.format.data,
        movie_id=add_form.movie_id.data,
        cinema_hall_id=add_form.cinema_hall_id.data
    ).first()
    
    if existing_projection:
        flash('Projekcija sa unetim parametrima vec postoji. Pokusajte ponovo.', 'danger')
        return redirect(url_for('projections.projections_list'))
    
    if add_form.validate_on_submit():
        new_projection = Projection(
            date=add_form.date.data,
            time=add_form.time.data,
            version=add_form.version.data,
            format=add_form.format.data,
            tickets_sold=add_form.tickets_sold.data,
            revenue=add_form.revenue.data,
            movie_id=add_form.movie_id.data,
            cinema_hall_id=add_form.cinema_hall_id.data
        )
        db.session.add(new_projection)
        db.session.commit()
        flash('Projekcija je uspešno dodata!', 'success')
        return redirect(url_for('projections.projections_list'))
    else:
        for field, errors in add_form.errors.items():
            for error in errors:
                flash(f"Greška u polju {getattr(add_form, field).label.text}: {error}", 'danger')
    
    return redirect(url_for('projections.projections_list'))


@projections.route('/projections/delete_projection/<int:projection_id>', methods=['GET', 'POST'])
@login_required
def delete_projection(projection_id):
    projection = Projection.query.get_or_404(projection_id)
    db.session.delete(projection)
    db.session.commit()
    flash('Projekcija je uspešno obrisana!', 'success')
    return redirect(url_for('projections.projections_list'))


@projections.route('/projections/details/<int:projection_id>')
@login_required
def projection_details(projection_id):
    projection = Projection.query.get_or_404(projection_id)
    
    # Izračunavanje broja nedelja prikazivanja i ukupnog broja prikazivanja
    # Ovo je primer logike, trebalo bi je prilagoditi stvarnim potrebama
    weeks_showing = (datetime.date.today() - projection.movie.release_date).days // 7 + 1
    total_screenings = Projection.query.filter_by(movie_id=projection.movie_id).count()
    
    return jsonify({
        'movie_title': projection.movie.local_title,
        'date': projection.date.strftime('%d.%m.%Y'),
        'time': projection.time.strftime('%H:%M'),
        'version': projection.version,
        'format': projection.format,
        'tickets_sold': projection.tickets_sold,
        'revenue': projection.revenue,
        'weeks_showing': weeks_showing,
        'total_screenings': total_screenings
    })