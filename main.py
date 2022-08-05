import json
import requests

from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


def get_all_teams():
    leagues_base_url = "https://www.fifaratings.com/leagues/"
    teams = []

    response = requests.get(leagues_base_url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    team_table = soup.find("table", {"class": "table table-sm table-striped nowrap mb-0"})
    team_links = team_table.find_all("a", href=True)
    
    for team_link in team_links:
        if "/league/" in team_link["href"]:
            teams.append(team_link["href"])

    return teams


def get_team_info(team_url: str):
    team_data = []
    html_content = requests.get(team_url, headers=headers)

    soup = BeautifulSoup(html_content.content, "lxml")
    team_table = soup.find("table", {"class": "table table-striped table-sm table-hover mb-0"})
    team_infos = team_table.tbody.find_all("tr")

    for team_info in team_infos:
        try:
            team_tds = team_info.find_all("td")

            if len(team_tds) > 3:
                team_url = team_tds[1].find("a")["href"]
                team_name = team_tds[1].text.strip().split(" ")
                team_name = team_name[0] + " " + team_name[1]
                team_points = team_tds[2].text.strip()
                
                team_data.append({
                    "url": team_url,
                    "name": team_name,
                    "points": team_points
                })
        except:
            pass

    return team_data


def get_team_players(data: dict):
    html_content = requests.get(data.get('url'), headers=headers)

    members = []
    soup = BeautifulSoup(html_content.content, "lxml")
    player_table = soup.find(
        "table", attrs={"class": "table table-striped table-sm table-hover mb-0"})
    team_members_tr = player_table.tbody.find_all("tr")


    for team_member in team_members_tr:
        try:
            team_member_td = team_member.find_all("td")
            player = team_member_td[1].text.strip().split(" ")
            player_name = player[0] + " " + player[1] + " " + player[2] + " " + player[3]
            player_overall_points = team_member_td[2].text.strip()
            player_potential_points = team_member_td[3].text.strip()

            member = {
                "name": player_name.strip(),
                "Overall": player_overall_points,
                "Potential": player_potential_points
            }
            members.append(member)
        except:
            pass

    data["players"] = members

    return data

def main():
    all_teams = []
    teams = get_all_teams()

    for team in teams:
        team_infos = get_team_info(team)

        for team_info in team_infos:
            data = get_team_players(team_info)
            all_teams.append(data)

    with open("data.json", "w") as f:
        json.dump(all_teams, f)

main()
