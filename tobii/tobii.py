from __future__ import annotations

from ctypes import pointer

from tobii.engine import (
    tobii_api_create,
    tobii_api_destroy,
    tobii_api_t,
    tobii_device_create,
    tobii_device_destroy,
    tobii_device_process_callbacks,
    tobii_device_t,
    tobii_device_url_receiver_t,
    tobii_enumerate_local_device_urls,
    tobii_eye_position_normalized_callback_t,
    tobii_eye_position_normalized_subscribe,
    tobii_gaze_point_callback_t,
    tobii_gaze_point_subscribe,
    tobii_get_api_version_func,
    tobii_head_pose_callback_t,
    tobii_head_pose_subscribe,
    tobii_version_t,
    tobii_wait_for_callbacks,
)


def get_version():
    version = tobii_version_t()
    result = tobii_get_api_version_func(pointer(version))
    assert result == 0, "tobii_get_api_version_func failed"
    return version


def available_devices(api) -> list[bytes]:
    devices = []

    @tobii_device_url_receiver_t
    def _append_device(url, user_data):
        devices.append(url)

    tobii_enumerate_local_device_urls(api, _append_device, None)
    return devices


class TobiiEngine:
    def __init__(self, interval: float = 0.05):
        self.api = pointer(tobii_api_t())
        self.devices = []
        self.connected_device = pointer(tobii_device_t())
        self.interval = interval
        self.data = {
            "Timestamp": 0,
            "Validity": 0,
            "Position": [0, 0],
            "gaze_point": [0, 0],
            "head_pose": [0, 0, 0, 0, 0, 0],
        }
        self._callbacks = []

    def __enter__(self):
        assert self.api is not None
        error = tobii_api_create(pointer(self.api), None, None)
        assert error == 0, f"tobii_api_create failed, error code {error}"
        self.devices = available_devices(self.api)
        self.connected_device = self.create_callback()
        # tobii_device_reconnect(self.connected_device)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __del__(self):
        tobii_device_destroy(self.connected_device)
        tobii_api_destroy(self.api)
        self.api = None
        self.devices = []

    def create_callback(self, index: int = 0):
        if index >= len(self.devices):
            raise IndexError("device index out of range")
        device = self.connected_device
        tobii_device_create(self.api, self.devices[index], 1, device)

        @tobii_gaze_point_callback_t
        def gaze_point_callback(gaze_point, user_data):
            self.data["Timestamp"] = gaze_point.contents.timestamp_us
            self.data["Validity"] = gaze_point.contents.validity.value
            self.data["Position"] = [*gaze_point.contents.position_xy]

            self.data["gaze_point"] = [*gaze_point.contents.position_xy]

        @tobii_head_pose_callback_t
        def head_pose_callback(head_pose, user_data):
            self.data["Timestamp"] = head_pose.contents.timestamp_us
            self.data["Position Validity"] = head_pose.contents.position_validity.value
            self.data["Rotation Validity"] = [
                validity.value for validity in head_pose.contents.rotation_validity_xyz
            ]
            self.data["Position XYZ"] = [*head_pose.contents.position_xyz]
            self.data["Rotation XYZ"] = [*head_pose.contents.rotation_xyz]

            self.data["head_pose"] = [
                *head_pose.contents.position_xyz,
                *head_pose.contents.rotation_xyz,
            ]

        @tobii_eye_position_normalized_callback_t
        def eye_position_normalized_callback(eye_position, user_data):
            self.data["Timestamp"] = eye_position.contents.timestamp_us
            self.data["Left Validity"] = eye_position.contents.left_validity.value
            self.data["Right Validity"] = eye_position.contents.right_validity.value
            self.data["Left XYZ"] = [*eye_position.contents.left_xyz]
            self.data["Right XYZ"] = [*eye_position.contents.right_xyz]

            self.data["eye_position"] = [
                *eye_position.contents.left_xyz,
                *eye_position.contents.right_xyz,
            ]

        tobii_gaze_point_subscribe(device, gaze_point_callback, None)
        tobii_eye_position_normalized_subscribe(
            device, eye_position_normalized_callback, None
        )
        tobii_head_pose_subscribe(device, head_pose_callback, None)

        # callback will be removed when return if not stored
        self._callbacks.extend(
            [
                gaze_point_callback,
                head_pose_callback,
                eye_position_normalized_callback,
            ]
        )
        return device

    def read(self):
        device = self.connected_device
        if device is None:
            raise RuntimeError("no device connected")
        tobii_wait_for_callbacks(1, pointer(device))
        tobii_device_process_callbacks(device)
        return self.data

    def __iter__(self):
        device = self.connected_device
        if device is None:
            raise RuntimeError("no device connected")

        while True:
            tobii_wait_for_callbacks(1, pointer(device))
            tobii_device_process_callbacks(device)
            yield self.data
