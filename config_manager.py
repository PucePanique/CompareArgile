import os
import xml.etree.ElementTree as ET

CONFIG_FILE = "config.xml"

DEFAULT_CONFIG = {
    "theme": "litera",
    "language": "fr",
    "font": "Arial",
    "font_choices": "Arial,Courier,Times New Roman,Verdana",
    "window_width": "950",
    "window_height": "700",
    "default_width_cm": "25",
    "default_height_cm": "20",
    "title_fontsize": "16",
    "axis_fontsize": "12",
    "legend_fontsize": "10",
    "legend_ncol": "2",
    "legend_loc": "upper center",
    "legend_bbox": "(0.5, -0.2)",
    "plot_figsize": "(10, 8)",
    "color_default": "No Color",
    "color_bg": "white",
    "themes": "cosmo,flatly,journal,litera,minty,pulse,sandstone,united,yeti,darkly,superhero,cyborg,solar,vapor"
}


def parse_value(value: str):
    """Essaie de convertir une valeur XML en int, float, tuple, ou string."""
    value = value.strip()

    if value.startswith("(") and value.endswith(")"):
        try:
            return tuple(map(float, value[1:-1].split(",")))
        except Exception:
            return value

    if "," in value:
        return [v.strip() for v in value.split(",")]

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value


def serialize_value(value):
    """Convertit la valeur Python en string pour XML."""
    if isinstance(value, (list, tuple)):
        return ",".join(str(v) for v in value)
    return str(value)


def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        tree = ET.parse(CONFIG_FILE)
        root = tree.getroot()
        config = {}
        for child in root:
            config[child.tag] = parse_value(child.text or "")
        # Ajoute les valeurs manquantes
        for key, val in DEFAULT_CONFIG.items():
            if key not in config:
                config[key] = parse_value(val)
        return config
    except Exception as e:
        print(f"[config_manager] Erreur lors du chargement : {e}")
        return DEFAULT_CONFIG.copy()


def save_config(config_dict):
    root = ET.Element("config")
    for key, value in config_dict.items():
        el = ET.SubElement(root, key)
        el.text = serialize_value(value)
    tree = ET.ElementTree(root)
    with open(CONFIG_FILE, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)
