#!/usr/bin/env python3
"""
Prints bounding box values of process zones.

Usage: ./gen_process_zones.py datacubes.mapchete -b <left>, <bottom>, <right>, <top>
"""

import click
from tilematrix import TilePyramid
import yaml
from shapely import speedups
speedups.disable()


@click.command()
@click.argument(
    "mapchete_file",
    type=click.Path(exists=True)
)
@click.option(
    "--bounds", "-b",
    type=click.FLOAT,
    nargs=4,
    help="Spatial subset in Tile Pyramid CRS. (default: Tile Pyramid bounds)"
)
@click.option(
    "--zoom-delta",
    type=click.INT,
    default=5,
    help="Zoom levels above maximum zoom provided in mapchete configuration to determine "
    "process zone bounds. (default: 5, e.g. if max zoom is 13, process zoom levels will "
    "be tiles from zoom 8.)"
)
@click.option(
    "--wkt/--no-wkt",
    help="Output WKT strings instead of bounds"
)
def gen_process_zones(mapchete_file, bounds=None, zoom_delta=None, wkt=None):
    """Generate bounding boxes of process zones from mapchete config."""
    with open(mapchete_file) as src:
        config = yaml.load(src.read())

    tp = TilePyramid.from_dict(config["pyramid"])

    # TODO: we need to parse min/max zoom levels if provided in config
    max_zoom = config["zoom_levels"]

    bounds = bounds or tp.bounds

    process_zone_zoom = max_zoom - zoom_delta
    if process_zone_zoom < 0:
        raise TypeError(
            "zoom_delta cannot be larger than process max zoom ({})".format(max_zoom)
        )


    for tile in tp.tiles_from_bounds(bounds, process_zone_zoom):
        if(wkt):
            click.echo(str(tile.bbox()))
        else:
            click.echo(" ".join(list(map(str,tile.bounds()))))


if __name__ == '__main__':
    gen_process_zones()
