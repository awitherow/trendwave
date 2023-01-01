FROM python:3.10.9
WORKDIR /usr/src/app
RUN pip install pipenv
COPY ../Pipfile ../Pipfile.lock ${WORKDIR}
COPY . .
RUN pipenv install --system --deploy
CMD [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0" ]