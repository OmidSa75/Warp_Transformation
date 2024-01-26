import numpy as np


def load_landmarks(path: str, label: int) -> np.ndarray:
    """
    Load makesenseAI point landmarks (csv format) and extract width and height
    :param path: Path to the .csv landmark file
    :param label: which label to load
    :return: nd.array with (number_of_points, 2) shape
    """
    labels = np.loadtxt(path, dtype=np.object_, delimiter=',')
    labels = labels[labels[:, 0] == str(label)]
    return labels[:, [1, 2]].astype(np.int32)
