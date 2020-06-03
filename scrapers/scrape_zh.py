#!/usr/bin/env python3

import scrape_common as sc

url = "https://gd.zh.ch/internet/gesundheitsdirektion/de/themen/coronavirus.html"
dd = sc.DayData(canton='ZH', url=url)
d = sc.download(url, silent=True)
d = d.replace('&nbsp;', ' ')
d = d.replace('<strong>', ' ').replace('</strong>', ' ')
# d = sc.filter(r"Im Kanton Zürich sind zurzeit|\(Stand|Total ([0-9]+) Todesfälle|Spitalbehandlung|beatmet", d)
#                                 <h2>Aktuelle Situation im Kanton Zürich (24.3.2020, 9.30 Uhr)</h2>
#                         
#                         
#                         
#                         <p>Im Kanton Zürich sind zurzeit 1211 Personen positiv auf das Coronavirus getestet worden. Total 5 Todesfälle (78-jährig, 80, 88, 96, 97).</p>
# <p>(Stand 24.3.2020, 9.30 Uhr)</p>


# 2020-03-26
"""
				<h2>Aktuelle Situation im Kanton Zürich (26.3.2020, 9.30 Uhr)</h2>
			
			
			
			<p>Im Kanton Zürich sind zurzeit 1476 Personen positiv auf das Coronavirus getestet worden.</p>
<p>152 positiv Getestete befinden sich in Spitalbehandlung, davon werden 32 künstlich beatmet.</p>
<p>Total 9 Todesfälle (78-jährig, 78, 80, 80, 85, 88, 90, 96, 97).</p>
<p>Die Gesundheitsdirektion beschafft sich eine Maschine, die täglich automatisch bis zu 32'000 FFP2-Schutzmasken herstellen kann. In der zweiten Hälfte des Monats April ist die Maschine betriebsbereit.&nbsp;</p>
<p>(Stand 26.3.2020, 9.30 Uhr)</p>
"""

# 2020-03-27
"""
                                <h2>Aktuelle Situation im Kanton Zürich (27.3.2020, 9.30 Uhr)</h2>
...
                        <p>Im Kanton Zürich sind zurzeit 1578 Personen positiv auf das Coronavirus getestet worden.</p>
<p>156 positiv Getestete befinden sich in Spitalbehandlung, davon werden 37 künstlich beatmet.</p>
<p>Total 11 Todesfälle (75-jährig, 78, 78, 78, 80, 80, 85, 88, 90, 96, 97).</p>
<p>Um für den erwarteten Ansturm auf die Spitäler auch personell gerüstet zu sein, hat die Gesundheitsdirektion einen Pool für Gesundheitsfachpersonal eingerichtet. Spitäler können darüber rasch und unkompliziert zusätzliches Personal anfordern und die medizinische Versorgung so auch bei einem rasanten Anstieg an hospitalisierten Corona-Fällen sicherstellen. Gesundheitsfachpersonal kann sich ab sofort <a href="https://www.careanesth.com/covid-19/pool" target="_blank" rel="noopener noreferrer">hier bewerben.</a></p>
<p>Die Gesundheitsdirektion beschafft sich eine Maschine, die täglich automatisch bis zu 32'000 FFP2-Schutzmasken herstellen kann. In der zweiten Hälfte des Monats April ist die Maschine betriebsbereit.&nbsp;</p>
<p>(Stand 27.3.2020, 9.30 Uhr)</p>
"""

# 2020-03-31
"""
				<h2>Aktuelle Situation im Kanton Zürich (31.3.2020, 17.00 Uhr)</h2>
			
			
			
			<p>Zurzeit sind <strong>1960&nbsp;</strong>Personen mit Wohnsitz im Kanton Zürich positiv auf das Coronavirus getestet worden.</p>
<p><strong>197</strong>&nbsp;positiv Getestete befinden sich in Spitalbehandlung, davon werden <strong>51</strong> künstlich beatmet.</p>
<p>Total <strong>25</strong>&nbsp;Todesfälle (65-jährig, 70, 75, 75, 78, 78, 78, 80, 80, 80, 83, 84, 85, 85, 85, 86, 87, 88, 90, 91, 92, 94, 96, 97, 97).</p>
<p>Die Zahlen werden neu täglich um 17.00 Uhr publiziert.</p>
<p>Um für den erwarteten Ansturm auf die Spitäler auch personell gerüstet zu sein, hat die Gesundheitsdirektion einen Pool für Gesundheitsfachpersonal eingerichtet. Spitäler können darüber rasch und unkompliziert zusätzliches Personal anfordern und die medizinische Versorgung so auch bei einem rasanten Anstieg an hospitalisierten Corona-Fällen sicherstellen. Gesundheitsfachpersonal kann sich ab sofort <a href="https://www.careanesth.com/covid-19/pool" target="_blank" rel="noopener noreferrer">hier bewerben.</a></p>
<p>Die Gesundheitsdirektion beschafft sich eine Maschine, die täglich automatisch bis zu 32'000 FFP2-Schutzmasken herstellen kann. In der zweiten Hälfte des Monats April ist die Maschine betriebsbereit.&nbsp;</p>
<p>(Stand 31.3.2020, 17.00 Uhr)</p>
"""

# 2020-04-07
"""
<h3>Die Situation im Kanton Zürich am Dienstag, 7. April 2020, 15.00 Uhr</h3>
"""

date_time_info = sc.find('Stand (.+) Uhr', d)
if date_time_info is None:
    date_time_info = sc.find('Situation im Kanton Zürich\s*(?:am\s*)?(?:[A-Za-z]*[,:]?)?\(?([^)<]+)\)?', d)
dd.datetime = date_time_info

cases = sc.find('Im .* Zürich .* ([0-9]+) Person(en)? posit', d)
if not cases:
    cases = sc.find('Zurzeit sind\s*([0-9]+)\s*Personen mit Wohnsitz', d)
dd.cases = cases

deaths = sc.find('Im .* Zürich .* Total ([0-9]+) Todesfälle', d)
if not deaths:
    deaths = sc.find('Total\s*([0-9]+)\s*Todesfälle', d)
dd.deaths = deaths

dd.hospitalized = sc.find('([0-9]+)\s*positiv\s*Getestete\s*befinden\s*sich\s*in\s*Spitalbehandlung', d)

dd.vent = sc.find('davon\s*werden\s*([0-9]+)\s*künstlich\s*beatmet', d) or \
    sc.int_or_word(sc.find('davon\s+wird\s+(\S+)\s+Patient\s+künstlich\s+beatmet', d))

dd.isolated = sc.find(r'(\d+)\s+Personen\s+in\s+Isolation', d)
dd.quarantined = sc.find(r'(\d+)\s+in\s+Quarantäne', d)

print(dd)
