CREATE TABLE Department (
    departmentId int NOT NULL,
    name varchar(255) NOT NULL,
    leaderId int NOT NULL,
    PRIMARY KEY (departmentId),
    FOREIGN KEY (leaderId) REFERENCES Employee(employeeId)
);

CREATE TABLE Employeee (
    employeeId int NOT NULL,
    name varchar(255) NOT NULL,
    departmentId int NOT NULL,
    PRIMARY KEY (employeeId),
    FOREIGN KEY (departmentId) REFERENCES Department(departmentId)
);

INSERT INTO Department VALUES (0, "Test2", 0);
