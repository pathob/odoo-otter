from pathlib import Path

OTTER_PACKAGE = "odoo-otter"
OTTER_VERSION = "0.0.1"
OTTER_DESCRIPTION = "Otter - The Odoo time tracker"
OTTER_DIR = str(Path.home()) + "/.otter"
OTTER_CFG = f"{OTTER_DIR}/config.json"
OTTER_DB = f"{OTTER_DIR}/otter.db"

DOTS = '…'
SEPARATOR = ' | '

FORMAT_DATE = "%Y-%m-%d"
FORMAT_TIME = "%H:%M"
FORMAT_DATETIME = f"{FORMAT_DATE} {FORMAT_TIME}"
