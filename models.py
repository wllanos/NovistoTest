import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import datetime as _dt

import database as _database 


	

class Metric(_database.Base):
    __tablename__ = "metric"
    id = _sql.Column(_sql.Integer, primary_key=True, autoincrement=True)
    code = _sql.Column(_sql.String, unique=True)
    description = _sql.Column(_sql.String)

    value_definition = _orm.relationship("Definition", back_populates="metric")

class Definition(_database.Base):
    __tablename__ = "value_definition"
    id = _sql.Column(_sql.Integer, primary_key=True,autoincrement=True)
    label = _sql.Column(_sql.String)
    type = _sql.Column(_sql.String)
    metric_id = _sql.Column(_sql.Integer, _sql.ForeignKey("metric.id"))

    metric = _orm.relationship("Metric", back_populates="value_definition")
	