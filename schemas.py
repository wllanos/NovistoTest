from typing import List
import pydantic as _pydantic
  
  
class _DefinitionBase(_pydantic.BaseModel):
	label: str
	type: str
	metric_id: int 

class DefinitionCreate(_DefinitionBase):
	pass
	
class Definition(_DefinitionBase):
	id: int
	
	class Config:
		orm_mode = True

class _MetricBase(_pydantic.BaseModel):
	code: str
	description: str


class MetricCreate(_MetricBase):
	pass

class Metric(_MetricBase):
	id: int
	code: str
	description: str
	value_definition: List[Definition] = []
	
	class Config:
		orm_mode = True
	 