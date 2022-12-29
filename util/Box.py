

class Box(object):
    """
    盒子抽象类。
    会继承此类的包括：
    """
    def __init__(self):
        pass

    def add_object(self, new_object):
        """
        向字典中添加新的对象
        :param new_object: 新的对象。
        :return:
        """
        pass

    def get_object_list(self):
        """
        :return:
            字典中储存的所有object的 index_name
        """
        pass

    def get_object(self, index_name):
        """
        根据输入的index_name, 返回外部所请求的object
        :param index_name: 请求对象的 index_name
        :return:
            name为输入index_name的对象。
        """
        pass


