from datetime import datetime


def ranking_row(rank: int, name: str, country: str, team: str, points: int) -> str:
    return f"""<tr class="ranking-row">\
<td class="text-center">{rank+1}</td>\
<td class="text-center">{name}</td>\
<td class="text-center">{country}</td>\
<td class="text-center">{team}</td>\
<td class="text-center">{points}</td>\
</tr>"""


def tournaments_row(tournament_id: int, name: str, ts: int) -> str:
    return f"""<tr class="tournament-row">\
<td><a href="javascript:getResults({tournament_id}, '{name}')">{name}</a></td>\
<td class="text-center">{datetime.strptime(str(ts), '%Y%m%d').date()}</td>\
</tr>"""


def results_row(rank: int, name: str, points: int) -> str:
    return f"""<tr class="result-row">\
<td class="text-center">{rank}</td>\
<td class="text-center">{name}</td>\
<td class="text-center">{points}</td>\
</tr>"""
