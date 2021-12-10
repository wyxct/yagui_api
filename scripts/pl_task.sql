-- Table: layer2_pallet.pl_task
DROP TABLE if exists layer2_pallet.pl_task_report;
DROP TABLE if exists layer2_pallet.pl_task_type;
DROP TABLE if exists layer2_pallet.pl_task_relation;
DROP TABLE if exists layer2_pallet.pl_task;

CREATE TABLE layer2_pallet.pl_task
(
  id bigserial,
  task_type character varying(20), -- P2P:point to point, P2A:point to area, P2M:多点任务, A2P:area to point, BCID:bind cid, DCID:解绑托盘
  task_no character varying(100), -- the external id to identify a record
  from_pos character varying(50), -- start location of this task
  to_pos character varying(50), -- destination location of this task
  start_time timestamp with time zone,
  end_time timestamp with time zone,
  pos_list character varying(200), -- location list, multiple values are separated by commas
  next_pos character varying(50), -- next location of this task
  status character varying(10), -- 00:canled, 10:created, 20:handle, 30:in_progress, 50:completed, 90:error
  priority integer,
  cid character varying(50), -- name of cid
  cid_attribute jsonb, -- the property of cid
  custom_parm1 character varying(200),
  custom_parm2 character varying(200),
  source character varying(10), -- pda/pad/pc/interface/mq
  ip character varying(200),
  client_name character varying(200), -- the machine name of client
  client_type character varying(50), -- device identification
  memo character varying(200),
  ex character varying(200),
  optlist jsonb,
  created_user character varying(200), -- the user name that created this record
  created_timestamp timestamp with time zone DEFAULT now(), -- the timestamp when created this record
  last_updated_user character varying(200), -- the user name that updated this record most recently
  last_updated_timestamp timestamp with time zone DEFAULT now(), -- the timestamp when updated this record most recently
  CONSTRAINT pl_task_pk PRIMARY KEY (id),
  CONSTRAINT pl_task_uk UNIQUE (task_no)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE layer2_pallet.pl_task
  OWNER TO layer2_own;
GRANT ALL ON TABLE layer2_pallet.pl_task TO layer2_own;
GRANT SELECT ON TABLE layer2_pallet.pl_task TO layer2_readonly;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE layer2_pallet.pl_task TO layer2_write;
GRANT ALL ON TABLE layer2_pallet.pl_task TO layer3_own;
GRANT SELECT ON TABLE layer2_pallet.pl_task TO layer3_readonly;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE layer2_pallet.pl_task TO layer3_write;
GRANT ALL ON TABLE layer2_pallet.pl_task TO layer4_own;
GRANT SELECT ON TABLE layer2_pallet.pl_task TO layer4_readonly;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE layer2_pallet.pl_task TO layer4_write;
COMMENT ON COLUMN layer2_pallet.pl_task.id IS ' the internal id to identify a record ';
COMMENT ON COLUMN layer2_pallet.pl_task.task_type IS ' P2P:point to point, P2A:point to area, P2M:多点任务, A2P:area to point, BCID:bind cid, DCID:解绑托盘 ';
COMMENT ON COLUMN layer2_pallet.pl_task.task_no IS ' the external id to identify a record ';
COMMENT ON COLUMN layer2_pallet.pl_task.from_pos IS ' start location of this task ';
COMMENT ON COLUMN layer2_pallet.pl_task.to_pos IS ' destination location of this task ';
COMMENT ON COLUMN layer2_pallet.pl_task.pos_list IS ' location list, multiple values are separated by commas ';
COMMENT ON COLUMN layer2_pallet.pl_task.next_pos IS ' next location of this task ';
COMMENT ON COLUMN layer2_pallet.pl_task.status IS ' 00:canled, 10:created, 20:handle, 30:in_progress, 50:completed, 90:error ';
COMMENT ON COLUMN layer2_pallet.pl_task.cid IS ' name of cid ';
COMMENT ON COLUMN layer2_pallet.pl_task.cid_attribute IS ' the property of cid ';
COMMENT ON COLUMN layer2_pallet.pl_task.source IS ' pda/pad/pc/interface/mq ';
COMMENT ON COLUMN layer2_pallet.pl_task.client_name IS ' the machine name of client ';
COMMENT ON COLUMN layer2_pallet.pl_task.client_type IS ' device identification ';
COMMENT ON COLUMN layer2_pallet.pl_task.created_user IS ' the user name that created this record ';
COMMENT ON COLUMN layer2_pallet.pl_task.created_timestamp IS ' the timestamp when created this record ';
COMMENT ON COLUMN layer2_pallet.pl_task.last_updated_user IS ' the user name that updated this record most recently ';
COMMENT ON COLUMN layer2_pallet.pl_task.last_updated_timestamp IS ' the timestamp when updated this record most recently ';


-- Table: layer2_pallet.pl_task_relation
-- DROP TABLE layer2_pallet.pl_task_type;
-- DROP TABLE layer2_pallet.pl_task_relation;

CREATE TABLE layer2_pallet.pl_task_relation
(
  id bigserial,
  pl_task_id bigint,
  relation character varying(200),
  created_user character varying(200),
  created_timestamp timestamp with time zone DEFAULT now(),
  last_updated_user character varying(200),
  last_updated_timestamp timestamp with time zone DEFAULT now(),
  CONSTRAINT pl_task_relation_pk PRIMARY KEY (id),
  CONSTRAINT pl_task_relation_fk01 FOREIGN KEY (pl_task_id)
      REFERENCES layer2_pallet.pl_task (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE layer2_pallet.pl_task_relation
  OWNER TO postgres;
GRANT ALL ON TABLE layer2_pallet.pl_task_relation TO postgres;
GRANT ALL ON TABLE layer2_pallet.pl_task_relation TO layer2_own;
GRANT SELECT ON TABLE layer2_pallet.pl_task_relation TO layer2_readonly;
GRANT ALL ON TABLE layer2_pallet.pl_task_relation TO layer3_own;
GRANT SELECT ON TABLE layer2_pallet.pl_task_relation TO layer3_readonly;
GRANT ALL ON TABLE layer2_pallet.pl_task_relation TO layer4_own;
GRANT SELECT ON TABLE layer2_pallet.pl_task_relation TO layer4_readonly;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE layer2_pallet.pl_task_relation TO layer4_write;



-- Table: layer2_pallet.pl_task_type

-- DROP TABLE layer2_pallet.pl_task_type;

CREATE TABLE layer2_pallet.pl_task_type
(
  id serial,
  task_type character varying(200),
  ts_map character varying(200),
  created_user character varying(200),
  created_timestamp timestamp with time zone DEFAULT now(),
  last_updated_user character varying(200),
  last_updated_timestamp timestamp with time zone DEFAULT now(),
  CONSTRAINT pl_task_type_pk PRIMARY KEY (id),
  CONSTRAINT pl_task_type_uk UNIQUE (task_type)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE layer2_pallet.pl_task_type
  OWNER TO postgres;


-- Table: layer2_pallet.pl_task_relation
-- DROP TABLE layer2_pallet.pl_task_type;
-- DROP TABLE layer2_pallet.pl_task_relation;

CREATE TABLE layer2_pallet.pl_task_report
(
  id bigserial,
  pl_task_id bigint,
  reportdata  json,
  reporttype character varying(20),
  created_user character varying(200),
  created_timestamp timestamp with time zone DEFAULT now(),
  last_updated_user character varying(200),
  last_updated_timestamp timestamp with time zone DEFAULT now(),
  CONSTRAINT pl_task_report_pk PRIMARY KEY (id),
  CONSTRAINT pl_task_report_fk01 FOREIGN KEY (pl_task_id)
      REFERENCES layer2_pallet.pl_task (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE layer2_pallet.pl_task_report
  OWNER TO postgres;
GRANT ALL ON TABLE layer2_pallet.pl_task_report TO postgres;
GRANT ALL ON TABLE layer2_pallet.pl_task_report TO layer2_own;
GRANT SELECT ON TABLE layer2_pallet.pl_task_report TO layer2_readonly;
GRANT ALL ON TABLE layer2_pallet.pl_task_report TO layer3_own;
GRANT SELECT ON TABLE layer2_pallet.pl_task_report TO layer3_readonly;
GRANT ALL ON TABLE layer2_pallet.pl_task_report TO layer4_own;
GRANT SELECT ON TABLE layer2_pallet.pl_task_report TO layer4_readonly;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE layer2_pallet.pl_task_report TO layer4_write;