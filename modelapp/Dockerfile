FROM python:3.7

#RUN mkdir -p /home/appuser/app
WORKDIR /home/appuser/app

# Expose the port uWSGI will listen on
#EXPOSE 5000

# Copy the requirements file in order to install
# Python dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uwsgi

# Copy the rest of the codebase into the image
COPY . /home/appuser/app

# run the command to start uWSGI
CMD [ "/usr/local/bin/uwsgi", "--ini", "app.ini" ]
