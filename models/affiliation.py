class Afiliacion:
    def __init__(self, id=None, employee_id=None, eps="", 
                arl="",afp="", bank="", account_number="", account_type="" ):
        
        self.id = id 
        self.employee_id= employee_id
        self.eps = eps
        self.arl = arl
        self.afp = afp
        self.bank= bank
        self.account_number = account_number
        self.account_type = account_type

    def to_tuple(self):
        return (
            self.employee_id, self.eps, self.arl,self.afp,
            self.bank, self.account_number, self.account_type
        )
