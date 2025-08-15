import sqlite3
from bd.connection import conectar

# --- Lógica de migración ---
# Esta función solo se ejecuta una vez para pasar los datos antiguos a la nueva estructura.
def migrar_datos():
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN TRANSACTION;")

        # 1. Renombrar la tabla antigua de contratos
        cursor.execute("ALTER TABLE contracts RENAME TO contracts_old;")

        # 2. Crear las nuevas tablas (la de contratos y las de historial)
        # La tabla de contratos con el nuevo campo total_payment
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
                total_payment REAL, -- ¡El nuevo campo agregado!
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
            )
        """)
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

        # 3. Copiar los datos de la tabla antigua
        cursor.execute("SELECT * FROM contracts_old;")
        contratos_antiguos = cursor.fetchall()
        
        for contrato in contratos_antiguos:
            (
                id, employee_id, type_contract, start_date, end_date, state, contractor
            ) = contrato # <-- Asegúrate que estas 11 variables se corresponden con tu tabla contracts_old

            cursor.execute("""
                INSERT INTO contracts (id, employee_id, type_contract, start_date, end_date, state, contractor, total_payment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (id, employee_id, type_contract, start_date, end_date, state, contractor, 0)) # El 0 es el valor predeterminado

                
        # 4. Eliminar la tabla antigua
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