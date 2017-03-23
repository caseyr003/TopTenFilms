import webbrowser

class Movie():
    """
    The Movie Class contains relevant information for each movie

    Attributes:
        title (str): the title of the movie
        summary (str): a breif summary of the movie
        rating (str): rating out of 10 that The MovieDB rated the movie
        runtime (str): movie length in terms of hours and minutes
        year (str): the year the movie was released
        cover_image_url (str): url that contains the backdrop image
        poster_image_url (str): url that contains the poster image
        trailer_youtube_url (str): url that contains the youtube trailer
    """

    def __init__(self, movie_title, movie_summary, movie_rating, movie_runtime, movie_year, cover_image, poster_image, trailer_youtube):
        self.title = movie_title
        self.summary = movie_summary
        self.rating = movie_rating
        self.runtime = movie_runtime
        self.year = movie_year
        self.cover_image_url = cover_image
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube
