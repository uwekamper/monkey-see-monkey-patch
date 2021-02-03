# This is a quick experiment

This code repository shows how one could add an additional Flask Blueprint to the Lektor admin.

The packages folder contains only a stub of what could (in the future) become a facebook plugin for Lektor.

For this demonstration though, it does nothing with Facebook – it is just an example!


## What does the plugin do?

The plugin will register a new URL inside the Lektor admin. You can browse manually
to this URL by entering http://localhost:5000/facebook/hello
into the your browser. It will display a simple "Hello World" message.


## How to run this:

instead of the usual `lektor server` you must start the modified version of the Lektor
web-UI by using the commmand:

```
(poetry run) python ./modified_lektor.py server
```

## How to install:

You need poetry (https://python-poetry.org), then just switch to this directory and run `poetry install`.
