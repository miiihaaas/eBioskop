from datetime import datetime, timedelta, date
from ebioskop import app, db, cache
from ebioskop.models import BoxOfficeWeekly, Projection, Movie, Distributor, CinemaHall, Cinema
import traceback
from sqlalchemy import desc, func


def get_cinema_week(date=None):
    """Vraća broj bioskopske nedelje za dati datum (četvrtak-sreda)"""
    if date is None:
        date = datetime.now()
    days_since_thursday = (date.weekday() - 3) % 7
    thursday = date - timedelta(days=days_since_thursday)
    return thursday.isocalendar()[1], thursday.year

def get_week_dates(year, week_number):
    """Vraća početni i krajnji datum za datu bioskopsku nedelju"""
    # Format mora biti '2024-W48-4' a ne '48-W2024-4'
    first_day = datetime.strptime(f'{year}-W{week_number:02d}-4', '%Y-W%W-%w')  # četvrtak
    last_day = first_day + timedelta(days=6)  # sreda
    app.logger.debug(f"Week dates for {year}-W{week_number}: {first_day.date()} to {last_day.date()}")
    return first_day.date(), last_day.date()

def validate_week_param(week):
    """Validacija parametra za nedelju"""
    try:
        week = int(week) if week is not None else None
        if not week or week < 1 or week > 53:
            app.logger.warning(f"Nevalidna nedelja: {week}")
            raise ValueError('Nevalidna nedelja')
        app.logger.debug(f"Validirana nedelja: {week}")
        return week
    except (TypeError, ValueError) as e:
        app.logger.warning(f"Greška pri validaciji nedelje: {str(e)}")
        raise ValueError('Nevalidna nedelja')

def validate_year_param(year):
    """Validacija parametra za godinu"""
    try:
        year = int(year) if year is not None else None
        current_year = datetime.now().year
        if not year or year < 2020 or year > current_year:
            app.logger.warning(f"Nevalidna godina: {year}")
            raise ValueError('Nevalidna godina')
        app.logger.debug(f"Validirana godina: {year}")
        return year
    except (TypeError, ValueError) as e:
        app.logger.warning(f"Greška pri validaciji godine: {str(e)}")
        raise ValueError('Nevalidna godina')

def get_empty_totals():
    return {
        'weekly_bo': 0,
        'weekly_sales': 0,
        'last_week_bo': 0,
        'last_week_sales': 0,
        'total_bo': 0,
        'total_sales': 0
    }

def calculate_totals(box_office_items):
    """Izračunava ukupne vrednosti za box office podatke"""
    totals = {
        'weekly_earnings': sum(item.weekly_earnings or 0 for item in box_office_items),
        'weekly_admissions': sum(item.weekly_admissions or 0 for item in box_office_items),
        'last_week_earnings': sum(item.last_week_earnings or 0 for item in box_office_items),
        'last_week_admissions': sum(item.last_week_admissions or 0 for item in box_office_items),
        'total_earnings': 0,
        'total_admissions': 0
    }

    # Računamo ukupne vrednosti za sve filmove
    for item in box_office_items:
        # Dobavljamo sve box office podatke za ovaj film do trenutne nedelje
        historical_data = BoxOfficeWeekly.query.filter(
            BoxOfficeWeekly.movie_id == item.movie_id,
            BoxOfficeWeekly.year <= item.year,
            ((BoxOfficeWeekly.year < item.year) | 
             (BoxOfficeWeekly.year == item.year) & (BoxOfficeWeekly.week <= item.week))
        ).all()

        # Sabiramo sve earnings i admissions
        film_total_earnings = sum(data.weekly_earnings or 0 for data in historical_data)
        film_total_admissions = sum(data.weekly_admissions or 0 for data in historical_data)

        totals['total_earnings'] += film_total_earnings
        totals['total_admissions'] += film_total_admissions

    return totals

def calculate_percentage_change(current, previous):
    """Izračunava procentualnu promenu između dve vrednosti"""
    if not previous:
        return None
    try:
        return ((current - previous) / previous) * 100 if previous != 0 else None
    except (TypeError, ZeroDivisionError):
        return None

def get_position_change(current_position, movie_id, previous_week, previous_year):
    """Određuje promenu pozicije filma u odnosu na prošlu nedelju"""
    # Ako nemamo trenutnu poziciju, vraćamo None
    if current_position is None:
        return None

    # Tražimo podatke iz prošle nedelje
    previous_data = BoxOfficeWeekly.query.filter_by(
        movie_id=movie_id,
        week=previous_week,
        year=previous_year
    ).first()

    # Ako film nije bio prikazan prošle nedelje, vraćamo 'NOVI'
    if not previous_data:
        return 'NOVI'
    
    # Ako je pozicija ista, vraćamo '-'
    if previous_data.position == current_position:
        return '-'
    
    # Ako je nova pozicija bolja (manji broj), vraćamo '↑'
    # Ako je lošija (veći broj), vraćamo '↓'
    return '↑' if current_position < previous_data.position else '↓'

def format_box_office_data(box_office_items):
    """Formatira box office podatke za prikaz"""
    formatted_data = []
    
    for movie in box_office_items:
        # Dobavljamo istorijske podatke za film
        historical_data = BoxOfficeWeekly.query.filter(
            BoxOfficeWeekly.movie_id == movie.movie_id,
            BoxOfficeWeekly.year <= movie.year,
            ((BoxOfficeWeekly.year < movie.year) | 
             (BoxOfficeWeekly.year == movie.year) & (BoxOfficeWeekly.week <= movie.week))
        ).all()

        # Računamo ukupne vrednosti
        total_earnings = sum(data.weekly_earnings or 0 for data in historical_data)
        total_admissions = sum(data.weekly_admissions or 0 for data in historical_data)

        # Računamo broj nedelja prikazivanja
        weeks_shown = len(historical_data)

        # Računamo prethodnu nedelju i godinu
        previous_week = movie.week - 1
        previous_year = movie.year
        if previous_week < 1:
            previous_week = 52  # ili koji god je poslednji broj nedelje u godini
            previous_year -= 1

        # Dobavljamo promenu pozicije
        position_change = get_position_change(movie.position, movie.movie_id, previous_week, previous_year)

        # Računamo procentualnu promenu zarade
        earnings_change = calculate_percentage_change(movie.weekly_earnings or 0, movie.last_week_earnings or 0)

        # Formatiramo podatke za prikaz
        formatted_data.append({
            'position': movie.position,
            'movie_title': movie.movie.local_title,
            'company': movie.movie.company,
            'local_distributor': movie.distributor,
            'weekly_earnings': movie.weekly_earnings or 0,
            'weekly_admissions': movie.weekly_admissions or 0,
            'last_week_earnings': movie.last_week_earnings or 0,
            'last_week_admissions': movie.last_week_admissions or 0,
            'cinema_count': movie.cinema_count or 0,
            'weeks_shown': weeks_shown,
            'total_earnings': total_earnings,
            'total_admissions': total_admissions,
            'position_change': position_change,
            'earnings_change': earnings_change
        })
        app.logger.debug(f"Formatirani podaci za film {movie.movie.local_title}: {formatted_data[-1]}")
    
    return formatted_data

def update_box_office_data(week, year):
    """Ažurira box office podatke za datu nedelju"""
    try:
        app.logger.info(f"Početak ažuriranja box office podataka za nedelju {week}, godinu {year}")
        
        # Dobijanje datuma za trenutnu i prethodnu nedelju
        week_start, week_end = get_week_dates(year, week)
        prev_week_start, prev_week_end = get_week_dates(year, week - 1)
        
        app.logger.info(f"Period: {week_start} do {week_end}")
        app.logger.info(f"Prethodni period: {prev_week_start} do {prev_week_end}")
        
        # Debug logging za proveru projekcija
        projection_count = db.session.query(func.count(Projection.id)).filter(
            Projection.date.between(week_start, week_end)
        ).scalar()
        app.logger.debug(f"Broj projekcija u periodu {week_start} do {week_end}: {projection_count}")
        
        # Dobavljanje podataka za trenutnu nedelju
        app.logger.info("Dobavljanje podataka za trenutnu nedelju")
        current_week_data = db.session.query(
            Projection.movie_id,
            Movie.local_title.label('title'),
            Movie.distributor_id,
            Distributor.company_name.label('distributor'),
            Distributor.company_name.label('local_distributor'),
            func.count(Projection.id).label('projection_count'),
            func.sum(Projection.tickets_sold).label('weekly_admissions'),
            func.sum(Projection.revenue).label('weekly_earnings'),
            func.count(func.distinct(CinemaHall.cinema_properties_id)).label('cinema_count')
        ).select_from(Projection)\
        .join(Movie, Movie.id == Projection.movie_id)\
        .join(Distributor, Distributor.id == Movie.distributor_id)\
        .join(CinemaHall, CinemaHall.id == Projection.cinema_hall_id)\
        .filter(Projection.date.between(week_start, week_end))\
        .group_by(Projection.movie_id, Movie.local_title, Movie.distributor_id, Distributor.company_name)\
        .all()
        
        app.logger.info(f"Pronađeno {len(current_week_data)} filmova za trenutnu nedelju")
        
        # Dobavljanje podataka za prethodnu nedelju
        app.logger.info("Dobavljanje podataka za prethodnu nedelju")
        prev_week_data = db.session.query(
            Projection.movie_id,
            Movie.local_title.label('title'),
            Movie.distributor_id,
            Distributor.company_name.label('distributor'),
            Distributor.company_name.label('local_distributor'),
            func.count(Projection.id).label('projection_count'),
            func.sum(Projection.tickets_sold).label('weekly_admissions'),
            func.sum(Projection.revenue).label('weekly_earnings'),
            func.count(func.distinct(CinemaHall.cinema_properties_id)).label('cinema_count')
        ).select_from(Projection)\
        .join(Movie, Movie.id == Projection.movie_id)\
        .join(Distributor, Distributor.id == Movie.distributor_id)\
        .join(CinemaHall, CinemaHall.id == Projection.cinema_hall_id)\
        .filter(Projection.date.between(prev_week_start, prev_week_end))\
        .group_by(Projection.movie_id, Movie.local_title, Movie.distributor_id, Distributor.company_name)\
        .all()
        
        app.logger.info(f"Pronađeno {len(prev_week_data)} filmova za prethodnu nedelju")
        
        # Kreiranje rečnika za brži pristup prethodnim podacima
        prev_week_dict = {d.movie_id: d for d in prev_week_data}
        
        # Brisanje postojećih podataka
        app.logger.info("Brisanje postojećih podataka")
        BoxOfficeWeekly.query.filter_by(year=year, week=week).delete()
        
        # Prvo sortiramo podatke po zaradi
        current_week_list = list(current_week_data)
        current_week_list.sort(key=lambda x: (-1 * (x.weekly_earnings or 0), -1 * (x.weekly_earnings or 0)))
        
        # Kreiranje novih box office zapisa sa sortiranim pozicijama
        app.logger.info("Kreiranje novih box office zapisa")
        box_office_items = []
        
        # Prvo dodajemo filmove iz trenutne nedelje
        for position, movie_data in enumerate(current_week_list, 1):
            prev_data = prev_week_dict.get(movie_data.movie_id)
            box_office_item = BoxOfficeWeekly(
                movie_id=movie_data.movie_id,
                year=year,
                week=week,
                position=position,
                distributor=movie_data.distributor,
                local_distributor=movie_data.local_distributor,
                weekly_earnings=movie_data.weekly_earnings,
                weekly_admissions=movie_data.weekly_admissions,
                last_week_earnings=prev_data.weekly_earnings if prev_data else 0,
                last_week_admissions=prev_data.weekly_admissions if prev_data else 0,
                cinema_count=movie_data.cinema_count,
                weeks_shown=1,
                total_earnings=movie_data.weekly_earnings,
                total_admissions=movie_data.weekly_admissions
            )
            box_office_items.append(box_office_item)
        
        # Zatim dodajemo filmove koji su bili samo u prethodnoj nedelji
        next_position = len(box_office_items) + 1
        for movie_data in prev_week_data:
            if movie_data.movie_id not in [item.movie_id for item in box_office_items]:
                box_office_item = BoxOfficeWeekly(
                    movie_id=movie_data.movie_id,
                    year=year,
                    week=week,
                    position=next_position,
                    distributor=movie_data.distributor,
                    local_distributor=movie_data.local_distributor,
                    weekly_earnings=0,
                    weekly_admissions=0,
                    last_week_earnings=movie_data.weekly_earnings,
                    last_week_admissions=movie_data.weekly_admissions,
                    cinema_count=0,
                    weeks_shown=1,
                    total_earnings=movie_data.weekly_earnings,
                    total_admissions=movie_data.weekly_admissions
                )
                box_office_items.append(box_office_item)
                next_position += 1

        if box_office_items:
            # Prvo čuvamo objekte u sesiji
            db.session.bulk_save_objects(box_office_items)
            db.session.flush()

            # Ažuriramo weeks_shown i total_earnings za svaki film
            for item in box_office_items:
                # Dobavljamo sve istorijske podatke za film
                historical_data = BoxOfficeWeekly.query.options(db.joinedload(BoxOfficeWeekly.movie)).filter(
                    BoxOfficeWeekly.movie_id == item.movie_id,
                    BoxOfficeWeekly.year <= year,
                    ((BoxOfficeWeekly.year < year) | 
                     (BoxOfficeWeekly.year == year) & (BoxOfficeWeekly.week <= week))
                ).all()
                
                # Ažuriramo broj nedelja i ukupnu zaradu
                item.weeks_shown = len(historical_data)
                item.total_earnings = sum(data.weekly_earnings or 0 for data in historical_data)
                item.total_admissions = sum(data.weekly_admissions or 0 for data in historical_data)

            # Debug log pozicija
            app.logger.debug("Pozicije filmova:")
            for movie_data in current_week_list:
                app.logger.debug(f"Film: {movie_data.title}, Pozicija: {next(item.position for item in box_office_items if item.movie_id == movie_data.movie_id)}, "
                               f"Weekly: {movie_data.weekly_earnings}, Total: {sum(item.weekly_earnings or 0 for item in historical_data if item.movie_id == movie_data.movie_id)}")

            # Commit svih promena
            db.session.commit()
            
        app.logger.info("Uspešno završeno ažuriranje box office podataka")
        return True
        
    except Exception as e:
        app.logger.error(f"Greška prilikom ažuriranja box office podataka: {str(e)}")
        app.logger.error(traceback.format_exc())
        db.session.rollback()
        return False


def update_box_office_for_projection(projection):
    """Ažurira box office podatke za nedelju u kojoj je projekcija"""
    try:
        # Određujemo bioskopsku nedelju za datum projekcije
        week, year = get_cinema_week(projection.date)
        
        # Ažuriramo box office podatke za tu nedelju
        app.logger.info(f"Ažuriranje box office podataka za projekciju {projection.id} (nedelja {week}, godina {year})")
        update_box_office_data(week, year)
        
        return True
    except Exception as e:
        app.logger.error(f"Greška pri ažuriranju box office podataka za projekciju {projection.id}: {str(e)}")
        return False