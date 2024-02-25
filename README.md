# FastAPI Currency Conversion API

This project is a FastAPI application that provides an API for currency conversion. It allows fetching current exchange rates from an external API, storing them in a PostgreSQL database, and converting amounts between different currencies.

## Features

- Fetch and update exchange rates from an external API.
- Convert amounts between currencies using the latest exchange rates.
- Display the date and time of the last update of exchange rates.

## Prerequisites

- Docker
- Docker Compose

## Setup and Running

### Clone the Repository

First, clone this repository to your local machine:
```bash
git clone https://github.com/israelian/currency_converter_api.git
cd currency_converter_api
```

### Configuration

1. **Environment Variables**: Create a `.env` file in the root of your project directory. Replace here `your_exchange_api_key` with your actual external exchange API key.

   ```dotenv
   EXCHANGE_API_KEY=your_exchange_api_key
   ```

### Build and Start the Application

Use Docker Compose to build and start the application:

```bash
docker-compose up --build
```

### Applying Database Migrations

After the containers are up, apply database migrations to set up the initial schema:

```bash
docker-compose exec web alembic upgrade head
```

This command runs Alembic migrations within the `web` service container.

### Accessing the Application

With the application running, you can access the API at `http://localhost:8000`.

## API Endpoints

- **Update Exchange Rates**: `POST /update-rates/`

- **Convert Currency**: `GET /convert/?source={source_currency_code}&target={target_currency_code}&amount={amount}`
Example: `localhost:8000/convert?source=AMD&target=USD&amount=500`

- **Last Update Time**: `GET /last-update/`

## Running Tests

To run the automated tests for the application, use the following command:

```bash
docker-compose exec web pytest .tests.py
```

## Stopping the Application

To stop and remove the containers, use:

```bash
docker-compose down
```
