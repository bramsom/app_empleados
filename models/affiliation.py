class Afiliacion:
    def __init__(self, id=None, employee_id=None, affiliation_type="", 
                name="", bank="", account_number="", account_type="" ):
        
        self.id = id 
        self.employee_id= employee_id
        self.affiliation_type = affiliation_type
        self.name = name
        self.bank= bank
        self.account_number = account_number
        self.account_type = account_type

    def to_tuple(self):
        return (
            self.employee_id, self.affiliation_type, self.name, 
            self.bank, self.account_number, self.account_type
        )
