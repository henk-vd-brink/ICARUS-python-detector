import abc


class AbstractDetector(abc.ABC):
    pass


class FakeDetector(AbstractDetector):
    
    def detect(self, frame, meta_data={}):
        pass

    def __repr__(self):
        return "< FakeDetector >"