#!/usr/bin/env python

"""
Saves Fishtest CPU time contributions to a text file.
Requires Python >= 3.6 to take benefit of number formatting.
See README.md for more details.
"""

from datetime import date
from requests import get
from bs4 import BeautifulSoup

CPU_HOURS_THRESHOLD = 10000

page = get("https://tests.stockfishchess.org/contributors", allow_redirects=True, timeout=600)
soup = BeautifulSoup(page.content, "html.parser")

tbodys = soup.find_all("tbody")
assert len(tbodys) == 1
tbody = tbodys[0]
rows = tbody.find_all("tr")
contributors = []

for row in rows:
    tds = row.find_all("td")
    rank = tds.pop(0).text.strip()  # remove rank number (such as 1, 2, 3, ...)
    assert rank.isdigit()  # the first colun should be the numeric rank (a number)
    cpu_hours_str = tds[3].text.strip()
    cpu_hours_int = int(cpu_hours_str)
    games_played_str = tds[4].text.strip()
    games_played_int = int(games_played_str)
    if cpu_hours_int > CPU_HOURS_THRESHOLD:
        name = tds[0].text.strip()
        contributors.append([name, cpu_hours_int, games_played_int])

# join noob
noob = ["noobpwnftw", 0, 0]
noob_merge_names = {"ChessDBCN", "ChessDB_CN_WorkerPool"}
for t in contributors:
    if t[0] in noob_merge_names:
        noob[1] += t[1]
        noob[2] += t[2]
joined = [noob]
for t in contributors:
    if t[0] in noob_merge_names:
        pass
    else:
        joined.append(t)

# replace some names
replace_names = {}
replace_names["maximmasiutin"] = "Maxim Masiutin"
for t in contributors:
    if t[0] in replace_names:
        t[0] = replace_names[t[0]]

# output file
print(f"Contributors to Fishtest with >{CPU_HOURS_THRESHOLD:,} CPU hours, as of {date.today()}.")
print("Thank you!")
print("")
print(f"{'Username':32s} {'CPU Hours':>16s} {'Games played':>16s}")
print("------------------------------------------------------------------")
for contributor in joined:
    print(f"{contributor[0]:32s} {contributor[1]:16d} {contributor[2]:16d}")
