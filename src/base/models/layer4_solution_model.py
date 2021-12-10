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



class CartSkuTask(db.Model):
    __tablename__ = 'cart_sku_task'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    sku_task_type_id = db.Column(db.ForeignKey('sku_task_type.id'), index=True, info=' the name of this sku_task type ')
    sku_task_status_id = db.Column(db.ForeignKey('sku_task_status.id'), index=True, info=' status of task ')
    batch_no = db.Column(db.String(200), info=' batch number of sku task ')
    cart_id = db.Column(db.ForeignKey('cart.id'), index=True, info=' foreign key of cart.id ')
    item_id = db.Column(db.ForeignKey('item.id'), index=True, info=' foreign key of item.id ')
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



class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    item_category_id = db.Column(db.ForeignKey('item_category.id'), index=True)
    item_type_id = db.Column(db.ForeignKey('item_type.id'), index=True, info=' item type, foreign key of item_type.id ')
    wms_location_id = db.Column(db.ForeignKey('wms_location.id'), info=' wms location,foreign key of wms_location.id ')
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

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this item category ')
    description = db.Column(db.String(2000), info=' the description of this item category ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class ItemType(db.Model):
    __tablename__ = 'item_type'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this item type ')
    description = db.Column(db.String(2000), info=' the description of this item type ')
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



class SkuTaskStatu(db.Model):
    __tablename__ = 'sku_task_status'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this sku_task status ')
    description = db.Column(db.String(2000), info=' the description of this sku_task status ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class SkuTaskType(db.Model):
    __tablename__ = 'sku_task_type'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this sku_task type ')
    description = db.Column(db.String(2000), info=' the description of this sku_task type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class Station(db.Model):
    __tablename__ = 'station'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this station ')
    location_id = db.Column(db.ForeignKey('location.id'), info=' location of station ')
    status = db.Column(db.String(200), info=' status of station like "normal","closed" ')
    user_name = db.Column(db.String(200), info=' login user name ')
    station_type_id = db.Column(db.ForeignKey('station_type.id'), info=' station type ')
    station_label = db.Column(db.String(200), info=' label of station ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')

    location = db.relationship('Location', primaryjoin='Station.location_id == Location.id', backref='stations')
    station_type = db.relationship('StationType', primaryjoin='Station.station_type_id == StationType.id', backref='stations')



class StationSkuTask(db.Model):
    __tablename__ = 'station_sku_task'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    sku_task_type_id = db.Column(db.ForeignKey('sku_task_type.id'), index=True, info=' sku task type,foreign key of sku_task_type.id ')
    sku_task_status_id = db.Column(db.ForeignKey('sku_task_status.id'), index=True, info=' status of task ')
    batch_no = db.Column(db.String(200), info=' batch number of sku task ')
    cart_id = db.Column(db.ForeignKey('cart.id'), index=True, info=' foreign key of cart.id ')
    item_id = db.Column(db.ForeignKey('item.id'), index=True, info=' foreign key of item.id ')
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

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this station type ')
    description = db.Column(db.String(2000), info=' the description of this station type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class UserTask(db.Model):
    __tablename__ = 'user_task'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    user_task_type_id = db.Column(db.ForeignKey('user_task_type.id'), index=True)
    user_task_status_id = db.Column(db.ForeignKey('sku_task_status.id'), index=True)
    item_id = db.Column(db.Integer)
    batch_no = db.Column(db.String(200))
    pallet_id = db.Column(db.ForeignKey('object.id'))
    slot_id = db.Column(db.Integer)
    station_id = db.Column(db.ForeignKey('station.id'), index=True)
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



class UserTaskType(db.Model):
    __tablename__ = 'user_task_type'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this user task type ')
    catagory = db.Column(db.String(200), info=' the catagory of this user task type ')
    description = db.Column(db.String(2000), info=' the description of this user task type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class WmsLocation(db.Model):
    __tablename__ = 'wms_location'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    type = db.Column(db.Integer, info=' 1 for PTC,2 for GTP ')
    name = db.Column(db.String(200), info=' wms location name ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class Area(db.Model):
    __tablename__ = 'area'
    __table_args__ = {'schema': 'layer4_solution'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    area_type_id = db.Column(db.ForeignKey('layer4_solution.area_type.id'), info=' the name of this area type ')
    access_location_id = db.Column(db.ForeignKey('location.id'), info=' access location id of area ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')

    access_location = db.relationship('Location', primaryjoin='Area.access_location_id == Location.id', backref='areas')
    area_type = db.relationship('AreaType', primaryjoin='Area.area_type_id == AreaType.id', backref='areas')



class AreaType(db.Model):
    __tablename__ = 'area_type'
    __table_args__ = {'schema': 'layer4_solution'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this area type ')
    description = db.Column(db.String(2000), info=' the description of this area type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class CartArea(db.Model):
    __tablename__ = 'cart_area'
    __table_args__ = {'schema': 'layer4_solution'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    cart_id = db.Column(db.ForeignKey('cart.id'), index=True, info=' foreign key of cart.id ')
    area_id = db.Column(db.ForeignKey('layer4_solution.area.id'), index=True, info=' foreign key of area.id ')
    priority = db.Column(db.Integer, info=' priority of area ')
    commit_status = db.Column(db.Integer, info=' status of cart area ')
    active = db.Column(db.Boolean, info=' if the cart finished the area ')
    predicted_arrival_time = db.Column(db.DateTime(True), info=' predicted arrival time of the cart goto the area ')
    actual_arrival_time = db.Column(db.DateTime(True), info=' actual arrival time of the cart goto the area ')
    determined_eta = db.Column(db.DateTime(True), info=' determined_eta ')
    determined_sequence = db.Column(db.Integer, info=' access sequence of the area ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')

    area = db.relationship('Area', primaryjoin='CartArea.area_id == Area.id', backref='cart_areas')
    cart = db.relationship('Cart', primaryjoin='CartArea.cart_id == Cart.id', backref='cart_areas')



class CartContainer(db.Model):
    __tablename__ = 'cart_container'
    __table_args__ = {'schema': 'layer4_solution'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    cart_id = db.Column(db.ForeignKey('cart.id'), index=True, info=' foreign key of cart.id ')
    container_id = db.Column(db.ForeignKey('layer4_solution.container.id'), index=True, info=' foreign key of container.id ')
    position_in_cart = db.Column(db.Integer, info=' container position in cart ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    order_group_id = db.Column(db.ForeignKey('layer4_solution.order_group.id'))

    cart = db.relationship('Cart', primaryjoin='CartContainer.cart_id == Cart.id', backref='cart_containers')
    container = db.relationship('Container', primaryjoin='CartContainer.container_id == Container.id', backref='cart_containers')
    order_group = db.relationship('OrderGroup', primaryjoin='CartContainer.order_group_id == OrderGroup.id', backref='cart_containers')



class Container(db.Model):
    __tablename__ = 'container'
    __table_args__ = {'schema': 'layer4_solution'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this container ')
    length = db.Column(db.Float(53))
    width = db.Column(db.Float(53))
    height = db.Column(db.Float(53))
    weight = db.Column(db.Float(53))
    container_status_id = db.Column(db.ForeignKey('layer4_solution.container_status.id'))
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    container_type_id = db.Column(db.ForeignKey('layer4_solution.container_type.id'))
    order_group_id = db.Column(db.ForeignKey('layer4_solution.order_group.id'))

    container_status = db.relationship('ContainerStatu', primaryjoin='Container.container_status_id == ContainerStatu.id', backref='containers')
    container_type = db.relationship('ContainerType', primaryjoin='Container.container_type_id == ContainerType.id', backref='containers')
    order_group = db.relationship('OrderGroup', primaryjoin='Container.order_group_id == OrderGroup.id', backref='containers')



class ContainerLine(db.Model):
    __tablename__ = 'container_line'
    __table_args__ = {'schema': 'layer4_solution'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    cart_container_id = db.Column(db.ForeignKey('layer4_solution.cart_container.id'), index=True, info=' container id ')
    order_line_id = db.Column(db.ForeignKey('layer4_solution.order_line.id'), index=True, info=' order line id ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')

    cart_container = db.relationship('CartContainer', primaryjoin='ContainerLine.cart_container_id == CartContainer.id', backref='container_lines')
    order_line = db.relationship('OrderLine', primaryjoin='ContainerLine.order_line_id == OrderLine.id', backref='container_lines')



class ContainerStatu(db.Model):
    __tablename__ = 'container_status'
    __table_args__ = {'schema': 'layer4_solution'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this container_status ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class ContainerType(db.Model):
    __tablename__ = 'container_type'
    __table_args__ = {'schema': 'layer4_solution'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this container_type ')
    description = db.Column(db.String(2000), info=' the description of this container_type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class OrderGroup(db.Model):
    __tablename__ = 'order_group'
    __table_args__ = {'schema': 'layer4_solution'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    order_type_id = db.Column(db.ForeignKey('layer4_solution.order_type.id'), index=True, info=' order type of this order group, FOREIGN KEY of order_type.id')
    order_group_status_id = db.Column(db.ForeignKey('layer4_solution.order_group_status.id'), index=True, info=' order group status, FOREIGN KEY of order_group_status.id')
    request_physical_container_type = db.Column(db.ForeignKey('layer4_solution.container_type.id'), info=' the request physical container type of this order group, FOREIGN KEY of container_type.id')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    cart_id = db.Column(db.ForeignKey('cart.id'), index=True)

    cart = db.relationship('Cart', primaryjoin='OrderGroup.cart_id == Cart.id', backref='order_groups')
    order_group_status = db.relationship('OrderGroupStatu', primaryjoin='OrderGroup.order_group_status_id == OrderGroupStatu.id', backref='order_groups')
    order_type = db.relationship('OrderType', primaryjoin='OrderGroup.order_type_id == OrderType.id', backref='order_groups')
    container_type = db.relationship('ContainerType', primaryjoin='OrderGroup.request_physical_container_type == ContainerType.id', backref='order_groups')



class OrderGroupDetail(db.Model):
    __tablename__ = 'order_group_detail'
    __table_args__ = {'schema': 'layer4_solution'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    order_group_id = db.Column(db.ForeignKey('layer4_solution.order_group.id'), index=True, info=' order group id, FOREIGN KEY of order_group.id')
    order_info_id = db.Column(db.ForeignKey('layer4_solution.order_info.id'), index=True, info=' order info id, FOREIGN KEY of order_info.id')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    order_line_id = db.Column(db.ForeignKey('layer4_solution.order_line.id'), index=True, info='foreign key of order_line.id')

    order_group = db.relationship('OrderGroup', primaryjoin='OrderGroupDetail.order_group_id == OrderGroup.id', backref='order_group_details')
    order_info = db.relationship('OrderInfo', primaryjoin='OrderGroupDetail.order_info_id == OrderInfo.id', backref='order_group_details')
    order_line = db.relationship('OrderLine', primaryjoin='OrderGroupDetail.order_line_id == OrderLine.id', backref='order_group_details')



class OrderGroupStatu(db.Model):
    __tablename__ = 'order_group_status'
    __table_args__ = {'schema': 'layer4_solution'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this order_group_status ')
    description = db.Column(db.String(2000), info=' the description of this order_group_status ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class OrderInfo(db.Model):
    __tablename__ = 'order_info'
    __table_args__ = {'schema': 'layer4_solution'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    order_type_id = db.Column(db.ForeignKey('layer4_solution.order_type.id'), index=True, info=' order type,foreign key of order_type.id ')
    batch_no = db.Column(db.String(200), info=' the description of this order type ')
    order_no = db.Column(db.String(200), index=True, info=' order number ')
    order_status_id = db.Column(db.ForeignKey('layer4_solution.order_status.id'), index=True, info=' status of order ')
    length = db.Column(db.Float(53), info=' length of order  ')
    width = db.Column(db.Float(53), info=' width of order  ')
    height = db.Column(db.Float(53), info=' height of order  ')
    weight = db.Column(db.Float(53), info=' weight of order  ')
    required_arrival_time = db.Column(db.DateTime(True), info=' required finish time of the task ')
    destination_location_id = db.Column(db.Integer, info=' destination location the order will goto,foreign key of location.id ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    wave_no = db.Column(db.String(200), index=True, info='one container should not include two or more different wave_no order')
    priority = db.Column(db.Float(53), nullable=False, server_default=db.FetchedValue())
    order_subtype_id = db.Column(db.Integer, info=' order sub type,foreign key of order_type.id ')
    cart_type_id = db.Column(db.ForeignKey('cart_type.id'), info='this order should be completed by which type cart')

    cart_type = db.relationship('CartType', primaryjoin='OrderInfo.cart_type_id == CartType.id', backref='order_infos')
    order_status = db.relationship('OrderStatu', primaryjoin='OrderInfo.order_status_id == OrderStatu.id', backref='order_infos')
    order_type = db.relationship('OrderType', primaryjoin='OrderInfo.order_type_id == OrderType.id', backref='order_infos')



class OrderLine(db.Model):
    __tablename__ = 'order_line'
    __table_args__ = (
        db.UniqueConstraint('order_info_id', 'line_no'),
        {'schema': 'layer4_solution'}
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    order_type_id = db.Column(db.ForeignKey('layer4_solution.order_type.id'), index=True, info=' order type,foreign key of order_type.id ')
    order_info_id = db.Column(db.ForeignKey('layer4_solution.order_info.id'), index=True, info=' foreign key of order_info.id ')
    item_id = db.Column(db.ForeignKey('item.id'), index=True, info=' foreign key of item.id ')
    line_no = db.Column(db.Integer, info=' line number in same order ')
    quantity = db.Column(db.Integer, info=' order quantity ')
    dealed_quantity = db.Column(db.Integer, info=' dealed quantity ')
    order_status_id = db.Column(db.ForeignKey('layer4_solution.order_status.id'), index=True, info=' status of line ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    container_label = db.Column(db.String(64), info='the name of this container')
    batch_no = db.Column(db.String(200), info=' the description of this line type ')

    item = db.relationship('Item', primaryjoin='OrderLine.item_id == Item.id', backref='order_lines')
    order_info = db.relationship('OrderInfo', primaryjoin='OrderLine.order_info_id == OrderInfo.id', backref='order_lines')
    order_status = db.relationship('OrderStatu', primaryjoin='OrderLine.order_status_id == OrderStatu.id', backref='order_lines')
    order_type = db.relationship('OrderType', primaryjoin='OrderLine.order_type_id == OrderType.id', backref='order_lines')



class OrderSkuTask(db.Model):
    __tablename__ = 'order_sku_task'
    __table_args__ = {'schema': 'layer4_solution'}

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    order_line_id = db.Column(db.ForeignKey('layer4_solution.order_line.id'), index=True, info=' foreign key of order_line.id ')
    station_sku_task_id = db.Column(db.ForeignKey('station_sku_task.id'), index=True, info=' sku task id ')
    cart_sku_task_id = db.Column(db.ForeignKey('cart_sku_task.id'), index=True, info=' sku task id ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    cart_id = db.Column(db.Integer, index=True, info='foreign key of cart.id')
    user_task_id = db.Column(db.ForeignKey('user_task.id'), index=True, info='foreign key of user_task.id')

    cart_sku_task = db.relationship('CartSkuTask', primaryjoin='OrderSkuTask.cart_sku_task_id == CartSkuTask.id', backref='order_sku_tasks')
    order_line = db.relationship('OrderLine', primaryjoin='OrderSkuTask.order_line_id == OrderLine.id', backref='order_sku_tasks')
    station_sku_task = db.relationship('StationSkuTask', primaryjoin='OrderSkuTask.station_sku_task_id == StationSkuTask.id', backref='order_sku_tasks')
    user_task = db.relationship('UserTask', primaryjoin='OrderSkuTask.user_task_id == UserTask.id', backref='order_sku_tasks')



class OrderStatu(db.Model):
    __tablename__ = 'order_status'
    __table_args__ = {'schema': 'layer4_solution'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this order_status ')
    description = db.Column(db.String(2000))
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')



class OrderType(db.Model):
    __tablename__ = 'order_type'
    __table_args__ = {'schema': 'layer4_solution'}

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue(), info=' the internal id to identify a record ')
    name = db.Column(db.String(200), unique=True, info=' the name of this order type ')
    description = db.Column(db.String(2000), info=' the description of this order type ')
    created_user = db.Column(db.String(200), info=' the user name that created this record ')
    created_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when created this record ')
    last_updated_user = db.Column(db.String(200), info=' the user name that updated this record most recently ')
    last_updated_timestamp = db.Column(db.DateTime(True), server_default=db.FetchedValue(), info=' the timestamp when updated this record most recently ')
    catagory = db.Column(db.String(200))



t_view_active_cart_order_info = db.Table(
    'view_active_cart_order_info',
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
    db.Column('position_in_cart', db.Integer),
    db.Column('container_name', db.String(200)),
    db.Column('container_status', db.String(200)),
    db.Column('order_group_id', db.Integer),
    db.Column('order_group_status', db.String(200)),
    db.Column('order_info_id', db.Integer),
    db.Column('order_line_id', db.Integer),
    db.Column('station_sku_task_id', db.Integer),
    db.Column('cart_sku_task_id', db.Integer),
    schema='layer4_solution'
)



t_view_area_info = db.Table(
    'view_area_info',
    db.Column('id', db.Integer),
    db.Column('area_type_name', db.String(200)),
    db.Column('location_name', db.String(200)),
    db.Column('location_type', db.String(200)),
    schema='layer4_solution'
)



t_view_order_info = db.Table(
    'view_order_info',
    db.Column('rowno', db.BigInteger),
    db.Column('order_id', db.String(200)),
    db.Column('order_type', db.String(200)),
    db.Column('batch_no', db.String(200)),
    db.Column('wave_no', db.String(200)),
    db.Column('item_id', db.Integer),
    db.Column('quantity', db.Integer),
    db.Column('dealed_quantity', db.Integer),
    db.Column('line_id', db.Integer),
    db.Column('line_status_id', db.Integer),
    db.Column('order_status_id', db.Integer),
    db.Column('order_status', db.String(200)),
    db.Column('line_status', db.String(200)),
    db.Column('cart_id', db.Integer),
    db.Column('cart_name', db.String(200)),
    db.Column('order_group_id', db.String),
    db.Column('position_in_cart', db.Integer),
    db.Column('cart_sku_task_id', db.Integer),
    db.Column('station_sku_task_id', db.Integer),
    db.Column('container_label', db.String),
    db.Column('order_priority', db.Float(53)),
    schema='layer4_solution'
)
