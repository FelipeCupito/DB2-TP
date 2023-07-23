import sys
import uvicorn
from backendBanks.app.app import app
from backendBanks.app.config import settings

if __name__ == "__main__":
    # Obtener el número de puerto desde los argumentos de línea de comandos
    port = sys.argv[1] if len(sys.argv) > 1 else 8000
    uvicorn.run(app, host=settings.HOST, port=int(port))
