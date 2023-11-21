FROM 841964127262.dkr.ecr.us-east-1.amazonaws.com/ecr-base-image:alpine3.18-python_3.11.5-sec AS develop

WORKDIR /app

ADD . .

ENV HOST_IP=0.0.0.0
ENV HOST_PORT=22

#Comando para ejecutar proceso principal
CMD ["python", "./src/main.py"]
