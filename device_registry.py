from threading import Lock


class DeviceRegistry:
    _instance = None
    _lock = Lock()
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DeviceRegistry, cls).__new__(cls)
                    cls._instance.register = {}
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.register = {}
        self._initialized = True

    def register_device(self, fun: str, model, serializer, serializer_device):
        self.register[fun] = {
            "model": model,
            "serializer": serializer,
            "serializer_device": serializer_device,
        }

    def get_model(self, fun: str):
        if fun in self.register:
            return self.register[fun]["model"]
        raise KeyError("Function not registered: {}".format(fun))

    def get_serializer(self, fun: str):
        if fun in self.register:
            return self.register[fun]["serializer"]
        raise KeyError("Serializer not registered: {}".format(fun))

    def get_serializer_device(self, fun: str):
        if fun in self.register:
            return self.register[fun]["serializer_device"]
        raise KeyError("Serializer device not registered: {}".format(fun))

    @property
    def devices(self):
        return self.register.keys()
