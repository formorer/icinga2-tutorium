#HSLIDE

## Icinga2 Tutorium
#### Frühjahrsfachgespräch der GUUG 2017

#HSLIDE
## Vorstellungsrunde

#VSLIDE
## Wer bin ich? 

* Senior Consultant credativ GmbH
* Debian/GRML Open Source Entwickler
* über 15 Jahre Erfahrung mit Monitoring
* Scrum Master

#VSLIDE
## Wer sind sie / wer seid ihr? 

* Du / Sie? 
* Tätigkeitsfeld
* Erfahrungen mit Monitoring
* Erfahrungen mit Icinga2
* Erwartungen an das Tutorium

#HSLIDE

![Logo](http://www.icinga.org/wp-content/uploads/2009/05/icinga_logo4.png)

#VSLIDE
## Was ist Icinga2

Icinga2 ist ein OpenSource Monitoring System das einfache und komplexe 
Monitoringszenarien abbilden kann. 
<br />
**Icinga2 ist kein Nagios Fork**

#VSLIDE
## Features I

* Clusterfähig
* komplexe Konfigurationssprache
* Remote Agent
* Erweiterbar
* kompatibel zu den Monitoring Plugins
* Trending via
  * Graphite
  * InfluxDB
  * PNP4Nagios
  * OpenTSDB

#VSLIDE
## Features II

* Nativer Windows Support (Agent)
* semantisches Logging via GELF
* Darstellung von Businessprozessen
* ITL

#VSLIDE
## Clustering

* Master/Satellite
* Master/Master (HA)
* Automatische Lastverteilung (Worker)
* Mehrstufige Setups
* Konfigurationssynchronisation
* X509

#VSLIDE
## Master mit Satelliten

![Cluster](assets/cluster1.png)

#VSLIDE
## HA Master

![Cluster](assets/cluster2.png)


#HSLIDE
## Grundlagen

#VSLIDE
### Grundrinzip

![Cluster](https://raw.githubusercontent.com/formorer/icinga2-tutorium/ffg/assets/Icinga2_Grundprinzip.png)

#VSLIDE
### Hosts

* Zu jedem gemonitorten Objekt gehört ein Hostobjekt
* Die Verfügbarkeit des Hosts ergibt sich durch den Status des `hostalive` checks
* Hosts können den [Status](https://docs.icinga.com/icinga2/latest/doc/module/icinga2/chapter/monitoring-basics#host-states) **UP**, **DOWN** und **UNREACHABLE** haben

#VSLIDE
###Services

* Services werden immer einem Host zugeordnet
* Ihr Status ergibt sich aus dem Ergebniss ihres `check_command`s
* Hosts können den [Status](https://docs.icinga.com/icinga2/latest/doc/module/icinga2/chapter/monitoring-basics#service-states) **OK**, **WARNING**, **CRITICAL** und **UNKNOWN** haben.

#VSLIDE
### Hard und Softstates

Ein Service Check muss eine bestimmte Anzahl (`max_check_attempts`) von Ergebnissen durchlaufen bevor Notifizierungen ausgelöst werden und der **HARD** Status erreicht wird. 

#HSLIDE

## Konfigurationsdateien

#VSLIDE

### Verzeichnisstruktur

+++?gist=26a91af511a2bc7afb16a0816f9a6b39

#VSLIDE

### Host Objekt

+++?gist=3b79570a22fba8fe9e863d756b5724d9

#VSLIDE

### Simple Service

```cpp
apply Service "procs" {
  import "generic-service"

  check_command = "procs"

  assign where host.name == "myhostname"
}
```

####[check_procs](https://docs.icinga.com/icinga2/latest/doc/module/icinga2/chapter/plugin-check-commands#plugin-check-command-processes)

#VSLIDE

### Override Variables in Service

```cpp
apply Service "procs" {
  import "generic-service"

  check_command = "procs"

  vars.procs_argument = "some argument"
  assign where host.name == "myhostname"
}
```

####[Custom Attributed and Macros](https://docs.icinga.com/icinga2/latest/doc/module/icinga2/chapter/monitoring-basics#custom-attributes)

#HSLIDE

## Konfigurationssprache

#VSLIDE

### Kommentare

```cpp
// Kommentar
/*
 * Auch ein Kommentar
*/
# sogar ich bin ein Kommentar
```

#VSLIDE

### [einfache Datentypen](https://docs.icinga.com/icinga2/latest/doc/module/icinga2/chapter/language-reference?highlight-search=array#types)

```cpp
27.3 # floating point number
```
```cpp
2.5m # duration (ms (milliseconds), 
       s (seconds), 
       m (minutes), 
       h (hours) and 
       d (days))
```
```cpp
"Hello World" # string
{{{
  Multi
  Line
  String
}}}
```
```cpp
true / false # boolean
```
```cpp
null
```

#VSLIDE
### Arrays

```cpp
  [ "hello", 42 ]
```

#VSLIDE
### Dictionarys

```cpp
{
  address = "192.168.0.1"
  port = 443
  ssl = true
}
```


#VSLIDE

### Apply Direktive

* Die Apply Direktive wendet Objekte auf andere Objekte an
* Services auf Hosts
* Notifications auf Services/Hosts
* Abhängigkeiten
* Scope wird die `assign` und `ignore` Regeln bestimmt

#VSLIDE

```cpp
object HostGroup "postgresql-server" {
  display_name = "PostgreSQL Server"

  assign where match("*psql*", host.name)
  ignore where match("*test", host.name)
}
```

#VSLIDE

```
apply Notification "notify-complex-customer" to Service {
  import "compex-customer-notification"

  assign where match("*has gold support 24x7*", service.notes) \\
    && (host.vars.customer == "customer-xy" || host.vars.always_notify == true)
  ignore where match("*internal", host.name) || \\
    (service.vars.priority < 2 && host.vars.is_clustered == true)
}
```

#VSLIDE

###`apply for` Direktive

* Anwenden von Objekten auf Basis von Listen or Dictionaries
* Ermöglicht komplexe Objekterstellung

#VSLIDE
### Mit Listen

```cpp
object Host "hostname" {
  ...
  vars.partitions = [ '/', '/boot' ]
}

apply Service "partition " for (partition in host.vars.partitions) {
        import "generic-service"
        check_command = "disk"
        vars.disk_partition = partition
        display_name = "Partition " + partition
        assign where host.vars.partitions
}
```

#VSLIDE

### Mit Dictionaries

```cpp
object Host "hostname" {
  ...
  vars.http_vhosts["http"] = {
    http_uri = "/"
    http_ssl = true
  }
}

apply Service "vhost_" for (vhost => config in host.vars.http_vhosts) {
        import "generic-service"
        check_command = "http"
        vars += config
        display_name = "Virtual Host " + vhost
}
```

#HSLIDE

## Checks

#VSLIDE

### Basics

* Icinga2 selbst liefert keine Checks mit
* Alle Checks die mit Nagios kompatibel sind werden auch mit Icinga2 funktionieren
* Viele Checks sind in der [ITL](https://docs.icinga.com/icinga2/latest/doc/module/icinga2/chapter/plugin-check-commands) vordefiniert

#VSLIDE

### Monitoring Plugins

* **Die** Standard Checks für Nagios/Icinga/Icinga2
* [monitoring-plugins.org](https://www.monitoring-plugins.org/)

#VSLIDE

### Icinga Exchange

* [Portal für Checks](https://exchange.icinga.com/)

#VSLIDE

### Funktionsweise von Plugins

* Icinga interpretiert den Returnstatus eines Plugins

RC | Result
---|-------
0  | OK / UP
1  | WARN / UP
2  | CRITICAL / DOWN
3  | UNKNOWN / DOWN

#VSLIDE

* Ausgabe von Plugins wird ignoriert
* Sollte den [Monitoring Plugin Development Guidelines](https://www.monitoring-plugins.org/doc/guidelines.html) folgen
* Plugins werden grundsätzlich ohne Shell aufgerufen

#VSLIDE

### check command

```cpp
object CheckCommand "check_http" {
  command = [ PluginDir + "/check_http" ]

  arguments = {
    "-H" = "$http_vhost$"
    "-I" = "$http_address$"
    "-u" = "$http_uri$"
    "-p" = "$http_port$"
    "-S" = {
      set_if = "$http_ssl$"
    }
    "--sni" = {
      set_if = "$http_sni$"
    }
    "-a" = {
      value = "$http_auth_pair$"
      description = "Username:password on sites with basic authentication"
    }
    "--no-body" = {
      set_if = "$http_ignore_body$"
    }
    "-r" = "$http_expect_body_regex$"
    "-w" = "$http_warn_time$"
    "-c" = "$http_critical_time$"
    "-e" = "$http_expect$"
  }

  vars.http_address = "$address$"
  vars.http_ssl = false
  vars.http_sni = false
}
```

#HSLIDE

## [Notifications](https://docs.icinga.com/icinga2/latest/doc/module/icinga2/chapter/object-types#objecttype-notification)

#VSLIDE

* Notifications sind Scripte die bei bestimmten Events aufgerufen werden
* Notifications können an einen User und/oder eine Gruppe gebunden werden.
* Jede Notification kann einen Filter haben der bestimmt zu welchen Zeiten sie ausgelöst wird
* Jeder User kann einen Filter haben der bestimmt wann er notifiziert werden will. 
* Über `types` und `states` Filter kann man einstellen bei welchen Events die Notification auslöst.

#VSLIDE

### Notification Beispiel

```cpp
object Notification "localhost-ping-notification" {
  host_name = "localhost"
  service_name = "ping4"

  command = "mail-notification"

  users = [ "user1", "user2" ]

  types = [ Problem, Recovery ]
}
```

#VSLIDE

### notification command
```cpp
object NotificationCommand "mail-host-notification" {
  import "plugin-notification-command"

  command = [ SysconfDir + "/icinga2/scripts/mail-host-notification.sh" ]

  env = {
    NOTIFICATIONTYPE = "$notification.type$"
    HOSTALIAS = "$host.display_name$"
    HOSTADDRESS = "$address$"
    HOSTSTATE = "$host.state$"
    LONGDATETIME = "$icinga.long_date_time$"
    HOSTOUTPUT = "$host.output$"
    NOTIFICATIONAUTHORNAME = "$notification.author$"
    NOTIFICATIONCOMMENT = "$notification.comment$"
    HOSTDISPLAYNAME = "$host.display_name$"
    USEREMAIL = "$user.email$"
  }
}
```
#VSLIDE

### notification script
```bash
#!/bin/sh
template=`cat <<TEMPLATE
***** Icinga  *****

Notification Type: $NOTIFICATIONTYPE

Service: $SERVICEDESC
Host: $HOSTALIAS
Address: $HOSTADDRESS
State: $SERVICESTATE

Date/Time: $LONGDATETIME

Additional Info: $SERVICEOUTPUT

Comment: [$NOTIFICATIONAUTHORNAME] $NOTIFICATIONCOMMENT
TEMPLATE
`

/usr/bin/printf "%b" "$template" \\
| mail -s "$NOTIFICATIONTYPE - $HOSTDISPLAYNAME - $SERVICEDISPLAYNAME is $SERVICESTATE" $USEREMAIL

```
#HSLIDE

## Eskalationen

#VSLIDE

* Eskalation ermöglichen es Notifications nach einer bestimmten Zeit zu eskalieren 
* Mehrere Eskalationen können gleichzeitig und überlappend aktiv sein

#VSLIDE

### Ein Beispiel

Wenn nach 10 Minuten keiner auf den Alarm per E-Mail reagiert hat, wird eine SMS 
an das Team herausgeschickt. Sollte nach weiteren 20 Minuten auch hier keiner reagieren 
erzeugt Asterisk mit Sprachsynthese einen bösen Anruf an den Vorgesetzen.

#VSLIDE

### Konfiguration

```cpp
object User "first_alert" {
  display_name = "First Alert by Mail"
  vars.email = "it@localhost"
}
object User "second_alert" {
  display_name = "Second Alert by SMS"

  vars.mobile = "+49 1723 1234567"
}
apply Notification "first_alert" to Service {
  import "generic-notification"
  command = "mail-notification"
  users = [ "first_alert" ]
  times = {
    begin = 0m
    end = 30m
  }
  assign where service.name == "ping4"
}
apply Notification "second_alert" to Service {
  import "generic-notification"
  command = "sms-notification"
  users = [ "second_alert" ]
  times = {
    begin = 30m
    end = 60m
  }
  assign where service.name == "ping4"
}
```
#HSLIDE

## Downtimes

#VSLIDE

* Downtimes ermöglichen es Ausnahmezeiten festzulegen in denen keine Notifizierungen erfolgen sollen
* z.B.: (un)geplante Wartungen, Zeiten mit hoher Last

#VSLIDE

### Fixed Downtimes

* Beginnen und enden zu einem festgelegten Zeitpunkt

### Flexible Downtimes

* Flexibles Fenster
* Beginnt erst ab eintreten eines Events während der Downtime Periode
* Endet nach eintreten des Events und der definierten Downtime Dauer

#VSLIDE

```cpp
apply ScheduledDowntime "backup-downtime" to Service {
  author = "icingaadmin"
  comment = "Scheduled downtime for backup"

  ranges = {
    monday = "02:00-03:00"
    tuesday = "02:00-03:00"
    wednesday = "02:00-03:00"
    thursday = "02:00-03:00"
    friday = "02:00-03:00"
    saturday = "02:00-03:00"
    sunday = "02:00-03:00"
  }

  assign where "backup" in service.groups
}
```
#HSLIDE

## Dependencies

#VSLIDE

* Abhängigkeiten werden benutzt um Beziehungen zwischen Hosts und/oder Services auszudrücken
* Abhängigkeiten werden zur Erreichbarkeitsberechnung benutzt
* Abhängige Services / Hosts erzeugen keine Notifications wenn ihr Parent nicht erreichbar ist
* zwischen einem Host und seinen Services besteht eine implizite Abhängigkeit
* Abhängigkeiten reagieren nur auf Hard States (ausser `ignore_soft_states` ist `false`)

#VSLIDE

```cpp
apply Dependency "internet" to Host {
  parent_host_name = "dsl-router"
  disable_checks = true
  disable_notifications = true

  assign where host.name != "router"
}

apply Dependency "disable-host-service-checks" to Service {
  disable_checks = true
  assign where true
}
```

#HSLIDE

## Acknowledgments

#VSLIDE

* Ein Acknowledgment zeigt das man einen Alarm zur Kenntniss genommen hat
* Nach einem Acknowledge erfolgen keine weiteren Alarme
* Das Webfrontend sortiert die bestätigten Alarme hinter die unbestätigten Alarme
* **Sticky** Acknowledgement: das Acknowledgment verschwindet erst bei einem **OK** Status
* **Expiring** Ack: Wenn sich um das Problem nicht nach einer bestimmten Zeit gekümmert wurde, wird die Bestätigung entfernt

#HSLIDE

## Erweiterungen / Integration

#VSLIDE

### [Icinga-web2-director](https://github.com/Icinga/icingaweb2-module-director)

* Icingaweb2 Modul
* *Konfigurationswebfrontend* für Icinga2
* Module für den Import von verschiedenen Quellen:
  * CSV
  * Puppetdb
  * LDAP
  * Dateien
  * AWS
* REST API

#VSLIDE

![screenshot](https://github.com/Icinga/icingaweb2-module-director/raw/master/doc/screenshot/director/readme/director_main_screen.png)

#VSLIDE

# [Icingaweb2-Business-Process-View](https://github.com/Icinga/icingaweb2-module-businessprocess)

* Modellierung von Business Views
* *Manager* Kompatibilität
* Simulation von Incidents
* Webbasiserter Editor

#VSLIDE

![screenshot](https://github.com/Icinga/icingaweb2-module-businessprocess/raw/master/doc/screenshot/13_web-components-tile-renderer/1302_tile-and-subtree.png)

#VSLIDE

### Slack Integration

* [formorer/icinga2-slack-notification](https://github.com/formorer/icinga2-slack-notification)
* [spjmurray/slack-icinga2](https://github.com/spjmurray/slack-icinga2) (2way)
* [richardhauswald/icinga2-slack-notifications](https://exchange.icinga.com/richardhauswald/icinga2-slack-notifications)

#VSLIDE

### [Icinga2 Dashing](https://github.com/Icinga/dashing-icinga2)

* Sinatra/Dashing basiertes Dashboard
* Benutzt die API

#VSLIDE

![screenshot](https://github.com/Icinga/dashing-icinga2/raw/master/public/dashing_icinga2_overview.png)