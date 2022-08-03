import sqlalchemy.orm as _orm
import database as _database
import schemas as _schemas
import models as _models


def create_database():
	return _database.Base.metadata.create_all(bind=_database.engine)
	
def get_db():
	db = _database.SessionLocal()
	try:
		yield db
	finally:
		db.close()

def get_metric_by_code(db: _orm.Session, code: str):
	return db.query(_models.Metric).filter(_models.Metric.code == code).first()

def get_metric_by_id(db: _orm.Session, id: int):
	return db.query(_models.Metric).filter(_models.Metric.id == id).first()

def create_metric(db: _orm.Session, metric: _schemas.MetricCreate):
	db_metric = _models.Metric(code=metric.code, description=metric.description)
	db.add(db_metric)
	db.commit()
	db.refresh(db_metric)
	return db_metric

def get_metrics(db: _orm.Session, skip: int = 0, limit: int = 100):
	return db.query(_models.Metric).offset(skip).limit(limit).all()

def create_definition(db: _orm.Session, definition: _schemas.DefinitionCreate):
	db_definition = _models.Definition(metric_id=definition.metric_id, label=definition.label, type=definition.type)
	db.add(db_definition)
	db.commit()
	db.refresh(db_definition)
	return db_definition

def get_definitions(db: _orm.Session, skip: int = 0, limit: int = 100):
	return db.query(_models.Definition).offset(skip).limit(limit).all()

def get_definition_by_id(db: _orm.Session, id: int):
	return db.query(_models.Definition).filter(_models.Definition.id == id).first()

def get_definitions_by_metric_id(db: _orm.Session, metric_id: int):
	return db.query(_models.Definition).filter(_models.Definition.metric_id == metric_id).all()