class Contrato:
    def __init__(self, id=None, employee_id=None, type_contract="", 
                start_date="", end_date="", value_hour=0.0, number_hour=0.0, 
                monthly_payment=0.0, transport=0.0, state="", contractor=""):
        
        self.id = id
        self.employee_id = employee_id
        self.type_contract = type_contract.strip()
        self.start_date = str(start_date).strip()
        self.end_date = str(end_date).strip()
        self.value_hour = float(value_hour)
        self.number_hour = float(number_hour)
        self.monthly_payment = float(monthly_payment)
        self.transport = float(transport)
        self.state = state.strip()
        self.contractor = contractor.strip()

    def to_tuple(self):
        return (
            self.employee_id,
            self.type_contract,
            self.start_date,
            self.end_date,
            self.value_hour,
            self.number_hour,
            self.monthly_payment,
            self.transport,
            self.state,
            self.contractor
        )