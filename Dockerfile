# our base image
FROM python

WORKDIR /nlp

# install Python modules needed by the Python app
COPY requirements.txt /nlp
RUN pip3 install --no-cache-dir -r ./requirements.txt

# copy files required for the app to run
COPY main.py /nlp
COPY nlp.py /nlp
COPY nltk.txt /nlp


# tell the port number the container should expose
EXPOSE 5000

RUN python3 -m spacy download en

# run the application
CMD ["python3", "/nlp/main.py"]
