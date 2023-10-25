"""
Author: Andrew Benedictus Jamesie
Date: 2023/06/15
This is the app.py module
Usage:
- Routing the templates
- Core code for predict the machine learning
"""
import os
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)
model = load_model('model/model_smoteenn.h5', compile=False)
model.compile(
	optimizer=tf.optimizers.Adam(learning_rate=0.001),
	loss='binary_crossentropy',
	metrics=['accuracy']
)

@app.route('/')
def index():
	"""Render the index.html

	Returns:
		str: render template function
	"""
	return render_template('index.html')

@app.route('/about')
def about():
	"""Render the about.html

	Returns:
		str: render template function
	"""
	return render_template('about.html')

@app.route('/predict')
def predict():
	"""Render the predict.html

	Returns:
		str: render template function
	"""
	return render_template('predict.html')

def normalization(input_data):
	"""Perform data normalization on input data using MinMaxScaler()

	Args:
		input_data (np.array): Input data from the user that will be normalized

	Returns:
		(np.array): Normalized input data
	"""
	x_train = np.load('dataset/X_train_smoteenn.npy')
	x_test = np.load('dataset/X_test_smoteenn.npy')

	data_test = np.insert(x_test, 0, input_data, axis=0)
	print(f'\ninput data: {data_test[0]}')

	scaler = MinMaxScaler()
	scaler.fit(x_train)

	return scaler.transform(data_test)

@app.route('/result', methods=['GET', 'POST'])
def result():
	"""Render the predict.html

	Returns:
		str: render template function and result in boolean
	"""
	age = int(request.form['age'])
	iga = float(request.form['iga'])
	igg = float(request.form['igg'])
	igm = float(request.form['igm'])

	gender = 0 if request.form['gender'] == 'male' else 1

	diabetes = abdominal = sticky_stool = weight_loss = 0

	if request.form.get('diabetes'): diabetes = 1
	if request.form.get('abdominal'): abdominal = 1
	if request.form.get('sticky_stool'): sticky_stool = 1
	if request.form.get('weight_loss'): weight_loss = 1

	if request.form['dia_type'] == 'none': dia_type = 0
	elif request.form['dia_type'] == 'type 1': dia_type = 1
	else: dia_type = 2

	if request.form['diarrhoea'] == 'fatty': diarrhoea = 0
	elif request.form['diarrhoea'] == 'watery': diarrhoea = 1
	else: diarrhoea = 2

	if request.form['short_stature'] == 'variant': short_stature = 0
	elif request.form['short_stature'] == 'pss': short_stature = 1
	else: short_stature = 2

	if request.form['marsh_type'] == 'none': marsh_type = 0
	elif request.form['marsh_type'] == 'marsh type 0': marsh_type = 1
	elif request.form['marsh_type'] == 'marsh type 1': marsh_type = 2
	elif request.form['marsh_type'] == 'marsh type 2': marsh_type = 3
	elif request.form['marsh_type'] == 'marsh type 3a': marsh_type = 4
	elif request.form['marsh_type'] == 'marsh type 3b': marsh_type = 5
	else: marsh_type = 6

	input_data = [
		age, gender, diabetes, dia_type, diarrhoea, abdominal,
		short_stature, sticky_stool, weight_loss, iga, igg, igm, marsh_type
	]
	input_data_scaled = normalization(input_data)
	prediction = np.argmax(model.predict([input_data_scaled[[0]]]))

	if prediction == 0: classes = 'Atypical'
	elif prediction == 1: classes = 'Latent'
	elif prediction == 2: classes = 'None'
	elif prediction == 3: classes = 'Potential'
	elif prediction == 4: classes = 'Silent'
	else: classes = 'Typical'

	print(f'input data scaled: \n{input_data_scaled[[0]]}')
	print(f'prediction: {prediction}')
	print(f'classes: {classes}\n')

	return render_template('result.html', result=classes)

if __name__ == '__main__':
	app.run(debug=True, port=os.getenv('PORT', default=5000))