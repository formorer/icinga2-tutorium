# Remote Service config

## Host Object

[check_load documentation](https://docs.icinga.com/icinga2/latest/doc/module/icinga2/chapter/plugin-check-commands#plugin-check-command-load)

```
  object Host "remote" {
    import "generic-host"
    address = "remote"
    # example for overriding values
    vars.load_wload1 = 4
    vars.load_wload5 = 3
    vars.load_wload15 = 2

    vars.remote_client = "remote"
  }
```

## Example Service

```
  apply Service "load" {
    import "generic-service"
    check_command = "load"
    command_endpoint = host.vars.remote_client
    assign where host.vars.remote_client
  }
```

