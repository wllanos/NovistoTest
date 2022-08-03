import fastapi as _fastapi
import services as _services 
import schemas as _schemas
import sqlalchemy.orm as _orm
from typing import List
from pydantic import BaseModel
from fastapi_versioning import VersionedFastAPI, version
import function

app = _fastapi.FastAPI(title="NovistoAPI")

#run the script to create the missing table and load the csv file
function.main()
#_services.create_database()

@app.get("/",tags=["Home"])
@version(1, 0)
def home():
	return {"Message": "Welcome to Novisto API V1.0"}

############################################Metric
@app.post("/metrics/", response_model=_schemas.Metric, summary="Create a metric", 
	description= "Create a **metric** with all the required information.", tags=["Metrics"])
@version(1, 0)
def create_metric(metric: _schemas.MetricCreate, db: _orm.Session=_fastapi.Depends
			(_services.get_db)):
	db_metric = _services.get_metric_by_code(db=db, code=metric.code)
	if db_metric:
		raise _fastapi.HTTPException(
			status_code=400, detail="Code already created"
		)
	return _services.create_metric(db=db, metric=metric)


@app.get("/metrics/value-definitions/", response_model=List[_schemas.Metric] , summary="Get all metrics by range", 
	description="Get all **metrics** including **value definitions** registers.", tags=["Metrics"])
@version(1, 0)
def get_all_metrics_including_value_definitions(skip: int = 0, limit: int=100, 
			db: _orm.Session = _fastapi.Depends(_services.get_db)):
	metrics = _services.get_metrics(db=db, skip=skip, limit=limit)
	if metrics:
		return metrics
	raise _fastapi.HTTPException(
			status_code=404, detail = f"Records not found"
		)

		
@app.get("/metrics/{code}/value-definitions/", response_model=_schemas.Metric, summary="Get a metric by code", 
	description="Get an specific **metric** by code. **Note:** Results include related data to **value definitions** "
	,tags=["Metrics"])
@version(1, 0)
def get_a_metric_by_code_including_value_definitions(code: str, db: _orm.Session = 
			_fastapi.Depends(_services.get_db)):
	metrics = _services.get_metric_by_code(db=db, code=code)
	if metrics:
		return metrics
	raise _fastapi.HTTPException(
			status_code=404, detail = f"Code {code} : Does not exist"
		)

############################################Value Definition
@app.post("/value-definitions/", response_model=_schemas.Definition, summary="Create a value definition", 
	description="Create a **value definition** related to a **metric**", tags=["Value Definitions"])
@version(1, 0)
def create_value_definition(definition: _schemas.DefinitionCreate, db: _orm.Session=
			_fastapi.Depends(_services.get_db)):
	
	db_metric = _services.get_metric_by_id(db=db, id=definition.metric_id)
	if db_metric:
		return _services.create_definition(db=db, definition=definition)
	raise _fastapi.HTTPException(
		status_code=400, detail=f"Metric ID {definition.metric_id} : Does not exist"
	)


@app.get("/value-definitions/all/", response_model=List[_schemas.Definition], summary="Get all value definitions by range", 
	description="Get all **value definitions**", tags=["Value Definitions"])
@version(1, 0)
def get_all_value_definitions(skip: int=0, limit: int=100, db: _orm.Session = 
			_fastapi.Depends(_services.get_db)):
	definitions = _services.get_definitions(db=db, skip=skip, limit=limit)
	if definitions:
		return definitions
	raise _fastapi.HTTPException(
			status_code=404, detail = "Records not found" 
		)

@app.get("/value-definitions/{id}/", response_model=_schemas.Definition, summary="Get a value definition by id", 
	description="Get a **value definition** by id", tags=["Value Definitions"])
@version(1, 0)
def get_a_value_definition_by_id(id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
	definitions = _services.get_definition_by_id(db=db, id=id)
	if definitions:
		return definitions
	raise _fastapi.HTTPException(
			status_code=404, detail = f"Id {id} : Does not exist"
		)


@app.get("/value-definitions/{metric_id}/", response_model=List[_schemas.Definition], summary="Get a value definition by metric id", 
	description="Get a **value definitions** list by **metric id**", tags=["Value Definitions"])
@version(1, 0)
def get_value_definitions_by_metric_id(metric_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
	definitions = _services.get_definitions_by_metric_id(db=db, metric_id=metric_id)
	if definitions:
		return definitions
	raise _fastapi.HTTPException(
			status_code=404, detail = f"Metric Id {metric_id} : Does not exist" 
		)

app = VersionedFastAPI(app, default_api_version=(1))
