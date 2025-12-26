class PersonNotFoundError(Exception):
    def __init__(self, person_id: int):
        message = f"Person with id={person_id} not found"
        super().__init__(message)
        self.person_id = person_id
        self.message = message
