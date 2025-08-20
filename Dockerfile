FROM python:3.9-windowsservercore

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN pip install pyinstaller

CMD ["python", "build_config.py"]