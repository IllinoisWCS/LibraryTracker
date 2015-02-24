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
  available text not null,
  cover text not null,
  year integer,
  category text not null
);