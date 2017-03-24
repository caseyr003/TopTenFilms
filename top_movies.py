import webbrowser
import os
import re


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Casey's Top Ten Movies</title>
    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <link rel='stylesheet' media='screen' href='css/style.css' />
    <link rel='stylesheet' media='screen and (max-width: 991px)' href='css/small.css' />
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-info', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Casey's Top Ten Movies</a>
          </div>
        </div>
      </div>
    </div>
    <!-- Top Movies Content -->
    {movie_tiles}
    <div class="container">
      <div class="row">
        <div class="col-md-12 popular-title">
           <h2>Popular Movies on TMDB</h2>
        </div>
      </div>
    </div>
    <div class="container">
      <div class="row">
        {popular_movie_tiles}
      </div>
    </div>
    <footer>
      <h2>Thanks for checking out my top ten movies list!</h2>
      <h4>This project was created as part of Udacity's Full Stack Developer Nanodegree</h4>
      <h5>Feel free to connect with me below</h5>
      <a href="https://github.com/caseyr003">Github</a> | <a href="https://www.linkedin.com/in/casey003/">LinkedIn</a> | <a href="mailto:caseyross003@gmail.com">Email</a>
    </footer>
  </body>
</html>
'''


# A single movie entry with content on the right html template
movie_tile_content_right = '''
<div class="movie-container" style="background-image: url({cover_image_url})">
  <div class="container">
     <div class="row">
        <div class="col-md-4 rank-right">
           <h1>{movie_rank}</h1>
        </div>
        <div class="col-md-7 movie-info movie-tile pull-right" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
            <img class="poster-img" src="{poster_image_url}" width="180" height="280">
            <h2>{movie_title}</h2>
            <h6>{movie_year} | {movie_runtime} | {movie_rating}</h6>
            <h4>Overview</h4>
            <p>{movie_summary}</p>
            <img class="attribution-img" src="https://www.themoviedb.org/assets/static_cache/bb45549239e25f1770d5f76727bcd7c0/images/v4/logos/408x161-powered-by-rectangle-blue.png" width="127" height="50">
        </div>
     </div>
  </div>
</div>
'''


# A single movie entry with content on the left html template
movie_tile_content_left = '''
<div class="movie-container" style="background-image: url({cover_image_url})">
   <div class="container">
     <div class="row">
        <div class="col-md-7 movie-info movie-tile" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
            <img class="poster-img" src="{poster_image_url}" width="180" height="280">
            <h2>{movie_title}</h2>
            <h6>{movie_year} | {movie_runtime} | {movie_rating}</h6>
            <h4>Overview</h4>
            <p>{movie_summary}</p>
            <img class="attribution-img" src="https://www.themoviedb.org/assets/static_cache/bb45549239e25f1770d5f76727bcd7c0/images/v4/logos/408x161-powered-by-rectangle-blue.png" width="127" height="50">
        </div>
        <div class="col-md-4">
           <h1 class="rank-left">{movie_rank}</h1>
        </div>
     </div>
   </div>
</div>
'''

# A single popular movie entry html template
popular_movie_tile_content = '''
<div class="col-md-6">
   <div class="popular-movie-info" style="background-image: url({cover_image_url})">
      <img class="poster-img" src="{poster_image_url}" width="180" height="280">
      <h2>{movie_title}</h2>
      <h6>{movie_year} | {movie_rating}</h6>
      <img class="attribution-img" src="https://www.themoviedb.org/assets/static_cache/bb45549239e25f1770d5f76727bcd7c0/images/v4/logos/408x161-powered-by-rectangle-blue.png" width="127" height="50">
   </div>
</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for index, movie in enumerate(movies):
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        if index % 2 != 0:
            content += movie_tile_content_left.format(
                movie_title=movie.title,
                movie_summary=movie.summary,
                movie_rating=movie.rating,
                movie_runtime=movie.runtime,
                movie_year=movie.year,
                cover_image_url=movie.cover_image_url,
                poster_image_url=movie.poster_image_url,
                trailer_youtube_id=trailer_youtube_id,
                movie_rank=index+1
            )
        else:
            content += movie_tile_content_right.format(
                movie_title=movie.title,
                movie_summary=movie.summary,
                movie_rating=movie.rating,
                movie_runtime=movie.runtime,
                movie_year=movie.year,
                cover_image_url=movie.cover_image_url,
                poster_image_url=movie.poster_image_url,
                trailer_youtube_id=trailer_youtube_id,
                movie_rank=index+1
            )
    return content


def create_popular_movie_tiles_content(popular_movies):
    # The HTML content for this section of the page
    content = ''
    for movie in popular_movies:
        # Append the tile for the popular movie with its content filled in
        content += popular_movie_tile_content.format(
            movie_title=movie.title,
            movie_rating=movie.rating,
            movie_year=movie.year,
            cover_image_url=movie.cover_image_url,
            poster_image_url=movie.poster_image_url,
        )
    return content


def open_movies_page(movies, popular_movies):
    # Create or overwrite the output file
    output_file = open('top_movies.html', 'w')

    # Replace the movie/popular movie tiles placeholders with generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies),
        popular_movie_tiles=create_popular_movie_tiles_content(popular_movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)
