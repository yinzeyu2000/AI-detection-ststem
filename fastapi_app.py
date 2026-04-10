import os
import uuid
from pathlib import Path
import json
import base64
from fastapi import FastAPI, UploadFile, File, Query, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from ultralytics import RTDETR

WEIGHTS_PATH = os.getenv('RTDETR_WEIGHTS', 'runs/train/exp/weights/best.pt')
DEFAULT_PROJECT = os.getenv('RTDETR_PROJECT', 'runs/detect')
DEFAULT_NAME = os.getenv('RTDETR_NAME', 'exp')
UPLOAD_DIR = Path('uploads')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount('/static', StaticFiles(directory=DEFAULT_PROJECT), name='static')

model = None


@app.on_event('startup')
async def startup_event():
    global model
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    try:
        model = RTDETR(WEIGHTS_PATH)
    except Exception as e:
        raise RuntimeError(str(e))


@app.get('/health')
async def health():
    return {'status': 'ok', 'weights': WEIGHTS_PATH}


@app.post('/detect')
async def detect(
    request: Request,
    file: UploadFile = File(...),
    project: str = Query(DEFAULT_PROJECT),
    name: str = Query(DEFAULT_NAME),
    save: bool = Query(True),
    visualize: bool = Query(False),
    return_image: bool = Query(False),
):
    if model is None:
        raise HTTPException(status_code=500, detail='model not initialized')
    suffix = Path(file.filename).suffix or ''
    dst = UPLOAD_DIR / f'{uuid.uuid4().hex}{suffix}'
    try:
        with dst.open('wb') as f:
            for chunk in iter(lambda: file.file.read(1024 * 1024), b''):
                f.write(chunk)
    except Exception:
        raise HTTPException(status_code=400, detail='file save failed')
    try:
        results = model.predict(
            source=str(dst),
            project=project,
            name=name,
            save=save,
            visualize=visualize,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if not results:
        return JSONResponse({'status': 'ok', 'message': 'no results', 'input_file': str(dst)})
    r0 = results[0]
    save_dir = Path(r0.save_dir) if r0.save_dir else Path(project) / name
    rel = Path(os.path.relpath(save_dir, DEFAULT_PROJECT)).as_posix() if Path(DEFAULT_PROJECT) in save_dir.parents or save_dir == Path(DEFAULT_PROJECT) else None
    output_path = (save_dir / dst.name).as_posix()
    output_url = f'/static/{rel}/{dst.name}' if rel else None
    output_url_full = (str(request.base_url).rstrip('/') + output_url) if output_url else None
    detections_json = r0.tojson(normalize=True) if hasattr(r0, 'tojson') else '[]'
    try:
        detections = json.loads(detections_json)
    except Exception:
        detections = []
    image_b64 = None
    try:
        if return_image and suffix.lower() in ('.jpg', '.jpeg', '.png', '.bmp'):
            with open(output_path, 'rb') as f:
                image_b64 = base64.b64encode(f.read()).decode('utf-8')
    except Exception:
        image_b64 = None
    return {
        'status': 'ok',
        'input_file': str(dst),
        'output_dir': save_dir.as_posix(),
        'output_path': output_path,
        'output_url': output_url,
        'output_url_full': output_url_full,
        'detections': detections,
        'image_base64': image_b64,
    }

@app.post('/detect/')
async def detect_slash(
    request: Request,
    file: UploadFile = File(...),
    project: str = Query(DEFAULT_PROJECT),
    name: str = Query(DEFAULT_NAME),
    save: bool = Query(True),
    visualize: bool = Query(False),
):
    return await detect(request=request, file=file, project=project, name=name, save=save, visualize=visualize)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('fastapi_app:app', host='0.0.0.0', port=8000)
