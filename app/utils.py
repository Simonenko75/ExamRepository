from sqlalchemy import delete

from app.models import SensorValue, SensorName


def return_values(sensor_id, sensor_one, sensor_two):
    return {
        "Sensor": {
            "sensor_id": sensor_id,
            "sensor_value": sensor_one.value,
            "sensor_name": sensor_two.name_sensor
        }
    }


def item_list(stmt1, stmt2, number, database):
    lst_sensor = {}
    lst_2 = {}

    for i, name in enumerate(database.scalars(stmt2)):
        lst_2[f"sensor_name '{i}'"] = name

    for i, sensor_item in enumerate(database.scalars(stmt1)):
        lst_sensor[f"sensor_created '{sensor_item.id}'"] = sensor_item.created_at
        lst_sensor[f"sensor_name '{sensor_item.id}'"] = lst_2[f"sensor_name '{i}'"]
        lst_sensor[f"sensor_value '{sensor_item.id}'"] = sensor_item.value

    items = list(lst_sensor.items())
    data_sensors = {k: v for k, v in reversed(items)}
    lst_i = list(data_sensors.items())

    items_list = {}
    for i in range(number * 4):
        items_list[lst_i[i][0]] = lst_i[i][1]

    return items_list


def delete_first_sensor(stmt1, database):
    ld = [elem.id for elem in database.scalars(stmt1)]

    sensor_id = database.query(SensorValue).filter(SensorValue.id == ld[0]).one_or_none()
    stmt = (
        delete(SensorValue)
        .where(SensorValue.id == sensor_id.id)
        .execution_options(synchronize_session="fetch")
    )

    sensor = database.query(SensorName).filter(SensorName.user_id == sensor_id.id).one_or_none()
    stmt1 = (
        delete(SensorName)
        .where(SensorName.id == sensor.id)
        .execution_options(synchronize_session="fetch")
    )

    database.execute(stmt)
    database.execute(stmt1)
    database.commit()