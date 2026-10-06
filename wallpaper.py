from pathlib import Path


def get_current_wallpaper():
    config_path = (
        Path.home()
        / ".config"
        / "plasma-org.kde.plasma.desktop-appletsrc"
    )

    if not config_path.exists():
        raise FileNotFoundError(
            "KDE wallpaper configuration was not found."
        )

    with open(config_path, "r") as file:
        for line in file:
            if "WallpaperSource" not in line:
                continue

            value = line.split("=", 1)[1].strip()

            if value.startswith("file:"):
                value = value[5:]

            if value.endswith("+scene"):
                value = value[:-6]

            value = value.replace("$HOME", str(Path.home()))

            scene_path = Path(value)
            project_directory = scene_path.parent

            # Look for an image we can use for colour extraction
            for filename in [
                "preview.gif",
                "preview.jpg",
                "preview.jpeg",
                "preview.png",
            ]:
                image = project_directory / filename

                if image.exists():
                    return image

    raise FileNotFoundError(
        "Could not find an image for the current Wallpaper Engine project."
    )