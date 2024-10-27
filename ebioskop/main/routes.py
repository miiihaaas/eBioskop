from datetime import datetime, timedelta
from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_mail import Message, Mail
from sqlalchemy import desc, func
from ebioskop import app, db
from ebioskop.models import CinemaHall, Movie, Projection


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


def get_cinema_week(date=None):
    """Vraća broj bioskopske nedelje za dati datum (četvrtak-sreda)"""
    if date is None:
        date = datetime.now()
    days_since_thursday = (date.weekday() - 3) % 7
    thursday = date - timedelta(days=days_since_thursday)
    return thursday.isocalendar()[1], thursday.year

def get_week_dates(week_number, year):
    """Vraća početni i krajnji datum za datu bioskopsku nedelju"""
    first_day = datetime.strptime(f'{year}-W{week_number}-4', '%Y-W%W-%w')  # četvrtak
    last_day = first_day + timedelta(days=6)  # sreda
    return first_day.date(), last_day.date()

@main.route('/box_office', methods=['GET'])
def box_office():
    route_name = request.endpoint
    
    try:
        # Dobijanje trenutne i izabrane nedelje
        current_week, current_year = get_cinema_week()
        selected_week = request.args.get('week', type=int, default=current_week)
        selected_year = request.args.get('year', type=int, default=current_year)

        # Dobijanje datuma za trenutnu i prethodnu nedelju
        week_start, week_end = get_week_dates(selected_week, selected_year)
        prev_week_start = week_start - timedelta(days=7)
        prev_week_end = week_end - timedelta(days=7)

        # Upit za trenutnu nedelju
        current_week_data = db.session.query(
            Projection.movie_id,
            func.count(Projection.id).label('projection_count'),
            func.sum(Projection.tickets_sold).label('weekly_admissions'),
            func.sum(Projection.revenue).label('weekly_earnings'),
            func.count(func.distinct(CinemaHall.cinema_properties_id)).label('cinema_count')
        ).join(Movie).join(CinemaHall)\
        .filter(Projection.date.between(week_start, week_end))\
        .group_by(Projection.movie_id)\
        .order_by(desc(func.sum(Projection.revenue)))\
        .limit(20)\
        .all()

        if not current_week_data:
            flash(f'Nema podataka za nedelju {selected_week} u {selected_year}. godini', 'info')
            return render_template('box_office.html',
                                route_name=route_name,
                                movies=[],
                                totals={
                                    'weekly_bo': 0,
                                    'weekly_sales': 0,
                                    'previous_bo': 0,
                                    'previous_sales': 0,
                                    'total_bo': 0,
                                    'total_sales': 0
                                },
                                years=range(2020, datetime.now().year + 1),
                                current_year=current_year,
                                current_week=current_week)

        # Upit za prethodnu nedelju
        prev_week_data = db.session.query(
            Projection.movie_id,
            func.sum(Projection.tickets_sold).label('prev_admissions'),
            func.sum(Projection.revenue).label('prev_earnings')
        ).filter(Projection.date.between(prev_week_start, prev_week_end))\
        .group_by(Projection.movie_id)\
        .all()

        # Upit za ukupne podatke
        total_data = db.session.query(
            Projection.movie_id,
            func.sum(Projection.tickets_sold).label('total_admissions'),
            func.sum(Projection.revenue).label('total_earnings'),
            func.count(func.distinct(
                func.strftime('%Y-%W', Projection.date)
            )).label('weeks_shown')
        ).group_by(Projection.movie_id)\
        .all()

        # Kreiranje rečnika za brži pristup podacima
        prev_week_dict = {d.movie_id: d for d in prev_week_data}
        total_dict = {d.movie_id: d for d in total_data}

        # Dobavljanje prethodnih pozicija
        prev_positions = {}
        if prev_week_data:
            sorted_prev = sorted(prev_week_data, 
                               key=lambda x: x.prev_earnings if x.prev_earnings is not None else 0, 
                               reverse=True)
            prev_positions = {d.movie_id: idx + 1 for idx, d in enumerate(sorted_prev)}

        # Priprema podataka za prikaz
        movies_data = []
        for i, entry in enumerate(current_week_data, 1):
            movie = Movie.query.get(entry.movie_id)
            prev_data = prev_week_dict.get(entry.movie_id)
            total_data = total_dict.get(entry.movie_id)

            # Računanje procenta promene
            prev_earnings = prev_data.prev_earnings if prev_data else 0
            percent_change = None
            if prev_earnings and prev_earnings > 0:
                percent_change = ((entry.weekly_earnings - prev_earnings) / prev_earnings * 100)

            # Određivanje promene pozicije
            if not prev_data:
                change = 'NEW'
            else:
                prev_pos = prev_positions.get(entry.movie_id, 0)
                if prev_pos == i:
                    change = 'SAME'
                elif prev_pos > i:
                    change = 'UP'
                else:
                    change = 'DOWN'

            movies_data.append({
                'position': i,
                'movie': movie,
                'change': change,
                'weeks_shown': total_data.weeks_shown if total_data else 1,
                'cinema_count': entry.cinema_count or 0,
                'weekly_earnings': entry.weekly_earnings or 0,
                'weekly_admissions': entry.weekly_admissions or 0,
                'change_percentage': percent_change,
                'previous_earnings': prev_earnings,
                'previous_admissions': prev_data.prev_admissions if prev_data else 0,
                'total_earnings': total_data.total_earnings if total_data else entry.weekly_earnings,
                'total_admissions': total_data.total_admissions if total_data else entry.weekly_admissions
            })

        # Računanje ukupnih vrednosti
        totals = {
            'weekly_bo': sum(m['weekly_earnings'] for m in movies_data),
            'weekly_sales': sum(m['weekly_admissions'] for m in movies_data),
            'previous_bo': sum(m['previous_earnings'] for m in movies_data),
            'previous_sales': sum(m['previous_admissions'] for m in movies_data),
            'total_bo': sum(m['total_earnings'] for m in movies_data),
            'total_sales': sum(m['total_admissions'] for m in movies_data)
        }

        years = range(2020, datetime.now().year + 1)

        return render_template('box_office.html',
                            route_name=route_name,
                            movies=movies_data,
                            totals=totals,
                            years=years,
                            current_year=current_year,
                            current_week=current_week)

    except Exception as e:
        flash(f'Došlo je do greške: {str(e)}', 'error')
        return render_template('box_office.html',
                            route_name=route_name,
                            movies=[],
                            totals={
                                'weekly_bo': 0,
                                'weekly_sales': 0,
                                'previous_bo': 0,
                                'previous_sales': 0,
                                'total_bo': 0,
                                'total_sales': 0
                            },
                            years=range(2020, datetime.now().year + 1),
                            current_year=current_year,
                            current_week=current_week)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    route_name = request.endpoint
    return render_template('contact.html', route_name=route_name)