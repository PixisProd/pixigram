FROM python:3.13-slim


RUN pip install --no-cache-dir poetry


WORKDIR /app


COPY ../poetry.lock .
COPY ../pyproject.toml .
RUN poetry install --no-root


COPY . .


EXPOSE 8000


CMD [ "poetry", "run", "uvicorn", "server.src.main:app", "--host", "0.0.0.0", "--port", "8000" ]