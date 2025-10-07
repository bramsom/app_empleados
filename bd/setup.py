import sqlite3
from bd.connection import conectar
from datetime import date

# --- Lógica de migración ---
# Esta función solo se ejecuta una vez para pasar los datos antiguos a la nueva estructura.
import os

def eliminar_base_de_datos():
    db_path = "empleados.db"  # Ajusta la ruta si tu archivo está en otra carpeta
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ Base de datos eliminada correctamente.")
    else:
        print("La base de datos no existe.")
def migrar_datos():
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN TRANSACTION;")

        # 1. Rename the old table
        cursor.execute("ALTER TABLE contracts RENAME TO contracts_old;")

        # 2. Create the new tables (including the new history table)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                type_contract TEXT NOT NULL CHECK (
                    type_contract IN (
                        'CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO',
                        'CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO',
                        'CONTRATO SERVICIO HORA CATEDRA',
                        'CONTRATO APRENDIZAJE SENA',
                        'ORDEN PRESTACION DE SERVICIOS'
                    )
                ),
                start_date DATE NOT NULL,
                end_date DATE,
                state TEXT NOT NULL CHECK (state IN ('ACTIVO','FINALIZADO','RETIRADO')),
                contractor TEXT,
                total_payment REAL, 
                payment_frequency INTEGER,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS salary_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id INTEGER NOT NULL,
                monthly_payment REAL NOT NULL,
                transport REAL,
                effective_date DATE NOT NULL,
                FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hourly_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id INTEGER NOT NULL,
                value_hour REAL NOT NULL,
                number_hour INTEGER NOT NULL,
                effective_date DATE NOT NULL,
                FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE
            )
        """)
        # --- NUEVA TABLA DE HISTORIAL DE ORDEN DE SERVICIOS ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS service_order_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id INTEGER NOT NULL,
                old_total_payment REAL,
                new_total_payment REAL NOT NULL,
                old_payment_frequency INTEGER,
                new_payment_frequency INTEGER NOT NULL,
                effective_date DATE NOT NULL,
                FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE
            )
        """)

        # 3. Copy data from the old table
        # Assuming contracts_old has total_payment and payment_frequency
        cursor.execute("SELECT id, employee_id, type_contract, start_date, end_date, state, contractor, total_payment, payment_frequency FROM contracts_old;")
        contratos_antiguos = cursor.fetchall()
        
        for contrato in contratos_antiguos:
            (
                id, employee_id, type_contract, start_date, end_date, state, contractor, total_payment, payment_frequency
            ) = contrato

            # Insert into the new contracts table
            cursor.execute("""
                INSERT INTO contracts (id, employee_id, type_contract, start_date, end_date, state, contractor, total_payment, payment_frequency)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (id, employee_id, type_contract, start_date, end_date, state, contractor, total_payment, payment_frequency))

            # Insert into the appropriate history table based on contract type
            if type_contract == 'ORDEN PRESTACION DE SERVICIOS' and total_payment is not None and payment_frequency is not None:
                cursor.execute("""
                    INSERT INTO service_order_history (contract_id, old_total_payment, new_total_payment, old_payment_frequency, new_payment_frequency, effective_date)
                    VALUES (?, ?, ?, ?, ?, ?);
                """, (id, None, total_payment, None, payment_frequency, date.today()))

        # 4. Drop the old table
        cursor.execute("DROP TABLE contracts_old;")

        conn.commit()
        print("✅ Migración de datos completada con éxito.")
    
    except sqlite3.OperationalError as e:
        print(f"La migración ya fue realizada o hubo un error: {e}")
        conn.rollback()
    except sqlite3.Error as e:
        print(f"Error durante la migración: {e}")
        conn.rollback()
    finally:
        conn.close()

# --- Lógica de creación de tablas para uso regular ---
# Esta función solo se usa para crear las tablas si no existen.
def crear_tablas():
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

    # Tabla de contratos (con la nueva estructura)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            type_contract TEXT NOT NULL CHECK (
                type_contract IN (
                    'CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO',
                    'CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO',
                    'CONTRATO SERVICIO HORA CATEDRA',
                    'CONTRATO APRENDIZAJE SENA',
                    'ORDEN PRESTACION DE SERVICIOS'
                )
            ),
            start_date DATE NOT NULL,
            end_date DATE,
            state TEXT NOT NULL CHECK (
                state IN ('ACTIVO','FINALIZADO','RETIRADO')
            ),
            contractor TEXT,
            total_payment REAL,
            payment_frequency INTEGER,
        FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
        )"""
    )
    # Tabla de historial de salarios mensuales
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS salary_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER NOT NULL,
            monthly_payment REAL NOT NULL,
            transport REAL,
            effective_date DATE NOT NULL,
            FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE
        )
    """)
    # Tabla de historial de salarios por hora
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hourly_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER NOT NULL,
            value_hour REAL NOT NULL,
            number_hour INTEGER NOT NULL,
            effective_date DATE NOT NULL,
            FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE
        )
    """)
            # --- NUEVA TABLA DE HISTORIAL DE ORDEN DE SERVICIOS ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_order_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER NOT NULL,
            old_total_payment REAL,
            new_total_payment REAL NOT NULL,
            old_payment_frequency INTEGER,
            new_payment_frequency INTEGER NOT NULL,
            effective_date DATE NOT NULL,
            FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE
        )
    """)
    # Crear tabla de afiliaciones con campos adicionales
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS affiliations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            eps TEXT,
            arl TEXT,
            risk_level TEXT,
            afp TEXT,
            compensation_box TEXT,
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


# --- Lógica de ejecución ---
# Para ejecutar esto, primero llamas a la migración
# y luego, en cada inicio de la app, llamas a crear_tablas
# para asegurarte de que la estructura exista.

# migrar_datos()  # Solo la primera vez
# crear_tablas() # Llama a esto cada vez que inicies la app