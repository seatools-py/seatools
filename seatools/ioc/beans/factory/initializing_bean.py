import abc


class InitializingBean(abc.ABC):

    @abc.abstractmethod
    def after_properties_set(self):
        raise NotImplemented('未实现该方法')
