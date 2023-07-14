import json
from pathlib import Path
from typing import List, Dict

from pystac.extensions.eo import EOExtension as eo
import pystac_client
from pystac import Item
import planetary_computer
import rasterio
from rasterio import windows
from rasterio import features
from rasterio import warp
import numpy as np
from PIL import Image

import argparse

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)


def read_aoi_file(path: str) -> Dict:
    with open(Path(path)) as aoi_file:
        return json.loads(aoi_file.read())


def check_input_interval(interval: str):
    start, end = interval.split('/')
    if not any((start, end)):
        raise ValueError('Wrong interval input date, the right format is: 2019-06-01/2020-08-01')
    return interval


def save_image(images: List[Item], path: Path, area_of_interest: Dict):
    for image in images:
        image_address = image.assets["visual"].href
        with rasterio.open(image_address) as ds:
            aoi_bounds = features.bounds(area_of_interest)
            warped_aoi_bounds = warp.transform_bounds("EPSG:4326", ds.crs, *aoi_bounds)
            aoi_window = windows.from_bounds(transform=ds.transform, *warped_aoi_bounds)
            band_data = ds.read(window=aoi_window)
            file_name = 'samples/' + image.id + '.tiff'
            with rasterio.open(path/file_name, 'w', **ds.profile) as writer:
                writer.write(band_data)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Download Images using Microsoft Planetary Computer',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('--folder', '-f', required=True, help='Folder path to save images', type=Path)
    parser.add_argument('--aoi', '-a', required=True, help='Geometry as GeoJson', type=read_aoi_file)
    parser.add_argument(
        '--interval', '-t',
        required=True,
        type=check_input_interval,
        help='Time interval to download images with this format: 2019-06-01/2020-08-01',
    )
    return parser.parse_args()


if __name__ == '__main__':
    arguments = parse_args()
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        intersects=arguments.aoi,
        datetime=arguments.interval
    )
    items = search.item_collection()
    save_image(items.items, arguments.folder, arguments.aoi)
