from pathlib import Path
from typing import Dict

from src.sentinel.exception import NoScenesEnough
from src.sentinel.geo_tool import _check_intersection
from src.sentinel.s3_handler import _get_all_scenes


def search_images(geometry: Dict, start_date: str, end_date: str, targe_path: Path):
    all_scenes = _get_all_scenes(start_date, end_date)
    filtered_scenes = _check_intersection(geometry=geometry, scenes=all_scenes)
    if filtered_scenes:
        save_locally()
    else:
        raise NoScenesEnough()
