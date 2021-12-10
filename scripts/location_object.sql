-- Table: layer2_pallet.location

DROP TABLE if exists layer2_pallet.location_object;

CREATE TABLE layer2_pallet.location_object
(
  id serial,
  object_put_type integer, -- type of location, foreign key of location_type.id
  location_name character varying(200) NOT NULL, -- name of location
  opt_condition character varying(200), -- name of location
  created_user character varying(200), -- the user name that created this record
  created_timestamp timestamp with time zone DEFAULT now(), -- the timestamp when created this record
  last_updated_user character varying(200), -- the user name that updated this record most recently
  last_updated_timestamp timestamp with time zone DEFAULT now(), -- the timestamp when updated this record most recently
  CONSTRAINT location_object_pk PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE layer2_pallet.location_object
  OWNER TO layer2_own;
GRANT ALL ON TABLE layer2_pallet.location_object TO layer2_own;
GRANT SELECT ON TABLE layer2_pallet.location_object TO layer2_readonly;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE layer2_pallet.location_object TO layer2_write;
GRANT ALL ON TABLE layer2_pallet.location_object TO layer3_own;
GRANT SELECT ON TABLE layer2_pallet.location_object TO layer3_readonly;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE layer2_pallet.location_object TO layer3_write;
GRANT ALL ON TABLE layer2_pallet.location_object TO layer4_own;
GRANT SELECT ON TABLE layer2_pallet.location_object TO layer4_readonly;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE layer2_pallet.location_object TO layer4_write;
COMMENT ON COLUMN layer2_pallet.location_object.id IS ' the internal id to identify a record ';
COMMENT ON COLUMN layer2_pallet.location_object.object_put_type IS '0 空，其他非空';
COMMENT ON COLUMN layer2_pallet.location_object.location_name IS ' name of location ';


-- Index: layer2_pallet.location_i_01

-- DROP INDEX layer2_pallet.location_i_01;

CREATE INDEX location_object_i_01
  ON layer2_pallet.location_object
  USING btree
  (location_name);

-- Index: layer2_pallet.location_i_02

-- DROP INDEX layer2_pallet.location_i_02;


