def bbox2wkt(bbox: str):
    """
    Usage: bbox2wkt('350050.0 5315000.0 513890.0 5478840.0')
    """
    left, bottom, right, top = bbox.split(' ')
    return f'POLYGON(({left} {top}, {right} {top}, {right} {bottom}, {left} {bottom}, {left} {top}))'

with open('bounds_tiles.txt') as file:
    for bbox in file:
        print(bbox2wkt(bbox.rstrip()))