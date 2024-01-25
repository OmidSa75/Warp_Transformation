from typing import Tuple
import numpy as np
import cv2
from scipy.interpolate import griddata


def calculate_coordinates_by_landmark(points: np.ndarray) -> Tuple[int, int]:
    """
    Calculate the width and height of an array of points
    :param points: np.ndarray
    :return: Tuple[int, int]
    """
    top = points[:, :, 1].min()
    bottom = points[:, :, 1].max()
    left = points[:, :, 0].min()
    right = points[:, :, 0].max()
    width = right - left
    height = bottom - top
    return width, height


def point_to_point_mapping(
        target_wide: int,
        mask: np.ndarray,
        points: np.ndarray,
        target_points: np.ndarray,
        sticker: np.ndarray
):
    """

    :param target_wide:
    :param mask:
    :param points:
    :param target_points:
    :param sticker:
    :return:
    """
    top = points[:, 1].min()
    bottom = points[:, 1].max()
    left = points[:, 0].min()
    right = points[:, 0].max()
    points[:, 0] -= left
    points[:, 1] -= top
    cropped_sticker = sticker[top:bottom, left:right, -1]
    ratio = cropped_sticker.shape[0] / cropped_sticker.shape[1]
    new_height = int(target_wide * ratio)
    old_height, old_width = cropped_sticker.shape[:2]
    points[:, 0] = points[:, 0] * target_wide / old_width
    points[:, 1] = points[:, 1] * new_height / old_height
    cropped_sticker = cv2.resize(
        cropped_sticker,
        (target_wide, new_height),
        interpolation=cv2.INTER_CUBIC
    )
    mask[0: new_height, 0:target_wide] = cv2.cvtColor(cropped_sticker, cv2.COLOR_GRAY2BGR)
    grid_x_l, grid_y_l = np.meshgrid(np.arange(0, mask.shape[1]), np.arange(0, mask.shape[0]))
    source = points.copy()
    destination = target_points.squeeze(1)
    grid_z_l = griddata(destination, source, (grid_x_l, grid_y_l), method='cubic')
    map_x_l = grid_z_l[:, :, 0]
    map_y_l = grid_z_l[:, :, 1]
    map_x_32_l = map_x_l.astype(np.float32)
    map_y_32_l = map_y_l.astype(np.float32)
    mask = cv2.remap(mask, map_x_32_l, map_y_32_l, cv2.INTER_CUBIC)
    return mask
