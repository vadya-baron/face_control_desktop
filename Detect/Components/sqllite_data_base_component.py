import logging
import os
import pickle
import sqlite3
import datetime
import time
from typing import Union


class DataBaseHandler:
    def __init__(self, config: dict, debug: bool = False):
        self._debug = debug
        self._config = config
        self._db_name = self._config['dbname'] + '.db'
        self._db_path = self._config['db_dir'] + self._db_name
        self._conn = None

        if os.path.isfile(self._db_path):
            try:
                self._conn = sqlite3.connect(r'' + self._db_path)
                self._conn.row_factory = self.dict_factory
            except Exception as e:
                logging.exception(e)
                exit(1)
        else:
            logging.info('Запустите приложение Admin и добавьте сотрудников')

    def is_db_ready(self) -> bool:
        if self._conn is None:
            return False
        else:
            return True

    # EMPLOYEES
    def get_employees(self, statuses: list) -> list[dict]:
        data = []
        if self._conn is None:
            return data

        if statuses is None or len(statuses) == 0:
            logging.error('get_employees -> statuses = notfound')
            return data

        join_statuses = ','.join([str(i) for i in statuses])
        query = "WHERE status IN (" + join_statuses + ")"

        cursor = self._conn.cursor()
        try:
            cursor.execute("SELECT * FROM employees " + query + ";")
            data = cursor.fetchall()
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()

        return data

    def get_last_visit(self, employee_id: int, filters: dict) -> dict:
        query, _ = self._get_statistic_query(filters)
        if query != '':
            query = 'AND' + query

        result = {}
        cursor = self._conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM `employee_visits` WHERE employee_id = "+str(employee_id)+" " + query +
                " ORDER BY `visit_date` DESC"
            )
            result = cursor.fetchone()
        except Exception as e:
            cursor.close()
            logging.exception(e)
        finally:
            cursor.close()

        return result

    # VECTORS
    def get_vectors(self, employees_ids: list) -> list[dict]:
        if self._conn is None:
            return []

        if employees_ids is None or len(employees_ids) == 0:
            return []

        join_ids = ','.join([str(i) for i in employees_ids])
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

        for row in vectors:

            if not (type(row) is dict):
                continue

            if row.get('face_vector') is not None:
                row['face_vector'] = pickle.loads(row['face_vector'])

            if row.get('face_recognize_vector') is not None:
                row['face_recognize_vector'] = pickle.loads(row['face_recognize_vector'])

        return vectors

    # STATISTIC
    def add_visit(self, employee_id: int, direction: int) -> Union[bool, int]:
        if self._conn is None:
            return False

        if employee_id <= 0:
            return False

        result = False
        cursor = self._conn.cursor()
        try:
            # INSERT INTO users (name, age) VALUES ('Tom', 37);
            visit_date = '{date:%Y-%m-%d %H:%M:%S}'.format(date=datetime.datetime.now())
            sql = "INSERT INTO `employee_visits` (`employee_id`, `visit_date`, `direction`) " \
                  "VALUES ("+str(employee_id)+", '"+str(visit_date)+"', "+str(direction)+")"
            cursor.execute(sql)
            self._conn.commit()
            result = cursor.lastrowid
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()

        return result

    # HELPERS
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
