FROM pypy:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
ADD /config/requirements.txt /config/
RUN pip install --no-cache-dir -r /config/requirements.txt
RUN pip install psycopg2cffi
RUN mkdir /src;
WORKDIR /src
