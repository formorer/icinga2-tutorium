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

![Cluster](https://raw.githubusercontent.com/formorer/icinga2-tutorium/ffg/assets/Icinga2_Grundprinzip.png)

#VSLIDE

## Verzeichnisstruktur

+++?gist=26a91af511a2bc7afb16a0816f9a6b39

## Host Objekt

+++?gist=3b79570a22fba8fe9e863d756b5724d9

## Simple Service

```cpp
apply Service "procs" {
  import "generic-service"

  check_command = "procs"

  assign where host.name == "myhostname"
}
```

####[check_procs](https://docs.icinga.com/icinga2/latest/doc/module/icinga2/chapter/plugin-check-commands#plugin-check-command-processes)

#VSLIDE

## Override Variables in Service


```cpp
apply Service "procs" {
  import "generic-service"

  check_command = "procs"

  vars.procs_argument = "some argument"
  assign where host.name == "myhostname"
}
```

####(Custom Attributed and Macros)[https://docs.icinga.com/icinga2/latest/doc/module/icinga2/chapter/monitoring-basics#custom-attributes]

#HSLIDE

## Checks und wo sie herkommen

* Icinga2 selbst liefert keine Checks mit
* Alle Checks die mit Nagios kompatibel sind werden auch mit Icinga2 funktionieren
* Viele Checks sind in der (ITL)[https://docs.icinga.com/icinga2/latest/doc/module/icinga2/chapter/plugin-check-commands] vordefiniert

#VSLIDE

## Monitoring Plugins


* **Die** Standard Checks für Nagios/Icinga/Icinga2
* (monitoring-plugins.org)[https://www.monitoring-plugins.org/]

#VSLIDE

## Icinga Exchange

* (Portal für Checks)[https://exchange.icinga.com/]