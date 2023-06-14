from enum import Enum, auto

_DEFAULT_SCENE_PATH = '/vsis3/sentinel-cogs/sentinel-s2-l2a-cogs/{scene_id}'


class BasicImageBand(Enum):
    RED = 'B02'
    GREEN = 'B03'
    BLUE = 'B04'
    NIR = 'B08'


class ImageMode(Enum):
    RGB = auto()
    RGB_NIR = auto()


image_mode = {
    ImageMode.RGB: [BasicImageBand.RED, BasicImageBand.GREEN, BasicImageBand.BLUE],
    ImageMode.RGB_NIR: [BasicImageBand.RED, BasicImageBand.GREEN, BasicImageBand.BLUE, BasicImageBand.NIR]
}
