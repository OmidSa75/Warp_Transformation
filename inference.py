from warp_transformation import point_to_point_mapping, calculate_coordinates_by_landmark
from warp_transformation.utils import load_landmarks
import cv2


if __name__ == '__main__':
    source_sticker = cv2.imread('samples/Bouteille.png')
    target_image = cv2.imread('samples/target.png')
    source_landmarks = load_landmarks('samples/Bouteille.csv', label=0)
    target_landmarks = load_landmarks('samples/target.csv', label=0)

    target_width, target_height = calculate_coordinates_by_landmark(source_sticker)

    mask = point_to_point_mapping(
        target_wide=target_width,
        mask=target_image.copy(),
        points=source_landmarks.copy(),
        target_points=target_landmarks.copy(),
        sticker=source_sticker.copy(),
    )
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', mask)
    while cv2.waitKey(0) != ord('q'):
        continue
    cv2.destroyAllWindows()

