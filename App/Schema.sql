-- CREATE TABLE Hospital (
-- 	ID INTEGER PRIMARY KEY AUTOINCREMENT,
-- 	Name VARCHAR,
-- 	Address VARCHAR
-- );

-- CREATE TABLE Doctor (
-- 	ID INTEGER PRIMARY KEY AUTOINCREMENT,
-- 	Name VARCHAR,
-- 	HospitalID INTEGER,
-- 	Specialization VARCHAR,
-- 	Contact_No VARCHAR,
-- 	FOREIGN KEY(HospitalID) REFERENCES Hospital(ID)
-- );

-- CREATE TABLE Patient (
-- 	ID INTEGER PRIMARY KEY AUTOINCREMENT,
-- 	Name VARCHAR,
-- 	Address VARCHAR,
-- 	Contact_No VARCHAR
-- );

-- CREATE TABLE Condition (
-- 	ID INTEGER PRIMARY KEY AUTOINCREMENT,
-- 	Name VARCHAR,
-- 	Category VARCHAR
-- );

-- CREATE TABLE Appointment (
-- 	ID INTEGER PRIMARY KEY AUTOINCREMENT,
-- 	DoctorID INTEGER,
-- 	PatientID INTEGER,
-- 	ConditionID INTEGER,
-- 	Timestamp DATETIME,
-- 	Fees DECIMAL,
-- 	FOREIGN KEY(DoctorID) REFERENCES Doctor(ID),
-- 	FOREIGN KEY(PatientID) REFERENCES Patient(ID),
-- 	FOREIGN KEY(ConditionID) REFERENCES Condition(ID)
-- );

-- CREATE TABLE Pharmacy (
-- 	ID INTEGER PRIMARY KEY AUTOINCREMENT,
-- 	Name VARCHAR,
-- 	Address VARCHAR
-- );

-- CREATE TABLE Invoice (
-- 	ID INTEGER PRIMARY KEY AUTOINCREMENT,
-- 	PharmacyID INTEGER,
-- 	AppointmentID INTEGER,
-- 	Amount DECIMAL,
-- 	FOREIGN KEY(PharmacyID) REFERENCES Pharmacy(ID),
-- 	FOREIGN KEY(AppointmentID) REFERENCES Appointment(ID)
-- );





-- Break The Query 2025

CREATE TABLE "Account" (
	"ID"	INTEGER,
	"AccountNumber"	VARCHAR(20) NOT NULL UNIQUE,
	"AccountType"	TEXT NOT NULL CHECK("AccountType" IN ('Savings', 'Current', 'Fixed Deposit')),
	"Balance"	DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
	"CustomerID"	INTEGER NOT NULL,
	"BranchID"	INTEGER NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT),
	FOREIGN KEY("BranchID") REFERENCES "Branch"("ID"),
	FOREIGN KEY("CustomerID") REFERENCES "Customer"("ID")
);

CREATE TABLE "Branch" (
	"ID"	INTEGER,
	"Name"	TEXT NOT NULL,
	"Address"	TEXT NOT NULL,
	"IFSC_Code"	TEXT NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
CREATE TABLE "Customer" (
	"ID"	INTEGER,
	"Name"	TEXT NOT NULL,
	"Email"	TEXT NOT NULL UNIQUE,
	"Phone"	TEXT NOT NULL,
	"Address"	TEXT NOT NULL,
	"DateOfBirth"	DATE NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT)
);


CREATE TABLE "Employee" (
	"ID"	INTEGER,
	"Name"	TEXT NOT NULL,
	"Position"	TEXT NOT NULL,
	"Salary"	DECIMAL(10, 2) NOT NULL,
	"BranchID"	INTEGER NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT),
	FOREIGN KEY("BranchID") REFERENCES "Branch"("ID")
);

CREATE TABLE "Loan" (
	"ID"	INTEGER,
	"LoanType"	TEXT NOT NULL CHECK("LoanType" IN ('Home Loan', 'Car Loan', 'Personal Loan', 'Education Loan')),
	"Amount"	REAL NOT NULL,
	"InterestRate"	REAL NOT NULL,
	"LoanDate"	DATE NOT NULL,
	"CustomerID"	INTEGER NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT),
	FOREIGN KEY("CustomerID") REFERENCES "Customer"("ID")
);

CREATE TABLE "LoanPayment" (
	"ID"	INTEGER,
	"PaymentAmount"	REAL NOT NULL,
	"PaymentDate"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"LoanID"	INTEGER NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT),
	FOREIGN KEY("LoanID") REFERENCES "Loan"("ID")
);



CREATE TABLE "Transaction" (
	"ID"	INTEGER,
	"TransactionType"	TEXT NOT NULL CHECK("TransactionType" IN ('Deposit', 'Withdrawal', 'Transfer')),
	"Amount"	REAL NOT NULL,
	"TransactionDate"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"AccountID"	INTEGER NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT),
	FOREIGN KEY("AccountID") REFERENCES "Account"("ID")
);
