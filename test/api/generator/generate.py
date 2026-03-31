import json
import os
import sys
from pathlib import Path

def find_script(scripts_dir, method, path):
    clean_path = path.replace('/api/', '').replace('/', '-').strip('-')
    script_name = f"after-{clean_path}.js"
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
    
    path_groups = {}
    
    for path, methods in openapi.get("paths", {}).items():
        for method, details in methods.items():
            if method.lower() not in ["get", "post", "put", "delete", "patch"]:
                continue
            
            path_parts = [p for p in path.strip("/").split("/") if p]
            
            if len(path_parts) >= 3:
                module_name = path_parts[1] if len(path_parts) > 1 else "other"
                endpoint_name = path_parts[-1]
                
                if module_name not in path_groups:
                    path_groups[module_name] = {
                        "name": module_name,
                        "item": []
                    }
                
                endpoint_group = None
                for item in path_groups[module_name]["item"]:
                    if item["name"] == endpoint_name:
                        endpoint_group = item
                        break
                
                if not endpoint_group:
                    endpoint_group = {
                        "name": endpoint_name,
                        "item": []
                    }
                    path_groups[module_name]["item"].append(endpoint_group)
                
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
                
                endpoint_group["item"].append(item)
            else:
                module_name = "other"
                
                if module_name not in path_groups:
                    path_groups[module_name] = {
                        "name": module_name,
                        "item": []
                    }
                
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
                
                path_groups[module_name]["item"].append(item)
    
    api_group["item"] = list(path_groups.values())
    collection["item"] = [api_group]
    
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)
    
    return output_path

def main():
    current_dir = Path(__file__).parent
    openapi_path = current_dir.parent / "env" / "api-docs.json"
    scripts_dir = current_dir.parent / "script"
    env_path = current_dir.parent / "env" / "iia-dev.postman_environment.json"
    output_path = current_dir / "generated" / "iia-server-collection.json"
    
    if not openapi_path.exists():
        print(f"Error: OpenAPI file not found: {openapi_path}")
        sys.exit(1)
    
    result = generate_collection(openapi_path, scripts_dir, env_path, output_path)
    print(f"Generated: {result}")

if __name__ == "__main__":
    main()