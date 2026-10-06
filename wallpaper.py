from pathlib import Path
import sqlite3
import subprocess


DB_PATH = (
    Path.home()
    / ".var"
    / "app"
    / "org.waywallen.waywallen"
    / "data"
    / "waywallen"
    / "waywallen-v2.db"
)

STEAM_PATH = (
    Path.home()
    / ".local"
    / "share"
    / "Steam"
)


def get_current_wallpaper():
    result = subprocess.run(
        [
            "qdbus-qt6",
            "org.waywallen.waywallen.Daemon",
            "/org/waywallen/waywallen/Daemon",
            "org.freedesktop.DBus.Properties.Get",
            "org.waywallen.waywallen.Daemon1",
            "CurrentWallpaperId"
        ],
        capture_output=True,
        text=True,
        check=True
    )

    wallpaper_id = result.stdout.strip()

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT preview_path
            FROM item
            WHERE id = ?
            """,
            (wallpaper_id,)
        )

        row = cursor.fetchone()

    if row is None:
        raise FileNotFoundError(
            f"Wallpaper ID {wallpaper_id} was not found in Waywallen."
        )

    preview_path = STEAM_PATH / row[0]

    if not preview_path.exists():
        raise FileNotFoundError(
            f"Wallpaper preview was not found: {preview_path}"
        )

    return preview_path