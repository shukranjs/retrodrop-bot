# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential

COPY . .

# Install Poetry
RUN pip install poetry

# Install Python dependencies via Poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi


# Expose any necessary ports (optional)
EXPOSE 8080

# Run the bot
CMD ["poetry", "run", "python", "main.py"]
