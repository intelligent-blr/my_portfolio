Konzept
Ich habe eine Konsolenanwendung zur Filmsuche in der Sakila-Datenbank erstellt.
Als Datenquelle verwende ich eine Testdatenbank mit Filmen, die auf meinem lokalen Server installiert ist.
Alle eingegebenen Suchanfragen werden in einer separaten Tabelle in einer eigenen Datenbank gespeichert. Die Anwendung ermöglicht es, auf Befehl die beliebtesten Suchanfragen anzuzeigen.

Projektziel:
- Implementierung der Suchszenarien:
- Suche nach Schlüsselwort: Es werden 10+ Filme gefunden.
- Suche nach Genre und Jahr: Es werden 10+ Filme gefunden.
- Anzeige der beliebtesten Suchanfragen, nach denen gesucht wurde.

Projektablauf:

1. Ich habe die Testdatenbank auf meinem lokalen Server installiert und mich mit der Tabellenstruktur und den Inhalten vertraut gemacht, einschließlich der Beziehungen und Datentypen.
Ich habe einige Abfragen geschrieben, die Filme eines bestimmten Genres oder eines bestimmten Jahres anzeigen.
2. Basierend auf dem Verständnis der Datenbankstruktur und der Szenarien habe ich die erforderlichen SQL-Abfragen erstellt. Ich habe funktionierende Abfragen vorbereitet, die später in der Python-Anwendung verwendet werden.
3. Ich habe Abfragen erstellt, die die gewählten Suchbegriffe in einer separaten Tabelle speichern.
4. Ich habe Abfragen geschrieben, die die Suchanfragen nach Beliebtheit sortiert ausgeben – die häufigsten Suchanfragen erscheinen zuerst.
5. Nachdem die Abfragen funktionierten, habe ich die Python-Anwendung geplant und entwickelt sowie die Integration mit der Datenbank umgesetzt.
Die Anwendung wird aus der Konsole gestartet und arbeitet interaktiv, indem sie auf Eingaben wartet.
Der Benutzer gibt Befehle ein und erhält die Ergebnisse direkt in der Konsole.
Ich habe überlegt, welche Module/Klassen benötigt werden und wie die Logik auf verschiedene Module/Klassen/Funktionen verteilt werden kann.
Die gesamte Datenbankarbeit ist in einem separaten Modul implementiert, das vom Modul für die Benutzerinteraktion verwendet wird. Auch die Darstellung der Ergebnisse ist in ein separates Modul ausgelagert.
