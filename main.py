from fastapi import FastAPI
import os
import uvicorn

app = FastAPI()

FILE_PATH = "/app/data/test_file.txt"

@app.get("/")
def landing(name:str = "Stranger"):
    return {"message": f"Hello, {name}!"}
    
@app.get("/secret")
def read_secret():
    secret_value = os.getenv("MY_SECRET_KEY", "Secret not found")
    return {"Secret Value": secret_value}

@app.get("/configmap")
def read_configmap():
    configmap_value = os.getenv("MY_CONFIG_MAP", "Secret not found")
    return {"Secret Value": configmap_value}

@app.post("/write")
def write_to_file(content: str):
    try:
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)  # Ensure directory exists
        with open(FILE_PATH, "w") as file:
            file.write(content)
        return {"message": "Content written to file successfully!", "written_content": content}
    except Exception as e:
        return {"error": str(e)}

@app.get("/read")
def read_from_file():
    try:
        with open(FILE_PATH, "r") as file:
            file_content = file.read()
        return {"message": "Content read successfully!", "file_content": file_content}
    except FileNotFoundError:
        return {"error": "File not found. Write some content first!"}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)