import datetime
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import VARCHAR, DATE, UUID
from sqlalchemy.orm import relationship, column_property
from db.database import Base


class InventoryInfo(Base):
    __tablename__ = "inventory_info"

    uid = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR, nullable=False)
    receipt_data = Column(DateTime, default=datetime.datetime.now())
    model = Column(VARCHAR, nullable=False)
    document = Column(VARCHAR, nullable=False)
    date_of_registration = Column(DateTime)
    cost = Column(VARCHAR, nullable=False)
    useful_life = Column(DateTime)
    note = Column(VARCHAR, nullable=False)
    write_off_day = Column(DateTime)
    inventory_number = Column(VARCHAR, index=True, nullable=False, unique=True)
    inventory_serial = Column(VARCHAR)
    responsible_uid = Column(UUID(as_uuid=True), ForeignKey("employee.uid"), index=True)
    object_types_uid = Column(UUID(as_uuid=True), ForeignKey("object_types.uid"), index=True)

    object_type = relationship("ObjectTypes", lazy="joined", innerjoin=True)
    responsible = relationship("Employee", lazy="joined", innerjoin=True)


class ObjectTypes(Base):
    __tablename__ = "object_types"

    uid = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    description = Column(VARCHAR, nullable=False)


class Employee(Base):
    __tablename__ = "employee"

    uid = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR, nullable=False)
    surname = Column(VARCHAR, nullable=False)
    patronymicon = Column(VARCHAR)
    fullname = column_property(name + " " + surname + " " + patronymicon)
    position = Column(VARCHAR, nullable=False)
    status = Column(VARCHAR, nullable=False)
    departments_uid = Column(ForeignKey("departments.uid"))
    room_uid = Column(ForeignKey("rooms.uid"))

    department = relationship("Departments", innerjoin=True, lazy="joined")
    room = relationship("Rooms", innerjoin=True, lazy="joined")
    temp_inventory_card = relationship('TempInventoryCard', back_populates='employee')


class Departments(Base):
    __tablename__ = "departments"

    uid = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR, nullable=False)


class Rooms(Base):
    __tablename__ = "rooms"

    uid = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    floor = Column(Integer, nullable=False)
    number = Column(VARCHAR, nullable=False)

    temp_inventory_card = relationship('TempInventoryCard', back_populates='room')


class InventoryCard(Base):
    __tablename__ = "inventory_card"

    uid = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    employee_uid = Column(ForeignKey("employee.uid"), nullable=False, index=True)
    inventory_info_uid = Column(ForeignKey("inventory_info.uid"), nullable=False, index=True, unique=True)
    room_uid = Column(ForeignKey("rooms.uid"), nullable=False, index=True)

    employee = relationship("Employee", lazy="joined", innerjoin=True)
    inventory_info = relationship("InventoryInfo", lazy="joined", innerjoin=True)
    room = relationship("Rooms", lazy="joined", innerjoin=True)
    temp_inventory_card = relationship("TempInventoryCard", back_populates="inventory_card")


class Movements(Base):
    __tablename__ = "movements"

    uid = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
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

    uid = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    employee_uid = Column(ForeignKey("employee.uid"), nullable=False)
    room_uid = Column(ForeignKey("rooms.uid"), nullable=False)
    inventory_card_uid = Column(ForeignKey("inventory_card.uid"), nullable=False)

    employee = relationship("Employee", back_populates='temp_inventory_card')
    inventory_card = relationship("InventoryCard", back_populates='temp_inventory_card')
    room = relationship("Rooms", back_populates='temp_inventory_card')


class TelegramUsers(Base):
    __tablename__ = "telegram_chat"

    uid = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    chat_uid = Column(Integer, nullable=True)
    phone_number = Column(VARCHAR)
