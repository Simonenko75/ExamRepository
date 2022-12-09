from pydantic import BaseModel


class SensorForm(BaseModel):
    value: float
    name_sensor: str

