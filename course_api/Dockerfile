FROM python:3.11

RUN apt update && apt install tzdata -y
ENV TZ="America/Sao_Paulo"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY *.py /app
COPY routes routes

CMD ["uvicorn", "api:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]