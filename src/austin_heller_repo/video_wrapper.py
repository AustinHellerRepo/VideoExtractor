from __future__ import annotations
import cv2
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
import numpy as np
from austin_heller_repo.common import BooleanReference, StringEnum
import uuid
import os


class VideoFilter(ABC):

    def apply_to_frame(self, *, frame: np.ndarray) -> np.ndarray:
        raise NotImplementedError()


class ImageFileTypeEnum(StringEnum):
    Jpeg = "jpeg"


class VideoWrapper():

    def __init__(self, *, video_capture: cv2.VideoCapture, video_filters: List[VideoFilter]):
        self.__video_capture = video_capture
        self.__video_filters = video_filters

    def extract_frames_to_directory(self, *, image_file_type: ImageFileTypeEnum, directory_path: str, is_cancelled: BooleanReference):

        image_extension = None
        if image_file_type == ImageFileTypeEnum.Jpeg:
            image_extension = "jpeg"
        else:
            raise NotImplementedError(f"ImageFileTypeEnum not implemented: {image_file_type}.")

        if not os.path.exists(directory_path):
            os.mkdir(directory_path)

        is_successful = True
        while not is_cancelled.get() and is_successful:
            is_successful, frame = self.__video_capture.read()
            if is_successful:
                for video_filter in self.__video_filters:
                    frame = video_filter.apply_to_frame(
                        frame=frame
                    )
                file_name = f"{uuid.uuid4()}.{image_extension}"
                file_path = os.path.join(directory_path, file_name)
                cv2.imwrite(file_path, frame)
