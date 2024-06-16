FROM python:3.10

RUN mkdir /tg_bot

WORKDIR /tg_bot

COPY requirements_bot.txt .

RUN pip install --root-user-action=ignore -r requirements_bot.txt

COPY ../.. .

#RUN chmod a+x ./docker/*.sh

CMD python3 main.py