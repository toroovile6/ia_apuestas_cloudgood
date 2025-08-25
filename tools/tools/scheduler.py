import os, time, subprocess, datetime as dt
import pytz

TZ = os.getenv("TIMEZONE", "Europe/Madrid")
tz = pytz.timezone(TZ)

def already_ran(flag_name: str) -> bool:
    path = f"/tmp/{flag_name}"
    return os.path.exists(path)

def set_ran(flag_name: str):
    open(f"/tmp/{flag_name}", "w").close()

def run(cmd: list[str]):
    print(f"[Scheduler] Ejecutando: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        print("[Scheduler] OK")
    except Exception as e:
        print(f"[Scheduler] ERROR: {e}")

def loop():
    print(f"[Scheduler] Iniciado. Zona horaria: {TZ}")
    print("[Scheduler] Tareas: Martes 22:00 -> settle_report ; Miércoles 00:00 -> make_report")
    while True:
        now = dt.datetime.now(tz)
        wd, hh, mm = now.weekday(), now.hour, now.minute
        today = now.strftime("%Y%m%d")

        if wd == 1 and hh == 22 and mm < 5 and not already_ran(f"settle_{today}.flag"):
            run(["python", "tools/settle_report.py", "--send"])
            set_ran(f"settle_{today}.flag")

        if wd == 2 and hh == 0 and mm < 5 and not already_ran(f"report_{today}.flag"):
            run(["python", "tools/update_model.py"])
            run(["python", "tools/make_report.py", "--send"])
            set_ran(f"report_{today}.flag")

        time.sleep(60)

if __name__ == "__main__":
    loop()
