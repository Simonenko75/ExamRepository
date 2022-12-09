from datetime import datetime
from fastapi import APIRouter, Depends, Body

from sqlalchemy import update, delete, select

from app.forms import SensorForm
from app.models import connect_db, SensorValue, SensorName
from app.utils import return_values, item_list

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World!!!"}


@router.get("/get/{sensor_id}")
def get_value_sensor(sensor_id: int, database=Depends(connect_db)):
    sensor_one = database.query(SensorValue).filter(SensorValue.id == sensor_id).one_or_none()
    sensor_two = database.query(SensorName).filter(SensorName.user_id == sensor_id).one_or_none()

    try:
        result = return_values(sensor_id, sensor_one, sensor_two)
    except:
        return "No date as this in DB!"

    return result


@router.post("/add/{number}")
def create_senior(number: int, sensor: SensorForm = Body(..., ember=True), database=Depends(connect_db)):

    new_sensor_value = SensorValue(value=sensor.value)
    database.add(new_sensor_value)
    database.commit()

    new_sensor_name = SensorName(name_sensor=sensor.name_sensor, user_id=new_sensor_value.id)
    database.add(new_sensor_name)
    database.commit()

    stmt1 = select(SensorValue)
    stmt2 = select(SensorName.name_sensor)

    result = item_list(stmt1, stmt2, number, database)

    return result


@router.put("/update/{sensor_id},{number}")
def update_sensor(sensor_id: int, number: int, sensor: SensorForm = Body(..., ember=True), database=Depends(connect_db)):
    stmt = (
        update(SensorValue)
        .where(SensorValue.id == sensor_id)
        .values(value=sensor.value)
        .values(created_at=datetime.now())
        .execution_options(synchronize_session="fetch")
    )

    stmt1 = (
        update(SensorName)
        .where(SensorName.user_id == sensor_id)
        .values(name_sensor=sensor.name_sensor)
        .execution_options(synchronize_session="fetch")
    )

    database.execute(stmt)
    database.execute(stmt1)

    database.commit()

    stmt1 = select(SensorValue)
    stmt2 = select(SensorName.name_sensor)

    result = item_list(stmt1, stmt2, number, database)

    return result


@router.delete("/delete/{sensor_id}")
def delete_sensor(sensor_id: int, database=Depends(connect_db)):
    stmt = (
        delete(SensorValue)
        .where(SensorValue.id == sensor_id)
        .execution_options(synchronize_session="fetch")
    )

    sensor = database.query(SensorName).filter(SensorName.user_id == sensor_id).one_or_none()
    stmt1 = (
        delete(SensorName)
        .where(SensorName.id == sensor.id)
        .execution_options(synchronize_session="fetch")
    )

    database.execute(stmt)
    database.execute(stmt1)
    database.commit()

    return {"Result": f"Successful delete sensor with id: {sensor_id}"}
