USE ihatch;
SHOW tables;
SHOW columns in user;

INSERT INTO user (name, surname, dob, email, hash) values ("Aidan", "Curley", "1974-09-18", "aidanpcurley@gmail.com", "123456");
INSERT INTO user (name, surname, dob, email, hash) values ("Thalita", "Vergilio", "1977-07-16", "tvergilio@gmail.com", "123456");
INSERT INTO user (name, surname, dob, email, hash) values ("Rampage", "Jackson", "2019-01-21", "qrj@gmail.com", "beak");
INSERT INTO sensor (user_id, is_connected) values (1, true);
INSERT INTO sensor (user_id, is_connected) values (2, true);
INSERT INTO sensor (user_id, is_connected) values (3, true);

INSERT INTO measurement (sensor_id, date_time, temperature, humidity) values(1, "2022-07-0314:21:30", 40.2, 38.43);