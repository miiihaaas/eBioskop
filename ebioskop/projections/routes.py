from calendar import monthrange
from datetime import datetime, date
import json
from flask import Blueprint, render_template, request, url_for, flash, redirect, jsonify
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload
from ebioskop import app, db
from ebioskop.models import Cinema, CinemaHall, CinemaProperties, Movie, Projection
from ebioskop.projections.forms import AddProjectionForm
from ebioskop.projections.functions import send_projection_notification_email


projections = Blueprint('projections', __name__)


from flask import request, jsonify
from sqlalchemy import extract

# @projections.route('/projections_list', methods=['GET'])
# @login_required
# def projections_list():
#     route_name = request.endpoint
    
#     # Dobijanje filter parametara
#     movie_id = request.args.get('film')
#     date_from = request.args.get('date_from')
#     date_to = request.args.get('date_to')
#     filter_format = request.args.get('filter_format')
#     version = request.args.get('verzija')
    
#     # Kreiranje osnovnog upita
#     query = Projection.query
    
#     if current_user.user_type == 'cinema':
#         query = query.join(CinemaHall).filter(
#             CinemaHall.cinema_properties_id == current_user.cinema_properties_id
#         )
    
#     # Primena filtera
#     if movie_id:
#         query = query.filter(Projection.movie_id == movie_id)
#     if date_from:
#         year, month = map(int, date_from.split('-'))
#         query = query.filter(extract('year', Projection.date) >= year,
#                             extract('month', Projection.date) >= month)
#     if date_to:
#         year, month = map(int, date_to.split('-'))
#         query = query.filter(extract('year', Projection.date) <= year,
#                             extract('month', Projection.date) <= month)
#     if filter_format:
#         query = query.filter(Projection.format == filter_format)
#     if version:
#         query = query.filter(Projection.version == version)
    
#     projections_list = query.options(joinedload(Projection.movie)).all()
    
#     movies = Movie.query.filter(Movie.release_date <= datetime.date.today()).all()
#     movies_data = [{
#         'id': movie.id,
#         'versions': movie.versions,
#         'projection_formats': movie.projection_formats
#     } for movie in movies]
    
#     add_form = AddProjectionForm()
#     add_form.movie_id.choices = [(movie.id, movie.local_title) for movie in movies]
#     add_form.cinema_hall_id.choices = [(hall.id, hall.hall_name) for hall in CinemaHall.query.filter_by(cinema_properties_id=current_user.cinema_properties_id).all()]
    
#     return render_template('projections_list.html', 
#                             route_name=route_name,
#                             projections_list=projections_list,
#                             add_form=add_form,
#                             movies_data=movies_data,
#                             movies=movies,
#                             filters={
#                                 'movie_id': movie_id,
#                                 'date_from': date_from,
#                                 'date_to': date_to,
#                                 'filter_format': filter_format,
#                                 'version': version
#                             })


@projections.route('/cinema_projections_list', methods=['GET'])
@login_required
def cinema_projections_list():
    """
    Prikazuje listu bioskopa za korisnike sa proširenim pravima pristupa.
    Ovo je početna strana gde korisnici biraju bioskop.
    """
    if current_user.user_type not in ['admin', 'user']:
        flash('Nemate pristup ovoj stranici.', 'danger')
        return redirect(url_for('main.home'))
        
    # Dohvatamo sve bioskope
    cinemas_list = Cinema.query.join(CinemaProperties).all()
    
    return render_template('cinema_projections_list.html', 
                         cinemas=cinemas_list,
                         route_name=request.endpoint)

@projections.route('/projections_list', methods=['GET'])
@login_required
def projections_list():
    """
    Prikazuje projekcije za određeni bioskop.
    Za prikazivače prikazuje njihove projekcije.
    Za korisnike prikazuje projekcije izabranog bioskopa.
    """
    route_name = request.endpoint
    
    # Dobijanje filter parametara
    movie_id = request.args.get('film')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    filter_format = request.args.get('filter_format')
    version = request.args.get('verzija')
    cinema_properties_id = request.args.get('cinema_properties_id')
    
    # Ako nisu postavljeni datumi, postavljamo tekući mesec
    if not date_from and not date_to:
        today = date.today()
        date_from = f"{today.year}-{today.month:02d}"
        date_to = f"{today.year}-{today.month:02d}"
    
    # Inicijalizacija varijabli
    cinema_info = None
    add_form = None
    
    # Kreiranje osnovnog upita
    query = Projection.query
    
    # Različita logika za različite tipove korisnika
    if current_user.user_type == 'cinema':
        # Prikazivač vidi samo svoje projekcije
        query = query.join(CinemaHall).filter(
            CinemaHall.cinema_properties_id == current_user.cinema_properties_id
        )
        
        # Forma za dodavanje projekcije samo za prikazivače
        movies = Movie.query.filter(Movie.release_date <= date.today()).all()
        add_form = AddProjectionForm()
        add_form.movie_id.choices = [(movie.id, movie.local_title) for movie in movies]
        add_form.cinema_hall_id.choices = [(hall.id, hall.hall_name) 
                                         for hall in CinemaHall.query.filter_by(
                                             cinema_properties_id=current_user.cinema_properties_id
                                         ).all()]
        
    elif current_user.user_type in ['user', 'admin']:
        if not cinema_properties_id:
            flash('Morate izabrati bioskop.', 'warning')
            return redirect(url_for('cinemas.cinema_projections_list'))
        
        # Korisnik vidi projekcije izabranog bioskopa
        query = query.join(CinemaHall).filter(
            CinemaHall.cinema_properties_id == cinema_properties_id
        )
        
        # Dohvatamo informacije o bioskopu
        cinema_props = CinemaProperties.query.get(cinema_properties_id)
        if cinema_props and cinema_props.cinema:
            cinema_info = cinema_props.cinema
    else:
        flash('Nemate pristup ovoj stranici.', 'danger')
        return redirect(url_for('main.home'))
    
    # Primena filtera
    if movie_id:
        query = query.filter(Projection.movie_id == movie_id)
    if date_from:
        year, month = map(int, date_from.split('-'))
        first_day = date(year, month, 1)
        query = query.filter(Projection.date >= first_day)
    if date_to:
        year, month = map(int, date_to.split('-'))
        _, last_day = monthrange(year, month)
        last_date = date(year, month, last_day)
        query = query.filter(Projection.date <= last_date)
    if filter_format:
        query = query.filter(Projection.format == filter_format)
    if version:
        query = query.filter(Projection.version == version)
    
    # Sortiramo projekcije po datumu i vremenu
    query = query.order_by(Projection.date.desc(), Projection.time.desc())
    
    # Dohvatamo projekcije
    projections_list = query.options(joinedload(Projection.movie)).all()
    
    # Dohvatamo sve filmove za filter
    movies = Movie.query.filter(Movie.release_date <= date.today()).all()
    movies_data = [{
        'id': movie.id,
        'versions': movie.versions,
        'projection_formats': movie.projection_formats
    } for movie in movies]
    
    return render_template('projections_list.html', 
                            route_name=route_name,
                            projections_list=projections_list,
                            add_form=add_form,
                            movies_data=movies_data,
                            movies=movies,
                            cinema_properties_id=cinema_properties_id,
                            cinema_info=cinema_info,
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
    if current_user.user_type not in ['cinema']:
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
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
        try:
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
            # Dohvatamo potrebne podatke za email
            movie = Movie.query.get(add_form.movie_id.data)
            cinema_hall = CinemaHall.query.get(add_form.cinema_hall_id.data)
            cinema = cinema_hall.cinema_properties.cinema
            
            # Šaljemo email obaveštenje
            email_sent = send_projection_notification_email(new_projection, movie, cinema, cinema_hall)
            
            if email_sent:
                flash('Projekcija je uspešno dodata i obaveštenje je poslato distributeru!', 'success')
            else:
                flash('Projekcija je dodata, ali nije bilo moguće poslati obaveštenje distributeru.', 'warning')
        except Exception as e:
            db.session.rollback()
            flash(f'Došlo je do greške prilikom dodavanja projekcije: {str(e)}', 'danger')
            return redirect(url_for('projections.projections_list'))
        # flash('Projekcija je uspešno dodata!', 'success')
        # return redirect(url_for('projections.projections_list'))
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
    try:
        projection = Projection.query.get_or_404(projection_id)
        
        # Pronalazimo prvu i poslednju projekciju za ovaj film
        first_projection = Projection.query.filter_by(movie_id=projection.movie_id).order_by(Projection.date).first()
        last_projection = Projection.query.filter_by(movie_id=projection.movie_id).order_by(Projection.date.desc()).first()
        
        if first_projection and last_projection:
            # Računamo broj nedelja od prve do poslednje projekcije
            weeks_showing = ((last_projection.date - first_projection.date).days // 7) + 1
        else:
            weeks_showing = 0
            
        # Ukupan broj projekcija
        total_screenings = Projection.query.filter_by(movie_id=projection.movie_id).count()
        
        return jsonify({
            'movie_title': projection.movie.local_title,
            'weeks_showing': weeks_showing,
            'total_screenings': total_screenings
        })
        
    except Exception as e:
        flash(f"Greška pri dobavljanju detalja projekcije: {str(e)}", 'danger')
        return jsonify({'error': 'Došlo je do greške prilikom učitavanja detalja'}), 500