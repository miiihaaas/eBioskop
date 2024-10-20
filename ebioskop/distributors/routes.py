from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import current_user
from ebioskop import app, db
from ebioskop.models import Cinema, CinemaHall, CinemaProperties, Distributor, DistributorRepresentative, Movie, Projection, Representative, User
from ebioskop.distributors.forms import EditDistributorForm, RegisterDistributorForm


distributors = Blueprint('distributor', __name__)


@distributors.route('/create_distributor', methods=['GET', 'POST'])
def create_distributor():
    if not current_user.is_authenticated or current_user.user_type != 'admin':
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    
    route_name = request.endpoint
    form = RegisterDistributorForm()
    
    if form.validate_on_submit():
        # Kreiranje novog distributera na osnovu podataka iz forme
        distributor = Distributor(
            company_name=form.company_name.data,
            country=form.country.data,
            address=form.address.data,
            postal_code=form.postal_code.data,
            city=form.city.data,
            email=form.email.data,
            phone=form.phone.data,
            pib=form.pib.data,
            mb=form.mb.data,
            authorized_person=form.authorized_person.data,
            website=form.website.data,
            youtube=form.youtube.data,
            facebook=form.facebook.data,
            instagram=form.instagram.data,
            tiktok=form.tiktok.data
        )
        
        # Dodavanje distributera u sesiju
        db.session.add(distributor)
        
        # Povezivanje sa izabranim zastupnicima
        for rep_name in form.representatives.data:
            representative = Representative.query.filter_by(name=rep_name).first()
            if representative:
                distributor_representative = DistributorRepresentative(distributor=distributor, representative=representative)
                db.session.add(distributor_representative)
        
        # Čuvanje promena u bazi
        db.session.commit()
        
        flash(f'Distributor {form.company_name.data} je uspešno kreiran!', 'success')
        return redirect(url_for('distributor.distributors_list'))
    
    return render_template('distributor.html', title='Kreiranje novog distributera', form=form, route_name=route_name)

@distributors.route('/edit_distributor/<int:distributor_id>', methods=['GET', 'POST'])
def edit_distributor(distributor_id):
    if not current_user.is_authenticated:
        flash('Morate biti prijavljeni da biste pristupili ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    if current_user.user_type != 'admin' and current_user.distributor_id != distributor_id:
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
        
    route_name = request.endpoint
    distributor = Distributor.query.get_or_404(distributor_id)
    form = EditDistributorForm()

    if form.validate_on_submit():
        distributor.company_name = form.company_name.data
        distributor.country = form.country.data
        distributor.address = form.address.data
        distributor.postal_code = form.postal_code.data
        distributor.city = form.city.data
        distributor.email = form.email.data
        distributor.phone = form.phone.data
        distributor.pib = form.pib.data
        distributor.mb = form.mb.data
        distributor.authorized_person = form.authorized_person.data
        distributor.website = form.website.data
        distributor.youtube = form.youtube.data
        distributor.facebook = form.facebook.data
        distributor.instagram = form.instagram.data
        distributor.tiktok = form.tiktok.data

        # Ažuriranje zastupnika
        existing_representatives = set(rep.name for rep in distributor.representatives)
        new_representatives = set(form.representatives.data)

        # Uklanjanje veza sa zastupnicima koji više nisu izabrani
        for rep_name in existing_representatives - new_representatives:
            rep = Representative.query.filter_by(name=rep_name).first()
            if rep:
                distributor_rep = DistributorRepresentative.query.filter_by(distributor_id=distributor.id, representative_id=rep.id).first()
                if distributor_rep:
                    db.session.delete(distributor_rep)

        # Dodavanje veza sa novim zastupnicima
        for rep_name in new_representatives - existing_representatives:
            rep = Representative.query.filter_by(name=rep_name).first()
            if rep:
                distributor_rep = DistributorRepresentative(distributor_id=distributor.id, representative_id=rep.id)
                db.session.add(distributor_rep)

        db.session.commit()
        if current_user.user_type == 'admin':
            flash(f'Distributor {form.company_name.data} je uspešno ažuriran!', 'success')
            return redirect(url_for('distributor.distributors_list'))
        else:
            flash(f'Uspešno ste ažurirali podatke distributera', 'success')
            return redirect(url_for('main.home'))
    
    elif request.method == 'GET':
        form.company_name.data = distributor.company_name
        form.country.data = distributor.country
        form.address.data = distributor.address
        form.postal_code.data = distributor.postal_code
        form.city.data = distributor.city
        form.email.data = distributor.email
        form.phone.data = distributor.phone
        form.pib.data = distributor.pib
        form.mb.data = distributor.mb
        form.authorized_person.data = distributor.authorized_person
        form.website.data = distributor.website
        form.youtube.data = distributor.youtube
        form.facebook.data = distributor.facebook
        form.instagram.data = distributor.instagram
        form.tiktok.data = distributor.tiktok
        form.representatives.data = [rep.name for rep in distributor.representatives]
    
    users = User.query.filter_by(distributor_id=distributor_id).all()
    
    return render_template('distributor.html', 
                            title=f'Ažuriranje distributera {distributor.company_name}', 
                            form=form,
                            distributor=distributor,
                            route_name=route_name,
                            users=users)

@distributors.route('/distributors_list')
def distributors_list():
    if current_user.user_type not in ['admin', 'user']:
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    route_name = request.endpoint
    distributors = Distributor.query.all()
    return render_template('distributors_list.html', distributors=distributors, route_name=route_name)


@distributors.route('/exhibitors', methods=['GET'])
def exhibitors():
    route_name = request.endpoint
    
    # Dobijanje trenutno ulogovanog distributera
    current_distributor = Distributor.query.get(current_user.distributor_id)
    
    # Dobijanje trenutnog datuma
    today = datetime.now().date()

    # Pronalaženje prvog četvrtka pre današnjeg dana
    start_date = today - timedelta(days=(today.weekday() - 3) % 7)

    # Formatiranje start_date u string
    start_date_str = start_date.strftime('%Y-%m-%d')

    # Postavljanje end_date na 7 dana nakon start_date
    end_date = start_date + timedelta(days=7)
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Dobijanje parametara za filtere
    start_date = request.args.get('start_date', start_date_str)
    end_date = request.args.get('end_date', end_date_str)
    status = request.args.get('status', 'active')

    # Pretvaranje stringova u datetime objekte
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # Dobijanje svih prikazivača koji prikazuju filmove ovog distributera
    exhibitors = Cinema.query.join(CinemaProperties).join(CinemaHall).join(Projection).join(Movie).filter(
        Movie.distributor_id == current_distributor.id
    ).distinct().all()
    
    exhibitors_data = []
    
    for exhibitor in exhibitors:
        projections = Projection.query.join(CinemaHall).join(CinemaProperties).join(Cinema).join(Movie).filter(
            Movie.distributor_id == current_distributor.id,
            Cinema.id == exhibitor.id,
            Projection.date.between(start_date, end_date)
        ).all()
        
        movies_data = {}
        for projection in projections:
            movie = projection.movie
            if movie.id not in movies_data:
                movies_data[movie.id] = {
                    'name': movie.local_title,
                    'versions': set(),
                    'formats': set(),
                    'projection_count': 0,
                    'weeks_showing': 0,
                    'tickets_sold': 0,
                    'revenue': 0
                }
            
            movies_data[movie.id]['versions'].add(projection.version)
            movies_data[movie.id]['formats'].add(projection.format)
            movies_data[movie.id]['projection_count'] += 1
            movies_data[movie.id]['tickets_sold'] += projection.tickets_sold
            movies_data[movie.id]['revenue'] += projection.revenue
        
        # Računanje broja nedelja prikazivanja
        for movie_id, data in movies_data.items():
            first_projection = Projection.query.join(Movie).filter(
                Movie.id == movie_id,
                Projection.cinema_hall_id.in_([hall.id for hall in exhibitor.properties.halls])
            ).order_by(Projection.date).first()
            
            if first_projection:
                weeks = (end_date - first_projection.date).days // 7
                data['weeks_showing'] = weeks + 1  # +1 jer uključujemo i tekuću nedelju
        
        exhibitors_data.append({
            'exhibitor': exhibitor,
            'movies': list(movies_data.values())
        })
    
    return render_template('exhibitors.html', 
                            route_name=route_name, 
                            exhibitors_data=exhibitors_data, 
                            start_date=start_date.strftime('%Y-%m-%d'), 
                            end_date=end_date.strftime('%Y-%m-%d'), 
                            projections=projections,
                            exhibitors=exhibitors,
                            status=status)