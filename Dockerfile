# Using the base image with Python 3.10
FROM python:3.10

# Set our working directory as app
WORKDIR /app
# Installing Python packages through requirements.txt file
# RUN pip install -r requirements.txt
RUN pip install flask gunicorn keras numpy scikit-learn tensorflow Werkzeug

# Copy the model's directory and server.py files
ADD ./model ./model
ADD app.py app.py

# Exposing port 5000 from the container
EXPOSE 5000
# Starting the Python application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]