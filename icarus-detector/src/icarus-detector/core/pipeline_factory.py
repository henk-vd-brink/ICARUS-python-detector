from . import stages


class PipelineFactory:
    def __init__(self):
        preprocess = stages.PreProcessing()
        detection = stages.Detection()
        postprocess = stages.PostProcessing()

        preprocess.successor = detection
        detection.successor = postprocess

        self.start = preprocess
    
    def get_pipeline(self):
        return self.start

if __name__ == "__main__":
    pf = PipelineFactory()
    pl = pf.get_pipeline()

    a = pl.handle("joe!")

    print(a, a)

