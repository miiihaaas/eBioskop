from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import current_user
from ebioskop import app, db
from ebioskop.models import Distributor, Movie
from ebioskop.distributors.forms import EditDistributorForm, RegisterDistributorForm
from ebioskop.movies.forms import EditMovieForm, RegisterMovieForm


movies = Blueprint('movies', __name__)


@movies.route('/movies_list', methods=['GET', 'POST'])
def movies_list():
    route_name = request.endpoint
    
    # Provera da li je korisnik autentifikovan
    if not current_user.is_authenticated:
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('users.login'))
    
    # Kreiranje i instanciranje formi
    register_form = RegisterMovieForm()
    edit_form = EditMovieForm()

    # Dinamički napuni SelectField opcije za produkciju zemalja i žanrove
    register_form.production_country.choices = [("USA", "USA"), ("UK", "UK"), ("France", "France")]
    edit_form.production_country.choices = register_form.production_country.choices
    register_form.genres.choices = [("Drama", "Drama"), ("Action", "Action"), ("Comedy", "Comedy")]
    edit_form.genres.choices = register_form.genres.choices

    # Kreiranje novog filma
    if register_form.validate_on_submit():
        if 'submit' in request.form:
            new_movie = Movie(
                original_title=register_form.original_title.data,
                local_title=register_form.local_title.data,
                director=register_form.director.data,
                actors=register_form.actors.data,
                production_country=register_form.production_country.data,
                production_company=register_form.production_company.data,
                production_year=register_form.production_year.data,
                duration=register_form.duration.data,
                versions=register_form.versions.data,
                projection_formats=register_form.projection_formats.data,
                poster=register_form.poster.data,
                images=[register_form.image_1.data, register_form.image_2.data, register_form.image_3.data],
                trailer_link=register_form.trailer_link.data,
                synopsis=register_form.synopsis.data,
                genres=register_form.genres.data,
                release_date=register_form.release_date.data,
                distributor_id=current_user.distributor_id  # dodeli ID trenutnog distributera
            )
            db.session.add(new_movie)
            db.session.commit()
            flash(f'Film "{new_movie.original_title}" je uspešno kreiran.', 'success')
            return redirect(url_for('movies.movies_list'))

    # Uređivanje filma
    if edit_form.validate_on_submit():
        if 'edit' in request.form:
            movie_id = request.form.get('movie_id')  # ID filma iz hidden input polja
            movie = Movie.query.get_or_404(movie_id)
            
            # Samo distributer vlasnik ili admin mogu uređivati
            if current_user.user_type == 'admin' or movie.distributor_id == current_user.distributor_id:
                movie.original_title = edit_form.original_title.data
                movie.local_title = edit_form.local_title.data
                movie.director = edit_form.director.data
                movie.actors = edit_form.actors.data
                movie.production_country = edit_form.production_country.data
                movie.production_company = edit_form.production_company.data
                movie.production_year = edit_form.production_year.data
                movie.duration = edit_form.duration.data
                movie.versions = edit_form.versions.data
                movie.projection_formats = edit_form.projection_formats.data
                movie.poster = edit_form.poster.data
                movie.images = [edit_form.image_1.data, edit_form.image_2.data, edit_form.image_3.data]
                movie.trailer_link = edit_form.trailer_link.data
                movie.synopsis = edit_form.synopsis.data
                movie.genres = edit_form.genres.data
                movie.release_date = edit_form.release_date.data
                
                db.session.commit()
                flash(f'Film "{movie.original_title}" je uspešno izmenjen.', 'success')
                return redirect(url_for('movies.movies_list'))
            else:
                flash('Nemate dozvolu za uređivanje ovog filma.', 'danger')

    # Prikaz liste filmova
    if current_user.user_type == 'distributor':
        movies_list = Movie.query.filter_by(distributor_id=current_user.distributor_id).all()
    elif current_user.user_type == 'admin':
        movies_list = Movie.query.all()

    return render_template('movies_list.html',
                            route_name=route_name,
                            movies_list=movies_list,
                            register_form=register_form,
                            edit_form=edit_form)