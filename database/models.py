import enum
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base

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
    entityId = Column(Integer, ForeignKey(Entity.id))
    entityGroupId = Column(String(250), ForeignKey(EntitiesGroup.tag))
    entityGroupVersion = Column(Integer, ForeignKey(EntitiesGroup.version))

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
    testServiceId = Column(Integer, ForeignKey(TestService.id))
    testServiceGroupId = Column(Integer, ForeignKey(TestServiceGroup.id))
    testServiceGroupVersion = Column(Integer, ForeignKey(TestServiceGroup.version))

class Campaign(Base):
    __tablename__ = 'campaign'
    tag = Column(String(50), primary_key=True)
    type = Column(Enum(campaignTypes), unique=False)
    status = Column(Enum(campaignStatus), unique=False)
    nextRun = Column(JSON, unique=False)

class Campaign_TestServiceGroup_EntitiesGroup(Base):
    __tablename__ = 'campaign_TestServiceGroup_EntitiesGroup'
    id = Column(Integer, primary_key=True)
    campaignId = Column(String(50), ForeignKey(Campaign.tag), unique=False)
    entitiesGroupId = Column(String(250), ForeignKey(EntitiesGroup.tag), unique=False)
    entitiesGroupVersion = Column(Integer, ForeignKey(EntitiesGroup.version), unique=False)
    testServiceGroupId = Column(Integer, ForeignKey(TestServiceGroup.id), unique=False)
    testServiceGroupVersion = Column(Integer, ForeignKey(TestServiceGroup.version), unique=False)

class Result(Base):
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True)
    cte_id = Column(Integer, ForeignKey(Campaign_TestServiceGroup_EntitiesGroup.id))
    outputPath = Column(String(250), unique=True)
    startTime = Column(TIMESTAMP, unique=False)
    endTime = Column(TIMESTAMP, unique=False)