from flask import Blueprint, request, jsonify
from facemodel import db
from datetime import datetime
from facemodel.models.user import User
from facemodel.ImageProcessor.image import get_image_id, process_image_id


# Create a Blueprint for identify_image routes
identify_image_bp = Blueprint('identify_image', __name__, url_prefix='/api/v1/identify_image')


@identify_image_bp.route('/', methods=['POST'])
def identify_image():
    if 'image' not in request.files:
        return jsonify({'message': 'Incomplete data or no file uploaded'}), 400

    image_file = request.files['image']

    image_id = process_image_id(image_file)

    # testing
    if image_id is None:
        image_id = 'testid1245'

    # Get user data with image_id
    user = User.query.filter_by(image_id=image_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({'user': user.format()}), 200
