# useful-custom-python-libs
A few useful self-written python libraries
___
## Logger
Use this custom logger to have a beautiful logging experience.
Supports multiple arguments to be formatted to string automatically.
Change color for single messages and separate your arguments witch customisable strings.
Use markdowns for fancy formats.
Two loggers documents your output for the last session and with history.
Use in productive space with different logging levels, for example errors only.
### `info(msg, *args, obj=None, join=" ", color=None)`
Logs a low level message.

| Parameter | Default | Description |
|-----------|---------|------------|
|  msg      | None |    The message to be logged |
| *args | None | Multiple messages can be given to this function, all arguments will be handled as string |
| obj | None | A reference to an object to find code position in easy way |
| join | ' ' | The string witch separates multiple arguments |
| color | None | The color of the message |


### `debug(msg, *args, obj=None, join=" ", color=None)`
Logs a message to be shown in debug mode

| Parameter | Default | Description |
|-----------|---------|------------|
|  msg      | None |    The message to be logged |
| *args | None | Multiple messages can be given to this function, all arguments will be handled as string |
| obj | None | A reference to an object to find code position in easy way |
| join | ' ' | The string witch separates multiple arguments |
| color | None | The color of the message |


### `warn(msg, *args, obj=None, join=" ", color=None)`
Logs a warning message to indicate that an error has occurred, but the program continues to run.

| Parameter | Default | Description |
|-----------|---------|------------|
|  msg      | None |    The message to be logged |
| *args | None | Multiple messages can be given to this function, all arguments will be handled as string |
| obj | None | A reference to an object to find code position in easy way |
| join | ' ' | The string witch separates multiple arguments |
| color | None | The color of the message |


### `error(msg, *args, obj=None, join=" ", color=None)`
Logs a critical error that may interrupt program execution.

| Parameter | Default | Description |
|-----------|---------|------------|
|  msg      | None |    The message to be logged |
| *args | None | Multiple messages can be given to this function, all arguments will be handled as string |
| obj | None | A reference to an object to find code position in easy way |
| join | ' ' | The string witch separates multiple arguments |
| color | None | The color of the message |
