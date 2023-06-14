from typing import List

import boto3
import numpy
import rasterio

from src.sentinel.constant import ImageMode, image_mode
from src.sentinel.exception import ImageModeNotExist


s3_client = boto3.client('s3')

# /1/1/1/2022/10/


def _get_all_scenes(start_date: str, end_date: str) -> List[str]:
    """
    Given a start date and end date paginate the S3 bucket to record all available images
    :param start_date:
    :param end_date:
    :return:
    """


def _download_image(image_address: str, target_dir: str, mode: ImageMode) -> None:
    """
    Get image on bucket and save in target directory
    :param image_address: Address of image on S3 Bucket
    :param target_dir: Directory path to save image
    :return: None
    """
    try:
        _mode = image_mode[mode]
    except KeyError:
        raise ImageModeNotExist()

    # build vrt here
    image_address += _mode if image_address[-1] == '/' else f'/{_mode}'
    with rasterio.open(image_address) as dataset:
        __store_locally(path=target_dir, data=dataset.read())


def __store_locally(path: str, data: numpy.array):
    ...
