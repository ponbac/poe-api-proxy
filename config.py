import os

class Config(object):
    FULL_PATH = os.path.dirname(os.path.realpath(__file__))

    # The absolute path of the directory containing images for users to download
    NINJA_DATA = FULL_PATH + "/cached_ninja_data"

    # How many minutes before pricing info counts as old
    MAX_AGE_NINJA_DATA = 15