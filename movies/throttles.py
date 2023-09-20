from rest_framework import throttling


class MovieListThrottle(throttling.AnonRateThrottle):
    rate = '6/min'