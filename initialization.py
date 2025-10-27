import crud
from models import User, Roles, AccessRule, ProductionElement

async def add_start_data():
    pes = [
        ProductionElement(name="ProductionElements"),
        ProductionElement(name="Rules"),
        ProductionElement(name="Roles"),
        ProductionElement(name="Users"),
        ProductionElement(name="Buildings"),
        ProductionElement(name="BuildingsInfo"),
        ProductionElement(name="BuildingsStats")
    ]

    roles = [
        Roles(name="Guest"),
        Roles(name="User"),
        Roles(name="Manager"),
        Roles(name="Admin"),
        Roles(name="Owner")
    ]

    guest_rules = [AccessRule(role=roles[0], production_element=pe) for pe in pes]
    guest_rules[4].read_permission = True

    user_rules = [AccessRule(role=roles[1], production_element=pe) for pe in pes]
    user_rules[4].read_permission = True
    user_rules[5].read_permission = True

    manager_rules = [AccessRule(role=roles[2], production_element=pe) for pe in pes]
    manager_rules[3].read_permission = True
    manager_rules[4].read_permission = True
    manager_rules[4].create_permission = True
    manager_rules[4].update_permission = True
    manager_rules[4].delete_permission = True
    manager_rules[5].read_permission = True
    manager_rules[5].create_permission = True
    manager_rules[5].update_permission = True
    manager_rules[5].delete_permission = True
    manager_rules[6].read_permission = True

    admin_rules = [AccessRule(role=roles[3], production_element=pe, read_permission=True) for pe in pes]
    admin_rules[3].create_permission = True
    admin_rules[3].update_permission = True
    admin_rules[3].delete_permission = True
    admin_rules[4].create_permission = True
    admin_rules[4].update_permission = True
    admin_rules[4].delete_permission = True
    admin_rules[5].create_permission = True
    admin_rules[5].update_permission = True
    admin_rules[5].delete_permission = True
    admin_rules[6].create_permission = True
    admin_rules[6].update_permission = True
    admin_rules[6].delete_permission = True

    owner_rules = [
        AccessRule(
            role=roles[3],
            production_element=pe,
            read_permission=True,
            create_permission=True,
            update_permission=True,
            delete_permission=True
        ) for pe in pes
    ]

    owner = [User(
        username="owner",
        email="",
        password_hash="",
        role=roles[4]
    )] # TODO: password_hash сделать из пароля в config

    for arr in (pes, roles, guest_rules, user_rules, manager_rules, admin_rules, owner_rules, owner):
        for el in arr:
            await crud.create(el)
