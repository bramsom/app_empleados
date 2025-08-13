class Afiliacion:
    def __init__(self, id, eps, arl, risk_level, afp, compensation_box, bank, account_number, account_type):
        self.id = id
        self.eps = eps
        self.arl = arl
        self.risk_level = risk_level
        self.afp = afp
        self.compensation_box = compensation_box
        self.bank = bank
        self.account_number = account_number
        self.account_type = account_type

    def to_tuple(self):
        return (
            self.id,
            self.eps, self.arl, self.risk_level,
            self.afp, self.compensation_box, self.bank,
            self.account_number, self.account_type)
    
class EmpleadoAfiliacion:
    def __init__(self, id, empleado, eps, arl, risk_level, afp, compensation_box, bank, account_number, account_type):
        self.id = id
        self.empleado = empleado  # This attribute receives the full name
        self.eps = eps
        self.arl = arl
        self.risk_level = risk_level
        self.afp = afp
        self.compensation_box = compensation_box
        self.bank = bank
        self.account_number = account_number
        self.account_type = account_type
    def to_tuple(self):
        return (
            self.empleado,
            self.eps, self.arl, self.risk_level,
            self.afp, self.compensation_box, self.bank,
            self.account_number, self.account_type
        )