class Empleado:
    def __init__(self, id=None, name="", last_name="", document_type="", document_number="",
                document_issuance="", birthdate="", phone_number="", residence_address="",
                RUT="", email=""):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.document_type = document_type
        self.document_number = document_number
        self.document_issuance = document_issuance
        self.birthdate = birthdate
        self.phone_number = phone_number
        self.residence_address = residence_address
        self.RUT = RUT
        self.email = email

    def to_tuple(self):
        return (
            self.name, self.last_name, self.document_type, self.document_number,
            self.document_issuance, self.birthdate, self.phone_number,
            self.residence_address, self.RUT, self.email
        )
