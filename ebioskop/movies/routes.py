from datetime import datetime
import os
from flask import Blueprint, current_app, jsonify, render_template, request, url_for, flash, redirect
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from ebioskop import app, db
from ebioskop.models import Distributor, Movie
from ebioskop.movies.forms import EditMovieForm, RegisterMovieForm
from ebioskop.movies.functions import save_image, send_email_about_movie


movies = Blueprint('movies', __name__)


@movies.route('/movies_list', methods=['GET', 'POST'])
@login_required
def movies_list():
    # Prikaz liste filmova
    if current_user.user_type == 'distributor':
        movies_list = Movie.query.filter_by(distributor_id=current_user.distributor_id).all()
    elif current_user.user_type in ['admin', 'cinema']:
        movies_list = Movie.query.all()
    else:
        flash('Nemate pravo pristupa ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    route_name = request.endpoint
    
    # Kreiranje formi
    register_form = RegisterMovieForm()
    edit_form = EditMovieForm()

    # Dinamički napuni SelectField opcije za produkciju zemalja i žanrove
    countries = [("USA", "USA"), ("UK", "UK"), ("France", "France")]  # Dodajte više zemalja po potrebi
    distributor_list = Distributor.query.all()
    today = datetime.now().date()

    register_form.production_country.choices = countries
    edit_form.production_country.choices = countries

    return render_template('movies_list.html',
                            route_name=route_name,
                            movies_list=movies_list,
                            register_form=register_form,
                            distributor_list=distributor_list,
                            today=today,
                            edit_form=edit_form)


@movies.route('/add_movie', methods=['POST'])
@login_required
def add_movie():
    print("Debug: Request method:", request.method)
    print("Debug: Request files:", request.files)
    print("Debug: Form data:", request.form)
    form = RegisterMovieForm()
    countries = [("USA", "USA"), ("UK", "UK"), ("France", "France")]
    form.production_country.choices = countries
    
    try:
        print(f'{form=}')
        if form.validate_on_submit():
            # Prvo kreiramo movie objekat bez slika
            new_movie = Movie(
                original_title=form.original_title.data,
                local_title=form.local_title.data,
                director=form.director.data,
                actors=form.actors.data,
                production_country=form.production_country.data,
                company=form.company.data,
                production_year=form.production_year.data,
                duration=form.duration.data,
                versions=form.versions.data,
                projection_formats=form.projection_formats.data,
                age_rating=form.age_rating.data,
                trailer_link=form.trailer_link.data,
                synopsis=form.synopsis.data,
                genres=form.genres.data,
                release_date=form.release_date.data,
                distributor_id=current_user.distributor_id,
                is_showing_finished=False
            )
            
            # Dodajemo movie u sesiju da bismo dobili ID
            db.session.add(new_movie)
            db.session.flush()
            

            # Čuvanje postera
            movie_id = f'{new_movie.id:04d}'
            poster_path = save_image(form.poster.data, f'{movie_id}_poster.jpg')
            if poster_path:
                new_movie.poster = poster_path

            # Čuvanje slika
            images = []
            for i, image_field in enumerate([form.image_1, form.image_2, form.image_3], start=1):
                image_path = save_image(image_field.data, f'{movie_id}_image_{i}.jpg')
                if image_path:
                    images.append(image_path)

            if images:
                new_movie.images = images

            # Sada commit-ujemo sve promene
            db.session.commit()

            flash(f'Film "{new_movie.original_title}" je uspešno kreiran.', 'success')
            #! implementirati funkcionalnost slanaj mejla svim distributerima i svim prikazivačima (tema podatak o datumu starta fima)
            #! implementirati funkcionalnost slanaj mejla svim distributerima i svim prikazivačima (tema podatak o datumu starta fima)
            send_email_about_movie(movie=new_movie, new_movie=True)
            #! implementirati funkcionalnost slanaj mejla svim distributerima i svim prikazivačima (tema podatak o datumu starta fima)
            #! implementirati funkcionalnost slanaj mejla svim distributerima i svim prikazivačima (tema podatak o datumu starta fima)
            return jsonify({"success": True, "message": "Film je uspešno dodat."})
        else:
            print(f"Greška: {str(form.errors)=}")
            return jsonify({"success": False, "errors": form.errors}), 400

    except Exception as e:
        db.session.rollback()
        print(f"Greška--: {str(e)}")
        return jsonify({"success": False, "message": "Doslo je do greske pri kreiranju filmova."}), 500


@movies.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    

    if request.method == 'GET':
        return jsonify({
            "id": movie.id,
            "original_title": movie.original_title,
            "local_title": movie.local_title,
            "director": movie.director,
            "actors": movie.actors,
            "production_country": movie.production_country,
            "company": movie.company,
            "production_year": movie.production_year,
            "duration": movie.duration,
            "versions": movie.versions,
            "projection_formats": movie.projection_formats,
            "age_rating": movie.age_rating,
            "poster": movie.poster,
            "images": movie.images,
            "trailer_link": movie.trailer_link,
            "synopsis": movie.synopsis,
            "genres": movie.genres,
            "release_date": movie.release_date.strftime('%Y-%m-%d') if movie.release_date else None,
            "is_showing_finished": movie.is_showing_finished
        })
    
    if current_user.user_type != 'admin' and movie.distributor_id != current_user.distributor_id:
        return jsonify({"success": False, "message": "Nemate dozvolu za uređivanje ovog filma."}), 403

    if request.method == 'POST':
        form = EditMovieForm()
        countries = [("USA", "USA"), ("UK", "UK"), ("France", "France")]
        form.production_country.choices = countries
        
        
        if form.validate_on_submit():
            movie.original_title = form.original_title.data
            movie.local_title = form.local_title.data
            movie.director = form.director.data
            movie.actors = form.actors.data
            movie.production_country = form.production_country.data
            movie.company = form.company.data
            movie.production_year = form.production_year.data
            movie.duration = form.duration.data
            movie.versions = form.versions.data
            movie.projection_formats = form.projection_formats.data
            movie.age_rating = form.age_rating.data
            movie.trailer_link = form.trailer_link.data
            movie.synopsis = form.synopsis.data
            movie.genres = form.genres.data
            movie.release_date = form.release_date.data
            movie.is_showing_finished = form.is_showing_finished.data

            # Obrada postera i slika
            if form.poster.data:
                movie.poster = save_image(form.poster.data, f'{movie.id:04d}_poster.jpg')
            
            new_images = []
            for i, image_field in enumerate([form.image_1, form.image_2, form.image_3], start=1):
                if image_field.data:
                    image_path = save_image(image_field.data, f'{movie.id:04d}_image_{i}.jpg')
                    if image_path:
                        new_images.append(image_path)
            
            if new_images:
                movie.images = new_images

            db.session.commit()
            flash(f'Film "{movie.original_title}" je uspešno izmenjen.', 'success')
            #! implementirati funkcionalnost slanaj mejla svim distributerima i svim prikazivačima (tema podatak o datumu starta fima)
            #! implementirati funkcionalnost slanaj mejla svim distributerima i svim prikazivačima (tema podatak o datumu starta fima)
            send_email_about_movie(movie)
            #! implementirati funkcionalnost slanaj mejla svim distributerima i svim prikazivačima (tema podatak o datumu starta fima)
            #! implementirati funkcionalnost slanaj mejla svim distributerima i svim prikazivačima (tema podatak o datumu starta fima)
            return jsonify({"success": True, "message": "Film je uspešno izmenjen."})
        else:
            return jsonify({"success": False, "errors": form.errors}), 400

    return jsonify({"success": False, "message": "Nevažeći zahtev."}), 400