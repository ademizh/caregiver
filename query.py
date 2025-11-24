from sqlalchemy import create_engine, text

DATABASE_URL = "mysql+pymysql://ademizh:7410qwert@ademizh.mysql.pythonanywhere-services.com/ademizh$default"

engine = create_engine(DATABASE_URL, echo=False)

def run_select(label, sql, params=None):
    print(f"\n===== {label} =====")
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        rows = result.fetchall()
        for row in rows:
            print(row)
        if not rows:
            print("(no rows)")


def run_execute(label, sql, params=None):
    print(f"\n===== {label} =====")
    with engine.begin() as conn:  # begin = с транзакцией
        result = conn.execute(text(sql), params or {})
        try:
            print("Rows affected:", result.rowcount)
        except Exception:
            pass


def update_3_1():
    sql = """
        UPDATE `user`
        SET phone_number = '+77773414141'
        WHERE given_name = 'Arman' AND surname = 'Armanov';
    """
    run_execute("3.1 Update Arman Armanov phone number", sql)


def update_3_2():
    sql = """
        UPDATE caregiver
        SET hourly_rate = CASE
            WHEN hourly_rate < 10 THEN hourly_rate + 0.3
            ELSE hourly_rate * 1.10
        END;
    """
    run_execute("3.2 Add commission to caregivers' hourly_rate", sql)


def delete_4_1():
    sql = """
        DELETE j
        FROM job j
        JOIN member m ON j.member_user_id = m.member_user_id
        JOIN `user` u ON m.member_user_id = u.user_id
        WHERE u.given_name = 'Amina' AND u.surname = 'Aminova';
    """
    run_execute("4.1 Delete jobs posted by Amina Aminova", sql)


def delete_4_2():
    sql = """
        DELETE m
        FROM member m
        JOIN address a ON m.member_user_id = a.member_user_id
        WHERE a.street = 'Kabanbay Batyr';
    """
    run_execute("4.2 Delete members who live on Kabanbay Batyr street", sql)

def simple_5_1():
    sql = """
        SELECT
            cu.given_name  AS caregiver_given_name,
            cu.surname     AS caregiver_surname,
            mu.given_name  AS member_given_name,
            mu.surname     AS member_surname
        FROM appointment a
        JOIN caregiver c   ON a.caregiver_user_id = c.caregiver_user_id
        JOIN `user` cu     ON c.caregiver_user_id = cu.user_id
        JOIN member m      ON a.member_user_id = m.member_user_id
        JOIN `user` mu     ON m.member_user_id = mu.user_id
        WHERE a.status = 'Accepted';
    """
    run_select("5.1 Caregiver and member names for accepted appointments", sql)


def simple_5_2():
    sql = """
        SELECT job_id
        FROM job
        WHERE LOWER(other_requirements) LIKE '%soft-spoken%';
    """
    run_select("5.2 Job IDs containing 'soft-spoken' in requirements", sql)


def simple_5_3():
    sql = """
        SELECT a.appointment_id, a.work_hours
        FROM appointment a
        JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
        WHERE c.caregiving_type = 'Babysitter';
    """
    run_select("5.3 Work hours of all babysitter appointments", sql)


def simple_5_4():
    sql = """
        SELECT DISTINCT
            u.given_name,
            u.surname,
            u.city,
            m.house_rules
        FROM member m
        JOIN `user` u ON m.member_user_id = u.user_id
        JOIN job j    ON j.member_user_id = m.member_user_id
        WHERE j.required_caregiving_type = 'Elderly Care'
          AND u.city = 'Astana'
          AND m.house_rules LIKE '%No pets.%';
    """
    run_select("5.4 Members looking for Elderly Care in Astana with 'No pets.' rule", sql)

def complex_6_1():
    sql = """
        SELECT
            u.given_name,
            u.surname,
            j.job_id,
            COUNT(ja.caregiver_user_id) AS num_applicants
        FROM job j
        JOIN member m        ON j.member_user_id = m.member_user_id
        JOIN `user` u        ON m.member_user_id = u.user_id
        LEFT JOIN job_application ja ON j.job_id = ja.job_id
        GROUP BY u.given_name, u.surname, j.job_id
        ORDER BY j.job_id;
    """
    run_select("6.1 Number of applicants for each job posted by a member", sql)


def complex_6_2():
    sql = """
        SELECT
            u.given_name,
            u.surname,
            SUM(a.work_hours) AS total_hours
        FROM appointment a
        JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
        JOIN `user` u    ON c.caregiver_user_id = u.user_id
        WHERE a.status = 'Accepted'
        GROUP BY u.given_name, u.surname
        ORDER BY total_hours DESC;
    """
    run_select("6.2 Total hours spent by caregivers for accepted appointments", sql)


def complex_6_3():
    sql = """
        SELECT
            u.given_name,
            u.surname,
            AVG(c.hourly_rate * a.work_hours) AS avg_earnings_per_appointment
        FROM appointment a
        JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
        JOIN `user` u    ON c.caregiver_user_id = u.user_id
        WHERE a.status = 'Accepted'
        GROUP BY u.given_name, u.surname
        ORDER BY avg_earnings_per_appointment DESC;
    """
    run_select("6.3 Average pay of caregivers (per accepted appointment)", sql)


def complex_6_4():
    sql = """
        SELECT
            u.given_name,
            u.surname,
            AVG(c.hourly_rate * a.work_hours) AS avg_earnings_per_appointment
        FROM appointment a
        JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
        JOIN `user` u    ON c.caregiver_user_id = u.user_id
        WHERE a.status = 'Accepted'
        GROUP BY u.given_name, u.surname
        HAVING AVG(c.hourly_rate * a.work_hours) >
               (
                   SELECT AVG(c2.hourly_rate * a2.work_hours)
                   FROM appointment a2
                   JOIN caregiver c2 ON a2.caregiver_user_id = c2.caregiver_user_id
                   WHERE a2.status = 'Accepted'
               )
        ORDER BY avg_earnings_per_appointment DESC;
    """
    run_select("6.4 Caregivers who earn above average (based on accepted appointments)", sql)


def derived_7():
    sql = """
        SELECT
            u.given_name,
            u.surname,
            SUM(c.hourly_rate * a.work_hours) AS total_cost
        FROM appointment a
        JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
        JOIN `user` u    ON c.caregiver_user_id = u.user_id
        WHERE a.status = 'Accepted'
        GROUP BY u.given_name, u.surname
        ORDER BY total_cost DESC;
    """
    run_select("7. Total cost to pay for each caregiver (accepted appointments)", sql)

def view_8_create_and_select():
    create_view_sql = """
        CREATE OR REPLACE VIEW job_applications_view AS
        SELECT
            ja.job_id,
            j.required_caregiving_type,
            j.other_requirements,
            ja.caregiver_user_id,
            cu.given_name AS caregiver_given_name,
            cu.surname    AS caregiver_surname,
            ja.date_applied
        FROM job_application ja
        JOIN job j        ON ja.job_id = j.job_id
        JOIN caregiver c  ON ja.caregiver_user_id = c.caregiver_user_id
        JOIN `user` cu    ON c.caregiver_user_id = cu.user_id;
    """
    run_execute("8.1 Create or replace VIEW job_applications_view", create_view_sql)

    select_view_sql = "SELECT * FROM job_applications_view;"
    run_select("8.2 View all job applications and applicants", select_view_sql)

if __name__ == "__main__":
    print("Connecting to database and executing Assignment 3 Part 2 queries...")

   
    update_3_1()
    update_3_2()

    delete_4_1()
    delete_4_2()

    simple_5_1()
    simple_5_2()
    simple_5_3()
    simple_5_4()

    complex_6_1()
    complex_6_2()
    complex_6_3()
    complex_6_4()

    derived_7()

    view_8_create_and_select()

    print("\nDone.")

