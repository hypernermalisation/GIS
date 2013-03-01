'''
This script produces a WeoGeoTableOfContents.json file using the .hdr file associated with
ENVI .bsq files.
'''

import fnmatch
import json
import os

def bandsSize(line):
    line = line.split()
    size = int(line[2])
    return size

def lineCount(line):
    line = line.split()
    lines = int(line[2])
    return lines


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

for file in find_files('.', '*.hdr'):
    with open(file, 'r') as header:
        head, tail = os.path.split(file)
        base, ext = os.path.splitext(tail)
        bands = 0
        lines = 0
        north = 0.0
        south = 0.0
        east = 0.0
        west = 0.0

        layerrange = [str(num) for num in range(bands)]
        numlayerrsstring = ';'.join([num for num in layerrange])
        layers = dict(zip(layerrange,layerrange))
        layers["WEO_TYPE"] = "LOOK_UP_TABLE"

        toc = {}
        toc["name"] = "NewFeatureType"
        toc["type"] = "FeatureCollection"

        features = []
        features.append(
            {
                "type":"Feature",
                "geometry":{"type": "Polygon",
                            "coordinates":[[
                                               [west,north],
                                               [east,north],
                                               [east,south],
                                               [west,south],
                                               [west,north]
                                           ]]},
                "properties":{
                    "LAYERS" : numlayerrsstring,
                    "PATH": "./" + base,
                    "EXTS": "hdr;bsq",
                    "WEO_MISCELLANEOUS_FILE":"No",
                    "WEO_TYPE":"WEO_FEATURE"
                }
            })
        features.append(
            {
                "geometry": None,
                "type": "Feature",
                "properties": layers
            }
        )
        toc["features"] = features
        outfilename = os.path.join(head,"WeoGeoTableOfContentsTEST.json" )
        outfile = open(outfilename, "w")
        encoder = json.JSONEncoder()
        outfile.write(encoder.encode(toc))
        outfile.close()
        print "{}{} TOC created".format(base, ext)
