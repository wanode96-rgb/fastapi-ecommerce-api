FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Save it.

Then also create a `.dockerignore` file in the same root folder with this content:
```
venv/
__pycache__/
*.pyc
*.pyo
.env
.git
*.md