from functools import wraps
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render
from django.conf import settings
from django.core.urlresolvers import reverse
from jmbovlive.utils import pml_redirect_timer_view

def pin_required(function):
    """
    Decorator to ask people to verify their pin before being able to access a view.
    """
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        msisdn = request.META.get('HTTP_X_UP_CALLING_LINE_ID', None)
        if not msisdn:
            return function(request, *args, **kwargs)

        auth_backend = ModelBackend()
        if request.session.get(settings.UMMELI_PIN_SESSION_KEY):
            return function(request, *args, **kwargs)

        if request.user.password:
            return pml_redirect_timer_view(request, settings.LOGIN_URL,
                    redirect_time = 0,
                    redirect_message = 'You need to login first.')
        else:
            return pml_redirect_timer_view(request, reverse('register'),
                    redirect_time = 0,
                    redirect_message = 'You need to create a pin first.')

    return wrapper

def phone_number_to_international(phone_number):
    if phone_number.startswith('27') and len(phone_number) == 11:
        return phone_number
    elif phone_number.startswith('0') and len(phone_number) == 10:
        return '27' + phone_number[1:]
    else:
        return 'invalid no'

def process_post_data_username(post):
    """
    converts username(phone number) to valid international phone number (27821234567)
    """
    if not post.get('username', None):
        return post

    post_data = post.copy()
    post_data['username'] = phone_number_to_international(post_data['username'])
    return post_data

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(file):
    image = Image.open(file)

    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
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

def get_lat_lon(file):
    exif_data = get_exif_data(file)
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = gps_info.get('GPSLatitude', None)
        gps_latitude_ref = gps_info.get('GPSLatitudeRef', None)
        gps_longitude = gps_info.get('GPSLongitude', None)
        gps_longitude_ref = gps_info.get('GPSLongitudeRef', None)

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon
