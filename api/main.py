import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response

app = FastAPI()

@app.get("/image.png")
async def get_image(request: Request):
    # Intentar capturar la IP desde las cabeceras de Vercel
    user_ip = request.headers.get("x-forwarded-for")
    if user_ip:
        user_ip = user_ip.split(",")[0].strip()
    else:
        user_ip = request.headers.get("x-real-ip", "IP no detectada")

    # Esto imprimirá la IP en la pantalla de Vercel Logs
    print(f"--- IP CAPTURADA: {user_ip} ---")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "imagen.png")

    # Si subiste una imagen la muestra, si no, genera un pixel transparente para no romper el enlace
    if os.path.exists(image_path):
        return FileResponse(image_path, media_type="image/png")
    else:
        pixel_transparente = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc`0\x00\x00\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82'
        return Response(content=pixel_transparente, media_type="image/png")

@app.get("/{path:path}")
async def catch_all(request: Request, path: str):
    return {"status": "online"}
