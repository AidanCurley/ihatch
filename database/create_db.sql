-- drop database ihatch;
create database IF NOT EXISTS ihatch;
use ihatch;

drop table IF EXISTS weight;
drop table IF EXISTS egg;

drop table IF EXISTS measurement;
drop table IF EXISTS hatch;

drop table IF EXISTS sensor;
drop table IF EXISTS user;

create table IF NOT EXISTS user
(
    id       int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name     varchar(50) NOT NULL,
    surname  varchar(50) NOT NULL,
    dob      varchar(50) NOT NULL,
    email    varchar(50) NOT NULL,
    hash     varchar(100) NOT NULL
);

create table IF NOT EXISTS sensor
(
    id              int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_id         int,
    is_connected    boolean,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

create table IF NOT EXISTS hatch
(
    id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_id     int,
    start_date  varchar(50),
    is_active   boolean,
    sensor_id   varchar(20),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

create table IF NOT EXISTS measurement
(
    id          int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    sensor_id   int,
    date_time   varchar(50),
    m_type      varchar(20),
    measurement    float,
    FOREIGN KEY (sensor_id) REFERENCES sensor(id)
);

create table IF NOT EXISTS egg
(
    id          int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    hatch_id    int,
    start_date  varchar(50),
    end_date    varchar(50),
    hatched     boolean,
    FOREIGN KEY (hatch_id) REFERENCES hatch(id)
);

create table IF NOT EXISTS weight
(
    id          int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    egg_id      int,
    date_time   varchar(50),
    weight      float,
    FOREIGN KEY (egg_id) REFERENCES egg(id)
);

GRANT ALL PRIVILEGES on ihatch.* to `ihatch-api-user`;
FLUSH PRIVILEGES;
