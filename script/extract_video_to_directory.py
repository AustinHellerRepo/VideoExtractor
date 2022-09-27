import sys
import os

#os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.getcwd())

try:
    from src.austin_heller_repo.video_wrapper import VideoWrapper, ImageFileTypeEnum
except ImportError:
    from austin_heller_repo.video_wrapper import VideoWrapper, ImageFileTypeEnum

from austin_heller_repo.common import BooleanReference
import uuid
import cv2
from datetime import datetime, timedelta

error = None
if len(sys.argv) != 2:
    error = f"Error: must supply file path to video file."
elif not os.path.exists(sys.argv[1]):
    error = f"Error: failed to find file at \"{sys.argv[1]}\"."
elif not os.path.isfile(sys.argv[1]):
    error = f"Error: not a file at \"{sys.argv[1]}\"."

if error is not None:
    print(error)
    raise Exception(error)

file_path = sys.argv[1]
directory_path = os.path.dirname(file_path)

frame_directory_path = os.path.join(directory_path, str(uuid.uuid4()))

video_wrapper = VideoWrapper(
    video_capture=cv2.VideoCapture(file_path),
    video_filters=[]
)

start_time = datetime.utcnow()
print(f"{datetime.utcnow()}: extracting video frames from \"{file_path}\" into \"{frame_directory_path}\".")

video_wrapper.extract_frames_to_directory(
    image_file_type=ImageFileTypeEnum.Jpeg,
    directory_path=frame_directory_path,
    is_cancelled=BooleanReference(
        value=False
    )
)

print(f"{datetime.utcnow()}: extracted video frames from \"{file_path}\" into \"{frame_directory_path}\".")
end_time = datetime.utcnow()
print(f"{datetime.utcnow()}: elapsed time: {(end_time - start_time).total_seconds()} seconds")
