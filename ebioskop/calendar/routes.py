from datetime import datetime, timedelta
from flask import Blueprint, render_template, request

from ebioskop.models import Movie


calendars = Blueprint('calendars', __name__)


@calendars.route('/distribution_calendar')
def distribution_calendar():
    # Get the start date from the query parameters or use two weeks ago as default
    start_date_str = request.args.get('start_date')
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = datetime.now().date() - timedelta(days=14)

    # Query movies starting from the start date, ordered by start date
    movies = Movie.query.filter(Movie.release_date >= start_date).order_by(Movie.release_date).all()

    # Group movies by start date
    movie_groups = {}
    for movie in movies:
        if movie.release_date not in movie_groups:
            movie_groups[movie.release_date] = []
        movie_groups[movie.release_date].append(movie)
    
    today = datetime.now().date()

    return render_template('distribution_calendar.html', 
                            movie_groups=movie_groups,
                            today=today,
                            start_date=start_date)