'''
This script produces a WeoGeoTableOfContents.json file using the .hdr file associated with
ENVI .bsq files using SAFE's FME 2013. The contents of this script are used in the 'PythonCaller Parameters' within FME. The workspace file, ENVI_workspace.fmw is end result used to create the TOC json files.
'''

import fmeobjects
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
                
class FeatureProcessor(object):
    def __init__(self):
        return
       
    def input(self,feature):
        hfile = feature.getAttribute('fme_dataset')[:-3] + 'hdr'
        print hfile
        with open(hfile, 'r') as header:
            head, tail = os.path.split(hfile)
            base, ext = os.path.splitext(tail)
            bands = 0
            lines = 0
            north = float(feature.getAttribute('NORTH'))
            south = float(feature.getAttribute('SOUTH'))
            east = float(feature.getAttribute('EAST'))
            west = float(feature.getAttribute('WEST'))
            for line in header:
                if 'bands' in line:
                    bands = bandsSize(line)
                elif 'lines' in line:
                    lines = lineCount(line)
                else :
                    continue

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
            outfilename = os.path.join(head,"WeoGeoTableOfContents.json" )
            outfile = open(outfilename, "w")
            encoder = json.JSONEncoder()
            outfile.write(encoder.encode(toc))
            outfile.close()
            print "{}{} TOC created".format(base, ext)
        return 
       
    def close(self):
        return
