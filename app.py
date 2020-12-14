import dateutil.parser
import babel
import logging
from logging import FileHandler, Formatter
from flask_cors import CORS
from flask import Flask
from config import Config


def create_app(config_class=Config):

    app = Flask(
        __name__,
        static_url_path='/static',
        template_folder='templates')

    app.config.from_object(config_class)
    app.app_context().push()

    CORS(app, resources={'/': {'origins': 'http://localhost'}})

    app.secret_key = app.config['CLIENT_SECRET']

    # ---------------------------------------------------------------------------
    # Pagination code for displaying database items
    # Unused as of now; save for future implementation
    # ---------------------------------------------------------------------------
    #
    # def paginate_items(request, selection):
    #     page = request.args.get('page', 1, type=int)
    #     start = (page - 1) * ITEMS_PER_PAGE
    #     end = start + ITEMS_PER_PAGE

    #     products = [product.format() for product in selection]
    #     current_products = products[start: end]

    #     return current_products

    # ----------------------------------------------------------------------------
    # Filters
    # ----------------------------------------------------------------------------

    def format_datetime(value, format='medium'):
        date = dateutil.parser.parse(value)
        if format == 'full':
            format = "EEEE MMMM, d, y 'at' h:mma"
        elif format == 'medium':
            format = "EE MM, dd, y h:mma"
        return babel.dates.format_datetime(date, format)

    app.jinja_env.filters['datetime'] = format_datetime

    # app.register_blueprint(swagger_bp, url_prefix='/swagger')

    if not app.debug:
        file_handler = FileHandler('error.log')
        file_handler.setFormatter(
            Formatter('%(asctime)s %(levelname)s: \
                %(message)s [in %(pathname)s:%(lineno)d]')
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('errors')

    return app
