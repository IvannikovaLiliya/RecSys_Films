FROM python:3.10

RUN mkdir /fastapi_app1

WORKDIR /fastapi_app1

COPY requirements_api.txt .

RUN pip install --root-user-action=ignore -r requirements_api.txt

COPY ../.. .

RUN chmod a+x ./*.sh

CMD ./api_run.sh