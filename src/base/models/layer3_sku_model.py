# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    cart_type_id = db.Column(db.ForeignKey('cart_type.id'), nullable=False, index=True, info=' type of cart,foreign key of cart_type.id ')
    object_id = db.Column(db.ForeignKey('object.id'), index=True, info=' cart label, foreign key of object.id ')
    status = db.Column(db.Integer, index=True, info=' status of cart ')
    bound_agv = db.Column(db.Integer, info=' bound agv of the cart ')
    current_station = db.Column(db.Integer)
    start_location = db.Column(db.ForeignKey('location.id'), index=True, info=' start location of the cart ')
    current_location = db.Column(db.ForeignKey('location.id'), info=' current location of the cart ')
    next_location = db.Column(db.ForeignKey('location.id'), info=' next location of the cart ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')

    cart_type = db.relationship('CartType', primaryjoin='Cart.cart_type_id == CartType.id', backref='carts')
    location = db.relationship('Location', primaryjoin='Cart.current_location == Location.id', backref='location_location_carts')
    location1 = db.relationship('Location', primaryjoin='Cart.next_location == Location.id', backref='location_location_carts_0')
    object = db.relationship('Object', primaryjoin='Cart.object_id == Object.id', backref='carts')
    location2 = db.relationship('Location', primaryjoin='Cart.start_location == Location.id', backref='location_location_carts')



class CartType(db.Model):
    __tablename__ = 'cart_type'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), nullable=False, unique=True, info=' the name of cart type ')
    description = db.Column(db.String(2000), info=' the description of cart type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    cart_catagory_type = db.Column(db.Integer, info='used by monitor to get what is the shape show in monitor for cart\r\n1 for order cart,2 for star cart')
    container_num = db.Column(db.Integer, info='how many container can the cart hold')



class ErrorCode(db.Model):
    __tablename__ = 'error_code'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    error_type_id = db.Column(db.ForeignKey('error_type.id'), nullable=False, info=' error type foreign key of error_type.id ')
    name = db.Column(db.String(200), nullable=False, info=' the name of error ')
    description = db.Column(db.String(2000), info=' the description of error ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    can_pick = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())
    can_replen = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())

    error_type = db.relationship('ErrorType', primaryjoin='ErrorCode.error_type_id == ErrorType.id', backref='error_codes')



class ErrorType(db.Model):
    __tablename__ = 'error_type'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), nullable=False, unique=True, info=' the name of error type ')
    description = db.Column(db.String(2000), info=' the description of error type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    location_type_id = db.Column(db.ForeignKey('location_type.id'), index=True, info=' type of location, foreign key of location_type.id ')
    location_name = db.Column(db.String(200), nullable=False, unique=True, info=' name of location ')
    layout_dock_id = db.Column(db.Integer, info=' dock id of the location that robot can access ')
    shelf_layer = db.Column(db.Integer, info='layer of this location')
    active = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue(), info=' if the location can access ')
    physical_label = db.Column(db.String(200), info=' physical label of this location ')
    posture_type_id = db.Column(db.ForeignKey('posture_type.id'), info=' the posture that the object put in the location ')
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

    location_type = db.relationship('LocationType', primaryjoin='Location.location_type_id == LocationType.id', backref='locations')
    posture_type = db.relationship('PostureType', primaryjoin='Location.posture_type_id == PostureType.id', backref='locations')



class LocationType(db.Model):
    __tablename__ = 'location_type'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this location type ')
    description = db.Column(db.String(2000), info=' the description of this location type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class Object(db.Model):
    __tablename__ = 'object'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    object_type_id = db.Column(db.ForeignKey('object_type.id'), nullable=False, index=True, info=' foreign key of object_type.id ')
    object_name = db.Column(db.String(200), nullable=False, unique=True, info=' name of object ')
    physical_label = db.Column(db.String(200), info=' label of object ')
    object_length = db.Column(db.Float(53), info=' length of object ')
    object_width = db.Column(db.Float(53), info=' width of object ')
    object_height = db.Column(db.Float(53), info=' height of object ')
    fit_location_id = db.Column(db.ForeignKey('location.id'), info=' declare witch location the object can put,foreign key of location.id ')
    error_code = db.Column(db.Integer, index=True, info=' 0 for normal,1 for abnormal ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    pallet_type = db.Column(db.Integer, info='2: metal pallet 1: plastic pallet')
    batch_no = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue(), info=' the batch number of the object')
    object_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info=' the status of the object, 0 for outbound non-available, 1 for outbound available ')

    fit_location = db.relationship('Location', primaryjoin='Object.fit_location_id == Location.id', backref='objects')
    object_type = db.relationship('ObjectType', primaryjoin='Object.object_type_id == ObjectType.id', backref='objects')


class PalletProperty(Object):
    __tablename__ = 'pallet_property'
    __table_args__ = {'schema': 'layer3_sku'}

    pallet_id = db.Column(db.ForeignKey('object.id'), primary_key=True, info=' the internal id to identify a record,foreign key of object.id ')
    bin_type_id = db.Column(db.ForeignKey('layer3_sku.bin_type.id'), index=True, info=' foreign key of bin_type.id ')
    item_type_id = db.Column(db.ForeignKey('layer3_sku.item_type.id'), info=' foreign key of item_type.id ')
    have_empty_slot = db.Column(db.Boolean, info=' if the pallet have empty slot ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')

    bin_type = db.relationship('BinType', primaryjoin='PalletProperty.bin_type_id == BinType.id', backref='pallet_properties')
    item_type = db.relationship('ItemType', primaryjoin='PalletProperty.item_type_id == ItemType.id', backref='pallet_properties')



class ObjectTask(db.Model):
    __tablename__ = 'object_task'

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    object_id = db.Column(db.ForeignKey('object.id'), nullable=False, index=True, info=' foreign key of object.id ')
    task_type_id = db.Column(db.ForeignKey('task_type.id'), nullable=False, index=True, info=' foreign key of task_type.id ')
    task_priority = db.Column(db.Float(53), info=' priority of task ')
    destination_location_id = db.Column(db.ForeignKey('location.id'), nullable=False, index=True, info=' destination location the object move to ')
    posture_type_id = db.Column(db.ForeignKey('posture_type.id'), info=' posture of the object on the destination location ')
    status_id = db.Column(db.ForeignKey('task_status.id'), nullable=False, index=True, info=' status of task ')
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

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), nullable=False, unique=True, info=' name of this object type ')
    description = db.Column(db.String(2000), info=' description of this object type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class PostureType(db.Model):
    __tablename__ = 'posture_type'

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
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    task_type_id = db.Column(db.ForeignKey('task_type.id'), nullable=False, info=' foreign key of task_type.id ')
    name = db.Column(db.String(200), info=' name of task status')
    description = db.Column(db.String(2000), info=' description of task ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')

    task_type = db.relationship('TaskType', primaryjoin='TaskStatu.task_type_id == TaskType.id', backref='task_status')



class TaskType(db.Model):
    __tablename__ = 'task_type'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), nullable=False, unique=True, info=' name of task type ')
    description = db.Column(db.String(2000), info=' description of task_type ')
    initial_priority = db.Column(db.Float(53), info=' init priority ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    category_id = db.Column(db.ForeignKey('task_type_category.id'), info='the category of task type.')

    category = db.relationship('TaskTypeCategory', primaryjoin='TaskType.category_id == TaskTypeCategory.id', backref='task_types')



class TaskTypeCategory(db.Model):
    __tablename__ = 'task_type_category'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), nullable=False, unique=True, info=' name of task type ')
    description = db.Column(db.String(2000), info=' description of task_type_category ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class BackupSlot(db.Model):
    __tablename__ = 'backup_slot'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True)
    pallet_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    slot_type_id = db.Column(db.Integer)
    slot_position_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    error_code_id = db.Column(db.Integer)
    batch_no = db.Column(db.String(200))
    validity_time = db.Column(db.DateTime(True))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True))
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True))
    error_code_array = db.Column(db.ARRAY(INTEGER()))



class BinType(db.Model):
    __tablename__ = 'bin_type'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), info=' the name of the bin ')
    enabled = db.Column(db.Boolean, info=' if the slot type enabled ')
    slot_types = db.Column(db.ARRAY(INTEGER()), info=' slot type the bin can hold ')
    fit_shelves = db.Column(db.ARRAY(INTEGER()), info=' shelves the bin can fit ')
    fit_pallet_types = db.Column(db.ARRAY(INTEGER()), info=' pallet type the bin can fit ')
    description = db.Column(db.String(2000), info=' the description of this bin type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    fit_object_type = db.Column(db.ARRAY(INTEGER()), info='bin fit object type')
    fit_slot_spot = db.Column(db.ARRAY(INTEGER()), info='fit slot position for static shelf or PTC shelf')



class CartSkuTask(db.Model):
    __tablename__ = 'cart_sku_task'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    sku_task_type_id = db.Column(db.ForeignKey('layer3_sku.sku_task_type.id'), index=True, info=' the name of this sku_task type ')
    sku_task_status_id = db.Column(db.ForeignKey('layer3_sku.sku_task_status.id'), index=True, info=' status of task ')
    batch_no = db.Column(db.String(200), info=' batch number of sku task ')
    cart_id = db.Column(db.ForeignKey('cart.id'), index=True, info=' foreign key of cart.id ')
    item_id = db.Column(db.ForeignKey('layer3_sku.item.id'), index=True, info=' foreign key of item.id ')
    quantity = db.Column(db.Integer, info=' order quantity ')
    dealed_quantity = db.Column(db.Integer, info=' dealed quantity ')
    required_arrival_time = db.Column(db.DateTime(True), info=' required finish time of the task ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    validity_time = db.Column(db.DateTime(True), info='validity time of the replen task for the sku')
    error_code = db.Column(db.Integer, server_default=db.FetchedValue(), info='reason why the cart_sku_task is error')

    cart = db.relationship('Cart', primaryjoin='CartSkuTask.cart_id == Cart.id', backref='cart_sku_tasks')
    item = db.relationship('Item', primaryjoin='CartSkuTask.item_id == Item.id', backref='cart_sku_tasks')
    sku_task_status = db.relationship('SkuTaskStatu', primaryjoin='CartSkuTask.sku_task_status_id == SkuTaskStatu.id', backref='cart_sku_tasks')
    sku_task_type = db.relationship('SkuTaskType', primaryjoin='CartSkuTask.sku_task_type_id == SkuTaskType.id', backref='cart_sku_tasks')



class ExternalMessageQueue(db.Model):
    __tablename__ = 'external_message_queue'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    log_type = db.Column(db.String(200))
    external_message_type_id = db.Column(db.ForeignKey('layer3_sku.external_message_type.id'), index=True, info='the type of this external task, should be brief and clear')
    external_message_status_id = db.Column(db.ForeignKey('layer3_sku.external_message_status.id'), index=True, info='the status of this external task')
    error_code_id = db.Column(db.ForeignKey('error_code.id'), info='the error information code')
    parameter_definition_int4_1 = db.Column(db.Float(53), info='the definition of parameter_int4_1')
    parameter_definition_int4_2 = db.Column(db.Float(53), info='the definition of parameter_int4_2')
    parameter_definition_int4_3 = db.Column(db.Float(53), info='the definition of parameter_int4_3')
    parameter_definition_int4_4 = db.Column(db.Float(53), info='the definition of parameter_int4_4')
    parameter_definition_int4_5 = db.Column(db.Float(53), info='the definition of parameter_int4_5')
    parameter_definition_int4_6 = db.Column(db.Float(53), info='the definition of parameter_int4_6')
    parameter_definition_varchar2000_1 = db.Column(db.String(2000), info='the definition of parameter_varchar2000_1')
    parameter_definition_varchar2000_2 = db.Column(db.String(2000), info='the definition of parameter_varchar2000_2')
    parameter_definition_varchar2000_3 = db.Column(db.String(2000), info='the definition of parameter_varchar2000_3')
    parameter_definition_varchar2000_4 = db.Column(db.String(2000), info='the definition of parameter_varchar2000_4')
    parameter_definition_json_1 = db.Column(db.String(2000), info='the definition of parameter_json_1 (JSON format should be preferred than text)')
    parameter_definition_text_1 = db.Column(db.String(2000), info='the definition of parameter_text_1 (the number of characters is infinite)')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')

    error_code = db.relationship('ErrorCode', primaryjoin='ExternalMessageQueue.error_code_id == ErrorCode.id', backref='external_message_queues')
    external_message_status = db.relationship('ExternalMessageStatu', primaryjoin='ExternalMessageQueue.external_message_status_id == ExternalMessageStatu.id', backref='external_message_queues')
    external_message_type = db.relationship('ExternalMessageType', primaryjoin='ExternalMessageQueue.external_message_type_id == ExternalMessageType.id', backref='external_message_queues')



class ExternalMessageStatu(db.Model):
    __tablename__ = 'external_message_status'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    name = db.Column(db.String(200), nullable=False, unique=True, server_default=db.FetchedValue(), info='the name of this command status, such as "waiting","cached", "in progress", "complete", "error"...')
    description = db.Column(db.String(2000), info='the descriptive information of this AGV command status')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')



class ExternalMessageType(db.Model):
    __tablename__ = 'external_message_type'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='internal id for identifying a record')
    name = db.Column(db.String(200), nullable=False, unique=True, info='the name of this message type, should be brief and clear')
    category = db.Column(db.String(200), info='to classify the message type, such as "item alter"...')
    description = db.Column(db.String(2000), info='the detailed description and definition of this message type')
    valid_parameter_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='how many parameters will be followed with this message type')
    parameter_definition_int4_1 = db.Column(db.String(2000), info='the definition of parameter_int4_1')
    parameter_definition_int4_2 = db.Column(db.String(2000), info='the definition of parameter_int4_2')
    parameter_definition_int4_3 = db.Column(db.String(2000), info='the definition of parameter_int4_3')
    parameter_definition_int4_4 = db.Column(db.String(2000), info='the definition of parameter_int4_4')
    parameter_definition_int4_5 = db.Column(db.String(2000), info='the definition of parameter_int4_5')
    parameter_definition_int4_6 = db.Column(db.String(2000), info='the definition of parameter_int4_6')
    parameter_definition_varchar2000_1 = db.Column(db.String(2000), info='the definition of parameter_varchar2000_1')
    parameter_definition_varchar2000_2 = db.Column(db.String(2000), info='the definition of parameter_varchar2000_2')
    parameter_definition_varchar2000_3 = db.Column(db.String(2000), info='the definition of parameter_varchar2000_3')
    parameter_definition_varchar2000_4 = db.Column(db.String(2000), info='the definition of parameter_varchar2000_4')
    parameter_definition_json_1 = db.Column(db.String(2000), info='the definition of parameter_json_1 (JSON format should be preferred than text)')
    parameter_definition_text_1 = db.Column(db.String(2000), info='the definition of parameter_text_1 (the number of characters is infinite)')
    created_user = db.Column(db.String(200), info='the user name that created this record')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the user name that updated this record most recently.')
    last_updated_user = db.Column(db.String(200), info='the user name that updated this record most recently.')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info='the timestamp when updated this record most recently')



class Item(db.Model):
    __tablename__ = 'item'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    item_category_id = db.Column(db.ForeignKey('layer3_sku.item_category.id'), index=True)
    item_type_id = db.Column(db.ForeignKey('layer3_sku.item_type.id'), index=True, info=' item type, foreign key of item_type.id ')
    wms_location_id = db.Column(db.ForeignKey('layer3_sku.wms_location.id'), info=' wms location,foreign key of wms_location.id ')
    item_name = db.Column(db.String(200), info=' name of item ')
    sku_no = db.Column(db.String(200), index=True, info=' sku number of item ')
    length = db.Column(db.Float(53), info=' length of item ')
    width = db.Column(db.Float(53), info=' width of item ')
    height = db.Column(db.Float(53), info=' height of item ')
    weight = db.Column(db.Float(53), info=' weight of item ')
    image = db.Column(db.String(2000), info=' image source of item ')
    enabled = db.Column(db.Boolean, info=' if this item enabled ')
    special_instructions = db.Column(db.String(2000), info=' special instructions of item ')
    description = db.Column(db.String(2000), info=' description of item ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    sku_daily_velocity = db.Column(db.Float(53), info='the goods need frequency per day')
    date_sensitive = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue(), info='FIFO flag')
    gtp_to_ptc_slot_num = db.Column(db.Integer)

    item_category = db.relationship('ItemCategory', primaryjoin='Item.item_category_id == ItemCategory.id', backref='items')
    item_type = db.relationship('ItemType', primaryjoin='Item.item_type_id == ItemType.id', backref='items')
    wms_location = db.relationship('WmsLocation', primaryjoin='Item.wms_location_id == WmsLocation.id', backref='items')



class ItemCategory(db.Model):
    __tablename__ = 'item_category'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this item category ')
    description = db.Column(db.String(2000), info=' the description of this item category ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class ItemCubing(db.Model):
    __tablename__ = 'item_cubing'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    item_id = db.Column(db.ForeignKey('layer3_sku.item.id'), info=' foreign key of item.id ')
    slot_type_id = db.Column(db.ForeignKey('layer3_sku.slot_type.id'), info=' slot type, foreign key of slot_type.id ')
    max_unit = db.Column(db.Integer, info=' max capacity the slot can hold the sku ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')

    item = db.relationship('Item', primaryjoin='ItemCubing.item_id == Item.id', backref='item_cubings')
    slot_type = db.relationship('SlotType', primaryjoin='ItemCubing.slot_type_id == SlotType.id', backref='item_cubings')



class ItemType(db.Model):
    __tablename__ = 'item_type'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this item type ')
    description = db.Column(db.String(2000), info=' the description of this item type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class ItemTypeRelation(db.Model):
    __tablename__ = 'item_type_relation'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    group_item_type_id = db.Column(db.ForeignKey('layer3_sku.item_type.id'), info=' parent item type,foreign key of item_type.id ')
    node_item_type_id = db.Column(db.ForeignKey('layer3_sku.item_type.id'), info=' child item type,foreign key of item_type.id ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')

    group_item_type = db.relationship('ItemType', primaryjoin='ItemTypeRelation.group_item_type_id == ItemType.id', backref='itemtype_item_type_relations')
    node_item_type = db.relationship('ItemType', primaryjoin='ItemTypeRelation.node_item_type_id == ItemType.id', backref='itemtype_item_type_relations_0')



class ItemUpc(db.Model):
    __tablename__ = 'item_upc'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    item_id = db.Column(db.ForeignKey('layer3_sku.item.id'), index=True, info=' foreign key of item.id ')
    upc_no = db.Column(db.String(200), index=True, info=' upc no of sku ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')

    item = db.relationship('Item', primaryjoin='ItemUpc.item_id == Item.id', backref='item_upcs')



class ReplenSplitRule(db.Model):
    __tablename__ = 'replen_split_rule'
    __table_args__ = (
        db.UniqueConstraint('sku_daily_velocity', 'max_split'),
        {'schema': 'layer3_sku'}
    )

    replen_split_rule_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info='Internal Id for identifying a record')
    sku_daily_velocity = db.Column(db.Float(53), info='A,B,C,D thresholds')
    max_split = db.Column(db.Integer, info='max number of splits')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class SkuTaskStatu(db.Model):
    __tablename__ = 'sku_task_status'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this sku_task status ')
    description = db.Column(db.String(2000), info=' the description of this sku_task status ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class SkuTaskType(db.Model):
    __tablename__ = 'sku_task_type'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this sku_task type ')
    description = db.Column(db.String(2000), info=' the description of this sku_task type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class Slot(db.Model):
    __tablename__ = 'slot'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    pallet_id = db.Column(db.ForeignKey('layer3_sku.pallet_property.pallet_id'), index=True, info=' foreign key of pallet_property.id ')
    item_id = db.Column(db.ForeignKey('layer3_sku.item.id'), index=True, info=' foreign key of item.id ')
    slot_type_id = db.Column(db.ForeignKey('layer3_sku.slot_type.id'), info=' foreign key of slot_type.id ')
    slot_position_id = db.Column(db.ForeignKey('layer3_sku.slot_position.id'), info=' foreign key of slot_position.position_id ')
    quantity = db.Column(db.Integer, info=' quantity the slot remaining ')
    error_code_id = db.Column(db.ForeignKey('error_code.id'), info=' error of the slot ')
    batch_no = db.Column(db.String(200), info=' batch number ')
    validity_time = db.Column(db.DateTime(True), info=' earliest replen time ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    error_code_array = db.Column(db.ARRAY(INTEGER()), info='error of the slot')

    error_code = db.relationship('ErrorCode', primaryjoin='Slot.error_code_id == ErrorCode.id', backref='slots')
    item = db.relationship('Item', primaryjoin='Slot.item_id == Item.id', backref='slots')
    pallet = db.relationship('PalletProperty', primaryjoin='Slot.pallet_id == PalletProperty.pallet_id', backref='slots')
    slot_position = db.relationship('SlotPosition', primaryjoin='Slot.slot_position_id == SlotPosition.id', backref='slots')
    slot_type = db.relationship('SlotType', primaryjoin='Slot.slot_type_id == SlotType.id', backref='slots')



class SlotAssignment(db.Model):
    __tablename__ = 'slot_assignment'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    sku_task_type_id = db.Column(db.ForeignKey('layer3_sku.sku_task_type.id'), index=True, info=' sku task type,foreign key of sku_task_type.id ')
    slot_id = db.Column(db.ForeignKey('layer3_sku.slot.id'), index=True, info=' foreign key of slot.id ')
    assign_quantity = db.Column(db.Integer, info=' assigned quantity to finish the task ')
    station_sku_task_id = db.Column(db.ForeignKey('layer3_sku.station_sku_task.id'), index=True, info=' foreign key of station_sku_task.id ')
    cart_sku_task_id = db.Column(db.ForeignKey('layer3_sku.cart_sku_task.id'), index=True, info=' foreign key of cart_sku_task.id ')
    object_task_id = db.Column(db.ForeignKey('object_task.id'), index=True)
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    pallet_id = db.Column(db.ForeignKey('object.id'), index=True)
    station_id = db.Column(db.ForeignKey('layer3_sku.station.id'), index=True)
    dealed_quantity = db.Column(db.Integer, server_default=db.FetchedValue(), info='dealed quantity for the slot assingment row')
    is_finished = db.Column(db.Boolean, server_default=db.FetchedValue(), info='if the slot assignment row is finished')

    cart_sku_task = db.relationship('CartSkuTask', primaryjoin='SlotAssignment.cart_sku_task_id == CartSkuTask.id', backref='slot_assignments')
    object_task = db.relationship('ObjectTask', primaryjoin='SlotAssignment.object_task_id == ObjectTask.id', backref='slot_assignments')
    pallet = db.relationship('Object', primaryjoin='SlotAssignment.pallet_id == Object.id', backref='slot_assignments')
    sku_task_type = db.relationship('SkuTaskType', primaryjoin='SlotAssignment.sku_task_type_id == SkuTaskType.id', backref='slot_assignments')
    slot = db.relationship('Slot', primaryjoin='SlotAssignment.slot_id == Slot.id', backref='slot_assignments')
    station = db.relationship('Station', primaryjoin='SlotAssignment.station_id == Station.id', backref='slot_assignments')
    station_sku_task = db.relationship('StationSkuTask', primaryjoin='SlotAssignment.station_sku_task_id == StationSkuTask.id', backref='slot_assignments')



class SlotAssignmentTriggerLog(db.Model):
    __tablename__ = 'slot_assignment_trigger_log'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    log_type = db.Column(db.String(200))
    slot_assignment_id = db.Column(db.Integer)
    sku_task_type_id = db.Column(db.Integer)
    slot_id = db.Column(db.Integer)
    assign_quantity = db.Column(db.Integer)
    station_sku_task_id = db.Column(db.Integer)
    cart_sku_task_id = db.Column(db.Integer)
    object_task_id = db.Column(db.BigInteger)
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True))
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True))
    pallet_id = db.Column(db.Integer)
    station_id = db.Column(db.Integer)
    dealed_quantity = db.Column(db.Integer)
    is_finished = db.Column(db.Boolean, server_default=db.FetchedValue())
    log_created_timestamp = db.Column(db.DateTime(True))



class SlotPosition(db.Model):
    __tablename__ = 'slot_position'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' name of the slot position ')
    replen_priority = db.Column(db.Integer, info='replen priority of slot')
    description = db.Column(db.String(2000), info=' the description of slot position ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class SlotTriggerLog(db.Model):
    __tablename__ = 'slot_trigger_log'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    log_type = db.Column(db.String(200))
    slot_id = db.Column(db.Integer)
    pallet_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    slot_type_id = db.Column(db.Integer)
    slot_position_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    error_code_id = db.Column(db.Integer)
    batch_no = db.Column(db.String(200))
    validity_time = db.Column(db.DateTime(True))
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    error_code_array = db.Column(db.ARRAY(INTEGER()))
    log_created_timestamp = db.Column(db.DateTime(True))



class SlotType(db.Model):
    __tablename__ = 'slot_type'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), info=' the name of this slot ')
    divided = db.Column(db.Boolean, info=' if the slot is divided ')
    enabled = db.Column(db.Boolean, info=' if the slot type enabled ')
    length = db.Column(db.Float(53), info=' length of slot ')
    width = db.Column(db.Float(53), info=' width of slot ')
    height = db.Column(db.Float(53), info=' height of slot ')
    weight = db.Column(db.Float(53), info=' max weight the type of slot can hold ')
    description = db.Column(db.String(2000), info=' the description of this slot type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class Station(db.Model):
    __tablename__ = 'station'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this station ')
    location_id = db.Column(db.ForeignKey('location.id'), info=' location of station ')
    status = db.Column(db.String(200), info=' status of station like "normal","closed" ')
    user_name = db.Column(db.String(200), info=' login user name ')
    station_type_id = db.Column(db.ForeignKey('layer3_sku.station_type.id'), info=' station type ')
    station_label = db.Column(db.String(200), info=' label of station ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')

    location = db.relationship('Location', primaryjoin='Station.location_id == Location.id', backref='stations')
    station_type = db.relationship('StationType', primaryjoin='Station.station_type_id == StationType.id', backref='stations')



class StationConfig(db.Model):
    __tablename__ = 'station_config'
    __table_args__ = (
        db.UniqueConstraint('station_id', 'station_type_id', 'config_name'),
        {'schema': 'layer3_sku'}
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    station_id = db.Column(db.ForeignKey('layer3_sku.station.id'), info=' foreign key of station.id ')
    station_type_id = db.Column(db.ForeignKey('layer3_sku.station_type.id'), info=' foreign key of station_type.id ')
    config_name = db.Column(db.String(200), info=' name of config ')
    config_value = db.Column(db.String(200), info=' value of config ')
    enabled = db.Column(db.Boolean, info=' if the config enabled ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')

    station = db.relationship('Station', primaryjoin='StationConfig.station_id == Station.id', backref='station_configs')
    station_type = db.relationship('StationType', primaryjoin='StationConfig.station_type_id == StationType.id', backref='station_configs')



class StationSkuTask(db.Model):
    __tablename__ = 'station_sku_task'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    sku_task_type_id = db.Column(db.ForeignKey('layer3_sku.sku_task_type.id'), index=True, info=' sku task type,foreign key of sku_task_type.id ')
    sku_task_status_id = db.Column(db.ForeignKey('layer3_sku.sku_task_status.id'), index=True, info=' status of task ')
    batch_no = db.Column(db.String(200), info=' batch number of sku task ')
    cart_id = db.Column(db.ForeignKey('cart.id'), index=True, info=' foreign key of cart.id ')
    item_id = db.Column(db.ForeignKey('layer3_sku.item.id'), index=True, info=' foreign key of item.id ')
    quantity = db.Column(db.Integer, info=' order quantity ')
    dealed_quantity = db.Column(db.Integer, info=' dealed quantity ')
    station_id = db.Column(db.Integer, index=True, info=' foreign key of station.id ')
    required_arrival_time = db.Column(db.DateTime(True), info=' required finish time of the task ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    error_code = db.Column(db.Integer, server_default=db.FetchedValue(), info='reason why the station_sku_task is error')
    validity_time = db.Column(db.DateTime(True), info='validity time of the replen task for the sku')

    cart = db.relationship('Cart', primaryjoin='StationSkuTask.cart_id == Cart.id', backref='station_sku_tasks')
    item = db.relationship('Item', primaryjoin='StationSkuTask.item_id == Item.id', backref='station_sku_tasks')
    sku_task_status = db.relationship('SkuTaskStatu', primaryjoin='StationSkuTask.sku_task_status_id == SkuTaskStatu.id', backref='station_sku_tasks')
    sku_task_type = db.relationship('SkuTaskType', primaryjoin='StationSkuTask.sku_task_type_id == SkuTaskType.id', backref='station_sku_tasks')



class StationType(db.Model):
    __tablename__ = 'station_type'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this station type ')
    description = db.Column(db.String(2000), info=' the description of this station type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class UserTask(db.Model):
    __tablename__ = 'user_task'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    user_task_type_id = db.Column(db.ForeignKey('layer3_sku.user_task_type.id'), index=True)
    user_task_status_id = db.Column(db.ForeignKey('layer3_sku.sku_task_status.id'), index=True)
    item_id = db.Column(db.Integer)
    batch_no = db.Column(db.String(200))
    pallet_id = db.Column(db.ForeignKey('object.id'))
    slot_id = db.Column(db.Integer)
    station_id = db.Column(db.ForeignKey('layer3_sku.station.id'), index=True)
    required_arrival_time = db.Column(db.DateTime(True))
    error_code = db.Column(db.Integer)
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    order_no = db.Column(db.String(200))
    error_reason = db.Column(db.String(200))

    pallet = db.relationship('Object', primaryjoin='UserTask.pallet_id == Object.id', backref='user_tasks')
    station = db.relationship('Station', primaryjoin='UserTask.station_id == Station.id', backref='user_tasks')
    user_task_status = db.relationship('SkuTaskStatu', primaryjoin='UserTask.user_task_status_id == SkuTaskStatu.id', backref='user_tasks')
    user_task_type = db.relationship('UserTaskType', primaryjoin='UserTask.user_task_type_id == UserTaskType.id', backref='user_tasks')



class UserTaskToObject(db.Model):
    __tablename__ = 'user_task_to_object'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    user_task_id = db.Column(db.Integer, index=True)
    user_task_status_id = db.Column(db.Integer, index=True)
    slot_id = db.Column(db.Integer)
    object_id = db.Column(db.Integer, index=True)
    station_id = db.Column(db.Integer, index=True)
    object_task_id = db.Column(db.Integer)
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class UserTaskToPtcObject(db.Model):
    __tablename__ = 'user_task_to_ptc_object'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    user_task_id = db.Column(db.Integer, index=True)
    user_task_status_id = db.Column(db.Integer, index=True)
    slot_id = db.Column(db.Integer)
    object_id = db.Column(db.Integer, index=True)
    created_user = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    last_updated_user = db.Column(db.String(200))
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue())



class UserTaskType(db.Model):
    __tablename__ = 'user_task_type'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this user task type ')
    catagory = db.Column(db.String(200), info=' the catagory of this user task type ')
    description = db.Column(db.String(2000), info=' the description of this user task type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



t_view_active_cart_task_info = db.Table(
    'view_active_cart_task_info',
    db.Column('cart_id', db.Integer),
    db.Column('cart_status', db.Integer),
    db.Column('cart_type', db.String(200)),
    db.Column('cart_object_id', db.Integer),
    db.Column('cart_label', db.String(200)),
    db.Column('bound_agv', db.Integer),
    db.Column('current_station', db.String(200)),
    db.Column('start_location', db.String(200)),
    db.Column('current_location', db.String(200)),
    db.Column('next_location', db.String(200)),
    db.Column('sku_task_type', db.String),
    db.Column('sku_task_id', db.Integer),
    db.Column('sku_task_item', db.Integer),
    db.Column('sku_task_status', db.String(200)),
    db.Column('slot_assignment_id', db.Integer),
    db.Column('slot_id', db.Integer),
    db.Column('assign_quantity', db.Integer),
    db.Column('object_task_id', db.BigInteger),
    db.Column('task_type', db.String(200)),
    db.Column('task_status', db.String(200)),
    db.Column('pallet_id', db.Integer),
    db.Column('pallet_label', db.String(200)),
    db.Column('destination_location', db.String(200)),
    schema='layer3_sku'
)



t_view_g2p_pickinfo = db.Table(
    'view_g2p_pickinfo',
    db.Column('rowno', db.BigInteger),
    db.Column('slot_assignment_id', db.Integer),
    db.Column('slot_id', db.Integer),
    db.Column('pallet_id', db.Integer),
    db.Column('pallet_name', db.String(200)),
    db.Column('assign_quantity', db.Integer),
    db.Column('slot_qty', db.Integer),
    db.Column('sku_task_id', db.Integer),
    db.Column('object_task_id', db.BigInteger),
    db.Column('item_id', db.Integer),
    db.Column('batch_no', db.String(200)),
    db.Column('quantity', db.Integer),
    db.Column('dealed_quantity', db.Integer),
    db.Column('status', db.String(200)),
    db.Column('cart_id', db.Integer),
    db.Column('cart_name', db.String(200)),
    db.Column('station_id', db.Integer),
    db.Column('pallet_location_id', db.Integer),
    db.Column('pallet_location', db.String(200)),
    db.Column('cart_location_id', db.Integer),
    db.Column('cart_location', db.String(200)),
    db.Column('cart_status', db.Integer),
    db.Column('next_location', db.Integer),
    db.Column('cart_next_location', db.String(200)),
    db.Column('destination_location_id', db.Integer),
    db.Column('dest_location', db.String(200)),
    db.Column('location_priority', db.Integer),
    db.Column('object_status', db.Text),
    db.Column('sku_task_type_id', db.Integer),
    db.Column('task_type', db.String(200)),
    db.Column('canpick', db.Boolean),
    db.Column('error_code', db.Integer),
    db.Column('error_msg', db.String(200)),
    db.Column('pallet_priority', db.BigInteger),
    schema='layer3_sku'
)



t_view_g2p_repleninfo = db.Table(
    'view_g2p_repleninfo',
    db.Column('slot_assignment_id', db.Integer),
    db.Column('slot_id', db.Integer),
    db.Column('pallet_id', db.Integer),
    db.Column('pallet_name', db.String(200)),
    db.Column('assign_quantity', db.Integer),
    db.Column('slot_qty', db.Integer),
    db.Column('sku_task_id', db.Integer),
    db.Column('object_task_id', db.BigInteger),
    db.Column('item_id', db.Integer),
    db.Column('batch_no', db.String(200)),
    db.Column('quantity', db.Integer),
    db.Column('dealed_quantity', db.Integer),
    db.Column('status', db.String(200)),
    db.Column('cart_id', db.Integer),
    db.Column('station_id', db.Integer),
    db.Column('pallet_location_id', db.Integer),
    db.Column('pallet_location', db.String(200)),
    db.Column('cart_location_id', db.Integer),
    db.Column('cart_location', db.String(200)),
    db.Column('cart_status', db.Integer),
    db.Column('next_location', db.Integer),
    db.Column('cart_next_location', db.String(200)),
    db.Column('destination_location_id', db.Integer),
    db.Column('dest_location', db.String(200)),
    db.Column('priority', db.Integer),
    db.Column('object_status', db.String(200)),
    db.Column('canpick', db.Boolean),
    schema='layer3_sku'
)



t_view_gtp_ic_info = db.Table(
    'view_gtp_ic_info',
    db.Column('rowno', db.BigInteger),
    db.Column('user_task_id', db.Integer),
    db.Column('error_reason', db.String(200)),
    db.Column('operation_id', db.Integer),
    db.Column('user_task_to_object_status', db.String(200)),
    db.Column('item_id', db.Integer),
    db.Column('item_name', db.String(200)),
    db.Column('description', db.String(2000)),
    db.Column('item_upc', db.ARRAY(VARCHAR())),
    db.Column('area_type', db.String(200)),
    db.Column('sku_no', db.String(200)),
    db.Column('slot_id', db.Integer),
    db.Column('max_limit_num', db.Integer),
    db.Column('quantity', db.Integer),
    db.Column('slot_position', db.String),
    db.Column('slot_position_id', db.Integer),
    db.Column('object_id', db.Integer),
    db.Column('pallet_name', db.String(200)),
    db.Column('station_label', db.String(200)),
    db.Column('object_task_id', db.Integer),
    db.Column('current_location_id', db.Integer),
    db.Column('pallet_current_location', db.String(200)),
    db.Column('destination_location_id', db.Integer),
    db.Column('destination_location_name', db.String(200)),
    db.Column('priority', db.Integer),
    db.Column('object_status', db.Text),
    schema='layer3_sku'
)



t_view_p2c_pickinfo = db.Table(
    'view_p2c_pickinfo',
    db.Column('rowno', db.BigInteger),
    db.Column('slot_assignment_id', db.Integer),
    db.Column('slot_id', db.Integer),
    db.Column('pallet_id', db.Integer),
    db.Column('pallet_name', db.String(200)),
    db.Column('assign_quantity', db.Integer),
    db.Column('slot_qty', db.Integer),
    db.Column('sku_task_id', db.Integer),
    db.Column('object_task_id', db.BigInteger),
    db.Column('item_id', db.Integer),
    db.Column('batch_no', db.String(200)),
    db.Column('quantity', db.Integer),
    db.Column('dealed_quantity', db.Integer),
    db.Column('line_status', db.String(200)),
    db.Column('cart_id', db.Integer),
    db.Column('cart_name', db.String(200)),
    db.Column('station_id', db.Integer),
    db.Column('pallet_location_id', db.Integer),
    db.Column('pallet_location', db.String(200)),
    db.Column('cart_location_id', db.Integer),
    db.Column('cart_location', db.String(200)),
    db.Column('cart_status', db.Integer),
    db.Column('next_location', db.Integer),
    db.Column('cart_next_location', db.String(200)),
    db.Column('current_location_id', db.Integer),
    db.Column('dest_location', db.String(200)),
    db.Column('location_priority', db.Integer),
    db.Column('object_status', db.Text),
    db.Column('sku_task_type_id', db.Integer),
    db.Column('task_type', db.String(200)),
    db.Column('canpick', db.Boolean),
    db.Column('error_code', db.Integer),
    db.Column('error_msg', db.String(200)),
    db.Column('pallet_priority', db.Integer),
    schema='layer3_sku'
)



t_view_ptc_ic_info = db.Table(
    'view_ptc_ic_info',
    db.Column('rowno', db.BigInteger),
    db.Column('user_task_id', db.Integer),
    db.Column('error_reason', db.String(200)),
    db.Column('operation_id', db.Integer),
    db.Column('user_task_to_ptc_object_status', db.String(200)),
    db.Column('item_id', db.Integer),
    db.Column('item_name', db.String(200)),
    db.Column('description', db.String(2000)),
    db.Column('item_upc', db.ARRAY(VARCHAR())),
    db.Column('area_type', db.String(200)),
    db.Column('sku_no', db.String(200)),
    db.Column('slot_id', db.Integer),
    db.Column('max_limit_num', db.Integer),
    db.Column('quantity', db.Integer),
    db.Column('slot_position', db.String),
    db.Column('slot_position_id', db.Integer),
    db.Column('object_id', db.Integer),
    db.Column('pallet_name', db.String(200)),
    db.Column('station_label', db.String),
    db.Column('object_task_id', db.Integer),
    db.Column('current_location_id', db.Integer),
    db.Column('pallet_current_location', db.String(200)),
    db.Column('destination_location_id', db.Integer),
    db.Column('destination_location_name', db.String(200)),
    db.Column('priority', db.Integer),
    db.Column('object_status', db.Text),
    schema='layer3_sku'
)



class WmsLocation(db.Model):
    __tablename__ = 'wms_location'
    __table_args__ = {'schema': 'layer3_sku'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    type = db.Column(db.Integer, info=' 1 for PTC,2 for GTP ')
    name = db.Column(db.String(200), info=' wms location name ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
