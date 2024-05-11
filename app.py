from flask import Flask, request, jsonify
from models.meal import Meal
from database import db

app = Flask(__name__)

app.config['SECRET_KEY'] = 'how_you_doin'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

@app.route('/meal', methods=['POST'])
def add_meal():
	data = request.json
	name = data.get('name')
	description = data.get('description')
	date_time = data.get('date_time')
	on_diet = False
	if data.get('on_diet') == 'true':
		on_diet = True
	
	if name:
		meal = Meal(name=name, description=description, date_time=date_time, on_diet=on_diet)
		db.session.add(meal)
		db.session.commit()
		return jsonify({'message': 'Meal registred successfully'})
	
	return jsonify({'message': 'Invalid informations'}), 400

@app.route('/meal/<int:meal_id>', methods=['PATCH'])
def update_meal(meal_id):
	meal = Meal.query.get(meal_id)

	if not meal:
		return jsonify({'message': 'Meal not found'}), 404
	
	data = request.json
	if 'name' in data:
		meal.name = data['name']
	
	if 'description' in data:
		meal.description = data['description']
	
	if 'date_time' in data:
		meal.date_time = data['date_time']
	
	if 'on_diet' in data:
		if 'on_diet' == 'true':
			meal.on_diet = True
		else:
			meal.on_diet = False
	
	db.session.commit()

	return jsonify({'message': 'Meal updated successufully.'})

@app.route('/meal/<int:meal_id>', methods=['DELETE'])
def delete_meal(meal_id):
	meal = Meal.query.get(meal_id)

	if not meal:
		return jsonify({'message': 'Meal not found'}), 404
	
	db.session.delete(meal)
	db.session.commit()
	return jsonify({'message': 'Meal deleted successfully.'})

@app.route('/meals', methods=['GET'])
def get_meals():
	meals = Meal.query.all()

	meal_list = []
	for meal in meals:
		meal_data ={
			'id': meal.id,
			'name': meal.name,
			'description': meal.description,
			'date_time': meal.date_time,
			'on diet': meal.on_diet
		}
		meal_list.append(meal_data)
	
	return jsonify(meal_list)

@app.route('/meal/<int:meal_id>', methods=['GET'])
def get_meal(meal_id):
	meal = Meal.query.get(meal_id)

	if not meal:
		return jsonify({'message': 'Meal not found'}), 404
	
	return jsonify({
		'id': meal.id,
		'name': meal.name,
		'description': meal.description,
		'date time': meal.date_time,
		'on diet': meal.on_diet
	})


@app.route('/hellow_world', methods=['GET'])
def hello_world():
	return 'Hello World'

if __name__ == '__main__':
	app.run(debug=True)
