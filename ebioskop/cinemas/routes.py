from flask import Blueprint, json, render_template, request, url_for, flash, redirect
from flask_login import current_user
from ebioskop import app, db
from ebioskop.cinemas.forms import EditCinemaForm, EditCinemaHallForm, EditCinemaPropertiesForm, EditCinemaRepresentativeForm, EditMemberMKPSForm, RegisterCinemaForm, RegisterCinemaHallForm, RegisterCinemaPropertiesForm, RegisterCinemaRepresentativeForm, RegisterMemberMKPSForm
from ebioskop.cinemas.functions import save_picture
from ebioskop.models import Cinema, CinemaHall, CinemaProperties, CinemaRepresentative, MemberMKPS, User
import os
from werkzeug.utils import secure_filename
from flask import current_app


cinemas = Blueprint('cinemas', __name__)


@cinemas.route('/cinemas_list', methods=['GET'])
def cinemas_list():
    if not current_user.is_authenticated or current_user.user_type != 'admin':
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    route_name = request.endpoint

    # Proveravamo da li je korisnik autentifikovan i da li je admin
    if not current_user.is_authenticated or current_user.user_type != 'admin':
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    
    # Dohvatanje svih prikazivača iz baze podataka
    cinemas_list = Cinema.query.all()
    
    # Renderovanje šablona sa listom prikazivača
    return render_template('cinemas_list.html', cinemas=cinemas_list, route_name=route_name)


@cinemas.route('/create_cinema', methods=['GET', 'POST'])
def create_cinema():
    if not current_user.is_authenticated or current_user.user_type != 'admin':
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    route_name = request.endpoint

    form = RegisterCinemaForm()
    form.city.choices = [('gm', 'Gornji Milanovac')]

    if form.validate_on_submit():
        # Kreiranje objekta Cinema sa podacima iz forme
        new_cinema = Cinema(
            name=form.name.data,
            country=form.country.data,
            address=form.address.data,
            postal_code=form.postal_code.data,
            city=form.city.data,
            email=form.email.data,  # Emaili se unose kao string, ali možemo ih splitovati po zarezima ako je potrebno
            phone=form.phone.data,
            legal_form=form.legal_form.data,
            pib=form.pib.data,
            mb=form.mb.data,
            website=form.website.data,
            social_links=form.social_links.data,  # Može biti JSON formatiran string
            is_member_mkps=form.is_member_mkps.data,
            is_member_ec=form.is_member_ec.data
        )

        # Dodavanje u bazu podataka
        db.session.add(new_cinema)
        db.session.commit()

        # Poruka o uspešnom dodavanju prikazivača
        flash(f'prikazivač "{new_cinema.name}" je uspešno dodat!', 'success')
        
        # Preusmeravanje na listu prikazivača ili početnu stranicu
        return redirect(url_for('cinemas.cinemas_list'))
    
    return render_template('cinema.html', title='Novi prikazivač', form=form, route_name=route_name)


@cinemas.route('/edit_cinema/<int:cinema_id>', methods=['GET', 'POST'])
def edit_cinema(cinema_id):
    if not current_user.is_authenticated:
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    if current_user.user_type == 'admin':
        # admin može da edituje bilo kojeg prikazivača
        pass
    elif current_user.cinema_id != cinema_id:
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    route_name = request.endpoint
    representatives = CinemaRepresentative.query.filter_by(cinema_id=cinema_id).all()
    cinema_properties = CinemaProperties.query.filter_by(cinema_id=cinema_id).all()
    
    form = EditCinemaForm()
    form.city.choices = [('gm', 'Gornji Milanovac')]

    edited_cinema = Cinema.query.get_or_404(cinema_id)
    if form.validate_on_submit():
        # Kreiranje objekta Cinema sa podacima iz forme
        edited_cinema = Cinema.query.get_or_404(cinema_id)
        edited_cinema.name = form.name.data
        edited_cinema.country = form.country.data
        edited_cinema.address = form.address.data
        edited_cinema.postal_code = form.postal_code.data
        edited_cinema.city = form.city.data
        edited_cinema.email = form.email.data
        edited_cinema.phone = form.phone.data
        edited_cinema.legal_form = form.legal_form.data
        edited_cinema.pib = form.pib.data
        edited_cinema.mb = form.mb.data
        edited_cinema.website = form.website.data
        edited_cinema.social_links = form.social_links.data
        edited_cinema.is_member_mkps = form.is_member_mkps.data
        edited_cinema.is_member_ec = form.is_member_ec.data
        db.session.commit()
        flash(f'prikazivač "{edited_cinema.name}" je uspešno izmenjen!', 'success')
        if current_user.user_type == 'admin':
            return redirect(url_for('cinemas.cinemas_list'))
        else:
            return redirect(url_for('main.home', cinema_id=cinema_id))
    if request.method == 'GET':
        form.name.data = edited_cinema.name
        form.country.data = edited_cinema.country
        form.address.data = edited_cinema.address
        form.postal_code.data = edited_cinema.postal_code
        form.city.data = edited_cinema.city
        form.email.data = edited_cinema.email
        form.phone.data = edited_cinema.phone
        form.legal_form.data = edited_cinema.legal_form
        form.pib.data = edited_cinema.pib
        form.mb.data = edited_cinema.mb
        form.website.data = edited_cinema.website
        form.social_links.data = edited_cinema.social_links
        form.is_member_mkps.data = edited_cinema.is_member_mkps
        form.is_member_ec.data = edited_cinema.is_member_ec
    return render_template('cinema.html', 
                            title='Izmeni prikazivač', 
                            form=form, 
                            edited_cinema=edited_cinema,
                            representatives=representatives,
                            cinema_properties=cinema_properties,
                            route_name=route_name)


@cinemas.route('/create_cinema_representative/<int:cinema_id>', methods=['GET', 'POST'])
def create_cinema_representative(cinema_id):
    if not current_user.is_authenticated or current_user.user_type != 'admin':
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    
    current_cinema_id = cinema_id
    route_name = request.endpoint
    form = RegisterCinemaRepresentativeForm()
    
    if form.validate_on_submit():
        if form.photo.data:
            try:
                picture_file = save_picture(form.photo.data, current_cinema_id)
            except Exception as e:
                current_app.logger.error(f"Greška pri čuvanju slike: {str(e)}")
                flash('Došlo je do greške pri čuvanju slike. Molimo pokušajte ponovo.', 'danger')
                return render_template('cinema_representative.html', form=form, route_name=route_name)
        else:
            picture_file = None
        
        representative = CinemaRepresentative(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            position=form.position.data,
            email=form.email.data,
            phone=form.phone.data,
            photo=picture_file,
            cinema_id=current_cinema_id
        )
        
        try:
            db.session.add(representative)
            db.session.commit()
            flash('Predstavnik je uspešno dodat.', 'success')
            return redirect(url_for('cinemas.edit_cinema', cinema_id=current_cinema_id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Greška pri dodavanju predstavnika: {str(e)}")
            flash('Došlo je do greške pri dodavanju predstavnika. Molimo pokušajte ponovo.', 'danger')
    
    return render_template('cinema_representative.html', 
                            form=form,
                            route_name=route_name)


@cinemas.route('/edit_cinema_representative/<int:representative_id>', methods=['GET', 'POST'])
def edit_cinema_representative(representative_id):
    representative = CinemaRepresentative.query.get_or_404(representative_id)
    if not current_user.is_authenticated:
        flash('Morate biti prijavljeni da biste pristupili ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    if current_user.user_type != 'admin' and current_user.cinema_id != representative.cinema_id:
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))

    route_name = request.endpoint
    form = EditCinemaRepresentativeForm(obj=representative)

    if form.validate_on_submit():
        representative.first_name = form.first_name.data
        representative.last_name = form.last_name.data
        representative.position = form.position.data
        representative.email = form.email.data
        representative.phone = form.phone.data
        
        if form.photo.data:
            try:
                old_picture = representative.photo
                new_picture = save_picture(form.photo.data, representative.cinema_id)
                representative.photo = new_picture

                # Brisanje stare slike ako postoji
                # if old_picture:
                #     old_picture_path = os.path.join(current_app.root_path, 'static', 'img', 'cinema_representative', old_picture)
                #     if os.path.exists(old_picture_path):
                #         os.remove(old_picture_path)
            except Exception as e:
                current_app.logger.error(f"Greška pri čuvanju nove slike: {str(e)}")
                flash('Došlo je do greške pri čuvanju nove slike. Ostali podaci su sačuvani.', 'warning')
        
        try:
            db.session.commit()
            flash('Podaci o predstavniku su uspešno izmenjeni.', 'success')
            return redirect(url_for('cinemas.edit_cinema', cinema_id=representative.cinema_id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Greška pri ažuriranju predstavnika: {str(e)}")
            flash('Došlo je do greške pri ažuriranju podataka. Molimo pokušajte ponovo.', 'danger')
    
    return render_template('cinema_representative.html', 
                            form=form, 
                            route_name=route_name,
                            representative=representative)



@cinemas.route('/create_cinema_properties/<int:cinema_id>', methods=['GET', 'POST'])
def create_cinema_properties(cinema_id):
    if not current_user.is_authenticated or current_user.user_type != 'admin':
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    if current_user.user_type == 'admin':
        # Admin može da kreira bioskop
        pass
    elif current_user.cinema_id != cinema_id:
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    
    route_name = request.endpoint
    form = RegisterCinemaPropertiesForm()
    
    if form.validate_on_submit():
        # Funkcija za čuvanje fajla
        def save_file(file, index):
            if file:
                # Kreiramo folder ako ne postoji
                folder_path = os.path.join(current_app.root_path, 'static', 'img', 'cinema_properties')
                os.makedirs(folder_path, exist_ok=True)
                
                # Generišemo ime fajla
                filename = f'cinema_properties_{cinema_id:03d}_{index}.{file.filename.rsplit(".", 1)[1].lower()}'
                file_path = os.path.join(folder_path, filename)
                
                # Čuvamo fajl
                file.save(file_path)
                return filename
            return None

        # Čuvanje uploadovanih slika
        photo_1_filename = save_file(form.photo_1.data, 1)
        photo_2_filename = save_file(form.photo_2.data, 2)

        cinema_properties = CinemaProperties(
            local_name=form.local_name.data,
            location=form.location.data,
            city_population=form.city_population.data,
            surrounding_population=form.surrounding_population.data,
            has_e_ticket_system=form.has_e_ticket_system.data,
            e_ticket_system=form.e_ticket_system.data,
            promotion_methods=form.promotion_methods.data,
            programming_methods=form.programming_methods.data,
            is_distributor=form.is_distributor.data,
            photo_1=photo_1_filename,
            photo_2=photo_2_filename,
            cinema_id=cinema_id
        )
        db.session.add(cinema_properties)
        db.session.commit()
        flash('Svojstva bioskopa su uspešno dodata.', 'success')
        return redirect(url_for('cinemas.edit_cinema', cinema_id=cinema_id))
    
    return render_template('cinema_properties.html', 
                            form=form,
                            route_name=route_name)


@cinemas.route('/edit_cinema_properties/<int:cinema_properties_id>', methods=['GET', 'POST'])
def edit_cinema_properties(cinema_properties_id):
    cinema_properties = CinemaProperties.query.get_or_404(cinema_properties_id)
    if not current_user.is_authenticated:
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    if current_user.user_type == 'admin':
        # Admin može da edituje bilo koji bioskop
        pass
    elif current_user.cinema_id and current_user.cinema_id == cinema_properties.cinema_id:
        # cinema_ceo može da edituje svoj bioskop
        pass
    elif current_user.cinema_properties_id and current_user.cinema_properties_id == cinema_properties_id:
        # cinema može da edituje svoj bioskop
        pass
    else:
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    
    route_name = request.endpoint
    halls = CinemaHall.query.filter_by(cinema_properties_id=cinema_properties_id).all()
    users = User.query.filter_by(cinema_properties_id=cinema_properties_id).all()
    form = EditCinemaPropertiesForm()

    def save_file(file, index):
        if file and file.filename:
            # Kreiramo folder ako ne postoji
            folder_path = os.path.join(current_app.root_path, 'static', 'img', 'cinema_properties')
            os.makedirs(folder_path, exist_ok=True)
            
            # Generišemo ime fajla
            filename = f'cinema_properties_{cinema_properties.cinema_id:03d}_{index}.{file.filename.rsplit(".", 1)[1].lower()}'
            file_path = os.path.join(folder_path, filename)
            
            # Čuvamo fajl
            file.save(file_path)
            return filename
        return None

    if form.validate_on_submit():
        cinema_properties.local_name = form.local_name.data
        cinema_properties.location = form.location.data
        cinema_properties.city_population = form.city_population.data
        cinema_properties.surrounding_population = form.surrounding_population.data
        cinema_properties.has_e_ticket_system = form.has_e_ticket_system.data
        cinema_properties.e_ticket_system = form.e_ticket_system.data if form.has_e_ticket_system.data else None
        cinema_properties.promotion_methods = form.promotion_methods.data
        cinema_properties.programming_methods = form.programming_methods.data
        cinema_properties.is_distributor = form.is_distributor.data
        
        # Obrada slika
        if form.photo_1.data:
            new_photo_1 = save_file(form.photo_1.data, 1)
            if new_photo_1:
                cinema_properties.photo_1 = new_photo_1
        
        if form.photo_2.data:
            new_photo_2 = save_file(form.photo_2.data, 2)
            if new_photo_2:
                cinema_properties.photo_2 = new_photo_2

        db.session.commit()
        flash('Podaci o bioskopu su uspešno ažurirani.', 'success')
        return redirect(url_for('cinemas.edit_cinema', cinema_id=cinema_properties.cinema_id))

    elif request.method == 'GET':
        form.local_name.data = cinema_properties.local_name
        form.location.data = cinema_properties.location
        form.city_population.data = cinema_properties.city_population
        form.surrounding_population.data = cinema_properties.surrounding_population
        form.has_e_ticket_system.data = cinema_properties.has_e_ticket_system
        form.e_ticket_system.data = cinema_properties.e_ticket_system
        form.promotion_methods.data = cinema_properties.promotion_methods
        form.programming_methods.data = cinema_properties.programming_methods
        form.is_distributor.data = cinema_properties.is_distributor
        # Ne postavljamo photo_1 i photo_2 jer su to FileField polja

    return render_template('cinema_properties.html', 
                            form=form, 
                            route_name=route_name,
                            cinema_properties=cinema_properties,
                            halls=halls,
                            users=users,
                            cinema_id=cinema_properties.cinema_id)


@cinemas.route('/create_cinema_hall/<int:cinema_properties_id>', methods=['GET', 'POST'])
def create_cinema_hall(cinema_properties_id):
    if not current_user.is_authenticated:
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    cinema_property = CinemaProperties.query.get_or_404(cinema_properties_id)
    if current_user.user_type == 'admin':
        # Admin može da kreira bioskopsku salu
        pass
    elif current_user.cinema_id and current_user.cinema_id == cinema_property.cinema_id:
        # cinema_ceo može da kreira bioskopsku salu
        pass
    elif current_user.cinema_properties_id and current_user.cinema_properties_id == cinema_properties_id:
        # cinema može da kreira bioskopsku salu
        pass
    else:
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))
    
    route_name = request.endpoint
    form = RegisterCinemaHallForm()
    
    # Provera da li je forma validna nakon podnošenja
    if form.validate_on_submit():
        # Kreiranje instance CinemaHall modela
        new_hall = CinemaHall(
            hall_name=form.hall_name.data,
            hall_capacity=form.hall_capacity.data,
            workdays=','.join(form.workdays.data),  # Spajanje lista u string za skladištenje
            employee_count=form.employee_count.data,
            year_built=form.year_built.data,
            dimensions=form.dimensions.data,
            distance_to_screen=form.distance_to_screen.data,
            has_power_supply=form.has_power_supply.data,
            seat_description=form.seat_description.data,
            has_air_conditioning=form.has_air_conditioning.data,
            has_heating=form.has_heating.data,
            has_acoustic_treatment=form.has_acoustic_treatment.data,
            has_acoustic_screen_treatment=form.has_acoustic_screen_treatment.data,
            has_interior_project_docs=form.has_interior_project_docs.data,
            has_tech_project_docs=form.has_tech_project_docs.data,
            screen_size=form.screen_size.data,
            sound_system=form.sound_system.data,
            is_digitalized=form.is_digitalized.data,
            projector_brand=form.projector_brand.data,
            projector_model=form.projector_model.data,
            projector_resolution=form.projector_resolution.data,
            projector_lumens=form.projector_lumens.data,
            projector_contrast=form.projector_contrast.data,
            server_brand=form.server_brand.data,
            server_model=form.server_model.data,
            has_3d_equipment=form.has_3d_equipment.data,
            has_silver_screen=form.has_silver_screen.data,
            connected_devices=','.join(form.connected_devices.data),  # Spajanje lista u string
            installation_date=form.installation_date.data,
            acquisition_method=','.join(form.acquisition_method.data),  # Spajanje lista u string
            has_video_projector=form.has_video_projector.data,
            video_projector_brand=form.video_projector_brand.data,
            video_projector_model=form.video_projector_model.data,
            video_projector_resolution=form.video_projector_resolution.data,
            connected_devices_to_video_projector=','.join(form.connected_devices_to_video_projector.data),
            has_35mm_projector=form.has_35mm_projector.data,
            projector_35mm_brand=form.projector_35mm_brand.data,
            projector_35mm_model=form.projector_35mm_model.data,
            cinema_properties_id=cinema_properties_id  # Veza sa CinemaProperties modelom
        )
        
        # Dodavanje i čuvanje u bazu
        db.session.add(new_hall)
        db.session.commit()

        flash('Sala je uspešno kreirana!', 'success')
        
        # Preusmeravanje na neku stranicu, na primer, listu sala za taj bioskop
        return redirect(url_for('cinemas.edit_cinema_properties', cinema_properties_id=cinema_properties_id))

    # U slučaju GET metode ili nevalidne forme, prikazuje se forma
    return render_template('cinema_hall.html', 
                            form=form,
                            route_name=route_name)


@cinemas.route('/edit_cinema_hall/<int:hall_id>', methods=['GET', 'POST'])
# @login_required
def edit_cinema_hall(hall_id):
    hall = CinemaHall.query.get_or_404(hall_id)
    cinema_property = CinemaProperties.query.get_or_404(hall.cinema_properties_id)
    
    if not has_permission_to_edit(current_user, cinema_property):
        flash('Nemate pravo da pristupite ovoj stranici.', 'warning')
        return redirect(url_for('main.home'))

    form = EditCinemaHallForm()

    if form.validate_on_submit():
        try:
            update_hall_from_form(hall, form)
            db.session.commit()
            flash('Detalji bioskopske sale su uspešno ažurirani!', 'success')
            return redirect(url_for('cinemas.edit_cinema_properties', cinema_properties_id=hall.cinema_properties_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Došlo je do greške prilikom ažuriranja: {str(e)}', 'danger')
    elif request.method == 'POST':
        flash('Molimo proverite unete podatke.', 'warning')
        flash(f'{form.errors}', 'danger')

    if request.method == 'GET':
        populate_form_from_hall(form, hall)

    return render_template('cinema_hall.html', title='Izmena bioskopske sale', form=form, hall=hall, route_name=request.endpoint)

def has_permission_to_edit(user, cinema_property):
    return (user.user_type == 'admin' or 
            (user.cinema_id and user.cinema_id == cinema_property.cinema_id) or
            (user.cinema_properties_id and user.cinema_properties_id == cinema_property.id))

def update_hall_from_form(hall, form):
    for field in form:
        if field.name != 'submit' and field.name != 'csrf_token':
            if isinstance(getattr(hall, field.name), db.JSON):
                setattr(hall, field.name, field.data)
            elif field.name in ['workdays', 'connected_devices', 'acquisition_method']:
                setattr(hall, field.name, field.data)
            else:
                setattr(hall, field.name, field.data)
    
    # Dodatna logika za uslovljena polja
    if not hall.is_digitalized:
        hall.projector_brand = None
        hall.projector_model = None
        hall.projector_resolution = None
        hall.projector_lumens = None
        hall.projector_contrast = None
        hall.server_brand = None
        hall.server_model = None
        hall.has_3d_equipment = None
        hall.has_silver_screen = None
    
    if not hall.has_video_projector:
        hall.video_projector_brand = None
        hall.video_projector_model = None
        hall.video_projector_resolution = None
        hall.connected_devices_to_video_projector = None
    
    if not hall.has_35mm_projector:
        hall.projector_35mm_brand = None
        hall.projector_35mm_model = None

def populate_form_from_hall(form, hall):
    for field in form:
        if field.name != 'submit' and field.name != 'csrf_token':
            if field.name == 'workdays':
                # Pretpostavljamo da je workdays JSON polje u bazi
                form.workdays.data = hall.workdays
            elif isinstance(getattr(hall, field.name), db.JSON):
                field.data = getattr(hall, field.name)
            else:
                field.data = getattr(hall, field.name)

@cinemas.route('/mkps_members_list', methods=['GET', 'POST'])
def mkps_members_list():
    route_name = request.endpoint
    members = MemberMKPS.query.all()
    return render_template('mkps_members_list.html', title='MKPS Members List', members=members, route_name=route_name)


@cinemas.route('/create_mkps_member', methods=['GET', 'POST'])
def create_mkps_member():
    route_name = request.endpoint
    form = RegisterMemberMKPSForm()
    # Populate the cinema choices
    form.cinema.choices = [(0, 'Select MKPS Cinema')] + [(c.id, c.name) for c in Cinema.query.filter_by(is_member_mkps=True).all()]
    
    if form.validate_on_submit():
        new_member = MemberMKPS(
            name=form.name.data,
            surname=form.surname.data,
            address=form.address.data,
            city=form.city.data,
            job_position=form.job_position.data,
            status=form.status.data
        )
        
        # Handle cinema selection
        if form.cinema.data != 0:  # If an MKPS cinema is selected
            new_member.cinema_id = form.cinema.data
        else:  # If a non-MKPS cinema is entered
            new_member.cinema_not_mkps = form.cinema_not_mkps.data
        
        # Handle emails
        if form.emails.data:
            new_member.set_emails([email.strip() for email in form.emails.data.split(',')])
        
        # Handle phone numbers
        if form.phones.data:
            new_member.set_phones([phone.strip() for phone in form.phones.data.split(',')])
        
        try:
            db.session.add(new_member)
            db.session.commit()
            flash('New MKPS member has been successfully created!', 'success')
            return redirect(url_for('cinemas.mkps_members_list'))  # Assume you have a route to list members
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while creating the member: {str(e)}', 'danger')
    
    return render_template('mkps_member.html', title='Create MKPS Member', form=form, route_name=route_name)


@cinemas.route('/edit_mkps_member/<int:member_id>', methods=['GET', 'POST'])
def edit_mkps_member(member_id):
    route_name = request.endpoint
    member = MemberMKPS.query.get(member_id)
    form = EditMemberMKPSForm(obj=member)
    form.cinema.choices = [(0, 'Select MKPS Cinema')] + [(c.id, c.name) for c in Cinema.query.filter_by(is_member_mkps=True).all()]
    if form.validate_on_submit():
        member.name = form.name.data
        member.surname = form.surname.data
        member.address = form.address.data
        member.city = form.city.data
        member.job_position = form.job_position.data
        member.status = form.status.data
        member.cinema_id = form.cinema.data
        member.cinema_not_mkps = form.cinema_not_mkps.data
        member.emails = form.emails.data
        member.phones = form.phones.data
        db.session.commit()
        flash('MKPS member has been successfully updated!', 'success')
        return redirect(url_for('cinemas.mkps_members_list'))

    return render_template('mkps_member.html', title='Create MKPS Member', form=form, route_name=route_name)