FROM python:3.8
COPY . /bitrix24_test_1
WORKDIR /bitrix24_test_1

RUN pip install -r requirements.txt
CMD ["python", "main.py"]