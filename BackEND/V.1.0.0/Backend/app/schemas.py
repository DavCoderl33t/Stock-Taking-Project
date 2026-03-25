from pydantic import BaseModel
from datetime import datetime

class ButtonPressResponse(BaseModel):
	id: int
	pressed_at: datetime

	class Config:
		from_attributes=True
class ButtonPressCount(BaseModel):
	count: int		