import datetime
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import VARCHAR, DATE
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from db.database import Base


class InventoryInfo(Base):
    __tablename__ = "inventory_info"

    uid = Column(UUIDType(binary=False), unique=True, primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR, nullable=False)
    receipt_data = Column(DATE, default=datetime.datetime.now())
    model = Column(VARCHAR, nullable=False)
    document = Column(VARCHAR, nullable=False)
    date_of_registration = Column(DATE)
    cost = Column(VARCHAR, nullable=False)
    useful_life = Column(DATE)
    note = Column(VARCHAR, nullable=False)
    write_off_day = Column(DATE)
    inventory_number = Column(VARCHAR, index=True, nullable=False, unique=True)
    inventory_serial = Column(VARCHAR)
    responsible_uid = Column(UUIDType(binary=False), ForeignKey("employee.uid"), index=True)
    object_types_uid = Column(UUIDType(binary=False), ForeignKey("object_types.uid"), index=True)

    object_type = relationship("ObjectTypes", lazy="joined", innerjoin=True)
    responsible = relationship("Employee", lazy="joined", innerjoin=True)


class ObjectTypes(Base):
    __tablename__ = "object_types"

    uid = Column(UUIDType(binary=False), unique=True, primary_key=True, default=uuid.uuid4)
    description = Column(VARCHAR, nullable=False)


class Employee(Base):
    __tablename__ = "employee"

    uid = Column(UUIDType(binary=False), unique=True, primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR, nullable=False)
    surname = Column(VARCHAR, nullable=False)
    patronymicon = Column(VARCHAR)
    position = Column(VARCHAR, nullable=False)
    status = Column(VARCHAR, nullable=False)
    departments_uid = Column(ForeignKey("departments.uid"))
    room_uid = Column(ForeignKey("rooms.uid"))

    department = relationship("Departments", lazy="joined", innerjoin=True)
    room = relationship("Rooms", lazy="joined", innerjoin=True)


class Departments(Base):
    __tablename__ = "departments"

    uid = Column(UUIDType(binary=False), unique=True, primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR, nullable=False)


class Rooms(Base):
    __tablename__ = "rooms"

    uid = Column(UUIDType(binary=False), unique=True, primary_key=True, default=uuid.uuid4)
    floor = Column(Integer, nullable=False)
    number = Column(VARCHAR, nullable=False)


class InventoryCard(Base):
    __tablename__ = "inventory_card"

    uid = Column(UUIDType(binary=False), unique=True, primary_key=True, default=uuid.uuid4)
    employee_uid = Column(ForeignKey("employee.uid"), nullable=False, index=True)
    inventory_info_uid = Column(ForeignKey("inventory_info.uid"), nullable=False, index=True)
    room_uid = Column(ForeignKey("rooms.uid"), nullable=False, index=True)

    employee = relationship("Employee", lazy="joined", innerjoin=True)
    inventory_info = relationship("InventoryInfo", lazy="joined", innerjoin=True)
    room = relationship("Rooms", lazy="joined", innerjoin=True)


class Movements(Base):
    __tablename__ = "movements"

    uid = Column(UUIDType(binary=False), unique=True, primary_key=True, default=uuid.uuid4)
    date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    reason = Column(VARCHAR)
    from_employee_uid = Column(ForeignKey("employee.uid"), nullable=False)
    to_employee_uid = Column(ForeignKey("employee.uid"), nullable=False)
    inventory_card_uid = Column(ForeignKey("inventory_card.uid"))

    from_employee = relationship("Employee", lazy="joined", innerjoin=True, foreign_keys=[from_employee_uid])
    to_employee = relationship("Employee", lazy="joined", innerjoin=True, foreign_keys=[to_employee_uid])
    inventory_card = relationship("InventoryCard", lazy="joined", innerjoin=True, foreign_keys=[inventory_card_uid])


class TempInventoryCard(Base):
    __tablename__ = "temp_inventory_card"

    uid = Column(UUIDType(binary=False), unique=True, primary_key=True, default=uuid.uuid4)
    date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    employee_uid = Column(ForeignKey("employee.uid"), nullable=False)
    room_uid_id = Column(ForeignKey("rooms.uid"), nullable=False)
    inventory_info_uid = Column(ForeignKey("inventory_info.uid"), nullable=False)

    employee = relationship("Employee", lazy="joined", innerjoin=True)
    inventory_info = relationship("InventoryInfo", lazy="joined", innerjoin=True)
    room = relationship("Rooms", lazy="joined", innerjoin=True)
