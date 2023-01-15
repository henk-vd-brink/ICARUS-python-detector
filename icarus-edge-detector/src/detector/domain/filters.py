import logging

logger = logging.getLogger(__name__)


class SelectionFilter:
    def __init__(self):
        pass

    def filter(self, frame):
        pass


class PersonOrPottedPlantSelectionFilter:
    def __init__(self):
        self._person_filter = PersonSelectionFilter()
        self._potted_plant_filter = PottedPlantSelectionFilter()

    def filter(self, frame):
        if self._person_filter.filter(frame) or self._potted_plant_filter.filter(frame):
            return True
        return False


class PottedPlantSelectionFilter:
    def filter(self, frame):
        potted_plant_detected = list(
            filter(lambda x: x.get("label") == "potted plant", frame.detections)
        )

        if not potted_plant_detected:
            logger.info("No potted plant detected")
            return False

        logger.info("Potted plant detected")
        return True


class PersonSelectionFilter:
    def filter(self, frame):
        person_detected = list(
            filter(lambda x: x.get("label") == "person", frame.detections)
        )

        if not person_detected:
            logger.info("No person detected")
            return False

        logger.info("Person detected")
        return True
