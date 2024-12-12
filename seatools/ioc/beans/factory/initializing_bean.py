import abc


class InitializingBean(abc.ABC):

    @abc.abstractmethod
    def after_properties_set(self):
        raise NotImplementedError
