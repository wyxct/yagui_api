# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Location(db.Model):
    __tablename__ = 'location'
    __table_args__ = {'schema': 'layer2_pallet'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    location_type_id = db.Column(db.ForeignKey('layer2_pallet.location_type.id'), index=True, info=' type of location, foreign key of location_type.id ')
    location_name = db.Column(db.String(200), nullable=False, unique=True, info=' name of location ')
    layout_dock_id = db.Column(db.Integer, info=' dock id of the location that robot can access ')
    shelf_layer = db.Column(db.Integer, info='layer of this location')
    active = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue(), info=' if the location can access ')
    physical_label = db.Column(db.String(200), info=' physical label of this location ')
    posture_type_id = db.Column(db.ForeignKey('layer2_pallet.posture_type.id'), info=' the posture that the object put in the location ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    operation_parameter_fetch = db.Column(db.Integer, info='fetch operation id')
    operation_parameter_put = db.Column(db.Integer, info='put operation id')
    center_pos_x = db.Column(db.Float(53), info='center point of this location, the coordinate value in X axis')
    center_pos_y = db.Column(db.Float(53), info='center point of this location, the coordinate value in Y axis')
    length = db.Column(db.Float(53), info='length of the location')
    width = db.Column(db.Float(53), info='width of the location')
    height = db.Column(db.Float(53), info='height of the location')
    is_leaf = db.Column(db.Boolean, info='if the location is leaf location')
    priority = db.Column(db.Float(53))
    exit_dock_id = db.Column(db.Integer)
    can_put = db.Column(db.Boolean, server_default=db.FetchedValue(), info='declare if the location can put pallet')
    is_booked = db.Column(db.Boolean, server_default=db.FetchedValue(), info='False for not booked,True for booked')

    location_type = db.relationship('LocationType', primaryjoin='Location.location_type_id == LocationType.id', backref='locations')
    posture_type = db.relationship('PostureType', primaryjoin='Location.posture_type_id == PostureType.id', backref='locations')



class LocationType(db.Model):
    __tablename__ = 'location_type'
    __table_args__ = {'schema': 'layer2_pallet'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this location type ')
    description = db.Column(db.String(2000), info=' the description of this location type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class Object(db.Model):
    __tablename__ = 'object'
    __table_args__ = {'schema': 'layer2_pallet'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    object_type_id = db.Column(db.ForeignKey('layer2_pallet.object_type.id'), nullable=False, index=True, info=' foreign key of object_type.id ')
    object_name = db.Column(db.String(200), nullable=False, unique=True, info=' name of object ')
    physical_label = db.Column(db.String(200), info=' label of object ')
    object_length = db.Column(db.Float(53), info=' length of object ')
    object_width = db.Column(db.Float(53), info=' width of object ')
    object_height = db.Column(db.Float(53), info=' height of object ')
    fit_location_id = db.Column(db.ForeignKey('layer2_pallet.location.id'), info=' declare witch location the object can put,foreign key of location.id ')
    error_code = db.Column(db.Integer, index=True, info=' 0 for normal,1 for abnormal ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    pallet_type = db.Column(db.Integer, info='2: metal pallet 1: plastic pallet')
    batch_no = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue(), info=' the batch number of the object')
    object_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info=' the status of the object, 0 for outbound non-available, 1 for outbound available ')
    extra_info = db.Column(db.JSON, info='extra info of the object')

    fit_location = db.relationship('Location', primaryjoin='Object.fit_location_id == Location.id', backref='objects')
    object_type = db.relationship('ObjectType', primaryjoin='Object.object_type_id == ObjectType.id', backref='objects')


class ObjectLocation(Object):
    __tablename__ = 'object_location'
    __table_args__ = {'schema': 'layer2_pallet'}

    object_id = db.Column(db.ForeignKey('layer2_pallet.object.id'), primary_key=True, info=' foreign key of object.id ')
    home_location_id = db.Column(db.ForeignKey('layer2_pallet.location.id'), index=True, info=' foreign key of location.id ')
    current_location_id = db.Column(db.ForeignKey('layer2_pallet.location.id'), unique=True, info=' foreign key of location.id ')
    current_object_task_id = db.Column(db.ForeignKey('layer2_pallet.object_task.id', ondelete='SET NULL'), index=True, info=' foreign key of object_task.id ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    logic_location_id = db.Column(db.Integer, info='logic reflact location for pick in agv')

    current_location = db.relationship('Location', uselist=False, primaryjoin='ObjectLocation.current_location_id == Location.id', backref='location_object_locations')
    current_object_task = db.relationship('ObjectTask', primaryjoin='ObjectLocation.current_object_task_id == ObjectTask.id', backref='object_locations')
    home_location = db.relationship('Location', primaryjoin='ObjectLocation.home_location_id == Location.id', backref='location_object_locations_0')



class ObjectTask(db.Model):
    __tablename__ = 'object_task'
    __table_args__ = {'schema': 'layer2_pallet'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    object_id = db.Column(db.ForeignKey('layer2_pallet.object.id'), nullable=False, index=True, info=' foreign key of object.id ')
    task_type_id = db.Column(db.ForeignKey('layer2_pallet.task_type.id'), nullable=False, index=True, info=' foreign key of task_type.id ')
    task_priority = db.Column(db.Float(53), info=' priority of task ')
    destination_location_id = db.Column(db.ForeignKey('layer2_pallet.location.id'), nullable=False, index=True, info=' destination location the object move to ')
    posture_type_id = db.Column(db.ForeignKey('layer2_pallet.posture_type.id'), info=' posture of the object on the destination location ')
    status_id = db.Column(db.ForeignKey('layer2_pallet.task_status.id'), nullable=False, index=True, info=' status of task ')
    required_arrival_time = db.Column(db.DateTime(True), info=' expected arrival time of the object ')
    predicted_arrival_time = db.Column(db.DateTime(True), info=' predicted arrival time of the object ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    keep_object_bound = db.Column(db.Boolean, info='whether keep the agv bound to the object after arriving the destination location; if true, keep bound; if fase, release the object; if null, both acceptable, depends on how the dispatch logic chooses.')
    required_arrival_sequence = db.Column(db.Integer, info='if not null, the object tasks to the same destination location must be finished according to this sequence.')
    rule_type_id = db.Column(db.Integer, info='declare the put rule for object task')

    destination_location = db.relationship('Location', primaryjoin='ObjectTask.destination_location_id == Location.id', backref='object_tasks')
    object = db.relationship('Object', primaryjoin='ObjectTask.object_id == Object.id', backref='object_tasks')
    posture_type = db.relationship('PostureType', primaryjoin='ObjectTask.posture_type_id == PostureType.id', backref='object_tasks')
    status = db.relationship('TaskStatu', primaryjoin='ObjectTask.status_id == TaskStatu.id', backref='object_tasks')
    task_type = db.relationship('TaskType', primaryjoin='ObjectTask.task_type_id == TaskType.id', backref='object_tasks')



class ObjectType(db.Model):
    __tablename__ = 'object_type'
    __table_args__ = {'schema': 'layer2_pallet'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), nullable=False, unique=True, info=' name of this object type ')
    description = db.Column(db.String(2000), info=' description of this object type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class PlTask(db.Model):
    __tablename__ = 'pl_task'
    __table_args__ = {'schema': 'layer2_pallet'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    task_type = db.Column(db.String(20), info=' P2P:point to point, P2A:point to area, P2M:多点任务, A2P:area to point, BCID:bind cid, DCID:解绑托盘 ')
    task_no = db.Column(db.String(100), unique=True, info=' the external id to identify a record ')
    from_pos = db.Column(db.String(50), info=' start location of this task ')
    to_pos = db.Column(db.String(50), info=' destination location of this task ')
    start_time = db.Column(db.DateTime(True))
    end_time = db.Column(db.DateTime(True))
    pos_list = db.Column(db.String(200), info=' location list, multiple values are separated by commas ')
    next_pos = db.Column(db.String(50), info=' next location of this task ')
    status = db.Column(db.String(10), info=' 00:canled, 10:created, 20:handle, 30:in_progress, 50:completed, 90:error ')
    priority = db.Column(db.Integer)
    cid = db.Column(db.String(50), info=' name of cid ')
    cid_attribute = db.Column(db.JSON, info=' the property of cid ')
    custom_parm1 = db.Column(db.String(200))
    custom_parm2 = db.Column(db.String(200))
    source = db.Column(db.String(10), info=' pda/pad/pc/interface/mq ')
    ip = db.Column(db.String(200))
    client_name = db.Column(db.String(200), info=' the machine name of client ')
    client_type = db.Column(db.String(50), info=' device identification ')
    memo = db.Column(db.String(200))
    ex = db.Column(db.String(200))
    optlist = db.Column(db.JSON)
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class PlTaskRelation(db.Model):
    __tablename__ = 'pl_task_relation'
    __table_args__ = {'schema': 'layer2_pallet'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    pl_task_id = db.Column(db.ForeignKey('layer2_pallet.pl_task.id'))
    relation = db.Column(db.String(200))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())

    pl_task = db.relationship('PlTask', primaryjoin='PlTaskRelation.pl_task_id == PlTask.id', backref='pl_task_relations')



class PlTaskReport(db.Model):
    __tablename__ = 'pl_task_report'
    __table_args__ = {'schema': 'layer2_pallet'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    pl_task_id = db.Column(db.ForeignKey('layer2_pallet.pl_task_report.id'))
    reportdata = db.Column(db.JSON)
    reporttype = db.Column(db.String(20))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())

    pl_task = db.relationship('PlTaskReport', remote_side=[id], primaryjoin='PlTaskReport.pl_task_id == PlTaskReport.id', backref='pl_task_reports')



class PlTaskType(db.Model):
    __tablename__ = 'pl_task_type'
    __table_args__ = {'schema': 'layer2_pallet'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    task_type = db.Column(db.String(200), unique=True)
    ts_map = db.Column(db.String(200))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class PostureType(db.Model):
    __tablename__ = 'posture_type'
    __table_args__ = {'schema': 'layer2_pallet'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), nullable=False, unique=True, info=' name of posture ')
    angle = db.Column(db.String(200), info=' angle in coordinates ')
    description = db.Column(db.String(2000), info=' description of posture ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class TaskStatu(db.Model):
    __tablename__ = 'task_status'
    __table_args__ = (
        db.UniqueConstraint('task_type_id', 'name'),
        {'schema': 'layer2_pallet'}
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    task_type_id = db.Column(db.ForeignKey('layer2_pallet.task_type.id'), nullable=False, info=' foreign key of task_type.id ')
    name = db.Column(db.String(200), info=' name of task status')
    description = db.Column(db.String(2000), info=' description of task ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')

    task_type = db.relationship('TaskType', primaryjoin='TaskStatu.task_type_id == TaskType.id', backref='task_status')



class TaskType(db.Model):
    __tablename__ = 'task_type'
    __table_args__ = {'schema': 'layer2_pallet'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), nullable=False, unique=True, info=' name of task type ')
    description = db.Column(db.String(2000), info=' description of task_type ')
    initial_priority = db.Column(db.Float(53), info=' init priority ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    category_id = db.Column(db.ForeignKey('layer2_pallet.task_type_category.id'), info='the category of task type.')

    category = db.relationship('TaskTypeCategory', primaryjoin='TaskType.category_id == TaskTypeCategory.id', backref='task_types')



class TaskTypeCategory(db.Model):
    __tablename__ = 'task_type_category'
    __table_args__ = {'schema': 'layer2_pallet'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), nullable=False, unique=True, info=' name of task type ')
    description = db.Column(db.String(2000), info=' description of task_type_category ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
