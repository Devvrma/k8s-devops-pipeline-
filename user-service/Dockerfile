FROM python:3.9-slim
WORKDIR /app
COPY . .
# Flask ke saath boto3 bhi install kar lo
RUN pip install flask boto3 
EXPOSE 5002
CMD ["python", "app.py"]