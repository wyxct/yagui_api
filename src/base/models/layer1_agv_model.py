# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Agv(db.Model):
    __tablename__ = 'agv'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    agv_type_id = db.Column(db.ForeignKey('layer1_agv.agv_type.id'), nullable=False, info='the type of this AGV, foreign key of agv_type.id')
    agv_name = db.Column(db.String(20), nullable=False, unique=True, info='the name of AGV')
    mac_address = db.Column(db.MACADDR, unique=True, info='the MAC address of this AGV')
    ip_address = db.Column(db.INET, info='the IP address of this AGV')
    agv_shell_port = db.Column(db.Integer, info='the connection port of the AGV shell service')
    agv_control_port = db.Column(db.Integer, info='the connection port of the AGV control software service (such as motion_template)')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')
    agv_layout_id = db.Column(db.Integer, info='Map id of where the car is currently located')
    agv_simulation_flg = db.Column(db.Boolean, server_default=db.FetchedValue(), info='The flg of the simulated agv and the real agv')

    agv_type = db.relationship('AgvType', primaryjoin='Agv.agv_type_id == AgvType.id', backref='agvs')


class AgvLocate(Agv):
    __tablename__ = 'agv_locate'
    __table_args__ = {'schema': 'layer1_agv'}

    agv_id = db.Column(db.ForeignKey('layer1_agv.agv.id'), primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    locate_type = db.Column(db.Integer, info='1 for QR code locate, 2 for laser locate')
    single_reference_id = db.Column(db.Integer, info='reference id of locate method')
    multiple_reference_ids = db.Column(db.ARRAY(INTEGER()), info='reference ids of locate method')
    deviation_level = db.Column(db.Float(53), info='deviation level')
    deviation_x = db.Column(db.Float(53), info='deviation of X axis')
    deviation_y = db.Column(db.Float(53), info='deviation of Y axis')
    deviation_angle = db.Column(db.Float(53), info='deviation of angle')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when created this record')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')
    description = db.Column(db.String(200), info='the description of the loc_error')
    position_x = db.Column(db.Float(53), info='the position where happen.x')
    position_y = db.Column(db.Float(53), info='the position where happen.y')
    angle = db.Column(db.Float(53), info='the angle where happen')
    layout_edge_id = db.Column(db.Integer, info='the current layout edge that the AGV is at')
    edge_percentage = db.Column(db.Float(53), info='the accurate point that the AGV on the layout edge can be determined by this percentage (0-1)')
    pos_angle = db.Column(db.Float(53), info='the locate pose angle ')


class AgvMaintenance(Agv):
    __tablename__ = 'agv_maintenance'
    __table_args__ = {'schema': 'layer1_agv'}

    agv_id = db.Column(db.ForeignKey('layer1_agv.agv.id'), primary_key=True, info='foreign key of agv.id')
    battery_total_capacity = db.Column(db.Float(53), info='the total capacity of the AGV battery (unit: A·h)')
    battery_charge_cycle = db.Column(db.Integer, info='how many cycles that the AGV battery has been recharged')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when created this record')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')
    total_ideal_distime = db.Column(db.Float(53), info='the full battery charging time')
    lifecycle = db.Column(db.Float(53), info='statistical Week of battery discharge')
    capacity = db.Column(db.Float(53), info='TotalIdealDisTime*0.8 / Life Cycle')
    charge_count = db.Column(db.Integer, info='battery charge count')
    replace_time = db.Column(db.DateTime(True), info='battery replacement time')
    avedistime = db.Column(db.Float(53), info='average single ideal discharge time ')
    aveweight = db.Column(db.Float(53), info='average single discharge percentage ')


class AgvRealtimeDatum(Agv):
    __tablename__ = 'agv_realtime_data'
    __table_args__ = {'schema': 'layer1_agv'}

    agv_id = db.Column(db.ForeignKey('layer1_agv.agv.id'), primary_key=True, info='foreign key of agv.id')
    current_agv_command_id = db.Column(db.ForeignKey('layer1_agv.agv_command.id'), info='foreign key of agv_command.id, the command that the agv is currently executing')
    position_x = db.Column(db.Float(53), info='the realtime position of this AGV: the coordinate value in X axis')
    position_y = db.Column(db.Float(53), info='the realtime position of this AGV: the coordinate value in Y axis')
    angle = db.Column(db.Float(53), info='the realtime position of this AGV: the angle in the absolute coordinate system of the map')
    layout_edge_id = db.Column(db.Integer, info='foreign key of layout_edge.id, the current layout edge that the AGV is at')
    edge_percentage = db.Column(db.Float(53), info='the accurate point that the AGV on the layout edge can be determined by this percentage (0-1)')
    angle_of_attack = db.Column(db.Float(53), info='the relative angle between the AGV and the layout edge')
    battery_percentage = db.Column(db.Float(53), info='the percentage value indicates how much battery energy is left (0-1)')
    battery_voltage = db.Column(db.Float(53), info='the voltage of the battery (unit: V)')
    battery_capacity = db.Column(db.Float(53), info='the capacity of the battery (unit: A·h)')
    battery_current = db.Column(db.Float(53), info='the current of the battery (unit: A)')
    remaining_distance = db.Column(db.Float(53), info='the total length of the remaining segments')
    agv_customized_data_type_id = db.Column(db.ForeignKey('layer1_agv.agv_customized_data_type.id'), info='foreigh key of agv_customized_data_type.id')
    parameter_int4_1 = db.Column(db.Integer, info='the definition of parameter_int4_1')
    parameter_int4_2 = db.Column(db.Integer, info='the definition of parameter_int4_2')
    parameter_int4_3 = db.Column(db.Integer, info='the definition of parameter_int4_3')
    parameter_int8_1 = db.Column(db.BigInteger, info='the definition of parameter_int8_1')
    parameter_float8_1 = db.Column(db.Float(53), info='the definition of parameter_float8_1')
    parameter_float8_2 = db.Column(db.Float(53), info='the definition of parameter_float8_2')
    parameter_bool_1 = db.Column(db.Boolean, info='the definition of parameter_bool_1')
    parameter_bool_2 = db.Column(db.Boolean, info='the definition of parameter_bool_2')
    parameter_varchar200_1 = db.Column(db.String(200), info='the definition of parameter_varchar200_1')
    parameter_varchar200_2 = db.Column(db.String(200), info='the definition of parameter_varchar200_2')
    parameter_json_1 = db.Column(db.JSON, info='the definition of parameter_json_1 (JSON format should be preferred than text)')
    parameter_text_1 = db.Column(db.Text, info='the definition of parameter_text_1 (the number of characters is infinite)')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')
    parameter_timestamp_1 = db.Column(db.DateTime(True), info='followed command parameter, see definition in agv_command_type table')
    parameter_timestamp_2 = db.Column(db.DateTime(True), info='followed command parameter, see definition in agv_command_type table')
    network_delay = db.Column(db.Float(53), info='network delay of agv(unit:ms)')

    agv_customized_data_type = db.relationship('AgvCustomizedDataType', primaryjoin='AgvRealtimeDatum.agv_customized_data_type_id == AgvCustomizedDataType.id', backref='agv_realtime_data')
    current_agv_command = db.relationship('AgvCommand', primaryjoin='AgvRealtimeDatum.current_agv_command_id == AgvCommand.id', backref='agv_realtime_data')


class AgvState(Agv):
    __tablename__ = 'agv_state'
    __table_args__ = {'schema': 'layer1_agv'}

    agv_id = db.Column(db.ForeignKey('layer1_agv.agv.id'), primary_key=True, server_default=db.FetchedValue(), info='foreign key of agv.id')
    agv_management_status_id = db.Column(db.ForeignKey('layer1_agv.agv_management_status.id'), nullable=False, server_default=db.FetchedValue(), info='foreign key of agv_management_status.id')
    can_be_connected = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue(), info='indicates whether the AGV can be connected when its management status is "in system"')
    network_connected = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue(), info='indicates whether the AGV is well connected to the network when it is running')
    dispatch_task_active = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue(), info='indicates whether the AGV has active dispatch tasks that are being executed')
    fault_happened = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue(), info='indicates whether the AGV is in a fault')
    safety_information = db.Column(db.String(2000), info='the detailed information of safety events such as which sensors are triggered')
    is_blocked = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue(), info='indicates whether the AGV is blocked by another AGV or certain obstacles')
    blocked_by_agv_id = db.Column(db.ForeignKey('layer1_agv.agv.id'), info='foreign key of agv.id, the AGV that blocks this AGV')
    block_information = db.Column(db.String(2000), info='other detailed information of blocking')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')
    network_status = db.Column(db.Integer, info='network status, 0 for normal, 1 for abnormal')
    is_charging = db.Column(db.Boolean, info='true for charging, false for discharge')
    safety_triggered = db.Column(db.Integer, info='0 for safety not triggered, 1 for safety triggered, 2 for slow down')
    traffic_status = db.Column(db.Integer, info='0 for unblocked, 1 for blocked')
    safety_enabled = db.Column(db.Boolean, info='if the safety protection enabled')
    bank_id = db.Column(db.String(2000), info='the area number when safety enabled')
    start_soc = db.Column(db.Boolean, server_default=db.FetchedValue(), info='if the agv need SOC charge')
    end_soc = db.Column(db.Boolean, server_default=db.FetchedValue(), info='if the agv need end SOC charge')

    agv_management_status = db.relationship('AgvManagementStatu', primaryjoin='AgvState.agv_management_status_id == AgvManagementStatu.id', backref='agv_states')
    blocked_by_agv = db.relationship('Agv', primaryjoin='AgvState.blocked_by_agv_id == Agv.id', backref='agv_states')


class AgvTaskDutyCycle(Agv):
    __tablename__ = 'agv_task_duty_cycle'
    __table_args__ = {'schema': 'layer1_agv'}

    agv_id = db.Column(db.ForeignKey('layer1_agv.agv.id'), primary_key=True, info='foreign key of agv_id')
    busy_time = db.Column(db.Float(53), info='the accumulate time  when agv has task  today,unit :s')
    dispatch_time = db.Column(db.Float(53), info='the accumulate time  when agv managestatus >= inDispatch today,unit :s')
    charge_time = db.Column(db.Float(53), info='the accumulate time  when agv has charge task(chargeon+charging+chargeoff) today,unit :s ')
    block_time = db.Column(db.Float(53), info='the accumulate time  when is_block is true  today,unit :s ')
    average_execute_time = db.Column(db.Float(53), info='average execute time per task')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), info='the timestamp  that updated this record most recently')
    last_updated_user = db.Column(db.String(200), info='the user name that last update this record')
    last_updated_timestamp = db.Column(db.DateTime(True), info='the timestamp when updated this record most recently')


class AgvTrafficConfig(Agv):
    __tablename__ = 'agv_traffic_config'
    __table_args__ = {'schema': 'layer1_agv'}

    agv_id = db.Column(db.ForeignKey('layer1_agv.agv.id'), primary_key=True, info='internal id for identifying a record,FOREIGN KEY of agv.id')
    map_id = db.Column(db.ForeignKey('layer1_agv.map.id'), info='map_id FOREIGN KEY of map.id')
    max_length = db.Column(db.Float(53), info='max path lenght the agv can apply')
    k1 = db.Column(db.Float(53))
    k2 = db.Column(db.Float(53))
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')

    map = db.relationship('Map', primaryjoin='AgvTrafficConfig.map_id == Map.id', backref='agv_traffic_configs')



class AgvBlock(db.Model):
    __tablename__ = 'agv_block'
    __table_args__ = {'schema': 'layer1_agv'}

    agv_id = db.Column(db.Integer, primary_key=True)
    is_blocked = db.Column(db.Boolean)
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    blocked_by_agv = db.Column(db.Integer)
    position_x = db.Column(db.Float(53))
    position_y = db.Column(db.Float(53))
    angle = db.Column(db.Float(53))
    layout_edge_id = db.Column(db.Float(53))
    edge_percentage = db.Column(db.Float(53))



class AgvCommand(db.Model):
    __tablename__ = 'agv_command'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='the internal id to identify a record')
    agv_command_type_id = db.Column(db.ForeignKey('layer1_agv.agv_command_type.id'), nullable=False, index=True, info='foreign key of agv_command_type.id')
    agv_command_status_id = db.Column(db.ForeignKey('layer1_agv.agv_command_status.id'), nullable=False, index=True, server_default=db.FetchedValue(), info='foreign key of agv_command_status.id')
    agv_command_error_detail = db.Column(db.String(2000), info='if the command encounters an error, this field will tell the detailed reason')
    priority = db.Column(db.Float(53), info='the priority of the commands, higher-priority commands go first')
    request_finish_time = db.Column(db.DateTime(True), info='the time that the dispatch logics request the AGV to finish this command')
    predicted_finish_time = db.Column(db.DateTime(True), info='the time that the dispatch engine predicts to finish this command')
    agv_id = db.Column(db.ForeignKey('layer1_agv.agv.id'), index=True, info='foreign key of agv.id')
    parameter_int4_1 = db.Column(db.Integer, info='followed command parameter, see definition in agv_command_type table')
    parameter_int4_2 = db.Column(db.Integer, info='followed command parameter, see definition in agv_command_type table')
    parameter_int4_3 = db.Column(db.Integer, info='followed command parameter, see definition in agv_command_type table')
    parameter_int4_4 = db.Column(db.Integer, info='followed command parameter, see definition in agv_command_type table')
    parameter_int4_5 = db.Column(db.Integer, info='followed command parameter, see definition in agv_command_type table')
    parameter_int4_6 = db.Column(db.Integer, info='followed command parameter, see definition in agv_command_type table')
    parameter_int8_1 = db.Column(db.BigInteger, info='followed command parameter, see definition in agv_command_type table')
    parameter_int8_2 = db.Column(db.BigInteger, info='followed command parameter, see definition in agv_command_type table')
    parameter_float8_1 = db.Column(db.Float(53), info='followed command parameter, see definition in agv_command_type table')
    parameter_float8_2 = db.Column(db.Float(53), info='followed command parameter, see definition in agv_command_type table')
    parameter_float8_3 = db.Column(db.Float(53), info='followed command parameter, see definition in agv_command_type table')
    parameter_float8_4 = db.Column(db.Float(53), info='followed command parameter, see definition in agv_command_type table')
    parameter_bool_1 = db.Column(db.Boolean, info='followed command parameter, see definition in agv_command_type table')
    parameter_bool_2 = db.Column(db.Boolean, info='followed command parameter, see definition in agv_command_type table')
    parameter_bool_3 = db.Column(db.Boolean, info='followed command parameter, see definition in agv_command_type table')
    parameter_bool_4 = db.Column(db.Boolean, info='followed command parameter, see definition in agv_command_type table')
    parameter_varchar200_1 = db.Column(db.String(200), info='followed command parameter, see definition in agv_command_type table')
    parameter_varchar200_2 = db.Column(db.String(200), info='followed command parameter, see definition in agv_command_type table')
    parameter_varchar200_3 = db.Column(db.String(200), info='followed command parameter, see definition in agv_command_type table')
    parameter_varchar200_4 = db.Column(db.String(200), info='followed command parameter, see definition in agv_command_type table')
    parameter_timestamp_1 = db.Column(db.DateTime(True), info='followed command parameter, see definition in agv_command_type table')
    parameter_timestamp_2 = db.Column(db.DateTime(True), info='followed command parameter, see definition in agv_command_type table')
    parameter_json_1 = db.Column(db.JSON, info='followed command parameter, see definition in agv_command_type table')
    parameter_text_1 = db.Column(db.Text, info='followed command parameter, see definition in agv_command_type table')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when created this record')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')
    obsolete_flag = db.Column(db.Boolean, server_default=db.FetchedValue(), info='if true, this record should be deleted or transloged')

    agv_command_status = db.relationship('AgvCommandStatu', primaryjoin='AgvCommand.agv_command_status_id == AgvCommandStatu.id', backref='agv_commands')
    agv_command_type = db.relationship('AgvCommandType', primaryjoin='AgvCommand.agv_command_type_id == AgvCommandType.id', backref='agv_commands')
    agv = db.relationship('Agv', primaryjoin='AgvCommand.agv_id == Agv.id', backref='agv_commands')



class AgvCommandLog(db.Model):
    __tablename__ = 'agv_command_log'
    __table_args__ = {'schema': 'layer1_agv'}

    log_id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='the internal id to identify a record')
    log_type = db.Column(db.String(200), server_default=db.FetchedValue(), info='INSERT.NEW/UPDATED.OLD/UPDATED.NEW/DELETED.OLD/TRUNCATED.OLD')
    id = db.Column(db.BigInteger, nullable=False, info='the internal id to identify a record')
    agv_command_type_id = db.Column(db.Integer, nullable=False, info='foreign key of agv_command_type.id')
    agv_command_status_id = db.Column(db.Integer, nullable=False, info='foreign key of agv_command_status.id')
    agv_command_error_detail = db.Column(db.String(2000), info='if the command encounters an error, this field will tell the detailed reason')
    priority = db.Column(db.Float(53), info='the priority of the commands, higher-priority commands go first')
    request_finish_time = db.Column(db.DateTime(True), info='the time that the dispatch logics request the AGV to finish this command')
    predicted_finish_time = db.Column(db.DateTime(True), info='the time that the dispatch engine predicts to finish this command')
    agv_id = db.Column(db.Integer, info='foreign key of agv.id')
    parameter_int4_1 = db.Column(db.Integer, info='followed command parameter, see definition in agv_command_type table')
    parameter_int4_2 = db.Column(db.Integer, info='followed command parameter, see definition in agv_command_type table')
    parameter_int4_3 = db.Column(db.Integer, info='followed command parameter, see definition in agv_command_type table')
    parameter_int4_4 = db.Column(db.Integer, info='followed command parameter, see definition in agv_command_type table')
    parameter_int4_5 = db.Column(db.Integer, info='followed command parameter, see definition in agv_command_type table')
    parameter_int4_6 = db.Column(db.Integer, info='followed command parameter, see definition in agv_command_type table')
    parameter_int8_1 = db.Column(db.BigInteger, info='followed command parameter, see definition in agv_command_type table')
    parameter_int8_2 = db.Column(db.BigInteger, info='followed command parameter, see definition in agv_command_type table')
    parameter_float8_1 = db.Column(db.Float(53), info='followed command parameter, see definition in agv_command_type table')
    parameter_float8_2 = db.Column(db.Float(53), info='followed command parameter, see definition in agv_command_type table')
    parameter_float8_3 = db.Column(db.Float(53), info='followed command parameter, see definition in agv_command_type table')
    parameter_float8_4 = db.Column(db.Float(53), info='followed command parameter, see definition in agv_command_type table')
    parameter_bool_1 = db.Column(db.Boolean, info='followed command parameter, see definition in agv_command_type table')
    parameter_bool_2 = db.Column(db.Boolean, info='followed command parameter, see definition in agv_command_type table')
    parameter_bool_3 = db.Column(db.Boolean, info='followed command parameter, see definition in agv_command_type table')
    parameter_bool_4 = db.Column(db.Boolean, info='followed command parameter, see definition in agv_command_type table')
    parameter_varchar200_1 = db.Column(db.String(200), info='followed command parameter, see definition in agv_command_type table')
    parameter_varchar200_2 = db.Column(db.String(200), info='followed command parameter, see definition in agv_command_type table')
    parameter_varchar200_3 = db.Column(db.String(200), info='followed command parameter, see definition in agv_command_type table')
    parameter_varchar200_4 = db.Column(db.String(200), info='followed command parameter, see definition in agv_command_type table')
    parameter_timestamp_1 = db.Column(db.DateTime(True), info='followed command parameter, see definition in agv_command_type table')
    parameter_timestamp_2 = db.Column(db.DateTime(True), info='followed command parameter, see definition in agv_command_type table')
    parameter_json_1 = db.Column(db.JSON, info='followed command parameter, see definition in agv_command_type table')
    parameter_text_1 = db.Column(db.Text, info='followed command parameter, see definition in agv_command_type table')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), info='the timestamp when created this record')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently')
    last_updated_timestamp = db.Column(db.DateTime(True), info='the timestamp when updated this record most recently')
    log_created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when this log record was created')



class AgvCommandStatu(db.Model):
    __tablename__ = 'agv_command_status'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    name = db.Column(db.String(200), nullable=False, unique=True, server_default=db.FetchedValue(), info='the name of this command status, such as "waiting","cached", "in progress", "complete", "error"...')
    description = db.Column(db.String(2000), info='the descriptive information of this AGV command status')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')



class AgvCommandType(db.Model):
    __tablename__ = 'agv_command_type'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    name = db.Column(db.String(200), nullable=False, unique=True, info='the name of this command type, should be brief and clear')
    category = db.Column(db.String(200), info='to classify the command type, such as "vehicle management", "vehicle control", "dispatch task", "layout management"...')
    description = db.Column(db.String(2000), info='the detailed description and definition of this command type')
    valid_parameter_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='how many parameters will be followed with this command type')
    parameter_definition_int4_1 = db.Column(db.String(2000), info='the definition of parameter_int4_1')
    parameter_definition_int4_2 = db.Column(db.String(2000), info='the definition of parameter_int4_2')
    parameter_definition_int4_3 = db.Column(db.String(2000), info='the definition of parameter_int4_3')
    parameter_definition_int4_4 = db.Column(db.String(2000), info='the definition of parameter_int4_4')
    parameter_definition_int4_5 = db.Column(db.String(2000), info='the definition of parameter_int4_5')
    parameter_definition_int4_6 = db.Column(db.String(2000), info='the definition of parameter_int4_6')
    parameter_definition_int8_1 = db.Column(db.String(2000), info='the definition of parameter_int8_1')
    parameter_definition_int8_2 = db.Column(db.String(2000), info='the definition of parameter_int8_2')
    parameter_definition_float8_1 = db.Column(db.String(2000), info='the definition of parameter_float8_1')
    parameter_definition_float8_2 = db.Column(db.String(2000), info='the definition of parameter_float8_2')
    parameter_definition_float8_3 = db.Column(db.String(2000), info='the definition of parameter_float8_3')
    parameter_definition_float8_4 = db.Column(db.String(2000), info='the definition of parameter_float8_4')
    parameter_definition_bool_1 = db.Column(db.String(2000), info='the definition of parameter_bool_1')
    parameter_definition_bool_2 = db.Column(db.String(2000), info='the definition of parameter_bool_2')
    parameter_definition_bool_3 = db.Column(db.String(2000), info='the definition of parameter_bool_3')
    parameter_definition_bool_4 = db.Column(db.String(2000), info='the definition of parameter_bool_4')
    parameter_definition_varchar200_1 = db.Column(db.String(2000), info='the definition of parameter_varchar200_1')
    parameter_definition_varchar200_2 = db.Column(db.String(2000), info='the definition of parameter_varchar200_2')
    parameter_definition_varchar200_3 = db.Column(db.String(2000), info='the definition of parameter_varchar200_3')
    parameter_definition_varchar200_4 = db.Column(db.String(2000), info='the definition of parameter_varchar200_4')
    parameter_definition_timestamp_1 = db.Column(db.String(2000), info='the definition of parameter_timestamp_1')
    parameter_definition_timestamp_2 = db.Column(db.String(2000), info='the definition of parameter_timestamp_2')
    parameter_definition_json_1 = db.Column(db.String(2000), info='the definition of parameter_json_1 (JSON format should be preferred than text)')
    parameter_definition_text_1 = db.Column(db.String(2000), info='the definition of parameter_text_1 (the number of characters is infinite)')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')



class AgvCustomizedDataType(db.Model):
    __tablename__ = 'agv_customized_data_type'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    name = db.Column(db.String(200), nullable=False, info='the name of this customized data type, should be brief and clear')
    description = db.Column(db.String(2000), info='the detailed description and definition of this customized data type')
    valid_parameter_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='how many parameters will be followed with this customized data type')
    parameter_definition_int4_1 = db.Column(db.String(2000), info='the parameter_definition_int4_1')
    parameter_definition_int4_2 = db.Column(db.String(2000), info='the parameter_definition_int4_2')
    parameter_definition_int4_3 = db.Column(db.String(2000), info='the parameter_definition_int4_3')
    parameter_definition_int8_1 = db.Column(db.String(2000), info='the parameter_definition_int8_1')
    parameter_definition_float8_1 = db.Column(db.String(2000), info='the parameter_definition_float8_1')
    parameter_definition_float8_2 = db.Column(db.String(2000), info='the parameter_definition_float8_2')
    parameter_definition_bool_1 = db.Column(db.String(2000), info='the parameter_definition_bool_1')
    parameter_definition_bool_2 = db.Column(db.String(2000), info='the parameter_definition_bool_2')
    parameter_definition_varchar200_1 = db.Column(db.String(2000), info='the parameter_definition_varchar200_1')
    parameter_definition_varchar200_2 = db.Column(db.String(2000), info='the parameter_definition_varchar200_2')
    parameter_definition_json_1 = db.Column(db.String(2000), info='the definition of parameter_json_1 (JSON format should be preferred than text)')
    parameter_definition_text_1 = db.Column(db.String(2000), info='the definition of parameter_text_1 (the number of characters is infinite)')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')



class AgvError(db.Model):
    __tablename__ = 'agv_error'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='the internal id to identify a record')
    agv_id = db.Column(db.ForeignKey('layer1_agv.agv.id'), info='foreign key of agv.id')
    agv_error_type_id = db.Column(db.ForeignKey('layer1_agv.agv_error_type.id'), info='foreign key of agv_error_type.id')
    error_information = db.Column(db.String(2000), info='extra detailed information of this error')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when created this record')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')
    error_occured_timestamp = db.Column(db.DateTime(True), info='when the error occured')
    error_last_updated_timestamp = db.Column(db.DateTime(True), info='when the error last updated')
    claimer = db.Column(db.String(200), info='who claim this error')

    agv_error_type = db.relationship('AgvErrorType', primaryjoin='AgvError.agv_error_type_id == AgvErrorType.id', backref='agv_errors')
    agv = db.relationship('Agv', primaryjoin='AgvError.agv_id == Agv.id', backref='agv_errors')



class AgvErrorCatagory(db.Model):
    __tablename__ = 'agv_error_catagory'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    name = db.Column(db.String(200), nullable=False, unique=True, info='the name of this AGV error catagory, such as "navigation error", "camera error", "charge error"...')
    description = db.Column(db.String(2000), info='the descriptive information of this AGV error catagory')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')



class AgvErrorLog(db.Model):
    __tablename__ = 'agv_error_log'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='the internal id to identify a record')
    log_type = db.Column(db.String(200), server_default=db.FetchedValue(), info='INSERT.NEW/UPDATED.OLD/UPDATED.NEW/DELETED.OLD/TRUNCATED.OLD')
    agv_id = db.Column(db.Integer, info='foreign key of agv.id')
    agv_error_type_id = db.Column(db.Integer, info='foreign key of agv_error_type.id')
    error_information = db.Column(db.String(2000), info='extra detailed information of this error')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), info='the timestamp when created this record')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently')
    last_updated_timestamp = db.Column(db.DateTime(True), info='the timestamp when updated this record most recently')
    log_created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when this log record was created')
    error_occured_timestamp = db.Column(db.DateTime(True), info='when the error occured')
    error_last_updated_timestamp = db.Column(db.DateTime(True), info='when the error last updated')



class AgvErrorSolution(db.Model):
    __tablename__ = 'agv_error_solution'
    __table_args__ = (
        db.UniqueConstraint('language', 'name'),
        {'schema': 'layer1_agv'}
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    language = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(2000))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class AgvErrorSolutionRelation(db.Model):
    __tablename__ = 'agv_error_solution_relation'
    __table_args__ = (
        db.UniqueConstraint('agv_error_type_id', 'agv_error_solution_id'),
        {'schema': 'layer1_agv'}
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    agv_error_type_id = db.Column(db.ForeignKey('layer1_agv.agv_error_type.id'))
    agv_error_solution_id = db.Column(db.ForeignKey('layer1_agv.agv_error_solution.id'))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())

    agv_error_solution = db.relationship('AgvErrorSolution', primaryjoin='AgvErrorSolutionRelation.agv_error_solution_id == AgvErrorSolution.id', backref='agv_error_solution_relations')
    agv_error_type = db.relationship('AgvErrorType', primaryjoin='AgvErrorSolutionRelation.agv_error_type_id == AgvErrorType.id', backref='agv_error_solution_relations')



class AgvErrorType(db.Model):
    __tablename__ = 'agv_error_type'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    name = db.Column(db.String(200), nullable=False, info='the name of this AGV error type, such as "navigation error", "camera error", "charge error"...')
    description = db.Column(db.String(2000), info='the descriptive information of this AGV error type')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')
    error_code = db.Column(db.Integer, info='the detail error code number')
    error_catagory_id = db.Column(db.ForeignKey('layer1_agv.agv_error_catagory.id'), info='the error type catagory')
    agv_type_id = db.Column(db.ForeignKey('layer1_agv.agv_type.id'), info='the type of agv')

    agv_type = db.relationship('AgvType', primaryjoin='AgvErrorType.agv_type_id == AgvType.id', backref='agv_error_types')
    error_catagory = db.relationship('AgvErrorCatagory', primaryjoin='AgvErrorType.error_catagory_id == AgvErrorCatagory.id', backref='agv_error_types')



class AgvLocateLog(db.Model):
    __tablename__ = 'agv_locate_log'
    __table_args__ = {'schema': 'layer1_agv'}

    log_id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    agv_id = db.Column(db.Integer, index=True, info='agv id')
    locate_type = db.Column(db.Integer, index=True, info='1 for QR code locate, 2 for laser locate')
    record_timestamp = db.Column(db.DateTime(True), index=True)
    single_reference_id = db.Column(db.Integer, index=True, info='reference id of locate method')
    multiple_reference_ids = db.Column(db.ARRAY(INTEGER()), info='reference ids of locate method')
    reference_quality = db.Column(db.Float(53), info='0-100')
    deviation_level = db.Column(db.Float(53), info='deviation level,0--rank0, 1--rank1 , 2---rank2')
    deviation_x = db.Column(db.Float(53), info='deviation of X axis')
    deviation_y = db.Column(db.Float(53), info='deviation of Y axis')
    deviation_angle = db.Column(db.Float(53), info='deviation of angle')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), info='the timestamp when created this record')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently')
    last_updated_timestamp = db.Column(db.DateTime(True), info='the timestamp when updated this record most recently')
    log_created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when this log record was created')
    description = db.Column(db.String(200), info='the description of the loc_error')
    pos_x = db.Column(db.Float(53), info='the position where happen.x')
    pos_y = db.Column(db.Float(53), info='the position where happen.y')
    pos_angle = db.Column(db.Float(53), info='the angle where happen')
    layout_edge_id = db.Column(db.Integer, info='the current layout edge that the AGV is at')
    edge_percentage = db.Column(db.Float(53), info='the accurate point that the AGV on the layout edge can be determined by this percentage (0-1)')
    reference_angle = db.Column(db.Float(53), info='the reference posture angle ')
    locate_state = db.Column(db.Float(53), info=' 0--Normal 、1--Guess、2--Leak')



class AgvLogicState(db.Model):
    __tablename__ = 'agv_logic_state'
    __table_args__ = {'schema': 'layer1_agv'}

    agv_id = db.Column(db.Integer, primary_key=True, index=True)
    state = db.Column(db.String(200))
    state_change_time = db.Column(db.DateTime(True))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class AgvMaintenanceLog(db.Model):
    __tablename__ = 'agv_maintenance_log'
    __table_args__ = {'schema': 'layer1_agv'}

    log_id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    log_type = db.Column(db.String(200), info='INSERT.NEW/UPDATED.OLD/UPDATED.NEW/DELETED.OLD/TRUNCATED.OLD')
    agv_id = db.Column(db.Integer, nullable=False, info='agv.id')
    battery_total_capacity = db.Column(db.Float(53), info='the total capacity of the AGV battery (unit: A·h)')
    battery_charge_cycle = db.Column(db.Integer, info='how many cycles that the AGV battery has been recharged')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), info='the timestamp when created this record')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently')
    last_updated_timestamp = db.Column(db.DateTime(True), info='the timestamp when updated this record most recently')
    log_created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    total_ideal_distime = db.Column(db.Float(53), info='the full battery charging time')
    lifecycle = db.Column(db.Float(53), info='statistical Week of battery discharge')
    capacity = db.Column(db.Float(53), info='TotalIdealDisTime*0.8 / Life Cycle')
    charge_count = db.Column(db.Integer, info='battery charge count')
    replace_time = db.Column(db.DateTime(True), info='battery replacement time')
    avedistime = db.Column(db.Float(53), info='average single ideal discharge time ')
    aveweight = db.Column(db.Float(53), info='average single discharge percentage ')



class AgvManagementStatu(db.Model):
    __tablename__ = 'agv_management_status'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    name = db.Column(db.String(200), nullable=False, unique=True, info='the name of this AGV type, such as "Picking AGV", "Cart AGV", "Order AGV"...')
    description = db.Column(db.String(2000), info='the descriptive information of this AGV type')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')



class AgvRealtimeDataLog(db.Model):
    __tablename__ = 'agv_realtime_data_log'
    __table_args__ = {'schema': 'layer1_agv'}

    log_id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='the internal id to identify a record')
    log_type = db.Column(db.String(200), server_default=db.FetchedValue(), info='INSERT.NEW/UPDATED.OLD/UPDATED.NEW/DELETED.OLD/TRUNCATED.OLD')
    agv_id = db.Column(db.Integer, index=True, info='foreign key of agv.id')
    current_agv_command_id = db.Column(db.BigInteger, info='foreign key of agv_command.id, the command that the agv is currently executing')
    position_x = db.Column(db.Float(53), index=True, info='the realtime position of this AGV: the coordinate value in X axis')
    position_y = db.Column(db.Float(53), index=True, info='the realtime position of this AGV: the coordinate value in Y axis')
    angle = db.Column(db.Float(53), index=True, info='the realtime position of this AGV: the angle in the absolute coordinate system of the map')
    layout_edge_id = db.Column(db.Integer, index=True, info='foreign key of layout_edge.id, the current layout edge that the AGV is at')
    edge_percentage = db.Column(db.Float(53), index=True, info='the accurate point that the AGV on the layout edge can be determined by this percentage (0-1)')
    angle_of_attack = db.Column(db.Float(53), info='the relative angle between the AGV and the layout edge')
    battery_percentage = db.Column(db.Float(53), info='the percentage value indicates how much battery energy is left (0-1)')
    battery_voltage = db.Column(db.Float(53), info='the voltage of the battery (unit: V)')
    battery_capacity = db.Column(db.Float(53), info='the capacity of the battery (unit: A·h)')
    battery_current = db.Column(db.Float(53), info='the current of the battery (unit: A)')
    remaining_distance = db.Column(db.Float(53), info='the total length of the remaining segments')
    agv_customized_data_type_id = db.Column(db.Integer, info='foreigh key of agv_customized_data_type.id')
    parameter_int4_1 = db.Column(db.Integer, info='the definition of parameter_int4_1')
    parameter_int4_2 = db.Column(db.Integer, info='the definition of parameter_int4_2')
    parameter_int4_3 = db.Column(db.Integer, info='the definition of parameter_int4_3')
    parameter_int8_1 = db.Column(db.BigInteger, info='the definition of parameter_int8_1')
    parameter_float8_1 = db.Column(db.Float(53), info='the definition of parameter_float8_1')
    parameter_float8_2 = db.Column(db.Float(53), info='the definition of parameter_float8_2')
    parameter_bool_1 = db.Column(db.Boolean, info='the definition of parameter_bool_1')
    parameter_bool_2 = db.Column(db.Boolean, info='the definition of parameter_bool_2')
    parameter_varchar200_1 = db.Column(db.String(200), info='the definition of parameter_varchar200_1')
    parameter_varchar200_2 = db.Column(db.String(200), info='the definition of parameter_varchar200_2')
    parameter_json_1 = db.Column(db.JSON, info='the definition of parameter_json_1 (JSON format should be preferred than text)')
    parameter_text_1 = db.Column(db.Text, info='the definition of parameter_text_1 (the number of characters is infinite)')
    last_updated_timestamp = db.Column(db.DateTime(True), info='the timestamp when updated this record most recently')
    log_created_timestamp = db.Column(db.DateTime(True), index=True, server_default=db.FetchedValue(), info='the timestamp when this log record was created')
    parameter_timestamp_1 = db.Column(db.DateTime(True), info='followed command parameter, see definition in agv_command_type table')
    parameter_timestamp_2 = db.Column(db.DateTime(True), info='followed command parameter, see definition in agv_command_type table')
    network_delay = db.Column(db.Float(53), info='network delay of agv(unit:ms)')



class AgvStateLog(db.Model):
    __tablename__ = 'agv_state_log'
    __table_args__ = {'schema': 'layer1_agv'}

    log_id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='the internal id to identify a record')
    log_type = db.Column(db.String(200), server_default=db.FetchedValue(), info='INSERT.NEW/UPDATED.OLD/UPDATED.NEW/DELETED.OLD/TRUNCATED.OLD')
    agv_id = db.Column(db.Integer, info='foreign key of agv.id')
    agv_management_status_id = db.Column(db.Integer, info='foreign key of agv_management_status.id')
    can_be_connected = db.Column(db.Boolean, info='indicates whether the AGV can be connected when its management status is "in system"')
    network_connected = db.Column(db.Boolean, info="indicates whether the AGV is well connected to the network when it's running")
    dispatch_task_active = db.Column(db.Boolean, info='indicates whether the AGV has active dispatch tasks that are being executed')
    fault_happened = db.Column(db.Boolean, info='indicates whether the AGV is in a fault')
    safety_information = db.Column(db.String(2000), info='the detailed information of safety events such as which sensors are triggered')
    is_blocked = db.Column(db.Boolean, info='indicates whether the AGV is blocked by another AGV or certain obstacles')
    blocked_by_agv_id = db.Column(db.Integer, info='foreign key of agv.id, the AGV that blocks this AGV')
    block_information = db.Column(db.String(2000), info='other detailed information of blocking')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), info='the timestamp when created this record')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently')
    last_updated_timestamp = db.Column(db.DateTime(True), info='the timestamp when updated this record most recently')
    log_created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when this log record was created')
    network_status = db.Column(db.Integer, info='network status, 0 for normal, 1 for abnormal')
    is_charging = db.Column(db.Boolean, info='true for charging, false for discharge')
    safety_triggered = db.Column(db.Integer, info='0 for safety not triggered, 1 for safety triggered, 2 for slow down')
    traffic_status = db.Column(db.Integer, info='0 for unblocked, 1 for blocked')
    safety_enabled = db.Column(db.Boolean, info='if the safety protection enabled')
    bank_id = db.Column(db.String(2000), info='the area number when safety enabled')



class AgvType(db.Model):
    __tablename__ = 'agv_type'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    name = db.Column(db.String(200), nullable=False, unique=True, info='the name of this AGV type, such as "Picking AGV", "Cart AGV", "Order AGV"...')
    description = db.Column(db.String(2000), info='the descriptive information of this AGV type')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')
    agv_use_type_id = db.Column(db.ForeignKey('layer1_agv.agv_use_type.id'), info='FK to the agv_use_type.id; agv_use_type represents the type from user view regardless of the uderlying small difference.')
    capacity = db.Column(db.Integer, server_default=db.FetchedValue(), info='declare how many agv location the agv has')

    agv_use_type = db.relationship('AgvUseType', primaryjoin='AgvType.agv_use_type_id == AgvUseType.id', backref='agv_types')



class AgvUseType(db.Model):
    __tablename__ = 'agv_use_type'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    name = db.Column(db.String(200), nullable=False, unique=True, info='the name of this AGV type from user view regardless of the small hardware difference')
    description = db.Column(db.String(2000), info='the descriptive information of this AGV use type')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')
    agv_use_type_category_id = db.Column(db.ForeignKey('layer1_agv.agv_use_type_category.id'))

    agv_use_type_category = db.relationship('AgvUseTypeCategory', primaryjoin='AgvUseType.agv_use_type_category_id == AgvUseTypeCategory.id', backref='agv_use_types')



class AgvUseTypeCategory(db.Model):
    __tablename__ = 'agv_use_type_category'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.String(2000))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class DeviceConfig(db.Model):
    __tablename__ = 'device_config'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='fk io.id ')
    ip_address = db.Column(db.String(200), info='the ip of this device')
    port = db.Column(db.Integer, info='the port of this device')
    device_name = db.Column(db.String(200), info='the name of this device')
    device_id = db.Column(db.Integer, unique=True, info='the id of this device')
    device_type_id = db.Column(db.Integer, info='the type of this device')
    heartbeat_address = db.Column(db.Integer)
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')



class DeviceIoRelation(db.Model):
    __tablename__ = 'device_io_relation'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    relation_type_id = db.Column(db.Integer, nullable=False)
    io_id = db.Column(db.ForeignKey('layer1_agv.io.id'), nullable=False, index=True)
    io_value = db.Column(db.ForeignKey('layer1_agv.io_status_type.id'), nullable=False, index=True)
    device_iddress = db.Column(db.String(200))
    device_value = db.Column(db.Integer)
    write_io_id = db.Column(db.ForeignKey('layer1_agv.io.id'), index=True)
    write_io_value = db.Column(db.ForeignKey('layer1_agv.io_status_type.id'), index=True)
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    request_addr1 = db.Column(db.String)
    request_addr2 = db.Column(db.String)
    request_value = db.Column(db.String)
    response_value = db.Column(db.String)

    io = db.relationship('Io', primaryjoin='DeviceIoRelation.io_id == Io.id', backref='io_device_io_relations')
    io_status_type = db.relationship('IoStatusType', primaryjoin='DeviceIoRelation.io_value == IoStatusType.id', backref='iostatustype_device_io_relations')
    write_io = db.relationship('Io', primaryjoin='DeviceIoRelation.write_io_id == Io.id', backref='io_device_io_relations_0')
    io_status_type1 = db.relationship('IoStatusType', primaryjoin='DeviceIoRelation.write_io_value == IoStatusType.id', backref='iostatustype_device_io_relations_0')



class Io(db.Model):
    __tablename__ = 'io'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    name = db.Column(db.String(200), nullable=False, info='the name of this io type, should be brief and clear')
    io_type_id = db.Column(db.ForeignKey('layer1_agv.io_type.id'), info='internal id for identifying a record')
    description = db.Column(db.String(2000), info='the detailed description and definition of this io type')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')
    device_id = db.Column(db.ForeignKey('layer1_agv.device_config.id'))

    device = db.relationship('DeviceConfig', primaryjoin='Io.device_id == DeviceConfig.id', backref='ios')
    io_type = db.relationship('IoType', primaryjoin='Io.io_type_id == IoType.id', backref='ios')


class IoState(Io):
    __tablename__ = 'io_state'
    __table_args__ = {'schema': 'layer1_agv'}

    io_id = db.Column(db.ForeignKey('layer1_agv.io.id'), primary_key=True, server_default=db.FetchedValue(), info='fk io.id ')
    io_status_id = db.Column(db.ForeignKey('layer1_agv.io_status_type.id'), info='the status of this io')
    io_value_int4_1 = db.Column(db.Integer, info='the value of the io')
    io_value_int4_2 = db.Column(db.Integer, info='the value of the io')
    io_value_int4_3 = db.Column(db.Integer, info='the value of the io')
    io_value_int4_4 = db.Column(db.Integer, info='the value of the io')
    io_value_json = db.Column(db.JSON, info='the json value of the io')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')

    io_status = db.relationship('IoStatusType', primaryjoin='IoState.io_status_id == IoStatusType.id', backref='io_states')



class IoCommand(db.Model):
    __tablename__ = 'io_command'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    io_command_type_id = db.Column(db.ForeignKey('layer1_agv.io_command_type.id'), info='the name of this io type, should be brief and clear')
    io_id = db.Column(db.Integer, info='to classify the io type')
    io_status_id = db.Column(db.ForeignKey('layer1_agv.io_status_type.id'), info='to classify the io type')
    io_value_int4_1 = db.Column(db.Integer, info='description of io_command.io_value_int4_1')
    io_value_int4_2 = db.Column(db.Integer, info='description of io_command.io_value_int4_2')
    io_value_int4_3 = db.Column(db.Integer, info='description of io_command.io_value_int4_3')
    io_value_int4_4 = db.Column(db.Integer, info='description of io_command.io_value_int4_4')
    io_value_json = db.Column(db.JSON, info='description of io_command.io_value_json')
    notify_io_manager_flag = db.Column(db.Boolean, server_default=db.FetchedValue(), info='description of io_command.io_value_int4_2')
    obsolete_flag = db.Column(db.Boolean, server_default=db.FetchedValue(), info='description of io_command.io_value_int4_3')
    update_version_no = db.Column(db.Integer, info='description of io_command.io_value_int4_4')
    feedback_version_no = db.Column(db.Integer, info='description of io_command.io_value_json')
    description = db.Column(db.String(2000))
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')

    io_command_type = db.relationship('IoCommandType', primaryjoin='IoCommand.io_command_type_id == IoCommandType.id', backref='io_commands')
    io_status = db.relationship('IoStatusType', primaryjoin='IoCommand.io_status_id == IoStatusType.id', backref='io_commands')


class IoCommandExecutionDatum(IoCommand):
    __tablename__ = 'io_command_execution_data'
    __table_args__ = {'schema': 'layer1_agv'}

    io_command_id = db.Column(db.ForeignKey('layer1_agv.io_command.id'), primary_key=True, server_default=db.FetchedValue(), info='the name of this io type, should be brief and clear')
    io_command_status_id = db.Column(db.ForeignKey('layer1_agv.io_command_status.id'), info='to classify the io type')
    feedback_info = db.Column(db.JSON, info='description of io_command_execution_data.io_value_json')
    io_manager_note = db.Column(db.String(2000), info='description of io_command_execution_data.io_value_int4_4')
    notify_user_flag = db.Column(db.Boolean, server_default=db.FetchedValue(), info='description of io_command_execution_data.io_value_int4_2')
    obsolete_flag = db.Column(db.Boolean, server_default=db.FetchedValue(), info='description of io_command_execution_data.io_value_int4_3')
    update_version_no = db.Column(db.Integer, info='description of io_command_execution_data.io_value_int4_4')
    feedback_version_no = db.Column(db.Integer, info='description of io_command_execution_data.io_value_json')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')

    io_command_status = db.relationship('IoCommandStatu', primaryjoin='IoCommandExecutionDatum.io_command_status_id == IoCommandStatu.id', backref='io_command_execution_data')



class IoCommandStatu(db.Model):
    __tablename__ = 'io_command_status'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    name = db.Column(db.String(200), nullable=False, unique=True, info='the name of this io type, should be brief and clear')
    description = db.Column(db.String(2000), info='the detailed description and definition of this io type')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')



class IoCommandType(db.Model):
    __tablename__ = 'io_command_type'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    name = db.Column(db.String(200), nullable=False, unique=True, info='the name of this io type, should be brief and clear')
    category = db.Column(db.String(200), info='to classify the io type')
    parameter_definition_int4_1 = db.Column(db.String(2000), info='the definition of parameter_int4_1')
    parameter_definition_int4_2 = db.Column(db.String(2000), info='the definition of parameter_int4_2')
    parameter_definition_int4_3 = db.Column(db.String(2000), info='the definition of parameter_int4_3')
    parameter_definition_int4_4 = db.Column(db.String(2000), info='the definition of parameter_int4_4')
    parameter_definition_json = db.Column(db.String(2000), info='the definition of parameter_definition_json')
    description = db.Column(db.String(2000), info='the detailed description and definition of this io type')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')



class IoStatusType(db.Model):
    __tablename__ = 'io_status_type'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    name = db.Column(db.String(200), nullable=False, unique=True, info='the name of this io type, should be brief and clear')
    category = db.Column(db.String(200), info='to classify the io type')
    description = db.Column(db.String(2000), info='the detailed description and definition of this io type')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')



class IoType(db.Model):
    __tablename__ = 'io_type'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    name = db.Column(db.String(200), nullable=False, unique=True, info='the name of this io type, should be brief and clear')
    category = db.Column(db.String(200), info='to classify the io type')
    description = db.Column(db.String(2000), info='the detailed description and definition of this io type')
    parameter_definition_int4_1 = db.Column(db.String(2000), info='the definition of parameter_int4_1')
    parameter_definition_int4_2 = db.Column(db.String(2000), info='the definition of parameter_int4_2')
    parameter_definition_int4_3 = db.Column(db.String(2000), info='the definition of parameter_int4_3')
    parameter_definition_int4_4 = db.Column(db.String(2000), info='the definition of parameter_int4_4')
    parameter_definition_json = db.Column(db.String(2000), info='the definition of parameter_definition_json')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')



class MaintenanceAbnormalAgvLog(db.Model):
    __tablename__ = 'maintenance_abnormal_agv_log'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='the internal id to identify a record')
    agv_id = db.Column(db.Integer, info='the agv id')
    opt_id = db.Column(db.Integer, info='opt_id')
    fork_direction = db.Column(db.Integer, info='fork_stretch_derection')
    pallet_height = db.Column(db.Float(53), info='pallet height in docks.xml p6/1000.0')
    calibrate_x = db.Column(db.Float(53), info='fork_veh_calibrate_x')
    position_x = db.Column(db.Float(53), info='current position')
    position_y = db.Column(db.Float(53), info='current position')
    pos_angle = db.Column(db.Float(53), info='current position')
    deviation_x = db.Column(db.Float(53), info='pallet loc deviation by fork camera')
    deviation_y = db.Column(db.Float(53), info='pallet loc deviation by fork camera')
    deviation_angle = db.Column(db.Float(53), info='pallet loc deviation by fork camera')
    reocord_time = db.Column(db.DateTime(True), info='when the fork camera get the deviation')
    location_id = db.Column(db.Integer, info='the location of dock')
    dock_id = db.Column(db.Integer, info='dock id  ')
    dock_x = db.Column(db.Float(53), info='dock x point ')
    dock_y = db.Column(db.Float(53), info='doc  y point')
    dock_angle = db.Column(db.Float(53), info='the angle of dock ')
    log_created_timestamp = db.Column(db.DateTime(True), info='the timestamp when this log record was created')



class MaintenanceAgvBatteryLog(db.Model):
    __tablename__ = 'maintenance_agv_battery_log'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='the internal id to identify a record')
    agv_id = db.Column(db.Integer, info='the agv id')
    happened_time = db.Column(db.DateTime(True), info='happened_time')
    last_charge_count = db.Column(db.Integer, info=' last charge count ')
    before_count = db.Column(db.Integer, info='before_count')
    after_count = db.Column(db.Integer, info='after_count')
    error_charge_count = db.Column(db.String, info='error_charge_countIS')
    total_ideal_distime = db.Column(db.Float(53), info='the full battery charging time')
    lifecycle = db.Column(db.Float(53), info='statistical Week of battery discharge')
    capacity = db.Column(db.Float(53), info='TotalIdealDisTime*0.8 / Life Cycle')
    replace_time = db.Column(db.DateTime(True), info='battery replacement time')
    position_x = db.Column(db.Float(53), info='the position change agv_battery ')
    position_y = db.Column(db.Float(53), info='the position change agv_battery')
    angle = db.Column(db.Float(53), info='the agv angle when change agv_battery')
    layout_edge_id = db.Column(db.Integer, info='the layout_edge_id when change agv_battery ')
    edge_percentage = db.Column(db.Float(53), info='edge_percentage when change agv_battery')
    log_created_timestamp = db.Column(db.DateTime(True), info='the timestamp when this log record was created')
    avedistime = db.Column(db.Float(53), info='average single ideal discharge time ')
    aveweight = db.Column(db.Float(53), info='average single discharge percentage ')



class MaintenanceAgvBlockLog(db.Model):
    __tablename__ = 'maintenance_agv_block_log'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    agv_id = db.Column(db.Integer)
    blocked_start_time = db.Column(db.DateTime(True))
    blocked_end_time = db.Column(db.DateTime(True))
    blocked_duration_time = db.Column(db.Float(53), info='agv blocked time seconds, unit:seconds')
    log_created_timestamp = db.Column(db.DateTime(True))
    blocked_by_agv = db.Column(db.Integer)
    position_x = db.Column(db.Float(53))
    position_y = db.Column(db.Float(53))
    angle = db.Column(db.Float(53))
    layout_edge_id = db.Column(db.Float(53))
    edge_percentage = db.Column(db.Float(53))



class MaintenanceAgvChargeLog(db.Model):
    __tablename__ = 'maintenance_agv_charge_log'
    __table_args__ = {'schema': 'layer1_agv'}

    log_id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='the internal id to identify a record')
    agv_id = db.Column(db.Integer, index=True, info='agv id')
    task_id = db.Column(db.Integer, info='task id of engine')
    charge_command_created_timestamp = db.Column(db.DateTime(True), info='the timestamp when charge command created')
    engine_fetch_timestamp = db.Column(db.DateTime(True), info='the timestamp when engine fetch the charge command')
    engine_fetch_battery_voltage = db.Column(db.Float(53), info='the voltage of the battery when charge command created')
    engine_fetch_battery_percentage = db.Column(db.Float(53), info='percentage value of the battery when charge command created')
    charge_dock_id = db.Column(db.Integer, info='dock id of charge')
    charge_result_code = db.Column(db.Integer, info='charge result')
    total_retry_times = db.Column(db.Integer, info='times agv retry charge')
    charge_failed_code = db.Column(db.Integer, info='charge failed code, FOREIGN key of agv_error_type.id')
    begin_charge_battery_voltage = db.Column(db.Float(53), info='the voltage of the battery when begin charge')
    begin_charge_battery_percentage = db.Column(db.Float(53), info='percentage value of the battery when begin charge')
    end_charge_timestamp = db.Column(db.DateTime(True), info='the timestamp when end charge')
    end_charge_battery_voltage = db.Column(db.Float(53), info='the voltage of the battery when end charge')
    end_charge_battery_percentage = db.Column(db.Float(53), info='percentage value of the battery when end charge')
    maximum_battery_current = db.Column(db.Float(53), info='the max current of the battery (unit: A)')
    minimum_battery_current = db.Column(db.Float(53), info='the min current of the battery (unit: A)')
    average_battery_current = db.Column(db.Float(53), info='the average current of the battery (unit: A)')
    end_charge_reason = db.Column(db.String(200), info='reason of end charge')
    log_created_timestamp = db.Column(db.DateTime(True), index=True, server_default=db.FetchedValue(), info='the timestamp when this log record was created')
    engine_fetch_battery_soc = db.Column(db.Float(53), info='the percentage of the battery when engine begin fetch')
    begin_charge_battery_soc = db.Column(db.Float(53), info='the percentage of the battery when begin charge')
    end_charge_battery_soc = db.Column(db.Float(53), info='the percentage of the battery when end charge')
    charge_result_description = db.Column(db.String, info='the description of charg result')
    charge_result_timestamp = db.Column(db.DateTime(True), info='the charg result_code build time')
    position_x = db.Column(db.Float(53), info='the realtime position of this AGV: the coordinate value in X axis')
    position_y = db.Column(db.Float(53), info='the realtime position of this AGV: the coordinate value in Y axis')
    angle = db.Column(db.Float(53), info='the realtime position of this AGV: the angle in the absolute coordinate system of the map')
    layout_edge_id = db.Column(db.Integer, info='foreign key of layout_edge.id, the current layout edge that the AGV is at')
    edge_percentage = db.Column(db.Float(53), info='the accurate point that the AGV on the layout edge can be determined by this percentage (0-1)')
    chargepile = db.Column(db.String, info='the description of the sCharglePile')
    dock_id = db.Column(db.Integer, info='dock id ')



class MaintenanceAgvErrorLog(db.Model):
    __tablename__ = 'maintenance_agv_error_log'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='the internal id to identify a record')
    agv_id = db.Column(db.Integer, info='foreign key of agv.id')
    agv_error_type_id = db.Column(db.Integer, info='foreign key of agv_error_type.id')
    error_catagory_id = db.Column(db.Integer, info='foreign key of agv_error_type.id')
    error_code = db.Column(db.Integer, info='foreign key of agv_error_type.id')
    error_information = db.Column(db.String(2000), info='extra detailed information of this error')
    start_time = db.Column(db.DateTime(True), info='the user name that created this record')
    end_time = db.Column(db.DateTime(True), info='the timestamp when created this record')
    position_x = db.Column(db.Float(53), info='the user name that updated this record most recently')
    position_y = db.Column(db.Float(53), info='the timestamp when updated this record most recently')
    angle = db.Column(db.Float(53))
    layout_edge_id = db.Column(db.Integer, info='the user name that updated this record most recently')
    edge_percentage = db.Column(db.Float(53), info='the timestamp when updated this record most recently')
    log_created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when this log record was created')
    error_occured_timestamp = db.Column(db.DateTime(True), info='when the error occured ')
    error_last_updated_timestamp = db.Column(db.DateTime(True), info='when the error last updated')



class MaintenanceAgvLogicState(db.Model):
    __tablename__ = 'maintenance_agv_logic_state'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    agv_id = db.Column(db.Integer, index=True)
    state = db.Column(db.String(200))
    start_time = db.Column(db.DateTime(True), index=True)
    end_time = db.Column(db.DateTime(True), index=True)
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    log_created_timestamp = db.Column(db.DateTime(True))



class MaintenanceAgvNetworkDelayLog(db.Model):
    __tablename__ = 'maintenance_agv_network_delay_log'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='the internal id to identify a record')
    agv_id = db.Column(db.Integer, index=True, info='the agv id')
    network_delay = db.Column(db.Float(53), info='network_delay time')
    position_x = db.Column(db.Float(53), info='current position')
    position_y = db.Column(db.Float(53), info='current position')
    layout_edge_id = db.Column(db.Integer, info='the edge_id in layout')
    edge_percentage = db.Column(db.Float(53), info=' edge percentage')
    eigen_insert_time = db.Column(db.DateTime(True), index=True, info='the timestamp when eigen excute')
    log_created_timestamp = db.Column(db.DateTime(True), info='the timestamp when this log record was created')
    agv_management_status_id = db.Column(db.Integer, index=True, info='--foreign key of agv_state.agv_management_status_id ')



class MaintenanceAgvStateLog(db.Model):
    __tablename__ = 'maintenance_agv_state_log'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='the internal id to identify a record')
    agv_id = db.Column(db.Integer, info='the agv id')
    state_change_type = db.Column(db.Integer, info='state_change_type --1--network_status变化 2--safety_triggered  3--safety_enabled')
    sub_type = db.Column(db.Integer)
    begin_time = db.Column(db.DateTime(True), info='begin_time')
    end_time = db.Column(db.DateTime(True), info='end_time')
    description = db.Column(db.String, info='safety_information')
    position_x = db.Column(db.Float(53), info='the realtime position of this AGV: the coordinate value in X axis')
    position_y = db.Column(db.Float(53), info='the realtime position of this AGV: the coordinate value in Y axis')
    angle = db.Column(db.Float(53), info='the realtime position of this AGV: the coordinate value in Y axis')
    layout_edge_id = db.Column(db.Integer, info=' the current layout edge that the AGV is at')
    edge_percentage = db.Column(db.Float(53), info='the accurate point that the AGV on the layout edge can be determined by this percentage (0-1)')
    bank_id = db.Column(db.String(2000), info='trigger safety area number')
    log_created_timestamp = db.Column(db.DateTime(True), info='the timestamp when this log record was created')



class MaintenanceAgvTaskDutyCycleLog(db.Model):
    __tablename__ = 'maintenance_agv_task_duty_cycle_log'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='the internal id to identify a record')
    agv_id = db.Column(db.Integer, info='foreign key of agv_id')
    busy_time = db.Column(db.Float(53), info='the accumulate time  when agv has task  today,unit :s')
    dispatch_time = db.Column(db.Float(53), info='the accumulate time  when agv managestatus >= inDispatch today,unit :s')
    charge_time = db.Column(db.Float(53), info='the accumulate time  when agv has charge task(chargeon+charging+chargeoff) today,unit :s ')
    block_time = db.Column(db.Float(53), info='the accumulate time  when is_block is true  today,unit :s ')
    average_execute_time = db.Column(db.Float(53), info='average execute time per task')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), info='the timestamp  that updated this record most recently')
    last_updated_user = db.Column(db.String(200), info='the user name that last update this record')
    last_updated_timestamp = db.Column(db.DateTime(True), info='the timestamp when updated this record most recently')
    log_created_timestamp = db.Column(db.DateTime(True), info='the timestamp when this log record was created')



class Map(db.Model):
    __tablename__ = 'map'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    name = db.Column(db.String(200), nullable=False, unique=True, info='the name of this map')
    description = db.Column(db.String(2000), info='the descriptive information of this map')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')



class MapAgvOverride(db.Model):
    __tablename__ = 'map_agv_override'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    override_type = db.Column(db.Integer, index=True, info='1 for this override only take effect for the agv, 2 for this override only take effect for all agv except the agv')
    agv_id = db.Column(db.Integer, index=True, info='agv_id')
    map_edge_id = db.Column(db.ForeignKey('layer1_agv.map_edge.id'), index=True, info='edge id, FOREIGN KEY of map_edge.id')
    weight = db.Column(db.Float(53), info='the override weight of this map edge')
    available_flag = db.Column(db.Boolean, info='angle of the agv in the dock')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')

    map_edge = db.relationship('MapEdge', primaryjoin='MapAgvOverride.map_edge_id == MapEdge.id', backref='map_agv_overrides')



class MapCommand(db.Model):
    __tablename__ = 'map_command'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record,FOREIGN KEY of agv.id')
    override_type = db.Column(db.Integer, info='same as map_agv_override.override_type')
    agv_id = db.Column(db.ForeignKey('layer1_agv.agv.id'), index=True, info='agv_id,FOREIGN KEY of agv.id')
    map_edge_id = db.Column(db.ForeignKey('layer1_agv.map_edge.id'), index=True, info='map_edge_id FOREIGN KEY of map_edge.id')
    weight = db.Column(db.Float(53), info='fluence weight')
    available_flag = db.Column(db.Boolean)
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')

    agv = db.relationship('Agv', primaryjoin='MapCommand.agv_id == Agv.id', backref='map_commands')
    map_edge = db.relationship('MapEdge', primaryjoin='MapCommand.map_edge_id == MapEdge.id', backref='map_commands')



class MapDock(db.Model):
    __tablename__ = 'map_dock'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    map_id = db.Column(db.ForeignKey('layer1_agv.map.id'), index=True)
    dock_id = db.Column(db.Integer, index=True)
    map_edge_id = db.Column(db.Integer, index=True, info='edge id, FOREIGN KEY of map_edge.id')
    map_edge_percentage = db.Column(db.Float(53), info='percentage in the edge of the dock')
    position_x = db.Column(db.Float(53), info='the position of this dock in map: the coordinate value in X axis')
    position_y = db.Column(db.Float(53), info='the position of this dock in map: the coordinate value in Y axis')
    angel = db.Column(db.Float(53), info='angle of the agv in the dock')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')

    map = db.relationship('Map', primaryjoin='MapDock.map_id == Map.id', backref='map_docks')



class MapEdge(db.Model):
    __tablename__ = 'map_edge'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    map_id = db.Column(db.ForeignKey('layer1_agv.map.id'), index=True, info='the map id of this edge related to')
    layout_edge_id = db.Column(db.Integer, index=True, info='edge id in layout xml file')
    layout_wop_id = db.Column(db.Integer, info='wop id in layout xml file related to thie edge')
    start_node_id = db.Column(db.Integer, info='start node of this edge')
    end_node_id = db.Column(db.Integer, info='end node of this edge')
    edge_length = db.Column(db.Float(53), info='length of thie edge')
    speed_limit = db.Column(db.Float(53), info='limit speed of agv move in the edge')
    weight = db.Column(db.Float(53), info='weight of the edge')
    available_flag = db.Column(db.Boolean, index=True, info='if the edge is available')
    fluent_mode = db.Column(db.Integer, index=True, info='fluent mode of this edge')
    fluent_weight = db.Column(db.Float(53), info='fluent weight of this edge')
    fluent_available_flag = db.Column(db.Boolean, info='if the fluent take effect')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')

    map = db.relationship('Map', primaryjoin='MapEdge.map_id == Map.id', backref='map_edges')



class MapEdgeRelation(db.Model):
    __tablename__ = 'map_edge_relation'
    __table_args__ = (
        db.UniqueConstraint('from_map_edge_id', 'destination_map_edge_id'),
        {'schema': 'layer1_agv'}
    )

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    from_map_edge_id = db.Column(db.ForeignKey('layer1_agv.map_edge.id'))
    destination_map_edge_id = db.Column(db.ForeignKey('layer1_agv.map_edge.id'), info=' object id')
    cost = db.Column(db.Float(53))
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')

    destination_map_edge = db.relationship('MapEdge', primaryjoin='MapEdgeRelation.destination_map_edge_id == MapEdge.id', backref='mapedge_map_edge_relations')
    from_map_edge = db.relationship('MapEdge', primaryjoin='MapEdgeRelation.from_map_edge_id == MapEdge.id', backref='mapedge_map_edge_relations_0')



class MapNode(db.Model):
    __tablename__ = 'map_node'
    __table_args__ = {'schema': 'layer1_agv'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    map_id = db.Column(db.ForeignKey('layer1_agv.map.id'), index=True, info='the map id of this node related to')
    node_id = db.Column(db.Integer, index=True)
    position_x = db.Column(db.Float(53), info='the position of this node in map: the coordinate value in X axis')
    position_y = db.Column(db.Float(53), info='the position of this node in map: the coordinate value in Y axis')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')

    map = db.relationship('Map', primaryjoin='MapNode.map_id == Map.id', backref='map_nodes')



class VersionLog(db.Model):
    __tablename__ = 'version_log'
    __table_args__ = (
        db.UniqueConstraint('trunk', 'branch', 'version_no'),
        {'schema': 'layer1_agv'}
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
