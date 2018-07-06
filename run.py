import os

from ebi_image_service import create_app
from ebi_image_service.configuration import get_config

app = create_app(get_config(os.getenv('ENV', 'develop')))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
