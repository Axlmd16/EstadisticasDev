from bson import ObjectId
from typing import Any
from pydantic_core import CoreSchema
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler

class PyObjectId(ObjectId):
    def __init__(self, value: Any):
        if isinstance(value, str):
            if not ObjectId.is_valid(value):
                raise ValueError('Invalid ObjectId')
            value = ObjectId(value)
        elif not isinstance(value, ObjectId):
            raise ValueError('Invalid ObjectId')
        super().__init__(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        from pydantic_core.core_schema import str_schema
        # Solo validación como string para Pydantic v2
        return str_schema()

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        core_schema: CoreSchema,
        handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        return {
            'type': 'string',
            'format': 'objectid',
            'description': 'ObjectId de MongoDB',
            'example': '507f1f77bcf86cd799439011'
        }
        
    def __repr__(self) -> str:
        return f'PyObjectId({super().__repr__()})'