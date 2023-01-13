# PostgreSQL

# import psycopg2
# from psycopg2.errors import NotNullViolation
# import asyncpg
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
# from db import get_db
# from config import settings
# from db import get_db
# conn = asyncpg.connect(settings.DB_URL)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
# from config import settings


async_engine = create_async_engine("postgresql+asyncpg://magomed:12345678@localhost:5432/fastapi")


async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncSession:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()


# async def get_db() -> AsyncSession:
#     for i in range(10):
#         yield i
# вставка в таблицу temp
# def insert_depen_temp(device, employee, room):
#     sql_insert = f"""
#         insert into mainapp_tempinventorycard (uid , date, employee_uid_id, inventory_card_uid_id  , room_uid_id)
#         values((select uuid_generate_v4()),
#         (now()),
#         ('{employee}'),
#         (select inv.uid from mainapp_inventorycard inv where inv.inventory_number_uid_id = '{device}'),
#         ('{room}'));
#     """
#     try:
#         with conn.cursor() as curs:
#             curs.execute(sql_insert)
#             conn.commit()
#     except NotNullViolation as e:
#         curs = conn.cursor()
#         curs.execute("ROLLBACK")
#         # return "Данные не корректные"


# # проверка числится ли устройство за кем то
# def check_inventory_card(device: str) -> dict:
#     sql = f"""
#         select card.uid, info.name, info.model,em.uid, em.name,
#         em.surname, em.patronymic, room.uid, room.floor, room.number 
#         from mainapp_inventorycard card 
#         left join mainapp_inventoryinfo info 
#         on card.inventory_number_uid_id  = info.uid 
#         left join mainapp_employee em 
#         on card.employee_uid_id = em.uid 
#         left join mainapp_rooms room
#         on card.room_uid_id = room.uid 
#         where info.uid  = '{device}';
#     """
#     sql_name_devices = f"""
#         select mi.name, mi.model  from mainapp_inventoryinfo mi 
#         where uid = '{device}'
#     """
#     with conn.cursor() as curs:
#         curs.execute(sql)
#         data = curs.fetchall()
#         # проверяем числится ли за кем то устройство
#         if data:
#             data = data[0]
#             all_info = {
#                 "name_model": data[1:3],
#                 "uid_emp": data[3],
#                 "user_name_surname_pat": data[4:7],
#                 "floor_uid": data[7],
#                 "floor_number": data[8:10],
#             }
#             return all_info
#         # Если устройство не числится ни за кем
#         else:
#             curs.execute(sql_name_devices)
#             name_model = curs.fetchall()[0]
#             all_info = {
#                 "не учтённое устройство сверка": f"Устройство <b>{name_model[0]}</b>, модель <b>{name_model[1]}</b> ещё не используется, проведите учёт",
#                 "не учтённое устройство учёт": "None",
#             }
#             return all_info


# # Вставка в таблицу inventory_card
# def insert_inventorycard(all_devices: list, employee: str, office: str) -> dict:
#     response = {"учтён": [], "не учтён": [], "uid": {"employee": "", "office": "", "devices": [], "name_model": []}}

#     sql_user = f"""
#         select em.surname, em.name, em.patronymic 
#         from mainapp_employee em where em.uid = '{employee}';
#     """

#     with conn.cursor() as curs:
#         for dev in all_devices:
#             check_device = check_inventory_card(dev)  # возвращаем словарь
#             sql_name_devices = f"""
#                 select mi.name, mi.model  from mainapp_inventoryinfo mi 
#                 where uid = '{dev}'
#             """
#             sql_insert = f"""
#                 insert into mainapp_inventorycard (uid, inventory_number_uid_id, employee_uid_id, room_uid_id)
#                 values ((select uuid_generate_v4()),
#                 (select i.uid  
#                 from mainapp_inventoryinfo i 
#                 where i.uid = '{dev}'),
#                 ('{employee}'),
#                 ('{office}'));
#             """
#             # Если устройство не зарегано ни за кем
#             if "не учтённое устройство учёт" in check_device.keys():
#                 curs.execute(sql_insert)
#                 conn.commit()
#                 curs.execute(sql_name_devices)
#                 name_model = curs.fetchall()[0]  # <--- Название устройства и модель
#                 curs.execute(sql_user)
#                 employee_fio = curs.fetchall()[0]  # <--- ФИО сотрудника
#                 response["учтён"].append(
#                     f"Устройство <b>{name_model[0]}</b>, модель <b>{name_model[1]}</b> теперь учтено за cотрудником "
#                     f"<b>{' '.join(employee_fio)}</b>"
#                 )

#             # Если устройство зарегано на этого же пользователя и помещении
#             elif check_device["uid_emp"] == employee and check_device["floor_uid"] == office:
#                 response["учтён"].append(
#                     f"Устройство <b>{check_device['name_model'][0]}</b>, "
#                     f"модель <b>{check_device['name_model'][1]}</b> уже числится за "
#                     f"<b>{' '.join(check_device['user_name_surname_pat'])}</b> на "
#                     f"{check_device['floor_number'][0]} этаже в {check_device['floor_number'][1]} помещении"
#                 )
#             # Если устройство зарегано за сотрудником но находится в другом помещении
#             elif check_device["floor_uid"] != office and check_device["uid_emp"] == employee:
#                 response["не учтён"].append(
#                     f"Устройство <b>{check_device['name_model'][0]}</b>, модель <b>{check_device['name_model'][1]}</b> "
#                     f"зарегистрировано за {' '.join(check_device['user_name_surname_pat'])} "
#                     f"но находится в {check_device['floor_number'][0]} помещении на "
#                     f"{check_device['floor_number'][1]} этаже, попробуйте перенести устройство в нужное помещение"
#                 )
#                 response["uid"]["employee"] = employee
#                 response["uid"]["office"] = office
#                 response["uid"]["devices"].append(dev)
#                 response["uid"]["name_model"].append(" ".join(check_device["name_model"]))
#             # Если устройство зарегано не на нашем сотруднике
#             elif check_device["uid_emp"] != employee:
#                 response["не учтён"].append(
#                     f"Устройство <b>{check_device['name_model'][0]}</b>, модель <b>{check_device['name_model'][1]}</b> "
#                     f"зарегистрировано за <b>{' '.join(check_device['user_name_surname_pat'])}</b> "
#                     f"и находится в <b>{check_device['floor_number'][0]}</b> помещении на "
#                     f"<b>{check_device['floor_number'][1]}</b> этаже, попробуйте поменять владельца с помощью функции перемещения"
#                 )
#                 response["uid"]["employee"] = employee
#                 response["uid"]["office"] = office
#                 response["uid"]["devices"].append(dev)
#                 response["uid"]["name_model"].append(" ".join(check_device["name_model"]))

#     return response


# # ФИО сотрудника
# def select_bio_employee(employee_uid: str) -> str:
#     sql_user = f"""
#         select em.surname, em.name, em.patronymic 
#         from mainapp_employee em where em.uid = '{employee_uid}';
#     """
#     with conn.cursor() as curs:
#         curs.execute(sql_user)
#         user_name = curs.fetchall()[0]
#     return " ".join(user_name)


# # Сверка девайса с сотрудником и офисом
# def select(all_devices: list, user: str, office: str) -> dict:
#     response = {"учтён": [], "не учтён": [], "uid": {"employee": "", "office": "", "devices": [], "name_model": []}}

#     # Прогоняем каждое устройство
#     for dev in all_devices:
#         sql = f"""
#             select card.uid, info.name, info.model,em.uid, em.name,
#             em.surname, em.patronymic, room.uid, room.floor, room.number 
#             from mainapp_inventorycard card 
#             left join mainapp_inventoryinfo info 
#             on card.inventory_number_uid_id  = info.uid 
#             left join mainapp_employee em 
#             on card.employee_uid_id = em.uid 
#             left join mainapp_rooms room
#             on card.room_uid_id = room.uid 
#             where info.uid  = '{dev}';
#         """

#         sql_name_device = f"""
#             select mi.name, mi.model  from mainapp_inventoryinfo mi 
#             where uid = '{dev}'
#         """

#         with conn.cursor() as curs:
#             curs.execute(sql)
#             data = curs.fetchall()
#             # Проверяем числится ли за кем то данное устройство
#             if data:
#                 data = data[0]
#                 all_info = {
#                     "name_model": data[1:3],
#                     "uid_emp": data[3],
#                     "user_name_surname_pat": data[4:7],
#                     "floor_uid": data[7],
#                     "floor_number": data[8:10],
#                 }

#                 # Проверяем числится ли это устройство на данном сотруднике
#                 if all_info["uid_emp"] != user:
#                     insert_depen_temp(dev, user, office)
#                     response["учтён"].append(
#                         f"Устройство <b>{all_info['name_model'][0]}</b>, модель <b>{all_info['name_model'][1]}</b> числится за "
#                         f"<b>{' '.join(all_info['user_name_surname_pat'])}</b> на <b>{all_info['floor_uid'][0]}</b> этаже в помещении "
#                         f"<b>{all_info['floor_uid'][1]}</b>. Проведите перемещение если необходимо."
#                     )

#                 # Проверяем числится ли это устройство в этом офисе
#                 elif all_info["floor_uid"] != office:
#                     insert_depen_temp(dev, user, office)
#                     response["учтён"].append(
#                         f"Устройство <b>{all_info['name_model'][0]}</b>, модель <b>{all_info['name_model'][1]}</b> находится на "
#                         f"<b>{all_info['floor_number'][0]}</b> этаже в помещении <b>{all_info['floor_number'][1]}</b>"
#                     )

#                 # если всё ок то добавляем в response с ключем учтён
#                 else:
#                     response["учтён"].append(
#                         f"Устройство <b>{all_info['name_model'][0]}</b>, модель <b>{all_info['name_model'][1]}</b> сходится с cотрудником "
#                         f"<b>{' '.join(all_info['user_name_surname_pat'])}</b>"
#                     )
#             # Если устройство не числится то заполняем в отдельные ключи в словаре
#             else:
#                 # Достаем из БД имя устройства и модель.
#                 curs.execute(sql_name_device)
#                 name_model = curs.fetchall()[0]
#                 response["не учтён"].append(
#                     f"Устройство <b>{name_model[0]}</b>, модель <b>{name_model[1]}</b> ещё не используется, проведите учёт"
#                 )
#                 response["uid"]["employee"] = user
#                 response["uid"]["office"] = office
#                 response["uid"]["devices"].append(dev)
#                 response["uid"]["name_model"].append(" ".join(name_model))

#     return response


# # Вставка в таблицу movents
# def movents(all_devices: list, employee: str, office: str) -> dict:
#     response = {"учтён": [], "не учтён": []}
#     for dev in all_devices:
#         sql_employee = f"""
#             select em.surname, em.name, em.patronymic 
#             from mainapp_employee em where em.uid = '{employee}';
#         """

#         sql_name_device = f"""
#             select mi.name, mi.model  from mainapp_inventoryinfo mi 
#             where uid = '{dev}'
#         """
#         sql_update = f"""
#             insert into mainapp_movements (uid ,from_employee_uid_id, inventory_card_uid_id, to_employee_uid_id,  date)
#             values((select uuid_generate_v4()),
#             (select inv.employee_uid_id from mainapp_inventorycard inv where inv.inventory_number_uid_id = '{dev}'),
#             (select inv.uid  from mainapp_inventorycard inv where inv.inventory_number_uid_id = '{dev}'),
#             ('{employee}'),
#             (now()));

#             update mainapp_inventorycard a
#             set employee_uid_id = '{employee}',
#             room_uid_id = '{office}'
#             where inventory_number_uid_id = '{dev}';
#         """

#         with conn.cursor() as curs:
#             check_device = check_inventory_card(dev)
#             if "не учтённое устройство учёт" not in check_device.keys():
#                 # Добавляем в таблицу movents данные от кого -> кому | и делаем update таблицы inventory_card
#                 curs.execute(sql_update)
#                 conn.commit()  # <-- Сохроняем изменения
#                 # Так как хотим получить ФИО кому мы передали мы делаем еще один запрос для получения ФИО нашего сотруд.
#                 curs.execute(sql_employee)
#                 name_surname = curs.fetchall()[0]  # <-- Данные нашего сотрудника ФИО
#                 sql_room = f"""select room.floor, room.number from mainapp_rooms room where room.uid = '{office}' """
#                 curs.execute(sql_room)
#                 office_floor_number = curs.fetchall()[0]
#                 response["учтён"].append(
#                     f"Устройство <b>{check_device['name_model'][0]}</b> модель <b>{check_device['name_model'][1]}</b>  "
#                     f" теперь закреплено за <b>{' '.join(name_surname)}</b> на <b>{office_floor_number[0]}</b> этаже в <b>{office_floor_number[1]}</b> помещении"
#                 )

#             # Если устройство не числится то заполняем с ключом "не учтён"
#             else:
#                 curs.execute(sql_name_device)
#                 name_model = curs.fetchall()[0]
#                 response["не учтён"].append(
#                     f"Устройство <b>{name_model[0]}</b> модель <b>{name_model[1]}</b> ещё не используется, проведите учёт"
#                 )
#     return response


# # Детальная информация об устройстве
# def detail_device(device: str) -> str:
#     sql_device = f"""
#         select info."name", info.model, emp.surname, emp."name", emp.patronymic, room.floor, room."number" 
#         from mainapp_inventorycard inv 
#         left join mainapp_inventoryinfo info
#         on info.uid = inv.inventory_number_uid_id 
#         left join mainapp_employee emp
#         on emp.uid = inv.employee_uid_id 
#         left join mainapp_rooms room
#         on room.uid = inv.room_uid_id
#         where inv.inventory_number_uid_id = '{device}';
#     """

#     with conn.cursor() as curs:
#         curs.execute(sql_device)
#         result = curs.fetchall()
#         if result:
#             result = result[0]
#             return (
#                 f"Устройство: <b>{result[0]}</b>\n"
#                 f"Модель: <b>{result[1]}</b>\n"
#                 f'Сотрудник: <b>{" ".join(result[2:5])}</b>\n'
#                 f"Этаж: <b>{result[5]}</b>\n"
#                 f"Помещение: <b>{result[6]}</b>"
#             )
#         else:
#             return "Данное устройство не числится, проведите первичный учёт"


# # Детальная информация об офисе
# def detail_office(office: str) -> str:
#     sql_office = f"""
#         select room.floor as этаж,
#         room."number" as помещение, 
#         count(distinct inv.employee_uid_id) as колличество_сотрудников, 
#         count(inv.inventory_number_uid_id) as колличество_мат
#         from mainapp_rooms room
#         left join mainapp_inventorycard inv
#         on inv.room_uid_id = room.uid 
#         left join mainapp_employee emp
#         on emp.uid = inv.employee_uid_id
#         where room.uid = '{office}'
#         GROUP BY (этаж, помещение);
#     """

#     with conn.cursor() as curs:
#         curs.execute(sql_office)
#         result = curs.fetchall()
#         if result:
#             result = result[0]
#             return (
#                 f"Помещение: <b>{result[1]}</b>\n"
#                 f"Этаж: <b>{result[0]}</b>\n"
#                 f"Колличество сотрудников: <b>{result[2]}</b>\n"
#                 f"Колличество материальных ценнностей: <b>{result[3]}</b>"
#             )

#         else:
#             return "В данном помещении никто и ничто не числится"


# # Более подробная информация о офисе, кто находится в нем и сколько мат ценностей
# def detail_office_all(office):
#     sql = f"""
#         select emp.surname, emp."name", emp.patronymic, 
#         count(inv.inventory_number_uid_id) from mainapp_employee emp
#         left join mainapp_inventorycard inv
#         on inv.employee_uid_id = emp.uid 
#         where inv.room_uid_id = '{office}'
#         group by (emp.surname, emp."name", emp.patronymic);
#     """

#     with conn.cursor() as curs:
#         curs.execute(sql)
#         employees = curs.fetchall()
#         result = ""
#         for employee in employees:
#             result += f'Сотрудник <b>{" ".join(employee[0:3])}</b>: <b>{employee[3]}</b> мат ценностей\n'
#         return result


def detail_employee(employee: str) -> str:
    sql_employee = f"""
        SELECT emp.surname, emp."name", emp.patronymicon, coalesce(r.floor, 0) as flour, 
        coalesce(r."number", '') as "number", count(inv.uid)
        FROM employee emp
        LEFT JOIN inventory_card inv
        ON inv.employee_uid_id = emp.uid
        LEFT JOIN rooms r
        ON r.uid = inv.room_uid_id
        WHERE emp.uid = '{employee}'
        GROUP BY (r.floor, r."number", emp.surname, emp."name", emp.patronymicon);
    """
    with conn.cursor() as curs:
        curs.execute(sql_employee)
        result = curs.fetchall()
        if result:
            employee = f"<b>{' '.join(result[0][0:3])}</b>\n"
            for e in result:
                employee += f"‣ <b>{e[3]}</b> этаж <b>{e[4]}</b> помещение <b>{e[5]}</b> мат ценностей\n"
            return employee
        else:
            return "Такой сотрудник не числится"


async def check_id(user_id: int) -> bool:
    """
    Checks if a user with this id exists in the database
    """
    try:
        db = get_db()
        session: AsyncSession = await anext(db)
        sql = "select tg.uid from telegram_chat tg where tg.chat_uid = '%s';" % (int(user_id))
        cour = await session.execute(sql)
        user = cour.scalar()
        await session.commit()
        if user:
            return True
        else:
            return False
    except Exception:
        return False


async def update_chat_id(data: list[int, str]) -> bool:
    db = get_db()
    session: AsyncSession = await anext(db)
    chat_id = data[0]
    phone_number = data[1]
    sql_update = """UPDATE telegram_chat
                    SET chat_uid  = %s
                    WHERE
                    phone_number  = '%s'
                    returning chat_uid ;
                    """ % (chat_id, phone_number)
    try:
        cour = await session.execute(sql_update)
        result = cour.scalar()
        await session.commit()
        return result
    except Exception:
        return False


asyncio.run(update_chat_id([1234, '79112346524']))
