def singleton(class_):
    """
    singleton decorator makes sure there is one class instance in system
    param: class_: controlled class
    return: class_ only instance
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance
