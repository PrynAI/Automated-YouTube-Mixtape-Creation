# Automated YouTube Mixtape Creation

## Overview
This project is a modular Python application for automated mixtape production.

It provides three core capabilities:
1. Generate one mixed audio file from multiple uploaded tracks using smooth fade transitions.
2. Generate a YouTube-ready description with timestamped tracklist.
3. Optionally generate a video by combining the mixed audio with one static image.

The application is split into:
- FastAPI backend for file upload, job orchestration, status, and downloads.
- Streamlit frontend for user interaction.
- Service-layer media pipeline (audio mix, description, video render).

## Why This Architecture
The original feature logic was first validated in notebook/prototype code under `experiment_notebooks/logic.py`.

This app productionizes that logic into a modular structure so UI, API, and processing are separated and maintainable.

## Feature Mapping From Prototype To App
| Prototype Logic (`experiment_notebooks/logic.py`) | Production Module |
| --- | --- |
| `smooth_fade_mixtape(...)` | `app/services/audio/mixer.py` (`create_smooth_fade_mixtape`) |
| `generate_youtube_description_with_timestamps(...)` | `app/services/metadata/description.py` |
| `make_video_from_audio_optimized(...)` | `app/services/video/image_video.py` |
| Manual sequence in notebook | `app/services/pipeline/mixtape_orchestrator.py` |

## Tech Stack
- Backend API: FastAPI + Uvicorn
- Frontend UI: Streamlit (multi-page)
- Audio processing: pydub, ffmpeg
- Video rendering: ffmpeg + Pillow
- File handling: aiofiles
- HTTP client in UI: requests

## Repository Structure
```text
app/
  api/
    dto/                  # request/response models
    routers/              # health, jobs, downloads
    deps.py
    main.py
  core/
    config.py             # env + path settings
    exceptions.py
    logging.py
  domain/
    models.py             # job/pipeline models
  infrastructure/
    media/                # ffmpeg runner, adapters
    repositories/         # in-memory job store
    storage/              # upload saving + path management
  services/
    audio/                # discovery + mixing
    metadata/             # description generation
    video/                # static image video rendering
    pipeline/             # end-to-end orchestration
  ui/
    components/
    pages/
    api_client.py
    streamlit_app.py

data/
  uploads/
    audio/
    images/
  outputs/
    audio/
    descriptions/
    video/
  temp/

scripts/
  run_api.sh
  run_ui.sh
  smoke_test_pipeline.py

tests/
  integration/
  unit/
```

## Runtime Flow
1. User uploads audio files and optional image in Streamlit.
2. UI calls `POST /api/v1/jobs` with form-data files.
3. API stores uploads under `data/uploads/<type>/<job_id>/`.
4. Background task runs pipeline:
   - discover tracks (sorted)
   - mix audio with overlap fades
   - generate timestamp description
   - render video if image was uploaded
5. Job status is updated in in-memory store.
6. UI polls `GET /api/v1/jobs/{job_id}` and shows status/track timing.
7. Outputs are downloaded from `/api/v1/jobs/{job_id}/download/*`.

## API Endpoints
| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/jobs` | Create processing job (audio files + optional image + config) |
| `GET` | `/api/v1/jobs/{job_id}` | Get job status and output URLs |
| `GET` | `/api/v1/jobs/{job_id}/download/audio` | Download mixed audio |
| `GET` | `/api/v1/jobs/{job_id}/download/description` | Download description text |
| `GET` | `/api/v1/jobs/{job_id}/download/video` | Download rendered video |

## Configuration
Environment variables are documented in `.env.example`:
- `MIXTAPE_PROJECT_NAME`
- `MIXTAPE_API_V1_PREFIX`
- `MIXTAPE_CORS_ALLOW_ORIGINS`
- `MIXTAPE_DATA_DIR`
- `MIXTAPE_LOG_LEVEL`
- `FFMPEG_BINARY`
- `MIXTAPE_API_URL`

## Prerequisites
- Python
- ffmpeg installed and available in `PATH`
- Virtual environment recommended

Note:
- `pyproject.toml` currently declares `requires-python = ">=3.14.2"`.
- If your local environment uses an earlier Python version, either update Python or align this constraint with your target runtime.

## Setup
### Windows PowerShell (recommended)
```powershell
cd "C:\Users\riahl\OneDrive\UKCareer\Careers\Resume\Companies\PrynGlobal\FoundationsMVPBuild\GitHub\Automated-YouTube-Mixtape-Creation"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If activation is blocked:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Git Bash / WSL
```bash
cd /path/to/Automated-YouTube-Mixtape-Creation
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run The App
Use two terminals.

### Terminal 1: API
PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

Git Bash:
```bash
source .venv/bin/activate
bash scripts/run_api.sh
```

### Terminal 2: UI
PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
$env:MIXTAPE_API_URL="http://localhost:8000"
streamlit run app/ui/streamlit_app.py --server.port 8501
```

Git Bash:
```bash
source .venv/bin/activate
export MIXTAPE_API_URL="http://localhost:8000"
bash scripts/run_ui.sh
```

Open:
- API docs: `http://localhost:8000/docs`
- UI: `http://localhost:8501`

## How To Use
1. Open Step 1 (Upload) and add audio tracks, optional image.
2. Open Step 2 (Configure) and set transition/time metadata.
3. Open Step 3 (Generate), submit, then refresh status.
4. Open Step 4 (Results) to preview and download artifacts.

## Output Artifacts
For each job id:
- Audio: `data/outputs/audio/<job_id>_mixtape.mp3`
- Description: `data/outputs/descriptions/<job_id>_description.txt`
- Video (if image supplied): `data/outputs/video/<job_id>_mixtape.mp4`

## Development Notes
- Jobs are currently stored in memory (`JobStore`), so status is not persisted across API restarts.
- File artifacts are persisted to disk under `data/`.
- Track timestamps are computed using real overlap-aware start times from mixer output.

## Testing
Run available tests:
```bash
pytest -q
```

Smoke test with sample files:
```bash
python scripts/smoke_test_pipeline.py
```

## Troubleshooting
- `ModuleNotFoundError: No module named 'app'` in Streamlit:
  - Run from project root.
  - Use updated `scripts/run_ui.sh` (sets `PYTHONPATH`).
- `FFmpeg binary not found`:
  - Install ffmpeg and verify `ffmpeg -version` works.
  - Or set `FFMPEG_BINARY` to explicit executable path.
- Job status returns `failed`:
  - Check API terminal logs for underlying processing error.
  - Common issues: unsupported audio format, corrupt media, missing ffmpeg.


- Home page

![alt text](docs\image.png)

- Uploade page

![alt text](docs\image-1.png)

- Default configuration 

![alt text](docs\image-2.png)

- Generate audio & video track

- Results section to download tracks and description

![alt text](docs\image-3.png)