from datetime import datetime

class Contrato:
    def __init__(self, id=None, employee_id=None, type_contract="",
                 start_date="", end_date="", state="", contractor="",
                 total_payment=0.0,payment_frequency=0.0, monthly_payment=0.0, transport=0.0,
                 value_hour=0.0, number_hour=0.0):

        self.id = id
        self.employee_id = employee_id
        self.type_contract = type_contract.strip()
        self.start_date = str(start_date).strip()
        self.end_date = str(end_date).strip()
        self.state = state.strip()
        self.contractor = contractor.strip()
        self.total_payment = float(total_payment or 0.0)
        self.payment_frequency = float(payment_frequency)
        self.monthly_payment = float(monthly_payment)
        self.transport = float(transport)
        self.value_hour = float(value_hour)
        self.number_hour = float(number_hour) # <-- Nuevo campo

    def to_tuple(self):
        # Convertir fechas al formato YYYY-MM-DD para guardar en la base de datos
        try:
            start_date_iso = datetime.strptime(self.start_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Fecha de inicio inválida: {self.start_date}. Usa el formato dd/mm/yyyy.")
        
        # end_date puede ser None si el contrato es indefinido
        end_date_iso = None
        if self.end_date:
            try:
                end_date_iso = datetime.strptime(self.end_date, '%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError:
                raise ValueError(f"Fecha de corte inválida: {self.end_date}. Usa el formato dd/mm/yyyy.")

        return (
            self.employee_id,
            self.type_contract,
            start_date_iso,
            end_date_iso,
            self.value_hour,
            self.number_hour,
            self.monthly_payment,
            self.transport,
            self.state,
            self.contractor,
            self.total_payment,
            self.payment_frequency
        )