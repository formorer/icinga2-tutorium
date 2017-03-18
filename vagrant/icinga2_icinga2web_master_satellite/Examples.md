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

# Dynamic creation of objects

```

vars.hcoenvs.foo1 = { customername = "My customer foo", domainpart = "foo-test" }
vars.hcoenvs.bar1 = { customername = "just another customer bar", domainpart = "bar-test" }
vars.hcoenvs.baz1 = { customername = "oh, we even have a third customer baz", domainpart = "baz-test" }


for (hcoenv_name => config in vars.hcoenvs) {
  object Service "shibboleth_status" use(hcoenv_name, config){
    vars += config
    import "remote-service"
    display_name = "Shibboleth Status for " + vars.customername
    check_command = "http"
    vars.http_address = "shib." + vars.domainpart + ".domain.ext"
    vars.http_vhost = "shib." + vars.domainpart + ".domain.ext"
    vars.http_port = "443"
    vars.http_ssl = "true"
    vars.http_uri = "/Shibboleth.sso/Status"
    vars.http_expect = "HTTP/1.1 200"
    host_name = hcoenv_name + ".my.domain"

  }
}
```
