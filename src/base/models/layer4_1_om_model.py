# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class ConvertTable(db.Model):
    __tablename__ = 'convert_table'
    __table_args__ = {'schema': 'layer4_1_om'}

    cv_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    cv_name = db.Column(db.String(200), unique=True)
    cv_value = db.Column(db.String(200))
    cv_value_type = db.Column(db.String(200))



class Globalparameter(db.Model):
    __tablename__ = 'globalparameters'
    __table_args__ = {'schema': 'layer4_1_om'}

    gp_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    gp_name = db.Column(db.String(200), unique=True)
    gp_value = db.Column(db.String(200))
    gp_value_type = db.Column(db.String(200))



class InteractionInfo(db.Model):
    __tablename__ = 'interaction_info'
    __table_args__ = {'schema': 'layer4_1_om'}

    interaction_info_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    interaction_info_name = db.Column(db.String(200))
    interaction_info_desp = db.Column(db.String(200))
    interaction_info_type_id = db.Column(db.ForeignKey('layer4_1_om.interaction_info_type.id'))
    value_json = db.Column(db.JSON)
    info_status = db.Column(db.String(200))
    return_value = db.Column(db.String(2000))

    interaction_info_type = db.relationship('InteractionInfoType', primaryjoin='InteractionInfo.interaction_info_type_id == InteractionInfoType.id', backref='interaction_infos')



class InteractionInfoType(db.Model):
    __tablename__ = 'interaction_info_type'
    __table_args__ = {'schema': 'layer4_1_om'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.String(2000))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class Mapping(db.Model):
    __tablename__ = 'mapping'
    __table_args__ = {'schema': 'layer4_1_om'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(2000))
    mapping_id = db.Column(db.Integer)
    mapping_type_id = db.Column(db.ForeignKey('layer4_1_om.mapping_type.id'))
    parameter_int_1 = db.Column(db.Integer)
    parameter_int_2 = db.Column(db.Integer)
    parameter_int_3 = db.Column(db.Integer)
    parameter_int_4 = db.Column(db.Integer)
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    mapping_src_type = db.Column(db.String(200), info="'locaiton'\\'pallet'\\'object'")

    mapping_type = db.relationship('MappingType', primaryjoin='Mapping.mapping_type_id == MappingType.id', backref='mappings')



class MappingType(db.Model):
    __tablename__ = 'mapping_type'
    __table_args__ = {'schema': 'layer4_1_om'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.String(2000))
    valid_parameter_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class OmConfig(db.Model):
    __tablename__ = 'om_config'
    __table_args__ = {'schema': 'layer4_1_om'}

    cfg_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    cfg_name = db.Column(db.String(200), unique=True)
    cfg_desp = db.Column(db.String(200))
    cfg_value = db.Column(db.String(200))
    cfg_value_type = db.Column(db.String(200))



class OmContainer(db.Model):
    __tablename__ = 'om_container'
    __table_args__ = {'schema': 'layer4_1_om'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(200), unique=True)
    container_type = db.Column(db.String(200), info="'queue', 'stack', 'dict', 'list', 'set'")
    element_type = db.Column(db.String(200), info="'location', 'object', 'pallet'")
    value = db.Column(db.String(4000))
    desp = db.Column(db.String(200))
    value_type = db.Column(db.String(200), info="'list_str', 'list_int', 'dict_def'")



class Operator(db.Model):
    __tablename__ = 'operator'
    __table_args__ = (
        db.UniqueConstraint('order_id', 'index'),
        {'schema': 'layer4_1_om'}
    )

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    index = db.Column(db.Integer)
    name = db.Column(db.String(200))
    status = db.Column(db.String(200), info='waiting,running,finished,skip,retry,fail,cancel,done')
    parameters = db.Column(db.String(2000))
    order_id = db.Column(db.ForeignKey('layer4_1_om.order.order_id'))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    return_value = db.Column(db.String(200))
    return_value_type = db.Column(db.String(200))
    pre_opts = db.Column(db.String(200), info='like (1,2)')
    next_opts = db.Column(db.String(200), info='like (1,2)')
    task_ids = db.Column(db.String(200), info="like '(1,2)'")
    ret_code = db.Column(db.Integer, info='0表示成功，其余为错误码')
    show = db.Column(db.Boolean)

    order = db.relationship('Order', primaryjoin='Operator.order_id == Order.order_id', backref='operators')



class Order(db.Model):
    __tablename__ = 'order'
    __table_args__ = {'schema': 'layer4_1_om'}

    order_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    order_name = db.Column(db.String(200))
    dead_line = db.Column(db.DateTime(True))
    agv_list = db.Column(db.ARRAY(INTEGER()))
    ts_id = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), info='waiting/active/finish/error/waiting_cancel/cancel_finish/waiting_manually_finish/manually_finish')
    priority = db.Column(db.Integer)
    current_destination = db.Column(db.String(200))
    current_operation = db.Column(db.String(200))
    current_omi = db.Column(db.String(200))
    create_time = db.Column(db.DateTime(True))
    active_time = db.Column(db.DateTime(True))
    cancel_time = db.Column(db.DateTime(True))
    finished_time = db.Column(db.DateTime(True))
    order_trigger = db.Column(db.String(200))
    error_code = db.Column(db.Integer, info="    8: 'Agv Task Error',\r\n    101: 'Pallet not exist when load',\r\n    102: 'Pallet exist on dst when unload',\r\n    103: 'Pallet not exist on AGV when unload',\r\n    201: 'DB error when run sql',\r\n    301: 'Operator Error',\r\n    401: 'Logic Error', # 内部逻辑错误\r\n    501: 'TS Error',\r\n")
    mark = db.Column(db.String(200))
    msg_handled = db.Column(db.Integer, server_default=db.FetchedValue())



class OrderCommand(db.Model):
    __tablename__ = 'order_command'
    __table_args__ = {'schema': 'layer4_1_om'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    order_command_type_id = db.Column(db.ForeignKey('layer4_1_om.order_command_type.id'), nullable=False)
    order_command_status_id = db.Column(db.ForeignKey('layer4_1_om.order_command_status.id'), nullable=False, server_default=db.FetchedValue())
    parameters = db.Column(db.String(2000), nullable=False)
    order_command_error_detail = db.Column(db.String(2000))
    priority = db.Column(db.Float(53))
    request_finish_time = db.Column(db.DateTime(True))
    predicted_finish_time = db.Column(db.DateTime(True))
    order_id = db.Column(db.ForeignKey('layer4_1_om.order.order_id'))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    obsolete_flag = db.Column(db.Boolean, server_default=db.FetchedValue())
    order_type_id = db.Column(db.ForeignKey('layer4_1_om.order_task.id'))

    order_command_status = db.relationship('OrderCommandStatu', primaryjoin='OrderCommand.order_command_status_id == OrderCommandStatu.id', backref='order_commands')
    order_command_type = db.relationship('OrderCommandType', primaryjoin='OrderCommand.order_command_type_id == OrderCommandType.id', backref='order_commands')
    order = db.relationship('Order', primaryjoin='OrderCommand.order_id == Order.order_id', backref='order_commands')
    order_type = db.relationship('OrderTask', primaryjoin='OrderCommand.order_type_id == OrderTask.id', backref='order_commands')



class OrderCommandStatu(db.Model):
    __tablename__ = 'order_command_status'
    __table_args__ = {'schema': 'layer4_1_om'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(200), nullable=False, unique=True, server_default=db.FetchedValue())
    description = db.Column(db.String(2000))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class OrderCommandType(db.Model):
    __tablename__ = 'order_command_type'
    __table_args__ = {'schema': 'layer4_1_om'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(200), nullable=False, unique=True)
    category = db.Column(db.String(200))
    description = db.Column(db.String(2000))
    valid_parameter_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class OrderStatistic(db.Model):
    __tablename__ = 'order_statistic'
    __table_args__ = {'schema': 'layer4_1_om'}

    order_statistic_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    finish_num = db.Column(db.Integer)
    error_num = db.Column(db.Integer)
    cancel_num = db.Column(db.Integer)
    statistic_date = db.Column(db.Date)
    statistic_time = db.Column(db.DateTime(True))



class OrderTask(db.Model):
    __tablename__ = 'order_task'
    __table_args__ = {'schema': 'layer4_1_om'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    description = db.Column(db.String(2000), info='omi name')
    value_int_1 = db.Column(db.Integer, info='0表示不重新执行，直接返回return value，1表示重新执行')
    value_int_2 = db.Column(db.Integer, info='非task类型omi index')
    value_int_3 = db.Column(db.Integer)
    value_int_4 = db.Column(db.Integer)
    parameters = db.Column(db.String(2000))
    order_task_status_id = db.Column(db.ForeignKey('layer4_1_om.order_task_status.id'), nullable=False, server_default=db.FetchedValue())
    order_task__error_detail = db.Column(db.String(2000))
    priority = db.Column(db.Float(53))
    order_id = db.Column(db.ForeignKey('layer4_1_om.order.order_id'))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    return_value = db.Column(db.String(2000))
    return_value_type = db.Column(db.String(200))
    task_index = db.Column(db.Integer)

    order = db.relationship('Order', primaryjoin='OrderTask.order_id == Order.order_id', backref='order_tasks')
    order_task_status = db.relationship('OrderTaskStatu', primaryjoin='OrderTask.order_task_status_id == OrderTaskStatu.id', backref='order_tasks')



class OrderTaskStatu(db.Model):
    __tablename__ = 'order_task_status'
    __table_args__ = {'schema': 'layer4_1_om'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(200), nullable=False, unique=True, server_default=db.FetchedValue())
    description = db.Column(db.String(2000))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class T(db.Model):
    __tablename__ = 'ts'
    __table_args__ = {'schema': 'layer4_1_om'}

    ts_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    ts_name = db.Column(db.String(200), unique=True)
    parameters = db.Column(db.String(2000), nullable=False)
    create_time = db.Column(db.DateTime(True), server_default=db.FetchedValue())
