import os

os.makedirs('upload/', exist_ok=True)
os.makedirs('result/', exist_ok=True)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "admk:app",
        host='0.0.0.0',
        port=8000,
        reload=True
    )