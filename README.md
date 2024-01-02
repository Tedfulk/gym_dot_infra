# My FastAPI Application

This is a basic scaffold for a FastAPI application.

## Project Structure

The project has the following structure:

- `app/main.py`: The entry point of the FastAPI application.
- `tests/test_main.py`: Contains tests for the `main.py` file.

## Setup

1. Install the required packages:

```bash
poetry install
```

1. Run the application:

```bash
uvicorn app.main:app --reload
```

## Testing

To run the tests, use the following command:

```bash
pytest
```

## Contributing

Contributions are welcome. Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
