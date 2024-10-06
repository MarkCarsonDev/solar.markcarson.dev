import numpy as np
from noise import snoise2
from skimage import measure
from shapely.geometry import LineString
import datetime

stroke_color = "#e0ba74"
stroke_width = 2

def generate_topo_paths(noise_scale=500.0, heightmap_size=500, heightmap_ratio=16/9, scale_factor=700.0, line_interval=25.0, seed=None):
    """
    Generate contour lines from a simplex noise heightmap.
    """

    if seed is None:
        import datetime
        seed = datetime.datetime.now().timestamp()

    # rng = np.random.default_rng(int(seed)).integers(100000, 110000)
    rng = np.random.default_rng(int(seed)).integers(10, 110)

    
    # Calculate heightmap dimensions
    heightmap_width = int(heightmap_size * heightmap_ratio)
    heightmap_height = heightmap_size

    # Generate heightmap
    heightmap = np.zeros((heightmap_height, heightmap_width))
    for i in range(heightmap_height):
        for j in range(heightmap_width):
            # value = (snoise2(i / noise_scale, j / noise_scale) + 1) / 2
            value = (snoise2(i / noise_scale, j / noise_scale, base=rng) + 1) / 2
            # print(f"{value=}")
            heightmap[i][j] = value

    # Determine contour levels
    levels = [level / scale_factor for level in range(0, int(scale_factor)+1, int(line_interval))]

    # Find contours at each level
    contours_coords = []
    for level in levels:
        contours = measure.find_contours(heightmap, level)
        contours_coords.extend(contours)

    return contours_coords

def generate_svg_from_contours(contours_coords, simplify_tolerance=None):
    """
    Convert contour coordinates into SVG path data, with optional simplification.
    """
    paths = []
    for contour in contours_coords:
        if len(contour) < 2:
            continue  # Skip contours with too few points
        x = contour[:, 1]
        y = contour[:, 0]
        coords = list(zip(x, y))
        if simplify_tolerance is not None:
            line = LineString(coords)
            simplified_line = line.simplify(simplify_tolerance)
            simplified_coords = list(simplified_line.coords)
            if len(simplified_coords) < 2:
                continue
            coords = simplified_coords
        # Create path string
        path_data = 'M ' + ' '.join([f'{xi},{yi}' for xi, yi in coords])
        paths.append(path_data)
    # Combine all paths into one string
    topo_svg_paths = ''.join([f'<path d="{path}" stroke="{stroke_color}" stroke-width="{stroke_width}" fill="none" />\n' for path in paths])
    return topo_svg_paths

def generate_svg_image(topo_svg_paths, width, height):
    """
    Wrap the SVG paths into a complete SVG image.
    """
    svg_image = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" preserveAspectRatio="none">
{topo_svg_paths}
</svg>'''
    return svg_image

def generate_data_url(svg_content):
    """
    Convert SVG content into a data URL.
    """
    import base64
    # Encode the SVG content to bytes
    svg_bytes = svg_content.encode('utf-8')
    # Base64 encode the bytes
    base64_encoded_svg = base64.b64encode(svg_bytes).decode('utf-8')
    # Create the data URL with base64 encoding
    data_url = f'data:image/svg+xml;base64,{base64_encoded_svg}'
    return data_url

# Example usage:

# Generate contour coordinates
contours_coords = generate_topo_paths()

# Generate SVG paths with optional simplification (adjust 'simplify_tolerance' as needed)
simplify_tolerance = 0.1 # Adjust this value for more or less simplification
topo_svg_paths = generate_svg_from_contours(contours_coords, simplify_tolerance=simplify_tolerance)

# Wrap the paths into a complete SVG image
heightmap_size = 500
heightmap_ratio = 16/9
heightmap_width = int(heightmap_size * heightmap_ratio)
heightmap_height = heightmap_size
svg_content = generate_svg_image(topo_svg_paths, width=heightmap_width, height=heightmap_height)

# Now, 'svg_content' contains the complete SVG image
sonne_var("topography_svg", svg_content)

# Generate the data URL
data_url = generate_data_url(svg_content)
sonne_var("topography_data_url", data_url)
