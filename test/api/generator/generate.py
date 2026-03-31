import json
import os
import sys
from pathlib import Path
import argparse
import urllib.request
import urllib.error

def find_script(scripts_dir, method, path):
    clean_path = path.replace('/api/', '').replace('/', '-').strip('-')
    
    script_names = [
        f"after-{clean_path}.js",
    ]
    
    parts = clean_path.split('-')
    if len(parts) > 1:
        module = parts[0]
        method_name = '-'.join(parts[1:])
        method_name_no_dash = method_name.replace('-', '')
        script_names.append(f"after-{module}-{method_name_no_dash}.js")
    
    for script_name in script_names:
        script_path = scripts_dir / script_name
        if script_path.exists():
            with open(script_path, 'r', encoding='utf-8') as f:
                return f.read().splitlines()
    
    return None

def load_environment(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        env_data = json.load(f)
    
    variables = []
    for item in env_data.get("values", []):
        variables.append({
            "key": item["key"],
            "value": item["value"]
        })
    
    return variables

def generate_body_from_schema(openapi, details):
    request_body = details.get("requestBody")
    if not request_body:
        return None
    
    content = request_body.get("content", {})
    if "application/json" not in content:
        return None
    
    schema_info = content["application/json"]
    schema = schema_info.get("schema", {})
    
    if "$ref" in schema:
        ref_path = schema["$ref"]
        if ref_path.startswith("#/components/schemas/"):
            schema_name = ref_path.split("/")[-1]
            components = openapi.get("components", {})
            schemas = components.get("schemas", {})
            if schema_name in schemas:
                schema = schemas[schema_name]
    
    properties = schema.get("properties", {})
    if not properties:
        return None
    
    body_data = {}
    for prop_name, prop_schema in properties.items():
        example_value = prop_schema.get("example")
        if example_value is not None:
            body_data[prop_name] = example_value
        else:
            default_value = prop_schema.get("default")
            if default_value is not None:
                body_data[prop_name] = default_value
            else:
                prop_type = prop_schema.get("type", "string")
                if prop_type == "string":
                    body_data[prop_name] = f"{{{{{prop_name}}}}}"
                elif prop_type == "number" or prop_type == "integer":
                    body_data[prop_name] = 0
                elif prop_type == "boolean":
                    body_data[prop_name] = False
                elif prop_type == "array":
                    body_data[prop_name] = []
                elif prop_type == "object":
                    body_data[prop_name] = {}
    
    if not body_data:
        return None
    
    return {
        "mode": "raw",
        "raw": json.dumps(body_data, indent=4),
        "options": {
            "raw": {
                "language": "json"
            }
        }
    }

def generate_collection(openapi_path, scripts_dir, env_path, output_path):
    with open(openapi_path, 'r', encoding='utf-8') as f:
        openapi = json.load(f)
    
    collection = {
        "info": {
            "name": openapi["info"].get("title", "IIA Server API"),
            "description": openapi["info"].get("description", ""),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [],
        "variable": []
    }
    
    if env_path.exists():
        env_variables = load_environment(env_path)
        collection["variable"] = env_variables
    else:
        collection["variable"] = [
            {
                "key": "baseUrl",
                "value": "http://localhost:9424"
            }
        ]
    
    api_group = {
        "name": "api",
        "item": []
    }
    
    def get_or_create_group(parent, name):
        for item in parent.get("item", []):
            if item["name"] == name:
                return item
        new_group = {"name": name, "item": []}
        parent["item"].append(new_group)
        return new_group
    
    for path, methods in openapi.get("paths", {}).items():
        for method, details in methods.items():
            if method.lower() not in ["get", "post", "put", "delete", "patch"]:
                continue
            
            path_parts = [p for p in path.strip("/").split("/") if p]
            
            if len(path_parts) >= 3:
                current_group = api_group
                
                for i in range(1, len(path_parts) - 1):
                    part = path_parts[i]
                    current_group = get_or_create_group(current_group, part)
                
                endpoint_name = path_parts[-1]
                item_name = details.get("summary")
                if not item_name:
                    item_name = f"{method.upper()} {endpoint_name.replace('-', ' ').title()}"
                
                request = {
                    "method": method.upper(),
                    "header": [
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        },
                        {
                            "key": "Accept",
                            "value": "application/json"
                        }
                    ],
                    "url": {
                        "raw": f"{{{{baseUrl}}}}{path}",
                        "host": ["{{baseUrl}}"],
                        "path": path_parts
                    },
                    "description": details.get("description", "")
                }
                
                security = details.get("security")
                if security:
                    request["auth"] = {
                        "type": "bearer",
                        "bearer": [
                            {
                                "key": "token",
                                "value": "{{bearerToken}}",
                                "type": "string"
                            }
                        ]
                    }
                
                body = generate_body_from_schema(openapi, details)
                if body:
                    request["body"] = body
                
                item = {
                    "name": item_name,
                    "request": request,
                    "response": []
                }
                
                script_content = find_script(scripts_dir, method, path)
                if script_content:
                    item["event"] = [
                        {
                            "listen": "test",
                            "script": {
                                "type": "text/javascript",
                                "exec": script_content
                            }
                        }
                    ]
                
                current_group["item"].append(item)
            else:
                item_name = details.get("summary")
                if not item_name:
                    item_name = f"{method.upper()} {path}"
                
                request = {
                    "method": method.upper(),
                    "header": [
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        },
                        {
                            "key": "Accept",
                            "value": "application/json"
                        }
                    ],
                    "url": {
                        "raw": f"{{{{baseUrl}}}}{path}",
                        "host": ["{{baseUrl}}"],
                        "path": path_parts
                    },
                    "description": details.get("description", "")
                }
                
                body = generate_body_from_schema(openapi, details)
                if body:
                    request["body"] = body
                
                item = {
                    "name": item_name,
                    "request": request,
                    "response": []
                }
                
                script_content = find_script(scripts_dir, method, path)
                if script_content:
                    item["event"] = [
                        {
                            "listen": "test",
                            "script": {
                                "type": "text/javascript",
                                "exec": script_content
                            }
                        }
                    ]
                
                api_group["item"].append(item)
    collection["item"] = [api_group]
    
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)
    
    return output_path

def download_openapi_json(url, dest_path):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read()
    data = json.loads(raw.decode("utf-8"))
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return dest_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--openapi-url", default=os.environ.get("OPENAPI_URL", "http://localhost:9424/v3/api-docs"))
    args = parser.parse_args()

    current_dir = Path(__file__).parent
    openapi_path = current_dir.parent / "env" / "api-docs.json"
    scripts_dir = current_dir.parent / "script"
    env_path = current_dir.parent / "env" / "iia-dev.postman_environment.json"
    output_path = current_dir / "generated" / "iia-server-collection.json"
    
    if args.download or not openapi_path.exists():
        try:
            download_openapi_json(args.openapi_url, openapi_path)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as e:
            print(f"Error: Failed to download OpenAPI json from {args.openapi_url}: {e}")
            if not openapi_path.exists():
                sys.exit(1)
    
    result = generate_collection(openapi_path, scripts_dir, env_path, output_path)
    print(f"Generated: {result}")

if __name__ == "__main__":
    main()
