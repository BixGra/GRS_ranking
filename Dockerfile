FROM python:3.10

WORKDIR /etc/GRS_ranking

COPY ./requirements.txt /etc/GRS_ranking/.

RUN pip install --upgrade pip && pip --no-cache-dir install -r /etc/GRS_ranking/requirements.txt

COPY . /etc/GRS_ranking/.

ENV PYTHONPATH $PYTHONPATH:$PATH:/etc/GRS_ranking/src/

ENV PATH /opt/conda/envs/env/bin:$PATH

ENV PROJECT_PATH /etc/GRS_ranking/src/

RUN python src/init/database.py

RUN python src/init/ranking.py

EXPOSE 8000

ENTRYPOINT gunicorn -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker src.main:app --threads 2 --workers 1 --timeout 1000 --graceful-timeout 30
