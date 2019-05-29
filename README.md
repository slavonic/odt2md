# odt3md
Конвертирует LibreOffice документ в церковнослявянский вариант Markdown.

## Установка

Требования:
* Python 3.7

Устанавливаем из репозитория `pip`:

    pip install odt2md

Другой вариант установки - для разработчика:

    git clone https://github.com/slavonic/odt2md.git
    cd odt2md
    python3.7 -m venv .venv
    . .venv/bin/activate
    pip install wheel
    pip install -r requirements.txt

## Тестирование

Установите в варианте для разработчика, затем

    . .venv/bin/activate
    pip install pytest
    pytest .

## Запуск и работа

### Конвертирование

Чтобы сконвертировать в Markdown документ `sample.odt`, запустите команду `odt2md`:

    python -m odt2md.odt2md sample.odt sample.zip

Результатом работы будет архив `sample.zip`, содержащий основной Markdown файл с именем
`content.md`, а также картинки в под-директории `Pictures`.

### Настройка профиля
Профиль управляет логикой отображения стиля LibreOffice на стиль Markdown.

В выходном документе Markdown могут активироваться следующие стилевые сегменты:
1. `bold` - выделение жирным шрифтом (`True`/`False`)
2. `italic` - выделение наклоном (`True`/`False`)
3. `kinovar` - выделение киноварью (красным) (`True`/`False`)
4. `wide` - выделение разрядкой (`True`/`False`)

Во входном документе LibreOffice мы имеем следующие параметры:
1. `font` - имя шрифта. Например: `Times Roman Cyrillic`
2. `color` - цвет. Например: `#ff0000`
3. `size` - размер. Например: `17pt`
4. `bold` - жирность шрифта. Например: `normal`, `bold`
5. `italic` - наклонный шрифт. Например: `normal`, `italic`
Любое из этих значений может быть `None`, что означает что используется значение
по умолчанию.

Профиль по умолчанию делает так:
1. Если входной шрифт `bold`, то устанавливает Markdown стиль `bold=True`
2. Если входной шрифт `italic`, то устанавливает Markdown стиль `italic=True`
3. Когда цвет шрифта `color=="#ff0000`, то устанавливает Markdown стиль `kinovar=True`
4. Никогда не активирует Markdown стиль с разрядкой

Профиль по умолчанию таков:
```python
from odt2md.emphasis import MarkdownStyle

def profile(font, color, size, bold, italic):
    '''
    Default transformation from LibreOffice to Markdown style
    '''
    bold = (bold == 'bold')
    italic = (italic == 'italic')
    kinovar = (color == '#ff0000')

    return MarkdownStyle(
        bold=bold,
        italic=italic,
        kinovar=kinovar,
        wide=False
    )
```

Для настройки своего профиля, надо создать файл с определением желаемого преобразования
и передать его в `odt2md` с помощью ключа `--profile`. Например:

    python -m odt2md.odt2md --profile sample_profile.py sample.odt sample.zip

Проще всего начать с того, что скопировать профиль по умолчанию в `sample.md` и затем
отредактировать для получения желаемого эффекта.

### Просмотр стилей исходного документа

Для просмотра стилей, используемых в документе LibreOffice, запустите команду

    python -m odt2md.show_styles sample.odt

Команда покажет только стили, которые действительно используются. Стили, которые определены
но не используются показаны не будут.


