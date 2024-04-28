import enum
from sqlalchemy import Column, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, TIMESTAMP, Boolean, ForeignKey, Enum, JSON, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

class campaignTypes(enum.Enum):
    daily = "Daily"
    weekly = "Weekly"
    monthly = "Monthly"
    personalized = "Personalized"

class campaignStatus(enum.Enum):
    unactive = "Unactive"
    active = "Active"
    completed = "Completed"

Base = declarative_base()

class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer, primary_key=True)
    url = Column(String(250), unique=True)
    name = Column(String(150), unique=True)
    acronym = Column(String(50), unique=True)
    creationDate = Column(TIMESTAMP, unique=False)
    updateDate = Column(TIMESTAMP, unique=False)

class EntitiesGroup(Base):
    __tablename__ = 'entitiesGroup'
    tag = Column(String(250), primary_key=True)
    version = Column(Integer, primary_key=True, default=1, index=True)
    creationDate = Column(TIMESTAMP, unique=False)
    updateDate = Column(TIMESTAMP, unique=False)

class Entity_EntitiesGroup(Base):
    __tablename__ = 'entity_EntitiesGroup'
    id = Column(Integer, primary_key=True)
    entityId = Column(Integer)
    entityGroupId = Column(String(250))
    entityGroupVersion = Column(Integer)
    __table_args__ = (
        ForeignKeyConstraint(['entityId'], ['entity.id']),
        ForeignKeyConstraint(['entityGroupId', 'entityGroupVersion'], ['entitiesGroup.tag', 'entitiesGroup.version']),
    )

class TestService(Base):
    __tablename__ = 'testService'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    scriptName = Column(String(50), unique=True)

class TestServiceGroup(Base):
    __tablename__ = 'testServiceGroup'
    id = Column(Integer, primary_key=True)
    version = Column(Integer, primary_key=True, default=1, index=True)

class TestService_TestServiceGroup(Base):
    __tablename__ = 'testService_TestServiceGroup'
    id = Column(Integer, primary_key=True)
    testServiceId = Column(Integer)
    testServiceGroupId = Column(Integer)
    testServiceGroupVersion = Column(Integer)
    __table_args__ = (
        ForeignKeyConstraint(['testServiceId'], ['testService.id']),
        ForeignKeyConstraint(['testServiceGroupId', 'testServiceGroupVersion'], ['testServiceGroup.id', 'testServiceGroup.version']),
    )

class Campaign(Base):
    __tablename__ = 'campaign'
    tag = Column(String(50), primary_key=True)
    type = Column(Enum(campaignTypes), unique=False)
    status = Column(Enum(campaignStatus), unique=False)
    nextRun = Column(JSON, unique=False)

class Campaign_TestServiceGroup_EntitiesGroup(Base):
    __tablename__ = 'campaign_TestServiceGroup_EntitiesGroup'
    id = Column(Integer, primary_key=True)
    campaignId = Column(String(50), unique=False)
    entitiesGroupId = Column(String(250), unique=False)
    entitiesGroupVersion = Column(Integer, unique=False)
    testServiceGroupId = Column(Integer, unique=False)
    testServiceGroupVersion = Column(Integer, unique=False)
    __table_args__ = (
        ForeignKeyConstraint(['campaignId'], ['campaign.tag']),
        ForeignKeyConstraint(['entitiesGroupId', 'entitiesGroupVersion'], ['entitiesGroup.tag', 'entitiesGroup.version']),
        ForeignKeyConstraint(['testServiceGroupId', 'testServiceGroupVersion'], ['testServiceGroup.id', 'testServiceGroup.version']),
    )

class Result(Base):
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True)
    cte_id = Column(Integer, ForeignKey(Campaign_TestServiceGroup_EntitiesGroup.id))
    outputPath = Column(String(250), unique=True)
    startTime = Column(TIMESTAMP, unique=False)
    endTime = Column(TIMESTAMP, unique=False)