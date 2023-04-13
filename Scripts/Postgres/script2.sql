create table mirea.institutions
(
    id    integer     not null
        constraint institutions_pk
            primary key,
    title varchar(50) not null
);

alter table mirea.institutions
    owner to postgres;

create unique index institutions_id_uindex
    on mirea.institutions (id);

create table mirea.cafedra
(
    code           varchar(4)  not null
        constraint cafedra_pk
            primary key,
    title          varchar(50) not null,
    institution_id integer     not null
        constraint cafedra_institutions_id_fk
            references mirea.institutions
            on delete cascade
);

alter table mirea.cafedra
    owner to postgres;

create table mirea.speciality
(
    code         varchar(8)  not null
        constraint speciality_pk
            primary key,
    title        varchar(50) not null,
    cafedra_code varchar(4)  not null
        constraint speciality_cafedra_code_fk
            references mirea.cafedra
            on delete cascade
);

alter table mirea.speciality
    owner to postgres;

create unique index speciality_code_uindex
    on mirea.speciality (code);

create table mirea.gruppa
(
    code            varchar(10) not null,
    speciality_code varchar(8)  not null
        constraint gruppa_speciality_code_fk
            references mirea.speciality
            on delete cascade,
    end_year        integer     not null
);

alter table mirea.gruppa
    owner to postgres;

create unique index gruppa_name_uindex
    on mirea.gruppa (code);

create table mirea.student
(
    code        varchar(6)  not null
        constraint student_pk
            primary key,
    full_name   varchar(50) not null,
    gruppa_code varchar(10) not null
        constraint student_gruppa_code_fk
            references mirea.gruppa (code)
            on delete cascade
);

alter table mirea.student
    owner to postgres;

create unique index student_code_uindex
    on mirea.student (code);

create table mirea.course
(
    id        integer     not null
        constraint course_pk
            primary key,
    title     varchar(50) not null,
    spec_code varchar(8)  not null
        constraint course_spec_code_fk
            references mirea.speciality
            on delete cascade
);

alter table mirea.course
    owner to postgres;

create unique index course_id_uindex
    on mirea.course (id);

create table mirea.lesson
(
    id        integer     not null
        constraint lesson_pk
            primary key,
    title     varchar(50) not null,
    course_id integer     not null
        constraint lesson_course_id_fk
            references mirea.course
            on delete cascade
);

alter table mirea.lesson
    owner to postgres;

create unique index lesson_id_uindex
    on mirea.lesson (id);

create table mirea.time_table
(
    id            integer not null
        constraint time_table_pk
            primary key,
    date_time     timestamp,
    gruppa_code   varchar(10)
        constraint time_table_gruppa_code_fk
            references mirea.gruppa (code)
            on delete cascade,
    lesson_id     integer
        constraint time_table_lesson_id_fk
            references mirea.lesson
            on delete cascade,
    lesson_number integer
);

alter table mirea.time_table
    owner to postgres;

create unique index time_table_id_uindex
    on mirea.time_table (id);

create table mirea.visit
(
    id            integer               not null
        constraint visit_pk
            primary key,
    student_code  varchar(6)            not null
        constraint visit_student_code_fk
            references mirea.student
            on delete cascade,
    time_table_id integer               not null
        constraint visit_time_table_id_fk
            references mirea.time_table
            on delete cascade,
    is_visited    boolean default false not null
);

alter table mirea.visit
    owner to postgres;

create unique index visit_id_uindex
    on mirea.visit (id);

