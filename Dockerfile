# Dockerfile
FROM python:3.12

WORKDIR /app

# kopira requirments i instalira
COPY requirments.txt .
RUN pip install -r requirments.txt

# kopira flask prilojenieto
COPY . .

# pokazva porta
EXPOSE 5000

# zapochva flask prilojenieto
CMD ["python", "app.py"]
