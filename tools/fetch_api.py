import os, requests, datetime as dt, time
from dotenv import load_dotenv

load_dotenv()

API_BASE = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": os.getenv("API_SPORTS_KEY", "").strip()}

def _get(path, params, retries=3, sleep=1.5):
    if not HEADERS["x-apisports-key"]:
        raise RuntimeError("Falta API_SPORTS_KEY en variables de entorno.")
    url = f"{API_BASE}{path}"
    for i in range(retries):
        r = requests.get(url, headers=HEADERS, params=params, timeout=30)
        if r.status_code == 200:
            return r.json()
        time.sleep(sleep * (i+1))
    r.raise_for_status()

def fixtures_range(league_id: int, date_from: str, date_to: str, status=None):
    params = {"league": league_id, "from": date_from, "to": date_to, "season": _current_season()}
    if status: params["status"] = status
    return _get("/fixtures", params)

def fixtures_by_ids(fixture_ids):
    data = []
    for fid in fixture_ids:
        j = _get("/fixtures", {"id": fid})
        if j and j.get("response"):
            data.extend(j["response"])
    return data

def odds_by_fixture(fixture_id: int, bookmaker_id: int = 8):
    return _get("/odds", {"fixture": fixture_id, "bookmaker": bookmaker_id})

def _current_season():
    now = dt.datetime.utcnow()
    yr = now.year
    return yr if now.month >= 7 else yr-1
