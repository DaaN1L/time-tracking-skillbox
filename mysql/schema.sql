-- MySQL
DROP DATABASE IF EXISTS time_tracking;
CREATE DATABASE time_tracking;
USE time_tracking;


CREATE TABLE time_tracking.position (
    position_id     INT UNSIGNED NOT NULL AUTO_INCREMENT,
    position_nm     VARCHAR(255) NOT NULL,
    hh_billing_rate INT UNSIGNED NOT NULL,
    PRIMARY KEY (position_id),
    UNIQUE KEY (position_nm),
    CONSTRAINT ck__hh_billing_rate_positive
        CHECK (hh_billing_rate > 0)
);


CREATE TABLE time_tracking.employee (
    employee_id        INT UNSIGNED NOT NULL AUTO_INCREMENT,
    employee_full_name VARCHAR(255) NOT NULL UNIQUE,
    position_id        INT UNSIGNED NOT NULL,
    PRIMARY KEY (employee_id),
    CONSTRAINT fk__position__position_id
        FOREIGN KEY (position_id) 
        REFERENCES position (position_id)
        ON DELETE RESTRICT
);


create table time_tracking.task (
    task_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    task_cd VARCHAR(255) NOT NULL,
    PRIMARY KEY(task_id),
    UNIQUE KEY(task_cd)
);


CREATE TABLE time_tracking.timesheet (
    employee_id     INT UNSIGNED NOT NULL,
    task_id         INT UNSIGNED NOT NULL,
    task_start_dttm DATETIME     NOT NULL,
    task_end_dttm   DATETIME     NOT NULL,
    PRIMARY KEY (employee_id, task_id, task_start_dttm),
    CONSTRAINT fk__employee__employee_id
        FOREIGN KEY (employee_id)
        REFERENCES employee (employee_id)
        ON DELETE RESTRICT,
    CONSTRAINT fk__task__task_id
        FOREIGN KEY (task_id)
        REFERENCES task (task_id)
        ON DELETE CASCADE,
    CONSTRAINT ck__task_start_dttm_less_than_end_dttm
        CHECK (task_start_dttm < task_end_dttm)
);


CREATE TABLE time_tracking.timesheet_hist (
    employee_id     INT UNSIGNED NOT NULL,
    task_cd         VARCHAR(255) NOT NULL,
    task_start_dttm DATETIME     NOT NULL,
    task_end_dttm   DATETIME     NOT NULL,
    PRIMARY KEY (employee_id, task_cd, task_start_dttm),
    CONSTRAINT ck__hist__task_start_dttm_less_than_end_dttm
        CHECK (task_start_dttm < task_end_dttm)
);


# DELIMITER //
CREATE FUNCTION check_if_task_dates_overlap_for_employee(
    in_employee_id INT UNSIGNED,
    in_task_start_dttm DATETIME,
    in_task_end_dttm DATETIME
) RETURNS INT DETERMINISTIC
    BEGIN
        IF EXISTS(SELECT 1
                  FROM  time_tracking.timesheet
                  WHERE 1 = 1
                        AND in_employee_id = employee_id
                        AND (in_task_start_dttm BETWEEN task_start_dttm AND task_end_dttm
                            OR in_task_end_dttm BETWEEN task_start_dttm AND task_end_dttm))
        THEN RETURN 1;
        ELSE RETURN 0;
        END IF;
    END;


CREATE TRIGGER TR__timesheet_before_insert BEFORE INSERT ON time_tracking.timesheet
FOR EACH ROW
    BEGIN
        IF check_if_task_dates_overlap_for_employee(
                NEW.employee_id,
                NEW.task_start_dttm,
                NEW.task_end_dttm
            )
        THEN
            SET NEW.task_start_dttm = NULL;
        END IF;
    END;


CREATE TRIGGER TR__timesheet_after_delete AFTER DELETE ON time_tracking.timesheet
FOR EACH ROW
    BEGIN
        DECLARE task_code VARCHAR(250);

        SELECT t.task_cd
          INTO task_code
          FROM task t
         WHERE t.task_id = OLD.task_id;

        INSERT INTO timesheet_hist(employee_id, task_cd, task_start_dttm, task_end_dttm)
        VALUES
            (OLD.employee_id, task_code, OLD.task_start_dttm, OLD.task_end_dttm);

        IF NOT EXISTS(SELECT 1
                        FROM time_tracking.timesheet
                       WHERE task_id = OLD.task_id)
        THEN
            DELETE
              FROM task
             WHERE task_id = OLD.task_id;
        END IF;
    END;


# DELIMITER ;
