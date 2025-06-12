import sqlite3
from .connection import conectar

def crear_tablas():
    print("Tablas creadas")
    conn = conectar()
    cursor = conn.cursor()

    # Tabla de empleados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, 
            last_name TEXT NOT NULL,
            document_type TEXT NOT NULL,
            document_number INTEGER NOT NULL UNIQUE,
            document_issuance TEXT NOT NULL,
            birthdate DATE NOT NULL,
            phone_number INTEGER NOT NULL,         
            residence_address TEXT,
            RUT TEXT,
            email TEXT,
            position TEXT
        )
    """)

    # Tabla de contratos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            type_contract TEXT NOT NULL CHECK (
                type_contract IN (
                    'contrato individual de trabajo termino fijo',
                    'contrato individual de trabajo termino indefinido',
                    'contrato servicio hora_catedra',
                    'contrato aprendizaje sena',
                    'orden prestacion de servicios'
                )
            ),
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            value_hour REAL,
            number_hour INTEGER,
            monthly_payment REAL,
            transport REAL,
            state TEXT NOT NULL CHECK (
                state IN ('ACTIVO','FINALIZADO','RETIRADO')
            ),
            contractor TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
        )
    """)

    # Tabla de afiliaciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS affiliations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            affiliation_type TEXT NOT NULL CHECK (
                affiliation_type IN ('EPS', 'ARL', 'AFP', 'BANCO')
            ),
            name TEXT NOT NULL,
            bank TEXT,
            account_number TEXT,
            account_type TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
        )
    """)

    # Tabla de usuarios del sistema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT CHECK(rol IN ('aprendiz', 'administrador')) NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Tablas creadas correctamente.")
