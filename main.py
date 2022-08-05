import requests

from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


def get_all_teams():
    base_url = "https://salarysport.com"
    teams_base_url = "https://salarysport.com/tr/football/"
    teams = []

    response = requests.get(teams_base_url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    team_links = soup.find("div", attrs={
                           "class": "Layout__Box-sc-19mb7gg-0 Layout__Flex-sc-19mb7gg-1 OtherLinks__LinkContainer-sc-nrnd7r-0 jykxYM hkTbms bsemwg"})
    team_links_a = team_links.find_all("a", href=True)

    for team_link in team_links_a:
        teams.append(f"{base_url}{team_link['href']}")

    return teams


def get_team_players(url: str):
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url, headers=headers)

    # Parse the html content
    members = []
    soup = BeautifulSoup(html_content.content, "lxml")
    player_table = soup.find(
        "table", attrs={"class": "Table__TableStyle-sc-373fc0-0 koTFEC"})
    team_members_tr = player_table.tbody.find_all("tr")

    try:
        for team_member in team_members_tr:
            team_member_td = team_member.find_all("td")

            member = {
                "name": team_member_td[0].text,
                "weekly salary": team_member_td[1].text,
                "annual salary": team_member_td[2].text,
                "age": team_member_td[3].text,
                "position": team_member_td[4].text,
                "national": team_member_td[5].text
            }
            members.append(member)
    except:
        pass

    print(members)


def main():
    i = 0
    teams = get_all_teams()

    for team in teams:
        i += 1
        if i > 2:
            break
        try:
            get_team_players(team)
        except:
            print("Error: ", team)


main()
