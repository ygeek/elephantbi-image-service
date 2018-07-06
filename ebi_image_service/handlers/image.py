from flask import Blueprint
from flask_restful import Resource, Api, reqparse

from ebi_image_service.logger import config_logger
from ebi_image_service.utils.driver import WebDriver

logger = config_logger(__name__, 'info', 'image.log')
image_bp = Blueprint('image', __name__)
api = Api(image_bp)

# parser:
parser = reqparse.RequestParser()
parser.add_argument(
    'url',
    type=str,
    required=True,
    location='args'
)


class ImageHandler(Resource):

    def get(self):
        args = parser.parse_args()
        logger.info('[ImageHandler] GET starts, args: %s', args)

        with WebDriver() as driver:
            driver.get(args['url'])

        return {'success': True}


api.add_resource(ImageHandler, '/image')
