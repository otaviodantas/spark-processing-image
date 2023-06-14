from typing import Dict, List

from src.sentinel.constant import _DEFAULT_SCENE_PATH


def build_vrt(scene_id: str):
    scenes_path = __get_path_to_scenes(scene_id)
    band_string = ''
    expect_width, expect_height, transformation_string, crs = _get_metadata_from_image(scenes_path[0])
    for i, scene in enumerate(scenes_path):
        width, height, _, _ = _get_metadata_from_image(scene)
        band_string += '\n' + __build_vrt_band(band_url=scene, band_index=i + 1, source_size=(width, height), destination_size=(expect_width, expect_height))

    return f'''
    <VRTDataset rasterXSize="10980" rasterYSize="10980">
        <SRS dataAxisToSRSAxisMapping="1,2"> {crs} </SRS>
        <GeoTransform> {transformation_string} </GeoTransform>
        {band_string}
    </VRTDataset>
    '''


def __build_vrt_band(band_url: str, band_index: int, source_size: Tuple[int, int], destination_size: Tuple[int, int] = None):
    return f'''
    <VRTRasterBand dataType="UInt16" band="{band_index}">
        <SimpleSource>
          <SourceFilename relativeToVRT="0">{band_url}</SourceFilename>
          <SourceBand>1</SourceBand>
          <SourceProperties RasterXSize="{source_size[0]}" RasterYSize="{source_size[1]}" DataType="UInt16" BlockXSize="1024" BlockYSize="1024" />
          <SrcRect xOff="0" yOff="0" xSize="{source_size[0]}" ySize="{source_size[1]}" />
          <DstRect xOff="0" yOff="0" xSize="{destination_size[0]}" ySize="{destination_size[1]}" />
        </SimpleSource>
    </VRTRasterBand>
    '''


def __get_path_to_scenes(bands: List[str]) -> List[str]:
    return [
        '{scene_path}//{band}.tif'.format(scene_path=_DEFAULT_SCENE_PATH, band=band)
        for band in bands
    ]
    # return [path.format(scene_id=__resolve_scene_id(scene_id)) for path in full_path]


def __resolve_scene_id(scene_id: str) -> str:
    try:
        parts = scene_id.split('_')
        tile_utm = parts[-2]
        temp_date = parts[2].split("T")[0]
        u, t, m = tile_utm[1:3], tile_utm[3:4], tile_utm[4:6]
        if u.startswith('0'):
            u = u[1:]
        date = datetime.datetime.strptime(temp_date, '%Y%m%d')
        year, month = date.year, date.month
    except (ValueError, TypeError):
        raise ImageIdInvalid()

    return f'/{u}/{t}/{m}/{year}/{month}/{parts[0]}_{u}{t}{m}_{temp_date}_0_L2A'


def _check_intersection(geometry: Dict, scenes: List[str]) -> List[str]:
    """
    Check if geometry send are 100% inside the scenes, if doesn't it is removed from the original list
    :param geometry: Dict as geojson with the source geometry
    :param scenes: List of scene
    :return: Filtered Scenes
    """
