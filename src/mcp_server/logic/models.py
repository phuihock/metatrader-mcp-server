from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field
import uuid

class MCPBaseModel(BaseModel):
    """
    Base model for common validation/utilities.
    Provides JSON serialization and deserialization helpers.
    """
    def to_json(self, **kwargs) -> str:
        return self.json(**kwargs)

    @classmethod
    def from_json(cls, data: Union[str, bytes]) -> 'MCPBaseModel':
        return cls.parse_raw(data)

class MCPRequest(MCPBaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique request identifier.")
    command: str = Field(..., description="Command to execute.")
    parameters: Optional[Dict[str, Any]] = Field(default=None, description="Parameters for the command.")
    authentication: Optional[Dict[str, Any]] = Field(default=None, description="Authentication details.")

class MCPResponse(MCPBaseModel):
    response_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique response identifier.")
    status_code: int = Field(..., description="HTTP or application status code.")
    result: Optional[Any] = Field(default=None, description="Result of the command, if successful.")
    error_info: Optional[Dict[str, Any]] = Field(default=None, description="Error details, if any.")
