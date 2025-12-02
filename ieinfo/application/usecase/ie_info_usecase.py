class IEInfoUseCase:
    __Instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__Instance is None:
            cls.__Instance = super().__new__(cls)
        return cls.__Instance

    @classmethod
    def get_instance(cls):
        if cls.__Instance is None:
            cls.__Instance = cls()
        return cls.__Instance

