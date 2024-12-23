FROM python:3.10-slim

WORKDIR /BACKEND

RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    make \
    libopenblas-dev \
    liblapack-dev \
    libglib2.0-0 \
    libgl1-mesa-glx \
    && apt-get clean

COPY app /BACKEND/app
COPY templates /BACKEND/templates
COPY requirements.txt /BACKEND

RUN pip install --no-cache-dir -r requirements.txt

CMD ["fastapi", "run", "app/main.py"]