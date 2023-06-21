FROM python:3.11.3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.4.2

RUN pip install "poetry==$POETRY_VERSION"

# Set working directory
WORKDIR /code

# Install dependencies
COPY ./pyproject.toml ./poetry.lock /code/
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy project files
COPY . /code/

# Expose port (if needed)
EXPOSE 8000

# Run migrations and start the server
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000