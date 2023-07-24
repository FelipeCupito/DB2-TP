import sys
import uvicorn

from app.app import app
from app.config import settings

if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else 8000
    print(f"Running on port {port}")
    uvicorn.run(app, host=settings.HOST, port=int(port))
