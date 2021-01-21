create table posts
(
	title text,
	content text,
	id serial not null
		constraint posts_pk
			primary key
);

alter table posts owner to postgres;

create unique index posts_id_uindex
	on posts (id);
