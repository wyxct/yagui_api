-- Table: public.alarm_solution

-- DROP TABLE public.alarm_solution;

CREATE TABLE public.cron_task
(
  id serial,
  job_name character varying(100),
  job_des character varying(1000),
  active_flag boolean,
  created_user character varying(200),
  created_timestamp timestamp with time zone DEFAULT now(),
  last_updated_user character varying(200),
  last_updated_timestamp timestamp with time zone DEFAULT now(),
  CONSTRAINT cron_task_pk PRIMARY KEY (id),
  CONSTRAINT cron_task_uk UNIQUE (job_name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.cron_task
  OWNER TO public_own;
GRANT ALL ON TABLE public.cron_task TO public_own;
GRANT SELECT ON TABLE public.cron_task TO public_readonly;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE public.cron_task TO public_write;


CREATE TABLE public.cron_task_results
(
  id bigserial,
  job_name character varying(100),
  contents jsonb,
  created_user character varying(200),
  created_timestamp timestamp with time zone DEFAULT now(),
  last_updated_user character varying(200),
  last_updated_timestamp timestamp with time zone DEFAULT now(),
  CONSTRAINT cron_task_results_pk PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.cron_task_results
  OWNER TO public_own;
GRANT ALL ON TABLE public.cron_task_results TO public_own;
GRANT SELECT ON TABLE public.cron_task_results TO public_readonly;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE public.cron_task_results TO public_write;
