import sqlite3

DB_DIR = 'db'
DB_NAME = 'YanGPT.db'
DB_TABLE_USERS_NAME = 'users'


def create_db(database_name=DB_NAME):
    db_path = f'{database_name}'
    connection = sqlite3.connect(db_path)
    connection.close()


def execute_query(sql_query, data=None, db_path=f'{DB_NAME}'):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        if data:
            cursor.execute(sql_query, data)
        else:
            cursor.execute(sql_query)

        connection.commit()
        return cursor

    except sqlite3.Error as e:
        print("Ошибка при подключении базы данных:", e)

    finally:
        connection.close()


def execute_selection_query(sql_query, data=None, db_path=f'{DB_NAME}'):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        if data:
            cursor.execute(sql_query, data)
        else:
            cursor.execute(sql_query)

        rows = cursor.fetchall()
        connection.close()
        return rows

    except sqlite3.Error as e:
        print("Ошибка при подключении базы данных:", e)


def create_table(table_name):
    sql_query = f'CREATE TABLE IF NOT EXISTS {table_name} ' \
                f'(id INTEGER PRIMARY KEY, ' \
                f'user_id INTEGER, ' \
                f'subject TEXT, ' \
                f'level TEXT, ' \
                f'task TEXT, ' \
                f'answer TEXT)'
    execute_query(sql_query)


def get_all_rows(table_name):
    rows = execute_selection_query(f'SELECT * FROM {table_name}')
    for row in rows:
        print(row)


def clean_table(table_name):
    execute_query(f'DELETE FROM {table_name}')


def insert_row(values):
    columns = "(user_id, subject, level, task, answer)"
    sql_query = (f'INSERT INTO {DB_TABLE_USERS_NAME} {columns} '
                 f'VALUES (?, ?, ?, ?, ?)')
    execute_query(sql_query, values )


def is_value_in_table(table_name, column_name, value):
    sql_query = (f'SELECT {column_name} FROM {table_name}'
                 f' WHERE {column_name} = ?')
    rows = execute_selection_query(sql_query, (value,))
    return rows


def delete_user(user_id):
    if is_value_in_table(DB_TABLE_USERS_NAME, 'user_id', user_id):
        sql_query = f'DELETE FROM {DB_TABLE_USERS_NAME} WHERE user_id = ?'
        execute_query(sql_query, (user_id, ))


def update_row_value(user_id, column_name, new_value):
    if is_value_in_table(DB_TABLE_USERS_NAME,'user_id', user_id):
        sql_query = (f'UPDATE {DB_TABLE_USERS_NAME} SET {column_name} = ?'
                     f' WHERE user_id = ?')
        execute_query(sql_query, (new_value, user_id))
    else:
        print("Пользователь отсутствует.")


def get_data_for_user(user_id):
    if is_value_in_table(DB_TABLE_USERS_NAME, 'user_id', user_id):
        sql_query = (f'SELECT user_id, subject, level, task, answer'
                     f' FROM {DB_TABLE_USERS_NAME} WHERE user_id = ? LIMIT 1')
        row = execute_selection_query(sql_query, (user_id, ))[0]
        result = {
            'subject': row[1],
            'level': row[2],
            'task': row[3],
            'answer': row[4]
        }
        return result


def prepare_db(clean_if_exists=False):
    create_db()
    create_table(DB_TABLE_USERS_NAME)
    if clean_if_exists:
        clean_table(DB_TABLE_USERS_NAME)
