from datetime import datetime

class Contrato:
    def __init__(self, id=None, employee_id=None, type_contract="",
                 start_date="", end_date="", state="", contractor="",
                 total_payment=None, payment_frequency=None, monthly_payment=None, 
                 transport=None, value_hour=None, number_hour=None, position=""):

        self.id = id
        self.employee_id = employee_id
        self.type_contract = type_contract.strip()
        self.start_date = str(start_date).strip()
        self.end_date = str(end_date).strip()
        self.state = state.strip()
        self.contractor = contractor.strip()
        self.position = position.strip() if position is not None else None
        
        # --- CORRECCIÓN: Manejar los valores None antes de la conversión ---
        self.total_payment = float(total_payment) if total_payment is not None else None
        
        # payment_frequency es un texto, no un número
        self.payment_frequency = payment_frequency
        
        # Los siguientes campos pueden ser None
        self.monthly_payment = float(monthly_payment) if monthly_payment is not None else None
        self.transport = float(transport) if transport is not None else None
        self.value_hour = float(value_hour) if value_hour is not None else None
        self.number_hour = float(number_hour) if number_hour is not None else None
        # --- FIN DE LA CORRECCIÓN --- # <-- Nuevo campo

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
            self.payment_frequency,
            self.position
        )