def front_validation(func):
    def wrapper(data: dict, *args, **kwargs):
        return func(data, *args, **kwargs) if data.get('status') else data

    return wrapper
