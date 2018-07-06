from flask import Blueprint
from flask_restful import Resource, Api

from ebi_image_service.logger import config_logger
from ebi_image_service.utils.driver import WebDriver

logger = config_logger(__name__, 'info', 'image.log')
image_bp = Blueprint('image', __name__)
api = Api(image_bp)


class ImageHandler(Resource):

    def get(self, url):
        logger.info('[ImageHandler] GET starts, url: %s', url)

        with WebDriver() as driver:
            driver.get(url)

        return {'success': True}


api.add_resource(ImageHandler, '/image')
