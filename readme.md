### Connect U Project.

### Project Running Guide.

```bash
pipenv install
```

```bash
pipenv shell
```

# Project Documentation

-   `api app`
    In This App We Have All The Api's For The Project.
    and we have all models in this app.

-   `core app`
    In This App We Have All The Core Functionalities For The Project.
    Basically we just manage user authentication in this app.


# Editor Setup

.vscode `settings.json`

```json
{
    "editor.fontFamily": "Fira Code, Operator Mono",
    "editor.fontLigatures": true,
    "editor.wordWrap": "on",
    "editor.minimap.enabled": false,
    "editor.tokenColorCustomizations": {
        "textMateRules": [
            {
                "scope": "comment",
                "settings": {
                    "fontStyle": "italic"
                }
            }
        ]
    },
    "editor.cursorSmoothCaretAnimation": "on",
    "editor.cursorBlinking": "expand",
    "editor.fontSize": 17,
    "editor.lineHeight": 23,
    "editor.formatOnSave": true,

    "[python]": {
        "editor.defaultFormatter": "ms-python.autopep8",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }

        // linter flake8
    },

    //terminal
    "terminal.integrated.fontSize": 14,
    "terminal.integrated.fontWeight": "normal",
    "terminal.integrated.fontFamily": "Fira Code, Operator Mono",
    "workbench.colorTheme": "Learn with Sumit Theme"
}
```

.flake8

```bash
[flake8]

max-line-length = 160
```