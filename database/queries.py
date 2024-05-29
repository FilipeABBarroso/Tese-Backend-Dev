import json
from os import walk
from ast import List
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy import and_, distinct, exists, func, inspect, not_, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from .models import *
from database.initializer.initialize import engine
import os

async def updateTests():
  if not os.path.exists('database/servicesInfo.json'):
    print("JSON file 'servicesInfo.json' not found.")
    return
  with open('database/servicesInfo.json', 'r') as data:
    testsData = json.load(data)
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  out = []
  for (dirpath, dirnames, filenames) in walk("./controller/scripts"):
    for file in filenames:
      out.append([testsData[file]['testName'] or file, file])
    break
  await create_testServices(out)
  print("DB Creation completed!")

async def createDB():
  inspector = inspect(engine)
  existing_tables = inspector.get_table_names()
  if "entity" not in existing_tables:
    "Creating DB..."
    if not os.path.exists('database/servicesInfo.json'):
      print("JSON file 'servicesInfo.json' not found.")
      return
    with open('database/servicesInfo.json', 'r') as data:
      testsData = json.load(data)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    out = []
    for (dirpath, dirnames, filenames) in walk("./controller/scripts"):
      for file in filenames:
        out.append([testsData[file]['testName'] or file, file])
      break
    await create_testServices(out)
    print("DB Creation completed!")

async def create_testServices(data: dict[str, str]):
  with Session(engine) as session:
    testServices = []
    for name, scriptName in data:
      user = TestService(name=name, scriptName=scriptName)
      testServices.append(user)
      
    try:
      session.add_all(testServices)
      session.commit()
    except IntegrityError:
      session.rollback()

async def update_entity(url, new_name, new_acronym, new_url):
  with Session(engine) as session:
    try:
      result = session.execute(
          select(Entity)
          .filter(Entity.url == url)
      )
      entity = result.scalar_one()
    except NoResultFound:
        return False
    entity.name = new_name
    entity.acronym = new_acronym
    entity.url = new_url
    entity.updateDate = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    try:
      session.commit()
      return True
    except IntegrityError:
      session.rollback()
      return False

async def create_Entity_v2(list):
  with Session(engine) as session:
    '''entity_id = session.scalar(select(Entity.id).order_by(Entity.id.desc()).limit(1))
    if entity_id:
      entity_id += 1
    else:
      entity_id = 1'''
    for entityData in list:
      date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
      entity = Entity(name=entityData['name'], acronym=entityData['acronym'], url=entityData['url'], creationDate=date, updateDate=date)
      session.add(entity)
    try:
      session.commit()
    except IntegrityError:
      session.rollback()

#V1
async def create_Entity(name, url, tag, groupName, createGroup):
  with Session(engine) as session:
    entity_id = session.scalar(select(Entity.id).order_by(Entity.id.desc()).limit(1))
    group = None
    connection = None
    if(createGroup and tag != None and groupName != None):
      group = EntitiesGroup(tag=tag, groupName=groupName, creationDate=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    if entity_id:
      id = entity_id + 1
      print("id: ", id)
      print("tag: ", tag==None)
      entity = Entity(id=int(id), name=name, url=url, creationDate=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
      if(tag != None):
        connection = Entity_EntitiesGroup(entityId=int(id), entityGroupId=tag, entityGroupVersion=1)
    else:
      print("else")
      entity = Entity(id=1, name=name, url=url, creationDate=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
      if(tag != None):
        connection = Entity_EntitiesGroup(entityId=1, entityGroupId=tag, entityGroupVersion=1)

    try:
      if(createGroup):
        session.add_all([entity, group, connection])
      elif(tag != None):
        session.add_all([entity, connection])
      else:
        session.add_all([entity])
      session.commit()
    except IntegrityError:
      session.rollback()

async def create_group(tag):
  with Session(engine) as session:
    date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    group = EntitiesGroup(tag=tag, creationDate=date, updateDate=date)
    try:
      session.add(group)
      session.commit()
    except IntegrityError:
      session.rollback()

async def create_Group_Entities(entities, groupName, tag, createGroup, createEntity):
  with Session(engine) as session:
    dataToAdd = []
    group = None
    connection = None
    entity_id
    entity_id = session.scalar(select(Entity.id).order_by(Entity.id.desc()).limit(1))
    if entity_id:
      entity_id += 1
    else:
      entity_id = 1
    if(createGroup and tag != None and groupName != None):
      group = EntitiesGroup(tag=tag, groupName=groupName, creationDate=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
      dataToAdd.append(group)
    for entityData in entities:
      if(tag != None):
        connection = Entity_EntitiesGroup(entityId=int(entity_id), entityGroupId=tag, entityGroupVersion=1)
        dataToAdd.append(connection)
      entity = Entity(id=int(entity_id), name=entityData.get('name'), url=entityData.get('url'), creationDate=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
      dataToAdd.append(entity)
    try:
        session.add_all(dataToAdd)
        session.commit()
    except IntegrityError:
        session.rollback()

async def create_Group_Entities_Relation(entities, tag, version):
  with Session(engine) as session:
    dataToAdd = []
    try:
      groupDataResult = session.execute(
          select(EntitiesGroup)
          .where(and_(
            EntitiesGroup.tag == tag,
            EntitiesGroup.version == version
          ))
      )
      groupData = groupDataResult.scalar_one()
      newGroup= EntitiesGroup(tag=groupData.tag, version=int(int(groupData.version) + 1), creationDate=groupData.creationDate, updateDate=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
      session.add(newGroup)
      for entityData in entities:
        connection = Entity_EntitiesGroup(entityId=int(entityData.get('id')), entityGroupId=tag, entityGroupVersion=(version + 1))
        dataToAdd.append(connection)
      connDataResult = session.execute(
        select(Entity_EntitiesGroup)
        .select_from(Entity_EntitiesGroup)
        .where(and_(
          Entity_EntitiesGroup.entityGroupId == tag,
          Entity_EntitiesGroup.entityGroupVersion == version
        ))
      )
      connData = connDataResult.scalars()
      for conn in connData:
        newConn = Entity_EntitiesGroup(entityId=conn.entityId, entityGroupId=conn.entityGroupId, entityGroupVersion=(version + 1))
        dataToAdd.append(newConn)
      hasCampaignConn = session.execute(
        select(Campaign_TestServiceGroup_EntitiesGroup)
        .select_from(Campaign_TestServiceGroup_EntitiesGroup)
        .where(and_(
          Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupId == tag,
          Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupVersion == version
        ))
      )
      hasCampaignConnData = hasCampaignConn.scalar()
      if hasCampaignConnData is not None:
        max_version_subquery = (
          select(TestServiceGroup.id, func.max(TestServiceGroup.version).label("max_version"))
          .group_by(TestServiceGroup.id)
          .alias("max_version_subquery")
        )
        connCampDataResult = session.execute(
          select(Campaign_TestServiceGroup_EntitiesGroup)
          .select_from(Campaign_TestServiceGroup_EntitiesGroup)
          .join(max_version_subquery, and_(Campaign_TestServiceGroup_EntitiesGroup.testServiceGroupId == max_version_subquery.c.id,
            Campaign_TestServiceGroup_EntitiesGroup.testServiceGroupVersion == max_version_subquery.c.max_version))
          .where(and_(
            Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupId == tag,
            Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupVersion == version
          ))
        )
        connCampData = connCampDataResult.scalars()
        for connCamp in connCampData:
          print("aaaaaaa", connCamp.campaignId, connCamp.entitiesGroupId, connCamp.entitiesGroupVersion)
          newConnCamp = Campaign_TestServiceGroup_EntitiesGroup(campaignId=connCamp.campaignId, entitiesGroupId=connCamp.entitiesGroupId, entitiesGroupVersion=int(version + 1), testServiceGroupId=int(connCamp.testServiceGroupId), testServiceGroupVersion=int(connCamp.testServiceGroupVersion))
          dataToAdd.append(newConnCamp)
    except NoResultFound:
      return False
    try:
      session.add_all(dataToAdd)
      session.commit()
    except IntegrityError:
      session.rollback()

async def remove_Group_Entities_Relation(entities, tag, version):
  with Session(engine) as session:
    dataToAdd = []
    for entityData in entities:
      connection = Entity_EntitiesGroup(entityId=int(entityData.get('id')), entityGroupId=tag, entityGroupVersion=(version + 1))
      dataToAdd.append(connection)
    try:
      groupDataResult = session.execute(
          select(EntitiesGroup)
          .where(and_(
            EntitiesGroup.tag == tag,
            EntitiesGroup.version == version
          ))
      )
      groupData = groupDataResult.scalar_one()
      newGroup= EntitiesGroup(tag=groupData.tag, version=int(int(groupData.version) + 1), creationDate=groupData.creationDate, updateDate=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
      dataToAdd.append(newGroup)
    except NoResultFound:
      return False
    try:
      session.add_all(dataToAdd)
      session.commit()
    except IntegrityError:
      session.rollback()

def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    raise TypeError("Type not serializable")

def create_campaign_dates(start_date_str, end_date_str, interval):
  start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
  end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
  
  date_sequence = [start_date]
  
  if interval == "daily":
      delta = timedelta(days=1)
  elif interval == "weekly":
      delta = timedelta(weeks=1)
  elif interval == "monthly":
      delta = relativedelta(months=1)
  else:
      raise ValueError("Wrong campagin type")
  
  current_date = start_date
  while current_date < end_date:
      next_date = current_date + delta
      if interval == "monthly":
          next_date = next_date.replace(day=min(next_date.day, 28) + (next_date.month != (next_date + relativedelta(days=4)).month))
      date_sequence.append(next_date)
      current_date = next_date
  
  if date_sequence[-1].date() != end_date.date():
      date_sequence[-1] = end_date
  
  date_sequence_str = sorted(date_sequence)
  
  return date_sequence_str

async def create_Campaign(testsId, campaignTag, campaignType, dates, groupId, groupVersion):
  if campaignType != "personalized":
    parsed_dates = create_campaign_dates(dates[0], dates[1], campaignType)
    print(parsed_dates)
  else:
    parsed_dates = sorted([datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ") for date_str in dates])
    print(parsed_dates)

  with Session(engine) as session:
    dataToAdd = []
    last_entity_id = session.scalar(select(TestServiceGroup.id).order_by(TestServiceGroup.id.desc()).limit(1))
    entity_id = 1
    if last_entity_id:
      entity_id = last_entity_id + 1
    testServiceGroup = TestServiceGroup(id=entity_id, version=1)
    dataToAdd.append(testServiceGroup)
    for id in testsId:
      connection = TestService_TestServiceGroup(testServiceId=int(id), testServiceGroupId=entity_id, testServiceGroupVersion=1)
      dataToAdd.append(connection)
    campaign = Campaign(tag=campaignTag, type=getattr(campaignTypes, campaignType, None), status=getattr(campaignStatus, "active", None), nextRun=json.dumps(parsed_dates, default=datetime_serializer))
    dataToAdd.append(campaign)
    try:
      session.add_all(dataToAdd)
      session.commit()
      campaignConnection = Campaign_TestServiceGroup_EntitiesGroup(campaignId=campaignTag, entitiesGroupId=groupId, entitiesGroupVersion=groupVersion, testServiceGroupId=entity_id, testServiceGroupVersion=1)
      session.add(campaignConnection)
      session.commit()
    except IntegrityError:
        session.rollback()

async def get_campaigns():
  with Session(engine) as session:
    max_version_subquery = (
      select(TestServiceGroup.id, func.max(TestServiceGroup.version).label("max_version"))
      .group_by(TestServiceGroup.id)
      .alias("max_version_subquery")
    )
    max_date_subquery = (
      select(Result.cte_id, func.max(Result.endTime).label("max_date"))
      .group_by(Result.cte_id)
      .alias("max_date_subquery")
    )
    async_result = session.execute(
      select(Campaign, Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupId, func.count(TestService_TestServiceGroup.id), max_date_subquery.c.max_date)
      .select_from(Campaign)
      .join(Campaign_TestServiceGroup_EntitiesGroup, Campaign.tag == Campaign_TestServiceGroup_EntitiesGroup.campaignId)
      .join(max_version_subquery, and_(
        max_version_subquery.c.id == Campaign_TestServiceGroup_EntitiesGroup.testServiceGroupId,
        Campaign_TestServiceGroup_EntitiesGroup.testServiceGroupVersion == max_version_subquery.c.max_version
      ))
      .join(TestService_TestServiceGroup, and_(max_version_subquery.c.id == TestService_TestServiceGroup.testServiceGroupId, max_version_subquery.c.max_version == TestService_TestServiceGroup.testServiceGroupVersion))
      .outerjoin(max_date_subquery, max_date_subquery.c.cte_id == Campaign_TestServiceGroup_EntitiesGroup.id)
      .group_by(Campaign.tag, Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupId, max_date_subquery.c.max_date)
      .order_by(Campaign.tag.desc())
    )
    result = async_result.fetchall()
    campaigns = convertCampaignsDataIntoJson(result)
    return campaigns
  
async def get_group_campaigns(tag):
  groupTag = tag.split("-")[0]
  groupVersion = tag.split("-v")[1]
  with Session(engine) as session:
    max_version_subquery = (
      select(TestServiceGroup.id, func.max(TestServiceGroup.version).label("max_version"))
      .group_by(TestServiceGroup.id)
      .alias("max_version_subquery")
    )
    max_date_subquery = (
      select(Result.cte_id, func.max(Result.endTime).label("max_date"))
      .group_by(Result.cte_id)
      .alias("max_date_subquery")
    )
    async_result = session.execute(
      select(Campaign, Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupId, func.count(TestService_TestServiceGroup.id), max_date_subquery.c.max_date)
      .select_from(Campaign)
      .join(Campaign_TestServiceGroup_EntitiesGroup, and_(Campaign.tag == Campaign_TestServiceGroup_EntitiesGroup.campaignId,
        Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupId == groupTag, Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupVersion == groupVersion))
      .join(max_version_subquery, and_(
        max_version_subquery.c.id == Campaign_TestServiceGroup_EntitiesGroup.testServiceGroupId,
        Campaign_TestServiceGroup_EntitiesGroup.testServiceGroupVersion == max_version_subquery.c.max_version
      ))
      .join(TestService_TestServiceGroup, and_(max_version_subquery.c.id == TestService_TestServiceGroup.testServiceGroupId, max_version_subquery.c.max_version == TestService_TestServiceGroup.testServiceGroupVersion))
      .outerjoin(max_date_subquery, max_date_subquery.c.cte_id == Campaign_TestServiceGroup_EntitiesGroup.id)
      .group_by(Campaign.tag, Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupId, max_date_subquery.c.max_date)
      .order_by(Campaign.tag.desc())
    )
    result = async_result.fetchall()
    campaigns = convertCampaignsDataIntoJson(result)
    return campaigns

def convertCampaignsDataIntoJson(data):
  json_data = []
  for campaign, group, testCount, date in data:
    json_data.append({
        "tag": campaign.tag,
        "type": campaign.type.value,
        "status": campaign.status.value,
        "group": group,
        "tests": testCount,
        "lastRun": date
      })

  json_string = json.dumps(json_data, indent=4, default=str)
  return json_string

def convertEntitiesDataIntoJson(data):
  json_data = []
  for entity, groups_count in data:
    json_data.append({
        "id": entity.id,
        "name": entity.name,
        "acronym": entity.acronym,
        "url": entity.url,
        "creationDate": entity.creationDate,
        "updateDate": entity.updateDate,
        "groups": groups_count
      })

  json_string = json.dumps(json_data, indent=4, default=str)
  return json_string

async def get_entities():
  with Session(engine) as session:
    max_version_subquery = (
      select(EntitiesGroup.tag, func.max(EntitiesGroup.version).label("max_version"))
      .group_by(EntitiesGroup.tag)
      .alias("max_version_subquery")
    )
    async_result = session.execute(
      select(Entity, func.count(distinct(max_version_subquery.c.tag)).label("distinct_group_count"))
      .select_from(Entity)
      .outerjoin(Entity_EntitiesGroup, Entity.id == Entity_EntitiesGroup.entityId)
      .outerjoin(max_version_subquery, and_(
        max_version_subquery.c.tag == Entity_EntitiesGroup.entityGroupId,
        Entity_EntitiesGroup.entityGroupVersion == max_version_subquery.c.max_version
      ))
      .group_by(Entity)
      .order_by(Entity.id.desc())
    )
    result = async_result.fetchall()
    entities = convertEntitiesDataIntoJson(result)
    print(entities)
    return entities

def convertTestsDataIntoJson(data):
  json_data = []
  for test in data:
      json_data.append({
          "id": test[0].id,
          "name": test[0].name,
      })
  
  json_string = json.dumps(json_data, indent=4, default=str)
  return json_string

async def get_tests():
  with Session(engine) as session:
    async_result = session.execute(
      select(TestService)
      .order_by(TestService.id.desc()))
    result = async_result.fetchall()
    tests = convertTestsDataIntoJson(result)
    return tests

def convertSimpleEntitiesDataIntoJson(data):
  json_data = []
  for entity in data:
    json_data.append({
        "id": entity[0].id,
        "name": entity[0].name,
        "acronym": entity[0].acronym,
        "url": entity[0].url,
        "creationDate": entity[0].creationDate,
        "updateDate": entity[0].updateDate,
      })

  json_string = json.dumps(json_data, indent=4, default=str)
  return json_string

async def get_entities_without(tag):
  with Session(engine) as session:
    max_version_subquery = (
      select(EntitiesGroup.tag, func.max(EntitiesGroup.version).label("max_version"))
      .group_by(EntitiesGroup.tag)
      .alias("max_version_subquery")
    )
    max_version_conn = (
      select(Entity_EntitiesGroup.entityGroupId, Entity_EntitiesGroup.entityId, func.max(Entity_EntitiesGroup.entityGroupVersion).label("max_version"))
      .group_by(Entity_EntitiesGroup.entityGroupId, Entity_EntitiesGroup.entityId)
      .alias("max_version_conn")
    )
    async_result = session.execute(
      select(Entity)
      .select_from(Entity)
      .outerjoin(max_version_conn, Entity.id == max_version_conn.c.entityId)
      .outerjoin(max_version_subquery,
          max_version_subquery.c.tag == max_version_conn.c.entityGroupId
      )
      .where(
        or_(
          max_version_conn.c.entityId == None,
          and_(
            max_version_conn.c.entityGroupId != tag,
            ~exists().select_from(Entity, Entity_EntitiesGroup).where(and_(Entity_EntitiesGroup.entityId == Entity.id, Entity_EntitiesGroup.entityGroupId == tag))
          ),
          and_(
            max_version_conn.c.entityGroupId == tag,
            max_version_conn.c.max_version != max_version_subquery.c.max_version
          )
        )
      )
      .order_by(Entity.id.desc())
    )
      
    result = async_result.fetchall()
    entities = convertSimpleEntitiesDataIntoJson(result)
    print(entities)
    return entities

async def get_groups():
  with Session(engine) as session:
    try:
      max_version_subquery = (
        select(EntitiesGroup.tag, func.max(EntitiesGroup.version).label("max_version"))
        .group_by(EntitiesGroup.tag)
        .alias("max_version_subquery")
      )
      async_result = session.execute(
        select(EntitiesGroup, func.count(distinct(Entity_EntitiesGroup.id)), func.count(distinct(Campaign.tag)))
        .select_from(EntitiesGroup)
        .join(max_version_subquery, and_(
          EntitiesGroup.tag == max_version_subquery.c.tag,
          EntitiesGroup.version == max_version_subquery.c.max_version
        ))
        .outerjoin(Campaign_TestServiceGroup_EntitiesGroup, and_(EntitiesGroup.tag == Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupId,
          EntitiesGroup.version == Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupVersion))
        .outerjoin(Campaign, Campaign_TestServiceGroup_EntitiesGroup.campaignId == Campaign.tag)
        .outerjoin(Entity_EntitiesGroup, and_(Entity_EntitiesGroup.entityGroupId == EntitiesGroup.tag, Entity_EntitiesGroup.entityGroupVersion == EntitiesGroup.version))
        .group_by(EntitiesGroup)
        .order_by(EntitiesGroup.tag.desc())
      )
      result = async_result.fetchall()
      groups = convertMainGroupDataIntoJson(result)
      print(groups)
      return groups
    except NoResultFound:
      return None

def convertMainGroupDataIntoJson(data):
  json_data = []
  for entities_group, entity_count, campaign_count in data:
    json_data.append({
      "id": entities_group.tag,
      "entitiesCount": entity_count,
      "campaignsCount": campaign_count,
      "version": entities_group.version,
      "creationDate": entities_group.creationDate,
      "updateDate": entities_group.updateDate,
    })
  json_string = json.dumps(json_data, indent=4, default=str)
  return json_string

def convertGroupDataIntoJson(data):
  json_data = []
  for entities_group, test in data:
      json_data.append({
          "id": entities_group.tag,
          "hasCampaigns": str(not test is None),
          "version": entities_group.version,
          "creationDate": entities_group.creationDate,
          "updatenDate": entities_group.updateDate,
          
      })
  json_string = json.dumps(json_data, indent=4, default=str)
  return json_string

async def get_entity_groups(acronym):
  with Session(engine) as session:
    max_version_subquery = (
        select(EntitiesGroup.tag, func.max(EntitiesGroup.version).label("max_version"))
        .group_by(EntitiesGroup.tag)
        .alias("max_version_subquery")
      )
    async_result = session.execute(
      select(EntitiesGroup, func.count(Entity_EntitiesGroup.id), func.count(Campaign_TestServiceGroup_EntitiesGroup.id))
      .select_from(EntitiesGroup)
      .join(max_version_subquery, and_(
        EntitiesGroup.tag == max_version_subquery.c.tag,
        EntitiesGroup.version == max_version_subquery.c.max_version
      ))
      .outerjoin(Campaign_TestServiceGroup_EntitiesGroup, and_(EntitiesGroup.tag == Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupId,
        EntitiesGroup.version == Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupVersion))
      .outerjoin(Entity_EntitiesGroup, and_(Entity_EntitiesGroup.entityGroupId == EntitiesGroup.tag, Entity_EntitiesGroup.entityGroupVersion == EntitiesGroup.version))
      .filter(Entity.acronym == acronym)
      .group_by(EntitiesGroup.tag, EntitiesGroup.version)
      .order_by(EntitiesGroup.tag.desc())
    )
    result = async_result.fetchall()
    groups = convertMainGroupDataIntoJson(result)
    return groups

async def get_group(tag):
  with Session(engine) as session:
    max_version_subquery = (
      select(EntitiesGroup.tag, func.max(EntitiesGroup.version).label("max_version"))
      .group_by(EntitiesGroup.tag)
      .alias("max_version_subquery")
    )
    groups_number_subquery = (
      select(
          Entity.id,
          func.count().label("group_count")
      )
      .join(Entity_EntitiesGroup, Entity.id == Entity_EntitiesGroup.entityId)
      .join(max_version_subquery, and_(
          max_version_subquery.c.tag == Entity_EntitiesGroup.entityGroupId,
          Entity_EntitiesGroup.entityGroupVersion == max_version_subquery.c.max_version
      ))
      .group_by(Entity.id)
      .alias("groups_number_subquery")
    )
    async_result = session.execute(
      select(Entity, groups_number_subquery.c.group_count.label("distinct_group_count"))
      .select_from(Entity)
      .join(Entity_EntitiesGroup, and_(Entity.id == Entity_EntitiesGroup.entityId, Entity_EntitiesGroup.entityGroupId == tag))
      .join(max_version_subquery, and_(
        max_version_subquery.c.tag == Entity_EntitiesGroup.entityGroupId,
        Entity_EntitiesGroup.entityGroupVersion == max_version_subquery.c.max_version,
      ))
      .outerjoin(groups_number_subquery, Entity.id == groups_number_subquery.c.id)
      .group_by(Entity, groups_number_subquery)
      .order_by(Entity.id.desc()))
    result = async_result.fetchall()
    entities = convertEntitiesDataIntoJson(result)
    return entities

async def get_group_versions(tag):
  with Session(engine) as session:
    get_current_version = session.execute(
      select(func.max(EntitiesGroup.version))
      .where(EntitiesGroup.tag == tag)
      .group_by(EntitiesGroup.tag)
    )

    current_version = get_current_version.scalar_one()

    data_to_output = []
    for x in range(int(current_version)):
      async_result = session.execute(
        select(Entity)
        .select_from(Entity)
        .join(Entity_EntitiesGroup, and_(
          Entity.id == Entity_EntitiesGroup.entityId, 
          Entity_EntitiesGroup.entityGroupId == tag, 
          Entity_EntitiesGroup.entityGroupVersion == str(x + 1)
        ))
        .group_by(Entity)
        .order_by(Entity.id.desc()))
      result = async_result.fetchall()
      entities = json.loads(convertSimpleEntitiesDataIntoJson(result))

      get_version_date = session.execute(
      select(EntitiesGroup.updateDate)
      .where(and_(EntitiesGroup.tag == tag, EntitiesGroup.version == str(x + 1)))
      .group_by(EntitiesGroup.updateDate)
    )
      date = get_version_date.scalar_one()
      data_to_output.append({"version": x + 1, "entities": entities, "date": str(date)})
    
    return json.dumps(data_to_output)

def convertCampaignIntoJson(data):
  json_data = []
  for campaign in data: 
      json_data.append({
          "tag": campaign.tag,
          "type": campaign.type,
          "status": campaign.status,
          "nextRun": campaign.nextRun,
      })
  return json_data

async def getActiveCampaigns():
  with Session(engine) as session:
    async_result = session.execute(
      select(Campaign)
      .where(Campaign.status == 'active'))
    result = async_result.scalars().all()
    session.close()
    return convertCampaignIntoJson(result)
  
async def get_campaign_results(id):
  with Session(engine) as session:
    async_result = session.execute(
      select(Result, Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupVersion, Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupId)
      .join(Campaign_TestServiceGroup_EntitiesGroup, 
        and_(Campaign_TestServiceGroup_EntitiesGroup.campaignId == id,
          Campaign_TestServiceGroup_EntitiesGroup.id == Result.cte_id))
      .group_by(Result, Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupVersion, Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupId))
    result = async_result.fetchall()
    session.close()
    return convertCampaignResultsIntoJson(result)
  
def convertCampaignResultsIntoJson(data):
  json_data = []
  for result, version, group in data: 
    json_data.append({
        "path": result.outputPath,
        "date": result.endTime,
        "version": version,
        "group": group
    })
  return json.dumps(json_data, indent=4, default=str)
  
def convertCampaignTestsIntoJson(data):
  json_data = []
  for test in data: 
    json_data.append({
        "id": test.id,
        "name": test.name,
        "script": test.scriptName,
    })
  return json_data

async def get_campaign_tests(id):
  with Session(engine) as session:
    max_version_subquery = (
      select(TestServiceGroup.id, func.max(TestServiceGroup.version).label("max_version"))
      .group_by(TestServiceGroup.id)
      .alias("max_version_subquery")
    )
    async_result = session.execute(
      select(TestService)
      .outerjoin(TestService_TestServiceGroup, TestService_TestServiceGroup.testServiceId == TestService.id)
      .outerjoin(max_version_subquery, and_(max_version_subquery.c.id == TestService_TestServiceGroup.testServiceGroupId, 
        max_version_subquery.c.max_version == TestService_TestServiceGroup.testServiceGroupVersion))
      .join(Campaign_TestServiceGroup_EntitiesGroup, 
        and_(Campaign_TestServiceGroup_EntitiesGroup.campaignId == id,
          Campaign_TestServiceGroup_EntitiesGroup.testServiceGroupId == max_version_subquery.c.id,
          Campaign_TestServiceGroup_EntitiesGroup.testServiceGroupVersion == max_version_subquery.c.max_version))
      .group_by(TestService))
    result = async_result.scalars().all()
    session.close()
    return convertCampaignTestsIntoJson(result)
  
async def get_cte_id(tag):
  with Session(engine) as session:
    max_version_subquery = (
      select(TestServiceGroup.id, func.max(TestServiceGroup.version).label("max_version"))
      .group_by(TestServiceGroup.id)
      .alias("max_version_subquery")
    )
    async_result = session.execute(
      select(Campaign_TestServiceGroup_EntitiesGroup.id)
      .join(Campaign, and_(Campaign.tag == Campaign_TestServiceGroup_EntitiesGroup.campaignId, Campaign_TestServiceGroup_EntitiesGroup.campaignId == tag))
      .join(max_version_subquery, and_(max_version_subquery.c.id == Campaign_TestServiceGroup_EntitiesGroup.testServiceGroupId, 
        max_version_subquery.c.max_version == Campaign_TestServiceGroup_EntitiesGroup.testServiceGroupVersion))
      .group_by(Campaign_TestServiceGroup_EntitiesGroup.id))
    result = async_result.scalar_one()
    session.close()
    return result
  
def convertCampaignEntitiesIntoJson(data):
  json_data = []
  for entity in data: 
    json_data.append({
        "url": entity.url,
        "name": entity.name,
        "acronym": entity.acronym,
    })
  return json_data

async def get_campaign_entities(id):
  with Session(engine) as session:
    max_version_subquery = (
      select(EntitiesGroup.tag, func.max(EntitiesGroup.version).label("max_version"))
      .group_by(EntitiesGroup.tag)
      .alias("max_version_subquery")
    )
    async_result = session.execute(
      select(Entity)
      .outerjoin(Entity_EntitiesGroup, Entity_EntitiesGroup.entityId == Entity.id)
      .outerjoin(max_version_subquery, and_(max_version_subquery.c.tag == Entity_EntitiesGroup.entityGroupId, 
        max_version_subquery.c.max_version == Entity_EntitiesGroup.entityGroupVersion))
      .join(Campaign_TestServiceGroup_EntitiesGroup, 
        and_(Campaign_TestServiceGroup_EntitiesGroup.campaignId == id,
          Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupId == max_version_subquery.c.tag,
          Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupVersion == max_version_subquery.c.max_version))
      .group_by(Entity))
    result = async_result.scalars().all()
    session.close()
    return convertCampaignEntitiesIntoJson(result)
  
async def get_unused_campaign_tests(tag):
  with Session(engine) as session:
    max_version_subquery = (
      select(TestServiceGroup.id, func.max(TestServiceGroup.version).label("max_version"))
      .join(Campaign_TestServiceGroup_EntitiesGroup, Campaign_TestServiceGroup_EntitiesGroup.campaignId == tag)
      .group_by(TestServiceGroup.id)
      .alias("max_version_subquery")
    )
    max_version_conn = (
      select(TestService_TestServiceGroup.testServiceGroupId, TestService_TestServiceGroup.testServiceId, func.max(TestService_TestServiceGroup.testServiceGroupVersion).label("max_version"))
      .group_by(TestService_TestServiceGroup.testServiceGroupId, TestService_TestServiceGroup.testServiceId)
      .alias("max_version_conn")
    )

    async_result = session.execute(
      select(TestService)
      .select_from(TestService)
      .outerjoin(max_version_conn, TestService.id == max_version_conn.c.testServiceId)
      .outerjoin(max_version_subquery,
          max_version_subquery.c.id == max_version_conn.c.testServiceGroupId
      )
      .where(
        or_(
          max_version_conn.c.testServiceId == None,
          max_version_conn.c.max_version != max_version_subquery.c.max_version
        )
      )
      .order_by(TestService.id.desc())
    )
    result = async_result.scalars().all()
    return convertCampaignTestsIntoJson(result)


async def create_new_tests_services_version(tests, tag):
  with Session(engine) as session:
    dataToAdd = []
    try:
      testsVersion, entitiesVersion = session.execute(
        select(func.max(Campaign_TestServiceGroup_EntitiesGroup.testServiceGroupVersion), func.max(Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupVersion))
        .where(Campaign_TestServiceGroup_EntitiesGroup.campaignId == tag)).fetchone()
      campaignConn = session.execute(
        select(Campaign_TestServiceGroup_EntitiesGroup)
        .where(Campaign_TestServiceGroup_EntitiesGroup.campaignId == tag)).fetchone()

      newCampaign = Campaign_TestServiceGroup_EntitiesGroup(campaignId=tag, entitiesGroupId=campaignConn[0].entitiesGroupId, entitiesGroupVersion=entitiesVersion, testServiceGroupId=campaignConn[0].testServiceGroupId, testServiceGroupVersion=int(testsVersion) + 1)
      newTestService = TestServiceGroup(id=campaignConn[0].testServiceGroupId, version=int(testsVersion) + 1)
      session.add(newTestService)
      dataToAdd.append(newCampaign)

      connTestsDataResult = session.execute(
        select(TestService_TestServiceGroup)
        .select_from(TestService_TestServiceGroup)
        .where(and_(
          TestService_TestServiceGroup.testServiceGroupId == campaignConn[0].testServiceGroupId,
          TestService_TestServiceGroup.testServiceGroupVersion == testsVersion
        ))
      ).scalars().all()

      for testsData in connTestsDataResult:
        newTestConn = TestService_TestServiceGroup(testServiceId=testsData.testServiceId, testServiceGroupId=testsData.testServiceGroupId, testServiceGroupVersion=int(testsVersion)+1)
        dataToAdd.append(newTestConn)
      
      for test in tests:
        newTestConn = TestService_TestServiceGroup(testServiceId=test["id"], testServiceGroupId=campaignConn[0].testServiceGroupId, testServiceGroupVersion=int(testsVersion)+1)
        dataToAdd.append(newTestConn)
    except NoResultFound:
      return False
    try:
      session.add_all(dataToAdd)
      session.commit()
    except IntegrityError:
      session.rollback()

async def remove_tests_services(tests, tag):
  with Session(engine) as session:
    dataToAdd = []
    try:
      testsVersion, entitiesVersion = session.execute(
        select(func.max(Campaign_TestServiceGroup_EntitiesGroup.testServiceGroupVersion), func.max(Campaign_TestServiceGroup_EntitiesGroup.entitiesGroupVersion))
        .where(Campaign_TestServiceGroup_EntitiesGroup.campaignId == tag)).fetchone()
      campaignConn = session.execute(
        select(Campaign_TestServiceGroup_EntitiesGroup)
        .where(Campaign_TestServiceGroup_EntitiesGroup.campaignId == tag)).fetchone()

      print("VERSION: ", int(testsVersion) + 1)
      newTestService = TestServiceGroup(id=campaignConn[0].testServiceGroupId, version=int(testsVersion) + 1)
      session.add(newTestService)
      newCampaign = Campaign_TestServiceGroup_EntitiesGroup(campaignId=tag, entitiesGroupId=campaignConn[0].entitiesGroupId, entitiesGroupVersion=entitiesVersion, testServiceGroupId=campaignConn[0].testServiceGroupId, testServiceGroupVersion=int(testsVersion) + 1)
      dataToAdd.append(newCampaign)
      
      for test in tests:
        newTestConn = TestService_TestServiceGroup(testServiceId=test["id"], testServiceGroupId=campaignConn[0].testServiceGroupId, testServiceGroupVersion=int(testsVersion)+1)
        dataToAdd.append(newTestConn)
    except NoResultFound:
      return False
    try:
      session.commit()
      session.add_all(dataToAdd)
      session.commit()
    except IntegrityError:
      session.rollback()

async def update_campaign_and_create_result(tag, runs, cte, path, startTime):
  with Session(engine) as session:
    # Update Campaign dates
    try:
      result = session.execute(
          select(Campaign)
          .filter(Campaign.tag == tag)
      )
      campaign = result.scalar_one()
    except NoResultFound:
        return False
    campaign.nextRun = runs
    if len(runs) == 0:
      campaign.status = getattr(campaignStatus, "completed", None)
    try:
      session.commit()
    except IntegrityError:
      session.rollback()
      return False
    # Create result
    try:
      result = Result(cte_id=cte, outputPath=path, startTime=startTime, endTime=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
      session.add(result)
      session.commit()
    except IntegrityError:
      session.rollback()
      return False