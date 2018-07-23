create table if not exists counselors (
   id serial unique,
   lastname text,
   firstname text,
   mi text,
   code text primary key,
   affiliation text,                     /* COUNSELORS TABLE */
   city text
);

create table users(
  id serial unique,
  username text primary key,
  password text,
  contact text,
  code text,
  foreign key (code)
  references counselors(code)
);

create table userschedule(
  id serial unique,
  username text primary key,
  monday text[],
  tuesday text[],
  wednesday text[],
  thursday text[],
  friday text[]
);

create table appointment(
  id serial primary key,
  unid text,
  city text,
  clinic text,
  counselor text,
  date text,
  time text
);

-- get cities
create type city as (city text);
create or replace function getcities() returns setof city as
$$
	select distinct city from counselors;
$$
language 'sql';


-- get clinics per city selected
create type clinic as (clinic text);
create or replace function getclinics(in par_city text) returns setof clinic as
$$
   select affiliation from counselors where city = par_city;

$$
language 'sql';

--get counselor for selected clinic/hospital
create type counselor as (firstname text, mi text, lastname text, code text);
create or replace function getcounselor(in par_city text, in par_clinic text) returns setof counselor as
$$
   select firstname, mi, lastname, code from counselors where city = par_city and affiliation = par_clinic;

$$
language 'sql';



--getschedule for selected cunselor based on username which will be obtained from the users table
-- the CODE will be obtained from the getcounselor output
create or replace function getusername(in par_code text) returns text as
$$
   select username from users where code = par_code;
$$
language 'sql';


--getschedule for selected counselor using username
create type schedule as (monday text[], tuesday text[], wednesday text[], thursday text[], friday text[]);
create or replace function getschedule(in par_username text) returns setof schedule as
$$
   select monday, tuesday, wednesday, thursday, friday from userschedule where username = par_username;
$$
language 'sql';

--BEYOND THIS LINE ARE ALREADY CODES FOR TESTING PURPOSES

--add appointment


