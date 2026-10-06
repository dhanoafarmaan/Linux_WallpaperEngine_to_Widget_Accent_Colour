import dbus
import dbus.mainloop.glib
from gi.repository import GLib

from wallpaper import get_current_wallpaper
from colours_class import Colours
from widget import update_widget


WAYWALLEN_BUS = "org.waywallen.waywallen.Daemon"
WAYWALLEN_PATH = "/org/waywallen/waywallen/Daemon"
WAYWALLEN_INTERFACE = "org.waywallen.waywallen.Daemon1"


def update():
    path = get_current_wallpaper()

    wallpaper = Colours(path)
    wallpaper.extract_colours()

    cpu_colour, gpu_colour = wallpaper.get_accents()

    print(f"Wallpaper: {path}")
    print(f"CPU accent: {cpu_colour}")
    print(f"GPU accent: {gpu_colour}")

    update_widget(cpu_colour, gpu_colour)


def wallpaper_changed(interface, changed, invalidated):
    if interface != WAYWALLEN_INTERFACE:
        return

    if "CurrentWallpaperId" not in changed:
        return

    print("Wallpaper changed.")
    update()


dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()

bus.add_signal_receiver(
    wallpaper_changed,
    signal_name="PropertiesChanged",
    dbus_interface="org.freedesktop.DBus.Properties",
    path=WAYWALLEN_PATH
)

update()

loop = GLib.MainLoop()
loop.run()