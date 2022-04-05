Edit `config.ini` next to `main.py`. The file is created at first launch.

## Default values

```ini
[Settings]
debug = 0
dev = False
scale = 1
```

## Description

| Options | Type    | Nullable | Description                                                         | Values          |
|---------|---------|----------|---------------------------------------------------------------------|-----------------|
| `debug` | `int`   | Yes      | Set the verbosity of the script. Higher values will have more text. | `0`-`4`         |
| `dev`   | `bool`  | Yes      | Set dev mode. Will save images in `.temp/` folder.                  | `True`, `False` |
| `scale` | `float` | Yes      | Set scale.                                                          | `1`             |
|         |         |          |                                                                     |                 |

## More info

### Debug

Debug enum can be found here: <https://github.com/kevingrillet/Py-AFK/blob/main/utils/constant.py>

|    Name     | Value |
|:-----------:|:-----:|
|  `ALWAYS`   |  `0`  |
|   `INFO`    |  `1`  |
|   `CLASS`   |  `2`  |
| `FUNCTIONS` |  `3`  |
|   `DEBUG`   |  `4`  |
|             |       |

### Scale

Scale is based on mine: `HD` which is: `1920x1080`.

|        Name         | Resolution  | Scale |
|:-------------------:|:-----------:|:-----:|
| `HD 1080` / `1080p` | `1920x1080` |  `1`  |
|                     |             |       |

<hr>

<div align="center">
<a href="https://github.com/kevingrillet/Py-AFK/wiki/Home">Previous page</a>
|
<a href="https://github.com/kevingrillet/Py-AFK/wiki/Sources">Next page</a>
</div>
