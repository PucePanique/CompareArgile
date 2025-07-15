import os
import xml.etree.ElementTree as ET

DEFAULT_CONFIG = {
    "theme": "cosmo",
    "language": "fr",
    "font": "Segoe UI",
    "window_width": "500",
    "window_height": "400",
    "themes": "cosmo,flatly,journal,litera,minty,pulse,sandstone,united,yeti,darkly,superhero,cyborg,solar,vapor"
}

CONFIG_FILE = "config.xml"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    try:
        tree = ET.parse(CONFIG_FILE)
        root = tree.getroot()
        config = {child.tag: child.text.strip() for child in root}
        return {**DEFAULT_CONFIG, **config}
    except Exception as e:
        print(f"[config_manager] Erreur de lecture config.xml : {e}")
        return DEFAULT_CONFIG

def save_config(config_dict):
    root = ET.Element("config")
    for key, value in config_dict.items():
        el = ET.SubElement(root, key)
        el.text = str(value)
    tree = ET.ElementTree(root)
    with open(CONFIG_FILE, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)
