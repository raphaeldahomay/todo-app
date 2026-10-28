create database todoo_db;

\c todoo_db

create schema if not exists todoo_schema;

set search_path to todoo_schema;

create table users (
    user_id uuid primary key not null default gen_random_uuid()
    , first_name varchar(255) not null
    , last_name varchar(255) not null
    , username varchar(255) unique not null
    , pwd_hash text not null 
    , created_at timestampz not null default current_timestamp
    , is_active boolean not null default true
);

create table folders (
    folder_id uuid primary key not null default gen_random_uuid()
    , user_id uuid foreign key not null references users(user_id)
    , folder_name varchar(255) not null
    , created_at timestamptz not null default current_timestamp
    , updated_at timestamptz
    , is_deleted boolean not null default false
);

create table tasks (
    task_id uuid primary key default gen_random_uuid()
    , folder_id uuid not null references folders(folder_id)
    , task_desc varchar(255) not null
    , created_at timestamptz not null default current_timestamp
    , updated_at timestamptz
    , is_deleted boolean not null default false
    , due_date date
    , is_done boolean not null default false 
);

create index idx_folders_user_id on folders(user_id);

create index idx_tasks_folder_id on tasks(folder_id);