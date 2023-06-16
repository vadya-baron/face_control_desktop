import logging
import shutil
import sqlite3
import datetime
import time
from typing import Union
from pathlib import Path


class DataBaseHandler:
    def __init__(self, config: dict, debug: bool = False):
        self._debug = debug
        self._config = config
        self._db_name = self._config['dbname'] + '.db'
        self._db_path = self._config['db_dir'] + self._db_name
        self._db_backup_dir = self._config['backup_db_dir']

        f = open(self._config['dump_db_path'], 'r')
        try:
            sql_dump = f.read()
            self._conn = sqlite3.connect(r'' + self._db_path)
            self._conn.cursor().executescript(sql_dump)
            self._conn.row_factory = self.dict_factory
        except Exception as e:
            logging.exception(e)
            exit(1)
        finally:
            f.close()

    # EMPLOYEES
    def get_employees(self, filters: dict = None) -> list[dict]:
        if filters is not None:
            id = filters.get('id', None)
            ids = filters.get('ids', None)
            status = filters.get('status', None)
            query = ''
            if ids:
                for key, value in enumerate(ids):
                    ids[key] = int(value)

                join_ids = ','.join(ids)
                if query == '':
                    query = " id IN (" + join_ids + ")"
                else:
                    query = query + " AND id IN (" + join_ids + ")"

            if id:
                if query == '':
                    query = " id = " + str(id)
                else:
                    query = query + " AND id = " + str(id)

            if status:
                if query == '':
                    query = " status = " + str(status)
                else:
                    query = query + " AND status = " + str(status)

            if query != '':
                query = "WHERE" + query
        else:
            query = "WHERE status = 1"

        data = []
        cursor = self._conn.cursor()
        try:
            cursor.execute("SELECT * FROM employees " + query + ";")
            data = cursor.fetchall()
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()

        return data

    def get_employee(self, employee_id: int) -> Union[dict, None]:
        if employee_id is None:
            return None

        data = {}
        cursor = self._conn.cursor()
        try:
            cursor.execute("SELECT * FROM employees WHERE id = '" + str(employee_id) + "';")
            data = cursor.fetchone()
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()

        return data

    def save_employee(self, data: dict) -> Union[bool, int]:
        if data is None:
            return False

        insert_with_param = """
        INSERT INTO 'employees' 
        ('external_id', 'date_create', 'date_update', 'display_name', 'employee_position', 'status') 
        VALUES (?, ?, ?, ?, ?, ?);
        """

        insert_data = (
            data.get('external_id'),
            data.get('date_create'),
            data.get('date_update'),
            data.get('display_name'),
            data.get('employee_position'),
            data.get('status')
        )

        result = False
        cursor = self._conn.cursor()
        try:
            cursor.execute(insert_with_param, insert_data)
            self._conn.commit()
            result = cursor.lastrowid
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()

        return result

    def remove_employee(self, employee_id: int) -> bool:
        if employee_id is None or employee_id == 0:
            return False
        result = False
        cursor = self._conn.cursor()
        try:
            cursor.execute("DELETE FROM employees WHERE id = '" + str(employee_id) + "';")
            cursor.execute("DELETE FROM employee_visits WHERE employee_id = '" + str(employee_id) + "';")
            cursor.execute("DELETE FROM employees_vectors WHERE employee_id = '" + str(employee_id) + "';")
            self._conn.commit()
            result = True
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()

        return result

    def update_status_employee(self, id: int, status: int) -> bool:
        if id is None or id == 0 or status is None or status == 0:
            return False

        update = False
        cursor = self._conn.cursor()
        try:
            cursor.execute("SELECT * FROM `employees` WHERE id = " + str(id))
            result = dict(cursor.fetchone())

            if result.get('id') is None:
                cursor.close()
                return update

            cursor.execute("UPDATE `employees` SET status = '" + str(status) + "' WHERE id = '" + str(id) + "';")
            self._conn.commit()
            update = True
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()

        return update

    # VECTORS
    def add_employee_vectors(self, data: dict) -> bool:
        if data is None:
            return False

        insert_with_param = """
        INSERT INTO 'employees_vectors' 
        ('employee_id', 'face_vector', 'face_recognize_vector') 
        VALUES (?, ?, ?);
        """

        insert_data = (
            data.get('employee_id'),
            data.get('face_vector'),
            data.get('face_recognize_vector')
        )

        result = False
        cursor = self._conn.cursor()
        try:
            cursor.execute(insert_with_param, insert_data)
            self._conn.commit()
            result = True
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()

        return result

    def get_vectors(self, persons_ids: list) -> list[dict]:
        if persons_ids is None or len(persons_ids) == 0:
            return []

        join_ids = ','.join(persons_ids)
        query = "WHERE employee_id IN (" + join_ids + ")"

        vectors = []
        cursor = self._conn.cursor()
        try:
            cursor.execute("SELECT * FROM `employees_vectors` " + query)
            vectors = cursor.fetchall()
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()

        return vectors

    # STATISTIC
    def add_visit(self, employee_id: int, direction: int) -> Union[bool, int]:
        if employee_id <= 0:
            return False

        result = False
        cursor = self._conn.cursor()
        try:
            visit_date = '{date:%Y-%m-%d %H:%M:%S}'.format(date=datetime.datetime.now())
            sql = "INSERT INTO `employee_visits` (`employee_id`, `visit_date`, `direction`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (employee_id, visit_date, direction))
            self._conn.commit()
            result = cursor.lastrowid
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()

        return result

    def get_last_visit(self, employee_id: int, filters: dict) -> dict:
        query, _ = self._get_statistic_query(filters)
        if query != '':
            query = 'AND' + query

        result = {}
        cursor = self._conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM `employee_visits` WHERE employee_id = %s " + query + " ORDER BY `visit_date` DESC",
                employee_id
            )
            result = cursor.fetchone()
        except Exception as e:
            cursor.close()
            logging.exception(e)
        finally:
            cursor.close()

        return result

    def get_visits(self, filters: dict) -> list[dict]:
        query, limit_offset = self._get_statistic_query(filters)
        if query != '':
            query = 'WHERE' + query

        data = []
        cursor = self._conn.cursor()
        try:
            cursor.execute("SELECT * FROM `employee_visits` " + query + " ORDER BY `visit_date` DESC" + limit_offset)
            data = cursor.fetchall()
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()

        return data

    def get_start_end_working(self, for_date: str = None, employee_id: str = None) -> (list[dict], list[dict]):
        if for_date is None:
            for_date = '{date:%Y-%m-%d}'.format(date=datetime.datetime.now())

        common_where = ''
        if employee_id is not None:
            common_where = ' AND employee_id = ' + employee_id

        date_where = 'WHERE visit_date >= \'' + for_date + ' 00:00:00\' AND visit_date <= \'' + for_date + ' 23:59:59\''

        query_start = 'SELECT DISTINCT FIRST_VALUE(`id`) OVER `win` AS `id`, FIRST_VALUE(`direction`) OVER `win` AS ' \
                      '`direction`, FIRST_VALUE(`visit_date`) OVER `win` AS `visit_date`, `employee_id` FROM ' \
                      '`employee_visits` ' + date_where + ' AND direction = 0  ' + common_where + \
                      'WINDOW `win` AS (PARTITION BY `employee_id` ORDER BY `visit_date` ASC);'

        query_end = 'SELECT DISTINCT FIRST_VALUE(`id`) OVER `win` AS `id`, FIRST_VALUE(`direction`) OVER `win` AS ' \
                    '`direction`, FIRST_VALUE(`visit_date`) OVER `win` AS `visit_date`, `employee_id` FROM ' \
                    '`employee_visits` ' + date_where + '  AND direction = 1 ' + common_where + \
                    'WINDOW `win` AS (PARTITION BY `employee_id` ORDER BY `visit_date` DESC);'

        list_start = []
        list_end = []
        cursor = self._conn.cursor()
        try:
            cursor.execute(query_start)
            list_start = cursor.fetchall()

            cursor.execute(query_end)
            list_end = cursor.fetchall()
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()

        return list_start, list_end

    # HELPERS
    def backup_db(self):
        self._conn.close()
        backup_dir = self._db_backup_dir + self.get_time()
        try:
            Path(str(backup_dir)).mkdir(parents=True, exist_ok=True)
            shutil.copyfile(self._db_path, Path(backup_dir, self._db_name))
        except Exception as e:
            logging.exception(e)

    @staticmethod
    def get_time() -> str:
        return datetime.datetime.fromtimestamp(
            time.mktime(datetime.datetime.now().timetuple())
        ).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @staticmethod
    def _get_statistic_query(filters: dict) -> (str, str):
        if len(filters) == 0:
            return ''

        id = filters.get('id', None)
        employee_id = filters.get('employee_id', None)
        direction = filters.get('direction', None)
        date_from = filters.get('date_from', None)
        date_to = filters.get('date_to', None)
        employee_ids = filters.get('employee_ids', None)
        ids = filters.get('ids', None)
        limit = int(filters.get('limit', 0))
        page = int(filters.get('page', 0))
        all_data = bool(filters.get('all_data', False))

        query = ''
        if id:
            query = " id = " + str(id)

        if employee_id:
            if query == '':
                query = " employee_id = " + str(employee_id)
            else:
                query = query + " AND employee_id = " + str(employee_id)

        if direction:
            if query == '':
                query = " direction = " + str(direction)
            else:
                query = query + " AND direction = " + str(direction)

        if date_from:
            if query == '':
                query = " visit_date >= '" + date_from + "'"
            else:
                query = query + " AND visit_date >= '" + date_from + "'"

        if date_to:
            if query == '':
                query = " visit_date <= '" + date_to + "'"
            else:
                query = query + " AND visit_date <= '" + date_to + "'"

        if employee_ids:
            for key, value in enumerate(employee_ids):
                employee_ids[key] = int(value)

            join_employee_ids = ','.join(employee_ids)
            if query == '':
                query = " employee_id IN (" + join_employee_ids + ")"
            else:
                query = query + " AND employee_id IN (" + join_employee_ids + ")"

        if ids:
            for key, value in enumerate(ids):
                ids[key] = int(value)

            join_ids = ','.join(ids)
            if query == '':
                query = " id IN (" + join_ids + ")"
            else:
                query = query + " AND id IN (" + join_ids + ")"

        limit_offset = ''
        if all_data:
            return query, limit_offset

        if limit:
            limit_offset = " LIMIT " + str(limit)

        if page > 0 and limit > 0:
            offset = (page - 1) * limit
            limit_offset = limit_offset + " OFFSET " + str(offset)

        return query, limit_offset
