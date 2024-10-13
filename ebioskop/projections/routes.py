import json
from flask import Blueprint, render_template, request, url_for, flash, redirect, jsonify
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload
from ebioskop import app, db
from ebioskop.models import Cinema, CinemaHall, CinemaProperties, Movie, Projection
from ebioskop.projections.forms import AddProjectionForm


projections = Blueprint('projections', __name__)


@projections.route('/projections_list', methods=['GET'])
@login_required
def projections_list():
    route_name = request.endpoint
    if current_user.user_type == 'admin':
        projections_list = Projection.query.all()
    elif current_user.user_type == 'cinema':
        # projections_list = Projection.query.join(CinemaHall).join(CinemaProperties).join(Cinema).filter(Cinema.id == current_user.cinema_id).options(joinedload(Projection.movie)).all()
        projections_list = Projection.query.join(CinemaHall).filter(
            CinemaHall.cinema_properties_id == current_user.cinema_properties_id
        ).options(joinedload(Projection.movie)).all()
    else:
        flash('Nemate pravo pristupa ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    movies = Movie.query.all()
    movies_data = [{
        'id': movie.id,
        'versions': movie.versions,
        'projection_formats': movie.projection_formats
    } for movie in movies]
    
    add_form = AddProjectionForm()
    # Popunjavamo opcije za filmove
    add_form.movie_id.choices = [(movie.id, movie.local_title) for movie in movies]
    # Popunjavamo opcije za bioskopske sale
    add_form.cinema_hall_id.choices = [(hall.id, hall.hall_name) for hall in CinemaHall.query.filter_by(cinema_properties_id=current_user.cinema_properties_id).all()]
    return render_template('projections_list.html', 
                            route_name=route_name,
                            projections_list=projections_list,
                            add_form=add_form,
                            movies_data=movies_data
                            )


@projections.route('/projections/add_projection', methods=['POST'])
@login_required
def add_projection():
    movies = Movie.query.all()
    add_form = AddProjectionForm()
    add_form.movie_id.choices = [(movie.id, movie.local_title) for movie in movies]
    add_form.cinema_hall_id.choices = [(hall.id, hall.hall_name) for hall in CinemaHall.query.filter_by(cinema_properties_id=current_user.cinema_properties_id).all()]
    
    print(f'{add_form.data=}')
    
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