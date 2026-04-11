create database PRISM_DB;
use PRISM_DB;

create table Applications(
application_id int primary key identity(1,1),
application_name varchar(100) not null,
owner varchar(100) not null,
created_at datetime default getdate()
);

create table Assets(
asset_id int primary key identity(1,1),
application_id int not null,
asset_name varchar(100) unique,
asset_type varchar(50),
environment varchar(50),
created_at datetime default getdate(),
foreign key(application_id) references Applications(application_id)
);

create table Health_Results(
health_id int primary key identity(1,1),
asset_id int,
check_type varchar(50),
status varchar(20),
value varchar(50),
checked_at datetime default getdate(),
foreign key(asset_id) references Assets(asset_id)
);

create table Change_Tickets(
ticket_id varchar(50) primary key,
title varchar(255),
description varchar(500),
ci_name varchar(100),
change_type varchar(50),
status varchar(50),
asset_id int,
change_time datetime default getdate()
foreign key (ci_name) references Assets(asset_name),
foreign key (asset_id) references Assets(asset_id)
);

create table incidents(
incident_id int primary key identity(1,1),
application_id int not null,
issue_summary varchar(255),
root_cause varchar(500),
priority varchar(20),
status varchar(20),
created_at datetime default getdate(),
modified_time datetime default getdate(),
foreign key (application_id) references Applications(application_id)
);