FROM python
RUN pip install fastapi uvicorn
WORKDIR /app
COPY . .
WORKDIR /app/src
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
