FROM python:3.9.16
ENV TZ="Asia/Bangkok"
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt
COPY ./ /code
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
