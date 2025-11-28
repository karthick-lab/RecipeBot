def calculate_pieces(tray_width_in, tray_height_in):
    width_cm = tray_width_in * 2.54
    height_cm = tray_height_in * 2.54
    piece_area = 5 * 5  # 5cm x 5cm
    tray_area = width_cm * height_cm
    num_pieces = int(tray_area // piece_area)
    return num_pieces, "5cm x 5cm"