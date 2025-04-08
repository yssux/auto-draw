def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def frange(start, stop):
    while start <= stop:  # Use <= to include the stop value
        yield round(start, 2)  # Round to 2 decimal places
        start += 0.01  # Increment by 0.01 to control precision to 2 decimals

def pxToCm(px_size):
    return round((px_size / 96) * 2.54, 2)  # Keeps two decimal places
def px2ToCm2(area_px2):
    ppi = 102.5 #approx. my screen ppi
    area_in2 = area_px2 / (ppi ** 2)
    area_cm2 = area_in2 * 6.4516
    return round(area_cm2, 2)
def rectArea(height, width):
    return round(height * width, 2)
def sqArea(side):
    return round(side * side, 2)

def tri_equiArea(base, height):
    base = height
    return round(0.5 * base * height, 2)
def tri_isoArea(base, height):
    return round(0.5 * base * height, 2)
def tri_rectArea(base, height):
    return round(0.5 * base * height, 2)