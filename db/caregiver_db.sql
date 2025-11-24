CREATE TABLE `user` (
    user_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    given_name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    profile_description TEXT,
    `password` VARCHAR(255) NOT NULL
) ENGINE = InnoDB;

CREATE TABLE caregiver (
    caregiver_user_id INT UNSIGNED PRIMARY KEY,
    photo VARCHAR(255),
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    caregiving_type ENUM('Babysitter', 'Elderly Care', 'Playmate') NOT NULL,
    hourly_rate DECIMAL(8,2) NOT NULL,
    CONSTRAINT fk_caregiver_user
        FOREIGN KEY (caregiver_user_id)
        REFERENCES `user` (user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE member (
    member_user_id INT UNSIGNED PRIMARY KEY,
    house_rules TEXT,
    dependent_description TEXT,
    CONSTRAINT fk_member_user
        FOREIGN KEY (member_user_id)
        REFERENCES `user` (user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE address (
    member_user_id INT UNSIGNED NOT NULL,
    house_number VARCHAR(20) NOT NULL,
    street VARCHAR(255) NOT NULL,
    town VARCHAR(100) NOT NULL,
    PRIMARY KEY (member_user_id, house_number, street, town),
    CONSTRAINT fk_address_member
        FOREIGN KEY (member_user_id)
        REFERENCES member (member_user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE job (
    job_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    member_user_id INT UNSIGNED NOT NULL,
    required_caregiving_type ENUM('Babysitter', 'Elderly Care', 'Playmate') NOT NULL,
    other_requirements TEXT,
    date_posted DATE NOT NULL,
    CONSTRAINT fk_job_member
        FOREIGN KEY (member_user_id)
        REFERENCES member (member_user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE job_application (
    caregiver_user_id INT UNSIGNED NOT NULL,
    job_id INT UNSIGNED NOT NULL,
    date_applied DATE NOT NULL,
    PRIMARY KEY (caregiver_user_id, job_id),
    CONSTRAINT fk_job_application_caregiver
        FOREIGN KEY (caregiver_user_id)
        REFERENCES caregiver (caregiver_user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_job_application_job
        FOREIGN KEY (job_id)
        REFERENCES job (job_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE appointment (
    appointment_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    caregiver_user_id INT UNSIGNED NOT NULL,
    member_user_id INT UNSIGNED NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    work_hours DECIMAL(4,1) NOT NULL,
    status ENUM('Pending', 'Accepted', 'Declined', 'Cancelled') NOT NULL DEFAULT 'Pending',
    CONSTRAINT fk_appointment_caregiver
        FOREIGN KEY (caregiver_user_id)
        REFERENCES caregiver (caregiver_user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_appointment_member
        FOREIGN KEY (member_user_id)
        REFERENCES member (member_user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;



INSERT INTO `user` (
    user_id, email, given_name, surname, city, phone_number, profile_description, `password`
) VALUES
(1,  'arman.armanov@example.com',   'Arman',   'Armanov',   'Astana',   '+77010000001', 'Father of a 5-year-old son who likes painting.',                          'pass123'),
(2,  'amina.aminova@example.com',   'Amina',   'Aminova',   'Almaty',   '+77010000002', 'Mother seeking a reliable babysitter for her daughter.',                   'pass123'),
(3,  'dana.karimova@example.com',   'Dana',    'Karimova',  'Astana',   '+77010000003', 'Experienced babysitter with early childhood education background.',        'pass123'),
(4,  'serik.serikov@example.com',   'Serik',   'Serikov',   'Astana',   '+77010000004', 'Caregiver for elderly people with 5 years of experience.',                 'pass123'),
(5,  'aigerim.nurtas@example.com',  'Aigerim', 'Nurtas',    'Astana',   '+77010000005', 'Works part-time and sometimes hires caregivers; also babysits neighbors.', 'pass123'),
(6,  'timur.bek@example.com',       'Timur',   'Bek',       'Shymkent', '+77010000006', 'Student who works as a babysitter and playmate on weekends.',              'pass123'),
(7,  'aliya.sadykova@example.com',  'Aliya',   'Sadykova',  'Astana',   '+77010000007', 'Looking for a playmate for her shy son.',                                  'pass123'),
(8,  'olga.petrova@example.com',    'Olga',    'Petrova',   'Almaty',   '+77010000008', 'Professional nanny with medical background.',                               'pass123'),
(9,  'nurzat.kalykov@example.com',  'Nurzat',  'Kalykov',   'Astana',   '+77010000009', 'Can both hire caregivers and work as one.',                                'pass123'),
(10, 'madina.yeskendir@example.com','Madina',  'Yeskendir', 'Astana',   '+77010000010', 'Office worker who needs evening help with her son.',                       'pass123'),
(11, 'erlan.yermekov@example.com',  'Erlan',   'Yermekov',  'Almaty',   '+77010000011', 'Needs caregiver for his elderly mother.',                                  'pass123'),
(12, 'karina.suleimen@example.com', 'Karina',  'Suleimen',  'Astana',   '+77010000012', 'Single mother in Astana caring for her grandmother.',                      'pass123'),
(13, 'bolat.tolegen@example.com',   'Bolat',   'Tolegen',   'Astana',   '+77010000013', 'Experienced male caregiver, works with elderly people.',                   'pass123'),
(14, 'zarina.kalieva@example.com',  'Zarina',  'Kalieva',   'Astana',   '+77010000014', 'Psychology student, very good with children.',                             'pass123'),
(15, 'yermek.alim@example.com',     'Yermek',  'Alim',      'Shymkent', '+77010000015', 'Weekend babysitter available in Shymkent.',                                'pass123');



INSERT INTO caregiver (
    caregiver_user_id, photo, gender, caregiving_type, hourly_rate
) VALUES
(3,  'dana.jpg',    'Female', 'Babysitter',    8.50),
(4,  'serik.jpg',   'Male',   'Elderly Care', 12.00),
(5,  'aigerim.jpg', 'Female', 'Babysitter',    9.00),
(6,  'timur.jpg',   'Male',   'Playmate',      7.50),
(8,  'olga.jpg',    'Female', 'Babysitter',   11.00),
(9,  'nurzat.jpg',  'Male',   'Elderly Care', 10.00),
(10, 'madina.jpg',  'Female', 'Babysitter',    9.50),
(13, 'bolat.jpg',   'Male',   'Elderly Care', 15.00),
(14, 'zarina.jpg',  'Female', 'Playmate',      8.00),
(15, 'yermek.jpg',  'Male',   'Babysitter',   10.50);


INSERT INTO member (
    member_user_id, house_rules, dependent_description
) VALUES
(1,  'No smoking inside the apartment. Keep toys organized after playing.', 
     'I have a 5-year-old son who likes painting and drawing.'),
(2,  'Please be on time. Do not use your phone while the child is awake.', 
     'Daughter is 6 years old and likes board games.'),
(5,  'Pay attention to hygiene and always wash hands with the child.', 
     'Needs occasional help with her nephew, 4 years old.'),
(7,  'Quiet after 21:00. No loud music.', 
     'Has a shy 5-year-old son who needs a friendly playmate.'),
(9,  'Be respectful to neighbors. No loud guests.', 
     'Sometimes needs babysitter for younger brother.'),
(10, 'No junk food. Follow strict bedtime routine.', 
     'Son is 7 years old and very active after school.'),
(11, 'Be gentle and patient. No strong perfume.', 
     'Elderly mother with mobility issues.'),
(12, 'No pets. Please be calm and polite at home.', 
     'Grandmother needs daily assistance and companionship in Astana.'),
(13, 'Check doors and windows before leaving. Keep medicine out of reach.', 
     'Elderly father needs night supervision.'),
(14, 'Be soft-spoken and creative with activities.', 
     'Needs a playmate for 8-year-old daughter who loves art.');



INSERT INTO address (
    member_user_id, house_number, street, town
) VALUES
(1,  '10',  'Tauelsizdik',     'Astana'),
(2,  '25',  'Kabanbay Batyr',  'Almaty'),
(5,  '5A',  'Mangilik El',     'Astana'),
(7,  '7',   'Saryarka',        'Astana'),
(9,  '12',  'Abay',            'Astana'),
(10, '3',   'Republic',        'Astana'),
(11, '45',  'Kabanbay Batyr',  'Almaty'),
(12, '8',   'Turkestan',       'Astana'),
(13, '16',  'Seyfullin',       'Astana'),
(14, '2B',  'Dostyk',          'Astana');



INSERT INTO job (
    job_id, member_user_id, required_caregiving_type, other_requirements, date_posted
) VALUES
(1,  1,  'Babysitter',
     'Soft-spoken and creative babysitter needed for a 5-year-old boy who likes painting.',
     '2025-11-01'),
(2,  2,  'Babysitter',
     'Evening babysitter, patient and responsible, 2–3 times per week.',
     '2025-11-02'),
(3,  5,  'Playmate',
     'Playmate for active 4-year-old, likes drawing and outdoor games.',
     '2025-11-03'),
(4,  12, 'Elderly Care',
     'Soft-spoken caregiver for elderly grandmother, help with medicine and light cleaning.',
     '2025-11-04'),
(5,  11, 'Elderly Care',
     'Strong caregiver for elderly mother, able to cook simple meals.',
     '2025-11-05'),
(6,  7,  'Playmate',
     'Playmate for shy boy, must be soft-spoken and encouraging.',
     '2025-11-06'),
(7,  9,  'Babysitter',
     'Babysitter for weekends only, flexible hours.',
     '2025-11-07'),
(8,  10, 'Babysitter',
     'Evening babysitter, no smoking, help with homework and bedtime routine.',
     '2025-11-08'),
(9,  13, 'Elderly Care',
     'Night shifts for elderly care, monitoring and basic assistance.',
     '2025-11-09'),
(10, 14, 'Playmate',
      'Creative playmate, likes art and music activities.',
      '2025-11-10');



INSERT INTO job_application (
    caregiver_user_id, job_id, date_applied
) VALUES
(3,  1,  '2025-11-11'),
(5,  1,  '2025-11-11'),
(6,  2,  '2025-11-11'),
(8,  4,  '2025-11-12'),
(9,  4,  '2025-11-12'),
(10, 7,  '2025-11-13'),
(13, 5,  '2025-11-13'),
(14, 6,  '2025-11-14'),
(15, 3,  '2025-11-14'),
(3,  8,  '2025-11-15');


INSERT INTO appointment (
    appointment_id, caregiver_user_id, member_user_id,
    appointment_date, appointment_time, work_hours, status
) VALUES
(1,  3,  1,  '2025-11-15', '09:00:00', 3.0, 'Accepted'),
(2,  5,  1,  '2025-11-16', '14:00:00', 2.0, 'Pending'),
(3,  4,  11, '2025-11-15', '10:00:00', 4.0, 'Accepted'),
(4,  9,  12, '2025-11-16', '09:00:00', 5.0, 'Accepted'),
(5,  13, 11, '2025-11-17', '18:00:00', 3.5, 'Accepted'),
(6,  8,  2,  '2025-11-18', '19:00:00', 4.0, 'Declined'),
(7,  10, 10, '2025-11-19', '18:00:00', 2.5, 'Accepted'),
(8,  14, 7,  '2025-11-20', '11:00:00', 3.0, 'Pending'),
(9,  6,  5,  '2025-11-21', '15:00:00', 2.0, 'Accepted'),
(10, 15, 9,  '2025-11-22', '12:00:00', 6.0, 'Accepted');

