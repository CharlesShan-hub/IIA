# IIA Postman Collection Generator

Simple script to generate Postman Collection from OpenAPI specification.

## Usage

1. Make sure you have `uv` installed
2. Run `uv sync` to setup environment
3. Run `uv run python generate.py`

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