
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine.cursor import CursorResult
from config import settings


async_engine = create_async_engine(settings.DB_URL)

async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


def decor(func):
    async def wrapper(*args, **kwargs):
        db = get_db()
        session = await anext(db)
        return await func(*args, session=session, **kwargs)
    return wrapper


async def get_db() -> AsyncSession:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()


# вставка в таблицу temp
async def insert_depen_temp(device, employee, room) -> None:
    db = get_db()
    session: AsyncSession = await anext(db)
    sql_insert = """
        insert into temp_inventory_card (uid , date, employee_uid, inventory_card_uid, room_uid)
        values((select uuid_generate_v4()),
        (now()),
        ('%s'),
        (select inv.uid from inventory_card inv where inv.inventory_info_uid = '%s'),
        ('%s'));""" % (employee, device, room)
    try:
        await session.execute(sql_insert)
        await session.commit()
    except Exception:
        pass


# Проверка числится ли устройство за кем то
async def check_inventory_card(device: str) -> dict:
    sql = """
        SELECT card.uid, info.name, info.model, em.uid, em.name,
        em.surname, em.patronymicon, room.uid, room.floor, room.number
        from inventory_card card
        LEFT JOIN inventory_info info
        on card.inventory_info_uid  = info.uid
        LEFT JOIN employee em
        on card.employee_uid = em.uid
        LEFT JOIN rooms room
        on card.room_uid = room.uid
        WHERE info.uid  = '%s';
    """ % (device)
    sql_name_devices = """
        SELECT mi.name, mi.model  FROM inventory_info mi
        WHERE uid = '%s'
    """ % (device)
    db = get_db()
    session: AsyncSession = await anext(db)
    cour: CursorResult = await session.execute(sql)
    data = cour.fetchone()
    # проверяем числится ли за кем то устройство
    if data:
        all_info = {
            "name_model": data[1:3],
            "uid_emp": data[3],
            "user_name_surname_pat": data[4:7],
            "floor_uid": data[7],
            "floor_number": data[8:10],
        }
        return all_info
    # Если устройство не числится ни за кем
    else:
        cour = await session.execute(sql_name_devices)
        name_model = cour.fetchone()
        all_info = {
            "не учтённое устройство сверка": f"Устройство <b>{name_model[0]}</b>, \
            модель <b>{name_model[1]}</b> ещё не используется, проведите учёт",
            "не учтённое устройство учёт": "None",
        }
        return all_info


# Вставка в таблицу inventory_card
async def insert_inventory_card(all_devices: list, employee: str, office: str) -> dict:
    response = {"учтён": [], "не учтён": [], "uid": {"employee": "", "office": "", "devices": [], "name_model": []}}

    sql_user = """
        SELECT em.surname, em.name, em.patronymicon
        FROM employee em where em.uid = '%s';""" % (employee)
    for dev in all_devices:
        db = get_db()
        session: AsyncSession = await anext(db)
        check_device = await check_inventory_card(dev)  # возвращаем словарь
        sql_name_devices = """
            SELECT inv.name, inv.model
            FROM inventory_info inv
            WHERE uid = '%s';""" % (dev)
        sql_insert = """
            INSERT INTO inventory_card (uid, inventory_info_uid, employee_uid, room_uid)
            VALUES (
                (SELECT uuid_generate_v4()),
                (SELECT i.uid
                    FROM inventory_info i
                    WHERE i.uid = '%s'),
                ('%s'),
                ('%s'));""" % (dev, employee, office)

        # Если устройство не зарегано ни за кем
        if "не учтённое устройство учёт" in check_device.keys():
            await session.execute(sql_insert)
            name_cour: CursorResult = await session.execute(sql_name_devices)
            name_model = name_cour.fetchone()  # Название устройства и модель
            user_cour: CursorResult = await session.execute(sql_user)
            employee_fio = user_cour.fetchone()  # ФИО сотрудника
            response["учтён"].append(
                f"Устройство <b>{name_model[0]}</b>, модель <b>{name_model[1]}</b> теперь учтено за cотрудником "
                f"<b>{' '.join(employee_fio)}</b>"
            )
            await session.commit()

        # Если устройство зарегано на этого же пользователя и помещении
        elif check_device["uid_emp"] == employee and check_device["floor_uid"] == office:
            response["учтён"].append(
                f"Устройство <b>{check_device['name_model'][0]}</b>, "
                f"модель <b>{check_device['name_model'][1]}</b> уже числится за "
                f"<b>{' '.join(check_device['user_name_surname_pat'])}</b> на "
                f"{check_device['floor_number'][0]} этаже в {check_device['floor_number'][1]} помещении"
            )

        # Если устройство зарегано за сотрудником но находится в другом помещении
        elif check_device["floor_uid"] != office and check_device["uid_emp"] == employee:
            response["не учтён"].append(
                f"Устройство <b>{check_device['name_model'][0]}</b>, модель <b>{check_device['name_model'][1]}</b> "
                f"зарегистрировано за {' '.join(check_device['user_name_surname_pat'])} "
                f"но находится в {check_device['floor_number'][0]} помещении на "
                f"{check_device['floor_number'][1]} этаже, попробуйте перенести устройство в нужное помещение"
            )
            response["uid"]["employee"] = employee
            response["uid"]["office"] = office
            response["uid"]["devices"].append(dev)
            response["uid"]["name_model"].append(" ".join(check_device["name_model"]))

        # Если устройство зарегано не на нашем сотруднике
        elif check_device["uid_emp"] != employee:
            response["не учтён"].append(
                f"Устройство <b>{check_device['name_model'][0]}</b>, модель <b>{check_device['name_model'][1]}</b> "
                f"зарегистрировано за <b>{' '.join(check_device['user_name_surname_pat'])}</b> "
                f"и находится в <b>{check_device['floor_number'][0]}</b> помещении на "
                f"<b>{check_device['floor_number'][1]}</b> этаже, "
                f"попробуйте поменять владельца с помощью функции перемещения."
            )
            response["uid"]["employee"] = employee
            response["uid"]["office"] = office
            response["uid"]["devices"].append(dev)
            response["uid"]["name_model"].append(" ".join(check_device["name_model"]))

    return response


# ФИО сотрудника
@decor
async def select_bio_employee(employee_uid: str, session: AsyncSession) -> str:
    sql_user = """
        select e.surname, e.name, e.patronymicon
        from employee e where e.uid = '%s';""" % (employee_uid)
    # db = get_db()
    # session: AsyncSession = await anext(get_db())
    cour: CursorResult = await session.execute(sql_user)
    user_name = cour.fetchone()
    return " ".join(user_name)


# Сверка девайса с сотрудником и офисом
async def select(all_devices: list, user: str, office: str) -> dict:
    response = {"учтён": [], "не учтён": [], "uid": {"employee": "", "office": "", "devices": [], "name_model": []}}
    # Прогоняем каждое устройство
    for dev in all_devices:
        db = get_db()
        session: AsyncSession = await anext(db)
        sql = """
            SELECT card.uid, info.name, info.model, em.uid, em.name,
            em.surname, em.patronymicon, room.uid, room.floor, room.number
            FROM inventory_card card
            LEFT JOIN inventory_info info
            on card.inventory_info_uid  = info.uid
            LEFT JOIN employee em
            on card.employee_uid = em.uid
            LEFT JOIN rooms room
            on card.room_uid = room.uid
            where info.uid  = '%s';""" % (dev)

        sql_name_device = """
            SELECT info.name, info.model
            FROM inventory_info info
            WHERE uid = '%s';""" % (dev)

        cour: CursorResult = await session.execute(sql)
        data = cour.fetchone()
        # Проверяем числится ли за кем то данное устройство
        if data:
            all_info = {
                "name_model": data[1:3],
                "uid_emp": data[3],
                "user_name_surname_pat": data[4:7],
                "floor_uid": data[7],
                "floor_number": data[8:10],
            }

            # Проверяем числится ли это устройство на данном сотруднике
            if all_info["uid_emp"] != user:
                await insert_depen_temp(dev, user, office)
                response["учтён"].append(
                    f"Устройство <b>{all_info['name_model'][0]}</b>, "
                    f"модель <b>{all_info['name_model'][1]}</b> числится за "
                    f"<b>{' '.join(all_info['user_name_surname_pat'])}</b> на "
                    f"<b>{all_info['floor_number'][0]}</b> этаже в помещении "
                    f"<b>{all_info['floor_number'][1]}</b>. Проведите перемещение если необходимо."
                )

            # Проверяем числится ли это устройство в этом офисе
            elif all_info["floor_uid"] != office:
                await insert_depen_temp(dev, user, office)
                response["учтён"].append(
                    f"Устройство <b>{all_info['name_model'][0]}</b>, "
                    f"модель <b>{all_info['name_model'][1]}</b> находится на "
                    f"<b>{all_info['floor_number'][0]}</b> этаже в помещении <b>{all_info['floor_number'][1]}</b>"
                )

            # если всё ок то добавляем в response с ключем учтён
            else:
                response["учтён"].append(
                    f"Устройство <b>{all_info['name_model'][0]}</b>, "
                    f"модель <b>{all_info['name_model'][1]}</b> сходится с cотрудником "
                    f"<b>{' '.join(all_info['user_name_surname_pat'])}</b>"
                )
        # Если устройство не числится то заполняем в отдельные ключи в словаре
        else:
            # Достаем из БД имя устройства и модель.
            cour: CursorResult = await session.execute(sql_name_device)
            name_model = cour.fetchone()
            response["не учтён"].append(
                f"Устройство <b>{name_model[0]}</b>, модель <b>{name_model[1]}</b> ещё не используется, проведите учёт."
            )
            response["uid"]["employee"] = user
            response["uid"]["office"] = office
            response["uid"]["devices"].append(dev)
            response["uid"]["name_model"].append(" ".join(name_model))

    return response


async def movents(all_devices: list[str], employee: str, office: str) -> dict:
    response = {"учтён": [], "не учтён": []}
    for dev in all_devices:
        db = get_db()
        session: AsyncSession = await anext(db)
        sql_employee = """
            SELECT e.surname, e.name, e.patronymicon FROM employee e WHERE e.uid = '%s';""" % (employee)
        sql_name_device = """
            SELECT inv.name, inv.model  FROM inventory_info inv WHERE uid = '%s';""" % (dev)
        sql_insert = """
            INSERT INTO movements (uid, reason, from_employee_uid, inventory_card_uid, to_employee_uid,  date)
            values((SELECT uuid_generate_v4()),
            'telegram_movents',
            (SELECT inv.employee_uid from inventory_card inv WHERE inv.inventory_info_uid = '%(dev)s'),
            (SELECT inv.uid  from inventory_card inv WHERE inv.inventory_info_uid = '%(dev)s'),
            ('%(employee)s'),
            (now()));""" % {"dev": dev, "employee": employee}
        sql_update = """
            update inventory_card a
            set employee_uid = '%(employee)s',
            room_uid = '%(office)s'
            WHERE inventory_info_uid = '%(dev)s';""" % {"dev": dev, "employee": employee, "office": office}
        check_device = await check_inventory_card(dev)  # числится ли устройство за кем то
        if "не учтённое устройство учёт" not in check_device.keys():
            await session.execute(sql_insert)
            await session.execute(sql_update)
            # Добавляем в таблицу movents данные от кого -> кому | и делаем update таблицы inventory_card
            # Так как хотим получить ФИО кому мы передали мы делаем еще один запрос для получения ФИО нашего сотруд.
            cour: CursorResult = await session.execute(sql_employee)
            name_surname = cour.fetchone()  # <-- Данные нашего сотрудника ФИО
            sql_room = f"""select room.floor, room.number from rooms room where room.uid = '{office}' """
            cour = await session.execute(sql_room)
            office_floor_number = cour.fetchone()
            response["учтён"].append(
                f"Устройство <b>{check_device['name_model'][0]}</b> модель <b>{check_device['name_model'][1]}</b> "
                f"теперь закреплено за <b>{' '.join(name_surname)}</b> на <b>{office_floor_number[0]}</b> "
                f"этаже в <b>{office_floor_number[1]}</b> помещении"
            )
            await session.commit()
        # Если устройство не числится то заполняем с ключом "не учтён"
        else:
            cour = await session.execute(sql_name_device)
            name_model = cour.fetchone()
            response["не учтён"].append(
                f"Устройство <b>{name_model[0]}</b> модель <b>{name_model[1]}</b> ещё не используется, проведите учёт"
            )
    return response


async def detail_device(device: str) -> str:
    """
    Detailed information about the registred device.
    device is uid in inventory_info table.
    """
    sql = """
            SELECT info."name", info.model, emp.surname, emp."name", emp.patronymicon, room.floor, room."number"
            FROM inventory_card inv
            LEFT JOIN inventory_info info
            ON info.uid = inv.inventory_info_uid
            LEFT JOIN employee emp
            ON emp.uid = inv.employee_uid
            LEFT JOIN rooms room
            ON room.uid = inv.room_uid
            WHERE inv.inventory_info_uid  = '%s';""" % (device)
    try:
        db = get_db()
        session: AsyncSession = await anext(db)
        cour: CursorResult = await session.execute(sql)
        result = cour.fetchone()
    except Exception:
        return "Технические проблемы, попробуйте ещё раз."
    if result:
        return (
            f"Устройство: <b>{result[0]}</b>\n"
            f"Модель: <b>{result[1]}</b>\n"
            f'Сотрудник: <b>{" ".join(result[2:5])}</b>\n'
            f"Этаж: <b>{result[5]}</b>\n"
            f"Помещение: <b>{result[6]}</b>"
        )
    return "Данное устройство не числится, проведите первичный учёт."


async def detail_office(office: str) -> Union[str, bool]:
    """
    Information about the office.
    office is uid in rooms table
    """
    sql_office = """
        SELECT room.floor as этаж,
        room."number" as помещение,
        count(distinct inv.employee_uid) as колличество_сотрудников,
        count(inv.inventory_info_uid) as колличество_мат
        FROM rooms room
        LEFT JOIN inventory_card inv
        ON inv.room_uid = room.uid
        LEFT JOIN employee emp
        ON emp.uid = inv.employee_uid
        WHERE room.uid = '%s'
        GROUP BY (этаж, помещение);""" % (office)
    try:
        db = get_db()
        session: AsyncSession = await anext(db)
        cour: CursorResult = await session.execute(sql_office)
        result = cour.fetchone()
    except Exception:
        return "Технические проблемы, попробуйте ещё раз."
    if result:
        return (
            f"Помещение: <b>{result[1]}</b>\n"
            f"Этаж: <b>{result[0]}</b>\n"
            f"Колличество сотрудников: <b>{result[2]}</b>\n"
            f"Колличество материальных ценнностей: <b>{result[3]}</b>"
        )
    return "В данном помещении никто и ничто не числится"


async def detail_office_all(office: str) -> str:
    """
    Detailed information about the office, who is in it and how many mats of values.
    office is uid in rooms table.
    """

    sql = """
            SELECT emp.surname, emp."name", emp.patronymicon,
            count(inv.inventory_info_uid) from employee emp
            LEFT JOIN inventory_card inv
            ON inv.employee_uid = emp.uid
            WHERE inv.room_uid = '%s'
            GROUP BY (emp.surname, emp."name", emp.patronymicon);""" % (office)
    try:
        db = get_db()
        sesion: AsyncSession = await anext(db)
        cour: CursorResult = await sesion.execute(sql)
        employees = cour.fetchall()
    except Exception:
        return "Технические проблемы, попробуйте ещё раз."
    result = ""
    for employee in employees:
        result += f'Сотрудник <b>{" ".join(employee[0:3])}</b>: <b>{employee[3]}</b> мат ценностей\n'
    return result


async def detail_employee(employee: str) -> str:
    """
    Detailed information about the employee, namely on which floor,
    room is listed and how many mats of values have.
    """

    sql = """
        SELECT emp.surname, emp."name", emp.patronymicon, coalesce(r.floor, 0) as flour,
        coalesce(r."number", '') as "number", count(inv.uid)
        FROM employee emp
        LEFT JOIN inventory_card inv
        ON inv.employee_uid = emp.uid
        LEFT JOIN rooms r
        ON r.uid = inv.room_uid
        WHERE emp.uid = '%s'
        GROUP BY (r.floor, r."number", emp.surname, emp."name", emp.patronymicon);""" % (employee)
    try:
        db = get_db()
        session: AsyncSession = await anext(db)
        cour = await session.execute(sql)
        data = cour.fetchall()
        await session.close()
    except Exception:
        return "Технические проблемы, попробуйте ещё раз."
    if data:
        employee = f"<b>{' '.join(data[0][0:3])}</b>\n"  # Ivanov Ivan Ivanovich
        for detail in data:
            employee += f"‣ <b>{detail[3]}</b> этаж <b>{detail[4]}</b> помещение <b>{detail[5]}</b> мат ценностей\n"
        return employee
    return "Такой сотрудник не числится"


async def check_id(user_id: int) -> bool:
    """
    Checks if a user with this id exists in the database
    user_id is uid in telegram_chat table
    """
    try:
        db = get_db()
        session: AsyncSession = await anext(db)
        sql = "SELECT tg.uid FROM telegram_chat tg WHERE tg.chat_uid = '%s';" % (int(user_id))
        cour = await session.execute(sql)
        user = cour.scalar()
        await session.close()
    except Exception:
        return False
    if user:
        return True
    return False


async def update_chat_id(data: list[int, str]) -> bool:
    """
    Update chat_uid in telegram_chat table.
    data is a list where the first element is int(chat_uid), second is str(phone_number)
    format phone_number like '79998887766'
    """
    db = get_db()
    session: AsyncSession = await anext(db)
    chat_id = data[0]
    phone_number = data[1]
    sql_update = """
                UPDATE telegram_chat
                SET chat_uid  = %s
                WHERE
                phone_number  = '%s'
                returning chat_uid ;""" % (chat_id, phone_number)
    try:
        cour = await session.execute(sql_update)
        result: CursorResult = cour.scalar()
        await session.commit()
        return result
    except Exception:
        return False

import asyncio

print(asyncio.run(select_bio_employee("c9498c10-6c69-4771-9d15-73c8376d47bd")))