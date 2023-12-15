from flask import Blueprint, request, jsonify
from facemodel import db
from datetime import datetime
from facemodel.models.user import User
from facemodel.ImageProcessor.image import get_image_id


# Create a Blueprint for patient routes
raw_image_bp = Blueprint('raw_image', __name__, url_prefix='/api/v1/image')


@raw_image_bp.route('/', methods=['POST'])
def take_raw_image():
    if 'image' not in request.files or not all(key in request.form for key in ['email', 'first_name', 'last_name']):
        return jsonify({'message': 'Incomplete data or no file uploaded'}), 400

    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_file = request.files['image']

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'message': 'User already exists'}), 400

    # Check with the image if the user has been enrolled before
    image_id = get_image_id(image_file)
    print('image done', image_id)

    if image_id is None:
        image_id = 'testid1245'

    try:
        # Store image in User Db
        new_user = User(email=email, first_name=first_name, last_name=last_name, image_id=image_id)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User Created and Image processed successfully', 'userData': new_user.format()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to save image', 'error': str(e)}), 500


@raw_image_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    if not users:
        return jsonify({'message': 'No users found'}), 404
    return jsonify({'users': [user.format() for user in users], 'count': len(users)})