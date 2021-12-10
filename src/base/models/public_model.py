# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Alarm(db.Model):
    __tablename__ = 'alarm'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    alarm_type_id = db.Column(db.ForeignKey('public.alarm_type.id'), index=True)
    alarm_status_id = db.Column(db.ForeignKey('public.alarm_status.id'), index=True)
    alarm_object_type = db.Column(db.String(100))
    alarm_object = db.Column(db.String(100))
    error_code_id = db.Column(db.Integer)
    claimer = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    description_jsonb = db.Column(db.JSON)
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())

    alarm_status = db.relationship('AlarmStatu', primaryjoin='Alarm.alarm_status_id == AlarmStatu.id', backref='alarms')
    alarm_type = db.relationship('AlarmType', primaryjoin='Alarm.alarm_type_id == AlarmType.id', backref='alarms')



class AlarmSolution(db.Model):
    __tablename__ = 'alarm_solution'
    __table_args__ = (
        db.UniqueConstraint('language', 'solution_name'),
        {'schema': 'public'}
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    language = db.Column(db.String(100))
    solution_name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class AlarmSolutionRelation(db.Model):
    __tablename__ = 'alarm_solution_relation'
    __table_args__ = (
        db.UniqueConstraint('alarm_type_id', 'solution_id'),
        {'schema': 'public'}
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    alarm_type_id = db.Column(db.Integer)
    solution_id = db.Column(db.Integer)
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class AlarmStatu(db.Model):
    __tablename__ = 'alarm_status'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(1000))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class AlarmType(db.Model):
    __tablename__ = 'alarm_type'
    __table_args__ = (
        db.UniqueConstraint('alarm_name', 'module', 'sub_module'),
        {'schema': 'public'}
    )

    id = db.Column(db.Integer, primary_key=True)
    alarm_name = db.Column(db.String(100))
    module = db.Column(db.String(100))
    sub_module = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class CronTask(db.Model):
    __tablename__ = 'cron_task'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    job_name = db.Column(db.String(100), unique=True)
    job_des = db.Column(db.String(1000))
    active_flag = db.Column(db.Boolean)
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class CronTaskResult(db.Model):
    __tablename__ = 'cron_task_results'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    job_name = db.Column(db.String(100))
    contents = db.Column(db.JSON)
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class ErrorCode(db.Model):
    __tablename__ = 'error_code'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    error_type_id = db.Column(db.ForeignKey('public.error_type.id'), nullable=False, info=' error type foreign key of error_type.id ')
    name = db.Column(db.String(200), nullable=False, info=' the name of error ')
    description = db.Column(db.String(2000), info=' the description of error ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    can_pick = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())
    can_replen = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())

    error_type = db.relationship('ErrorType', primaryjoin='ErrorCode.error_type_id == ErrorType.id', backref='error_codes')



class ErrorQueue(db.Model):
    __tablename__ = 'error_queue'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    error_type_id = db.Column(db.ForeignKey('public.error_type.id'), nullable=False, info=' foreign key of message_type.id ')
    content = db.Column(db.JSON, info=' content of message ')
    status = db.Column(db.String(200), info=' status of message ')
    content_md5 = db.Column(db.String(32))
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')

    error_type = db.relationship('ErrorType', primaryjoin='ErrorQueue.error_type_id == ErrorType.id', backref='error_queues')



class ErrorType(db.Model):
    __tablename__ = 'error_type'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), nullable=False, unique=True, info=' the name of error type ')
    description = db.Column(db.String(2000), info=' the description of error type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class EventLevel(db.Model):
    __tablename__ = 'event_level'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class EventLog(db.Model):
    __tablename__ = 'event_log'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    event_type_id = db.Column(db.ForeignKey('public.event_type.id'), index=True)
    description = db.Column(db.String(1000))
    description_jsonb = db.Column(db.JSON)
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())

    event_type = db.relationship('EventType', primaryjoin='EventLog.event_type_id == EventType.id', backref='event_logs')



class EventType(db.Model):
    __tablename__ = 'event_type'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False, unique=True)
    event_level = db.Column(db.ForeignKey('public.event_level.id'))
    module = db.Column(db.String(100))
    sub_module = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())

    event_level1 = db.relationship('EventLevel', primaryjoin='EventType.event_level == EventLevel.id', backref='event_types')



class LoggingConfig(db.Model):
    __tablename__ = 'logging_config'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    log_table_type = db.Column(db.String(200), info=' log table type ')
    log_table_name = db.Column(db.String(200), unique=True, info=' log table name ')
    enabled = db.Column(db.Boolean, info=' if the log table should record ')
    duration_time = db.Column(db.Integer, info=' how long the log table will reserve the log records')
    transfer_time = db.Column(db.DateTime(True), info=' the time of the previous transfer ')
    description = db.Column(db.String(2000), info=' the description of this logging config ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class MessageQueue(db.Model):
    __tablename__ = 'message_queue'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    message_type_id = db.Column(db.ForeignKey('public.message_type.id'), nullable=False, index=True, info=' foreign key of message_type.id ')
    content = db.Column(db.JSON, info=' content of message ')
    status = db.Column(db.String(200), server_default=db.FetchedValue(), info=' status of message ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), index=True, server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    content_md5 = db.Column(db.String(32), index=True)

    message_type = db.relationship('MessageType', primaryjoin='MessageQueue.message_type_id == MessageType.id', backref='message_queues')



class MessageType(db.Model):
    __tablename__ = 'message_type'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), nullable=False, unique=True, info=' name of message ')
    category = db.Column(db.String(200), nullable=False, info=' category of message ')
    direction = db.Column(db.Integer, nullable=False, info=' 1 for Inbound, 2 for Outbound ')
    expired_time = db.Column(db.Float(53), info=' expired time of this message type ')
    description = db.Column(db.String(2000), info=' description of message ')
    accept_enable = db.Column(db.Boolean, info=' if accept this kind of message ')
    write_enable = db.Column(db.Boolean, info=' if record this kind of message ')
    report_enable = db.Column(db.Boolean, info=' if report this kind of message ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class ModuleVersion(db.Model):
    __tablename__ = 'module_version'
    __table_args__ = (
        db.UniqueConstraint('module', 'sub_module'),
        {'schema': 'public'}
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    module = db.Column(db.String(100))
    sub_module = db.Column(db.String(100))
    version = db.Column(db.String(100))
    path = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    parameter = db.Column(db.JSON)
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class OperationLog(db.Model):
    __tablename__ = 'operation_log'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    operation_type_id = db.Column(db.ForeignKey('public.operation_type.id'), nullable=False, index=True, info=' foreign key of operation.id ')
    content = db.Column(db.JSON, index=True, info=' concent of operation ')
    log_created_dttm = db.Column(db.DateTime(True), index=True, info=' created time of this operation ')

    operation_type = db.relationship('OperationType', primaryjoin='OperationLog.operation_type_id == OperationType.id', backref='operation_logs')



class OperationType(db.Model):
    __tablename__ = 'operation_type'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='the internal id to identify a record')
    name = db.Column(db.String(200), nullable=False, unique=True, info='name of operation')
    category = db.Column(db.String(200), nullable=False, info=' category of operation')
    description = db.Column(db.String(2000), info=' description of operation')
    enable = db.Column(db.Boolean, info=' if record this operation ')
    expired_time = db.Column(db.Float(53), info=' expired time of this operation log')
    created_user = db.Column(db.String(200), info=' the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when created this record')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')



class SystemConfig(db.Model):
    __tablename__ = 'system_config'
    __table_args__ = (
        db.UniqueConstraint('category', 'config_name'),
        {'schema': 'public'}
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    category = db.Column(db.String(200), nullable=False, info=' category of this config ')
    config_name = db.Column(db.String(200), nullable=False, info=' the name of config ')
    config_value = db.Column(db.String(200), info=' the value of config ')
    description = db.Column(db.String(2000), info=' the description of config type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class VersionLog(db.Model):
    __tablename__ = 'version_log'
    __table_args__ = (
        db.UniqueConstraint('trunk', 'branch', 'version_no'),
        {'schema': 'public'}
    )

    log_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    trunk = db.Column(db.String(20), info='trunk level is for different business lines: STAR, VIP...')
    branch = db.Column(db.String(20), info='branch level is for customized requirements:\r\neg.\r\n1 - empty base\r\n1.1 - Ardern Hills\r\n1.2 - SoCal\r\n1.2.1 - Testing with real agvs\r\n1.2.2 - Testing for full-scale release logic\r\n1.3 - Charlotte\r\n1.3.1 - Testing with real agvs\r\n')
    version_no = db.Column(db.String(20), info='version number, should always be four digits seperated by dots: \r\n1st digit is for architecture change or a lot of accumulated change;\r\n2nd digit is for general change that will be applied to all branches of the trunk (the update file may be same or similar to each branch);\r\n3rd digit is for customized change for specified branch;\r\n4th digit is for small unimportant change, temporary change, or some change made by persons not from the database-develop team;\r\neg.\r\n1.0.0.0 - the version running in Orlando in 2017-3;\r\n2.0.0.0 - the version running in Ardern Hills in 2017-10;\r\n3.0.0.0 - the version running in SoCal in 2018-5;\r\n3.1.0.0 - a new base version released by version controller;\r\n3.1.1.0 - a new version released by developers of database-develop team;\r\n3.1.1.1 - a new version temporarily released by others')
    update_type = db.Column(db.String(20), info='update type should be one of the followings:\r\n1, ramify: \r\n\tcreate a new branch, like b1 -> b1.1; code set does not change; version_no will not change;\r\n2, release: \r\n\tintegrate accumulated change as a new version, like v1.1.3.2 -> v1.2.0.0; code set does not change; branch does not change;\r\n3, full_backup: \r\n\tnot updated by scripts, updated by a database full backup, should only be used in very special cases, such as initial set-up or importing a lot a data;\r\n4, multiple_script: \r\n\ta combined script that contains more than one kinds of sql, should only be used when the content in the script is for a single batch of functionalities;\r\n5, structure: \r\n\ttables, triggers, types, sequences, grants;\r\n6, function: \r\n\tincluding trigger functions;\r\n7, configuration: \r\n\tlike system_config, bin, slot_type;\r\n8, basic_data: \r\n\tlike location, pallets;\r\n9, operational_data: \r\n\tlike item, cim, message, .etc.')
    update_content = db.Column(db.String(2000), info='detailed content listed out in this update')
    file_name = db.Column(db.String(200), unique=True, info='\r\nname of the database backup or script file; \r\nthese files must be stored systematically under a specified folder of the developer;\r\nnaming rule is:\r\n1, database_STAR-B1.2-V3.2.0.0_Socal develop base.backup\r\n2, DBscript_STAR-B1.2.1-V3.2.5.2_update pallet type.sql\r\n3, DBscript_STAR-B1-V3.3.0.0_cart interface change.sql\r\nthe database/DBscript and the trunk-branch-version_no should always be followed, the last part can be self-defined words;\r\nthe branch number should be at the level that this update can be applied to:\r\neg.\r\n"DBscript_STAR-B1.2.1-V3.2.5.2_update pallet type.sql" means it can only be applied to branch 1.2.1;\r\n"DBscript_STAR-B1-V3.3.0.0_cart interface change.sql" means it can be applied to branch 1 including its sub branch (1.1, 1.2, 1.3, 1.2.1, 1.2.2 .etc);\r\n.\r\n')
    created_user = db.Column(db.String(200), info='user name that created this version')
    created_timestamp = db.Column(db.DateTime(True), info='timestamp when this log was created')
    md5_hash = db.Column(db.String(200), info='a md5 hash value generated by the developer as an encrypted digital signature.')
    deploy_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='Record timestamp of deployment')
