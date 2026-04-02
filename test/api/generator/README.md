# IIA Postman Collection Generator

Simple script to generate Postman Collection from OpenAPI specification.

## Usage

1. Make sure you have `uv` installed
2. Run `uv sync` to setup environment
3. Run the generator:
   - **Default (Auto-download & Generate)**:
     `uv run python generate.py`
   - **Skip download (Use local cache)**:
     `uv run python generate.py --skip-download`
   - **Specify OpenAPI URL**:
     `uv run python generate.py --openapi-url http://localhost:9424/v3/api-docs`

## Features

- **Auto-sync**: Automatically downloads latest OpenAPI spec from local server.
- **Dynamic Hierarchy**: Groups APIs into folders based on path depth.
- **Script Injection**: Matches and injects post-processing scripts from `../script/`.
- **Environment Sync**: Injects variables from `../env/iia-dev.postman_environment.json`.
- **DTO Support**: Generates request bodies from DTO definitions with default values.
- **Auth Support**: Automatically configures Bearer Token authentication.

## Files

- `generate.py` - Main script
- `pyproject.toml` - Python project configuration
- `../env/api-docs.json` - OpenAPI specification input
- `../script/*.js` - Postman post-script files
- `../env/iia-dev.postman_environment.json` - Postman environment variables
- `generated/iia-server-collection.json` - Generated Postman Collection

## Script Naming Convention

Scripts should be named as `after-{path}.js` where `{path}` is the API path without `/api/` prefix, with slashes replaced by hyphens.

Examples:
- `/api/auth/login` → `after-auth-login.js`
- `/api/auth/refresh` → `after-auth-refresh.js`
- `/api/auth/sendcode` → `after-auth-sendcode.js`