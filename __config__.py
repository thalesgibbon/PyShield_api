def change_in_latitude(miles):
    import math

    earth_radius = 3960.0
    radians_to_degrees = 180.0 / math.pi

    return (miles / earth_radius) * radians_to_degrees


def m_to_miles(m):
    return (m / 1000) * 0.6213
7