BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "employees" (
	"id"	INTEGER NOT NULL UNIQUE,
	"external_id"	INTEGER,
	"date_create"	TEXT NOT NULL,
	"date_update"	TEXT,
	"display_name"	TEXT NOT NULL,
	"employee_position"	TEXT,
	"status"	INTEGER DEFAULT 1,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "employee_visits" (
	"id"	INTEGER NOT NULL UNIQUE,
	"employee_id"	INTEGER NOT NULL,
	"visit_date"	TEXT NOT NULL,
	"direction"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("employee_id") REFERENCES "employees"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "employees_vectors" (
	"id"	INTEGER NOT NULL UNIQUE,
	"employee_id"	INTEGER NOT NULL,
	"face_vector"	BLOB NOT NULL,
	"face_recognize_vector"	BLOB NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("employee_id") REFERENCES "employees"("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "employees_status" ON "employees" (
	"status"	ASC
);
CREATE INDEX IF NOT EXISTS "index_date_desc" ON "employee_visits" (
	"visit_date"	DESC
);
CREATE INDEX IF NOT EXISTS "index_direction" ON "employee_visits" (
	"direction"	ASC
);
CREATE INDEX IF NOT EXISTS "index_employee" ON "employee_visits" (
	"employee_id"	ASC
);
COMMIT;
