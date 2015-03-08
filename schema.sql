drop table if exists users;
create table users (
  id integer primary key autoincrement,
  netid text not null,
  password text not null
);

drop table if exists books;
create table books (
  id integer primary key autoincrement,
  name text not null,
  authors text not null,
  copies integer not null,
  available integer not null,
  cover text not null,
  year integer,
  category text
);

drop table if exists requests;
create table requests(
bookname text primary key not null,
category text not null,
author text
);
