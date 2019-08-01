#!/bin/python
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

file_folder = os.path.dirname(os.path.abspath(__file__)) + '/static/img/map-my-experience'
file_ext = '.JPG'


def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = Image.open(image)._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data


def _get_if_exist(data, key):
    if key in data:
        return data[key]
    return None


def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return {"lat": lat, "long": lon}


@app.route('/map/get-data', methods=['GET'])
def get_data():
    arr = []
    for file in os.listdir(file_folder):
        if file.endswith(file_ext):
            file_path = os.path.join(file_folder, file)
            exif_dict = get_exif_data(file_path)
            d = {
                "lat": get_lat_lon(exif_dict)['lat'],
                "long": get_lat_lon(exif_dict)['long'],
                "image_path": file
            }
            arr.append(d)
    return jsonify(arr)


@app.route('/')
def map_page():
	return render_template("map.html")


if __name__ == '__main__':
    app.run(host="localhost", port=5011, debug=True)
