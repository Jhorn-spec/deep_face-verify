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

    # process the image to get the image id
    # if corressponding user not found, throw error that user not in database
    # Expected return imageid
    image_id = process_image_id(image_file)

    if image_id == "error":
        return jsonify({'message': 'User not found'}), 404

    # testing remove when testing with live image
    if image_id is None:
        image_id = 'testid1245'

    # Get user data with image_id
    user = User.query.filter_by(image_id=image_id).first()
   

    return jsonify({'user': user.format()}), 200
