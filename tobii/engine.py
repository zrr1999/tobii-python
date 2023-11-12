from __future__ import annotations

import ctypes
import os

tobii_lib = ctypes.cdll.LoadLibrary(
    os.path.join(os.path.dirname(__file__), "tobii_stream_engine.dll")
)


class tobii_version_t(ctypes.Structure):
    _fields_ = [
        ("major", ctypes.c_int),
        ("minor", ctypes.c_int),
        ("revision", ctypes.c_int),
        ("build", ctypes.c_int),
    ]


class tobii_custom_alloc_t(ctypes.Structure):
    _fields_ = [
        ("mem_context", ctypes.c_void_p),
        (
            "malloc_func",
            ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t),
        ),
        ("free_func", ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)),
    ]


class tobii_custom_log_t(ctypes.Structure):
    _fields_ = [
        ("log_context", ctypes.c_void_p),
        ("log_func", ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_char_p)),
    ]


class tobii_api_t(ctypes.Structure):
    pass


class tobii_device_t(ctypes.Structure):
    pass


class tobii_field_of_use_t(ctypes.c_int):
    TOBII_FIELD_OF_USE_INTERACTIVE = 1
    TOBII_FIELD_OF_USE_ANALYTICAL = 2


tobii_error_t = ctypes.c_int
tobii_device_url_receiver_t = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_void_p)


tobii_get_api_version_func = tobii_lib.tobii_get_api_version
tobii_get_api_version_func.argtypes = [ctypes.POINTER(tobii_version_t)]
tobii_get_api_version_func.restype = ctypes.c_int

tobii_enumerate_local_device_urls = tobii_lib.tobii_enumerate_local_device_urls
tobii_enumerate_local_device_urls.argtypes = [
    ctypes.POINTER(tobii_api_t),
    tobii_device_url_receiver_t,
    ctypes.c_void_p,
]
tobii_enumerate_local_device_urls.restype = ctypes.c_int

# 定义 tobii_malloc_func_t 和 tobii_free_func_t
tobii_malloc_func_t = ctypes.CFUNCTYPE(
    ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t
)
tobii_free_func_t = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)

# 定义 tobii_log_func_t
tobii_log_func_t = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_char_p)

# 定义 tobii_api_create 函数
tobii_api_create = tobii_lib.tobii_api_create
tobii_api_create.argtypes = [
    ctypes.POINTER(ctypes.POINTER(tobii_api_t)),
    ctypes.POINTER(tobii_custom_alloc_t),
    ctypes.POINTER(tobii_custom_log_t),
]
tobii_api_create.restype = ctypes.c_int

# 定义 tobii_api_destroy 函数
tobii_api_destroy = tobii_lib.tobii_api_destroy
tobii_api_destroy.argtypes = [ctypes.POINTER(tobii_api_t)]
tobii_api_destroy.restype = ctypes.c_int


class tobii_validity_t(ctypes.c_int):
    TOBII_VALIDITY_INVALID = 0
    TOBII_VALIDITY_VALID = 1


class tobii_gaze_point_t(ctypes.Structure):
    _fields_ = [
        ("timestamp_us", ctypes.c_int64),
        ("validity", tobii_validity_t),
        ("position_xy", ctypes.c_float * 2),
    ]


tobii_gaze_point_callback_t = ctypes.CFUNCTYPE(
    None, ctypes.POINTER(tobii_gaze_point_t), ctypes.c_void_p
)

tobii_gaze_point_subscribe = tobii_lib.tobii_gaze_point_subscribe
tobii_gaze_point_subscribe.argtypes = [
    ctypes.POINTER(tobii_device_t),
    tobii_gaze_point_callback_t,
    ctypes.c_void_p,
]
tobii_gaze_point_subscribe.restype = tobii_error_t

tobii_gaze_point_unsubscribe = tobii_lib.tobii_gaze_point_unsubscribe
tobii_gaze_point_unsubscribe.argtypes = [ctypes.POINTER(tobii_device_t)]
tobii_gaze_point_unsubscribe.restype = tobii_error_t


class tobii_eye_position_normalized_t(ctypes.Structure):
    _fields_ = [
        ("timestamp_us", ctypes.c_int64),
        ("left_validity", tobii_validity_t),
        ("left_xyz", ctypes.c_float * 3),
        ("right_validity", tobii_validity_t),
        ("right_xyz", ctypes.c_float * 3),
    ]


tobii_eye_position_normalized_callback_t = ctypes.CFUNCTYPE(
    None, ctypes.POINTER(tobii_eye_position_normalized_t), ctypes.c_void_p
)

tobii_eye_position_normalized_subscribe = (
    tobii_lib.tobii_eye_position_normalized_subscribe
)
tobii_eye_position_normalized_subscribe.argtypes = [
    ctypes.POINTER(tobii_device_t),
    tobii_eye_position_normalized_callback_t,
    ctypes.c_void_p,
]
tobii_eye_position_normalized_subscribe.restype = tobii_error_t

tobii_eye_position_normalized_unsubscribe = (
    tobii_lib.tobii_eye_position_normalized_unsubscribe
)
tobii_eye_position_normalized_unsubscribe.argtypes = [ctypes.POINTER(tobii_device_t)]
tobii_eye_position_normalized_unsubscribe.restype = tobii_error_t


class tobii_head_pose_t(ctypes.Structure):
    _fields_ = [
        ("timestamp_us", ctypes.c_int64),
        ("position_validity", tobii_validity_t),
        ("position_xyz", ctypes.c_float * 3),
        ("rotation_validity_xyz", tobii_validity_t * 3),
        ("rotation_xyz", ctypes.c_float * 3),
    ]


tobii_head_pose_callback_t = ctypes.CFUNCTYPE(
    None, ctypes.POINTER(tobii_head_pose_t), ctypes.c_void_p
)

tobii_head_pose_subscribe = tobii_lib.tobii_head_pose_subscribe
tobii_head_pose_subscribe.argtypes = [
    ctypes.POINTER(tobii_device_t),
    tobii_head_pose_callback_t,
    ctypes.c_void_p,
]
tobii_head_pose_subscribe.restype = tobii_error_t

tobii_head_pose_unsubscribe = tobii_lib.tobii_head_pose_unsubscribe
tobii_head_pose_unsubscribe.argtypes = [ctypes.POINTER(tobii_device_t)]
tobii_head_pose_unsubscribe.restype = tobii_error_t

tobii_wait_for_callbacks = tobii_lib.tobii_wait_for_callbacks
tobii_wait_for_callbacks.argtypes = [
    ctypes.c_int,
    ctypes.POINTER(ctypes.POINTER(tobii_device_t)),
]
tobii_wait_for_callbacks.restype = tobii_error_t

# 定义 tobii_device_create 函数
tobii_device_create = tobii_lib.tobii_device_create
tobii_device_create.argtypes = [
    ctypes.POINTER(tobii_api_t),
    ctypes.c_char_p,
    tobii_field_of_use_t,
    ctypes.POINTER(ctypes.POINTER(tobii_device_t)),
]
tobii_device_create.restype = tobii_error_t

# 定义 tobii_device_destroy 函数
tobii_device_destroy = tobii_lib.tobii_device_destroy
tobii_device_destroy.argtypes = [ctypes.POINTER(tobii_device_t)]
tobii_device_destroy.restype = tobii_error_t

# 定义 tobii_device_reconnect 函数
tobii_device_reconnect = tobii_lib.tobii_device_reconnect
tobii_device_reconnect.argtypes = [ctypes.POINTER(tobii_device_t)]
tobii_device_reconnect.restype = tobii_error_t

# 定义 tobii_device_process_callbacks 函数
tobii_device_process_callbacks = tobii_lib.tobii_device_process_callbacks
tobii_device_process_callbacks.argtypes = [ctypes.POINTER(tobii_device_t)]
tobii_device_process_callbacks.restype = tobii_error_t

# 定义 tobii_device_clear_callback_buffers 函数
tobii_device_clear_callback_buffers = tobii_lib.tobii_device_clear_callback_buffers
tobii_device_clear_callback_buffers.argtypes = [ctypes.POINTER(tobii_device_t)]
tobii_device_clear_callback_buffers.restype = tobii_error_t


def available_devices(api) -> list[bytes]:
    devices = []

    @tobii_device_url_receiver_t
    def _append_device(url, user_data):
        devices.append(url)

    tobii_enumerate_local_device_urls(api, _append_device, None)
    return devices
