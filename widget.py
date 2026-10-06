import subprocess


def update_widget(cpu_colour, gpu_colour):
    cpu_r, cpu_g, cpu_b = cpu_colour
    gpu_r, gpu_g, gpu_b = gpu_colour

    cpu_rgb = f"{cpu_r},{cpu_g},{cpu_b}"
    gpu_rgb = f"{gpu_r},{gpu_g},{gpu_b}"

    script = f'''
var ds = desktops();

for (var i = 0; i < ds.length; i++) {{
    var w = ds[i].widgetById(87);

    if (w) {{
        w.currentConfigGroup = ["SensorColors"];

        w.writeConfig(
            "cpu/all/averageTemperature",
            "{cpu_rgb}"
        );

        w.writeConfig(
            "gpu/gpu0/temperature",
            "{gpu_rgb}"
        );

        w.currentConfigGroup = [];

        w.reloadConfig();
    }}
}}
'''

    subprocess.run([
        "qdbus-qt6",
        "org.kde.plasmashell",
        "/PlasmaShell",
        "org.kde.PlasmaShell.evaluateScript",
        script
    ])