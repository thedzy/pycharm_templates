# Pycharm Shell Templates

### My Shell templates using Apache Velcoity

## blank_shell.sh:

Standard shell with no parameters parsing

```shell
bash blank_shell.bash

2025-02-27T15:37:16 [ DEBUG    ] debug message
2025-02-27T15:37:16 [ INFO     ] info message
2025-02-27T15:37:16 [ WARNING  ] warning message
2025-02-27T15:37:16 [ ERROR    ] error message
2025-02-27T15:37:16 [ CRITICAL ] critical message
```

## blank_shell_getops_params.sh:

Standard shell with get ops defined paremeters and help

```shell
bash blank_shell_getops_params.bash -b -p test

2025-02-27T15:31:02 [ INFO     ] PARAMETER_B=true
2025-02-27T15:31:02 [ INFO     ] PARAMETER_P=test
```

## blank_shell_stdin_params.sh:

Standard shell with stdin parameters and positional parameters

```shell
echo stdin | bash blank_shell_stdin_params.bash 1 2 3

2025-02-27T15:35:34 [ INFO     ] Parameter 01: stdin
2025-02-27T15:35:34 [ INFO     ] Parameter 02: 1
2025-02-27T15:35:34 [ INFO     ] Parameter 03: 2
2025-02-27T15:35:34 [ INFO     ] Parameter 04: 3
```

## blank_shell_undefined_params.sh:

Standard shell with undefined parameters, any named parameter is parsed

```shell
bash blank_shell_undefined_params.bash 1 2 3 --test 1 -b -x 123

2025-02-27T15:33:33 [ INFO     ]            b = true
2025-02-27T15:33:33 [ INFO     ]   positional = ([0]="1" [1]="2" [2]="3")
2025-02-27T15:33:33 [ INFO     ]         test = 1
2025-02-27T15:33:33 [ INFO     ]            x = 123
```