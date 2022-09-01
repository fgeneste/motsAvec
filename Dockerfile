FROM python:3.9-slim

ENV MICRO_SERVICE=/home/app/webapp
# set work directory
RUN mkdir -p $MICRO_SERVICE
# where your code lives
WORKDIR $MICRO_SERVICE

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
# copy project
COPY . $MICRO_SERVICE
RUN pip install -r requirements.txt
RUN rm -f /usr/local/bin/pip
RUN rm -f /usr/local/bin/pip3
RUN rm -f /usr/local/bin/pip3.9
RUN rm -rf /home/.cache/pip
#RUN pip uninstall pip
EXPOSE 8501
CMD streamlit run main.py --server.enableCORS=false --server.enableXsrfProtection=false