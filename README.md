Поиск закупок на zakupki.gov.ru по нескольким словосочетаниям одновременно

# Запуск приложения с нуля
## Скачайте проект
### 1 Вариант: клонируйте через `Git`
скачайте и установите `Git` с официального [сайта](https://git-scm.com/install/windows)
откройте командную строку, перейдите в папкув которую хотите установить проект:
```cmd
cd "путь до папки"
```
и выполните команды:
```cmd
git clone https://github.com/boggart86/zakupki-pro-search.git
```
```cmd
git branch -u origin/main
```
чтобы обновить приложение:
```cmd
git pull
```
### 2 Вариант: скачайте и распакуйте zip-архив

<img width="630" height="448" alt="zakupki-pro-search-readme1" src="https://github.com/user-attachments/assets/1e0caacf-562c-49c8-8f76-77c2b1d8e2ec" />

## Скачайте пакетный менеджер `uv`
Для Windows введите в PowrShell:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
подробнее об [установке uv](https://docs.astral.sh/uv/getting-started/installation/)
## Установите `Python 3.12`
Введите в командную строку
```cmd
uv python install 3.12
```
## Запустите приложение
Запустите файл `start_app.bat` (в папке проекта)
Открется окно с командной строкой и (при первом запуске) начнется загрузка зависимостей проекта и вкладка с локальным сайтом приложения в браузере, когда загрузка закончится, запустится сервер приложения и сайт заработает.
Пока открыто окно командной строки - сайт работает.
