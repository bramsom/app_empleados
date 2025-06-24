class Contrato:
    def __init__(self, id=None, employee_id=None, type_contract="", 
                start_date="", end_date="", value_hour=0.0, number_hour=0.0, monthly_payment=0.0,
                transport=0.0, state="", contractor=""):
        
        self.id = id
        self.employee_id = employee_id
        self.type_contract = type_contract
        self.start_date = start_date
        self.end_date = end_date
        self.value_hour = value_hour
        self.number_hour = number_hour
        self.monthly_payment = monthly_payment
        self.transport = transport
        self.state = state
        self.contractor = contractor

    def to_tuple(self):
        return(
            self.employee_id, self.type_contract, self.start_date, self.end_date,
            self.value_hour, self.number_hour, self.monthly_payment, self.transport,
            self.state, self.contractor
        )