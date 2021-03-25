from rest_framework import serializers
from .coordinate import find_lat_long


def valid_zipcode(value):
    if value.upper()[0:3] != find_lat_long(value)["address"]["postalCode"][0:3]:
        raise serializers.ValidationError(
            "Please enter a valid Postal Code.")
