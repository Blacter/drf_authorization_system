<h3>Описание структуры управления ограничениями доступа</h3>

За основу взята модель RBAC (role-based access control)

Для разграничения доступа используются таблицы
usergroup, хранящая группы пользователей (роли),
accessactions, хранящая действия.

Пользователи добавляются в одну или несколько групп пользователей,
группы пользователей связаны с одним или несколькими действиями.

Если хотя бы у одной из ролей пользователя есть действие А,
то считается, что пользователь имеет доступ к действию А.
Если ни у одной из ролей нет действия В,
то считается, что пользователь не имеет доступ к действию В.

Действие связывается с определённым эндпоинтом с помощью декоратора,
в параметрах которого указывается соответствующее этому эндпоинту действие.

---

<h3>Аутентификация</h3>

Аутентификация выполнена на основе JWT, время жизни токена 5 минут.
Время жизни можно настроить в <пакет конфигурации>.settings.JWT_EXP.
Логика аутентификации сосредоточена в AuthenticationService

Токен хранится в cookies, токен извлекается и записывается в cookies 
с помощью middleware

---

для настройки БД используется .env файл в пакете конфигурации,
структура файла:
```
DATABASE_NAME="name_db"
DATABASE_USER="user_db"
DATABASE_PASSWORD="db_password"
DATABASE_HOST="host"
DATABASE_PORT="port"
SECRET_KEY="для валидации подписи jwt"
```
---

Интерфейс

signup path="/api_draft/v1/signup/" POST
пример тела запроса:
```json
{
    "first_name": "ИванА",
    "surname": "ИвановА",
    "patronymic": "ИвановичА",
    "email": "Ivan3@email.com",
    "password": "123456789",
    "password_repeat": "123456789"
}
```
login path="/api_draft/v1/login/" POST
пример тела запроса
```json
{
    "email": "Ivan3@email.com",
    "password": "123456789"
}
```

logout path="/api_draft/v1/logout/" GET

delete_profile  path="/api_draft/v1/delete_profile/" DELETE
(мягкое удаление профиля, профиль остаётся в БД, но соответствующему пользователю нельзя произвести логин)
Пример тела запроса (ввод логина, пароля для подтверждения действия)
```json
{
    "email": "Ivan1@email.com",
    "password": "123456789"
}
```
update_profile path="/api_draft/v1/update_profile/" PATCH
 (обновление ФИО целиком, либо части(отдельно имени и/или фамилии и/или отчества))
пример тела запроса:
```json
{
    "first_name": "ИванФ",
    "surname": "ИвановФ",
    "patronymic": "ИвановичФ"
}
```
ресурс доступный простому пользователю 
path = "/api_draft/v1/resource_simple/" GET

path = "/api_draft/v1/resource_vip/" GET
ресурс доступный вип-пользователю

path = "/api_draft/v1/resource_admin/" GET
ресурс доступный администраторам


<h3>управление правилами предоставления доступа</h3>

получить все роли с соответствующими им действиями
path = "/api_draft/v1/get_user_groups/" GET

получить роли пользователя
path = "/api_draft/v1/get_user_with_user_groups/?email=Ivan1@email.com" GET
пример query_string:
email=Ivan1@email.com

добавить пользователя в группу
path = "/api_draft/v1/add_user_group_to_user/" POST
пример тела запроса:
```json
{
    "email": "Ivan1@email.com",
    "group_name": "vip_user"
}
```
удалить пользователя из группы
path = "/api_draft/v1/delete_user_group_from_user/" POST
пример тела запроса
```json
{
    "email": "Ivan1@email.com",
    "group_name": "vip_user"
}
```
