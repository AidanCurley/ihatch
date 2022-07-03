USE ihatch;

INSERT INTO user (name, surname, dob, email, hash) values ("Aidan", "Curley", "1974-09-18", "aidanpcurley@gmail.com", "123456");
INSERT INTO sensor (user_id, is_connected) values (1, true);

