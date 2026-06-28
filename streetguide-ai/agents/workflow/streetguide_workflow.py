from agents.state import WorkflowState
from agents.tools import validate_image


class StreetGuideWorkflow:
    def __init__(self):
        self.state = WorkflowState()

    def reset(self):
        self.state = WorkflowState()

    def get_state(self):
        return self.state

    def set_image(self, image_path: str):
        self.state.image_path = image_path

    def validate_uploaded_image(self):
        if self.state.image_path is None:
            raise ValueError("No image has been provided.")

        result = validate_image(self.state.image_path)
        self.state.image_validation = result

        return result