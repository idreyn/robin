class DeviceStatus:
	DISCONNECTED = "disconnected"
	UNKNOWN = "unknown"
	BUSY = "busy"
	HARDWARE_UNAVAILABLE = "hardware-unavailable"
	READY = "ready"


class RemoteStatus:
	NO_SOCKET = "no-socket"
	DISCONNECTED = "disconnected"


class Message:
	CONNECT = "connect"
	DISCONNECT = "disconnect"
	HANDSHAKE_REMOTE = "handshake-remote"
	HANDSHAKE_DEVICE = "handshake-device"
	DEVICE_LISTING = "device-listing"
	CHOOSE_DEVICE ="choose-device"
	DEVICE_CHOICE_INVALID = "device-choice-invalid"
	DEVICE_CHOICE_SUCCESSFUL = "device-choice-successful"
	DEVICE_STATUS = "device-status"
	DEVICE_NEW_REMOTE = "device-new-remote"
	UPDATE_PULSE = "update-pulse"
	UPDATE_OVERRIDES = "update-overrides"
	RESTART_DEVICE = "restart-device"