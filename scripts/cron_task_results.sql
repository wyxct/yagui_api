-- Table: public.cron_task

 --DROP TABLE public.cron_task_results;

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
