import random
import mysql.connector
import rule
from geopy import distance


def connect_db():
    return mysql.connector.connect(
         host='localhost',
         port= 3306,
         database='lentopeli',
         user='user2',
         password='sala2',
         autocommit=True
    )


connection = connect_db()

#FUNCTIONS
#valitse peliin Suomen keskisuuret ja suuret lentokentät (yhteensä 31)
def get_airports():
    query = """SELECT ident, name, latitude_deg, longitude_deg
FROM airport
WHERE iso_country = 'FI' AND (type = 'large_airport'
OR type = 'medium_airport');"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    return result


#saada tehtävät tietokannasta
def get_tasks():
    query = "SELECT * FROM task ORDER BY RAND();"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_screen_names():
    sql = f"select screen_name from game"
    cursor = connection.cursor()
    cursor.execute(sql)
    list = cursor.fetchall()
    names = []
    for n in list:
        names.append(n[0])
    return names

def create_new_player(name):
    query = f"INSERT INTO game (screen_name) VALUES('{name}');"
    cursor = connection.cursor()
    cursor.execute(query)
    player_id = cursor.lastrowid
    return player_id

def get_existing_game_id(name):
    query = f"SELECT id FROM game WHERE screen_name = '{name}';"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    id = result[0]
    return id

#locations käytetään icao koodi
def update_game(game_id, p_range, p_flight, loca=None, goal_loca=None):
    if goal_loca is None:
        query = f"UPDATE game SET location = '{loca}', player_range = {p_range}, player_flight = {p_flight} WHERE id = {game_id};"
    # päivitä location, player_range, player_flight,  game-taulussa
    else:
        query = f"UPDATE game SET player_range = {p_range}, player_flight = {p_flight}, location = '{loca}', " \
                f"goal_id = 1, goal_location = '{goal_loca}' WHERE id = {game_id};"
    print(query)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)

#luoda uusi peli: insert current airport, player range, player flight, goal airport --> game taulu
def create_game(airports, p_range, p_flight, p_id):
    # peli arpoo aloituslentokentä ja lentokentä, joka timantti sijaitsee
    start = random.choice(airports)
    diamond = random.choice(airports)
    while start == diamond:
        start = random.choice(airports)
        diamond = random.choice(airports)
    start_icao = start['ident']
    diamond_icao = diamond['ident']
    update_game(p_id, p_range, p_flight, start_icao, diamond_icao)
    return (start, diamond)

#get airport info
def get_airport_info(icao_code):
    query = f"SELECT ident, name, latitude_deg, longitude_deg " \
            f"FROM airport WHERE ident = '{icao_code}'"
    #print(query)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchone()
    return result

#laskea etäiisyys kahden lentokentä valillä
def calc_distance(icao_1, icao_2):
    airport1 = get_airport_info(icao_1)
    airport2 = get_airport_info(icao_2)
    #print(airport1)
    airport1_coord = (airport1['latitude_deg'], airport1['longitude_deg'])
    airport2_coord = (airport2['latitude_deg'],airport2['longitude_deg'])
    distance_km = distance.distance(airport1_coord, airport2_coord).km
    dist_rounded = round(distance_km)
    #print(distance_km)
    return dist_rounded

#saada lentokentät, joille pelaaja voi lentää
# metrimäärällään
def get_airports_in_range(airports, cur_airport, p_range):
    airports_in_range = []
    for airport in airports:
        distance_km = calc_distance(cur_airport['ident'], airport['ident'])
        if distance_km <= p_range and distance_km != 0:
            airports_in_range.append(airport)
    return airports_in_range

#PELI ALKAA
#kysy tarvitseko näyttää pelin sääntö
show_rules = input("Haluatko lukea pelin sääntöjä? Yes/No: ")
if show_rules.lower().strip() != "no":
    rule.play_rules()

print("1. Olet uusi pelaaja.")
print("2. Olet pelannut aikaisemmin.")
choose = int(input("Anna toiminnan numero (1 tai 2): "))
player_names = get_screen_names()
if choose == 1:
    name = input("Anna nimesi: ")
    while name in player_names or name == "":
        if name in player_names:
            print(f"{name} on olemassa. Anna uusi nimi.")
        elif name == "":
            print(f"Et syötetty nimeä. Anna uusi nimi.")
        name = input("Luo pelinimi: ")
    player_id = create_new_player(name)
elif choose == 2:
    print("Tervetuloa etsimään timanttia!")
    name = input("Anna nimesi: ")
    while name not in player_names:
        print(f"Nimi: {name} ei löytyy listasta.")
        name = input("Anna nimesi: ")
    player_id = get_existing_game_id(name)

player_range = 1000
player_flight = 15

#pelin lentokentät
all_airports = get_airports()

#luo peli pelaajalle, palauta pelaajan aloitus lentokentä, pelin lentokentä, jossa timantti
(starting, diamond_airport) = create_game(all_airports, player_range, player_flight, player_id)

print(f"diamond: {diamond_airport}")

current = starting
print(f"starting: {starting}")

#pelin kaikki tehtävät
tasks = get_tasks()

#Boolean kun timantti on löytynyt
game_win = False
game_lose = False

#pelin loopi
while game_win == False:
    #näyttää kenttien tiedot, etäiisyys ja pelaajan oma kmmäärä sekä lentokertaa jäljellä pelaajalle
    current_name = get_airport_info(current['ident'])['name']
    current_to_diamond = calc_distance(current['ident'], diamond_airport['ident'])
    print(f"{name}, olet nyt {current_name} lentokentällä.")

    print(f"Sinulla on nyt {player_range} km ja {player_flight} lentokertaa jäljellä.")
    print(f"Etäisyys timanttiin on noin yli {round(current_to_diamond - 100)} km.")
    input("Jatkamaan painamalla Enter-näppäintä...")


    #kysy jos pelaaja halua lisätä kmmäärä tekemällä tehtävä
    question = input("Haluatko voittaa lisä kilometrimäärä tai jatka matka? Y = Haluan, Enter-näppäin: Ohita ")
    # if question = Y niin tässä pitää yhdistaa Annan task funktio tai jotain tehtävästä
    # vastaus oiken saa lisää km, muuten miinus
    # player_range += km jos voitti, -= km jos vastaus oli väärin
    #päivitä game taulu (+ tai - km)

    #laskea etäisyys ja näyttää lentokentät, joihin pelaaja on mahdollista lentää
    in_range = get_airports_in_range(all_airports, current, player_range)
    if len(in_range) == 0:
        print("Peli loppui! Sinun kilometrimäärä ei riittää lentämiseksi. ")
        game_lose = True
        break
    print(f"Mihin haluat lentää? On {len(in_range)} lentokenttää, mihin voit lentää kilometrimäärälläsi.")
    input("Lentokentät:...")
    in_range_icao_list = []
    for airport in in_range:
        in_range_icao_list.append(airport['ident'])
        distance_km = calc_distance(current['ident'], airport['ident'])
        print(f"{airport['name']}, ICAO-koodi: {airport['ident']}, etäisyys: {distance_km} km")
    print(in_range_icao_list)

    #kysy
    icao = input("Mihin haluat jatkaa matkaa? Lentokentän ICAO-koodi: ")
    #Oletetaan että pelaaja valitse Rovaniemi airport
    #Pyytä uudelleen ICAO-koodi, jos se ei ole yllä olevassa luettelossa
    while icao not in in_range_icao_list:
        icao = input("Väärä ICAO-koodi. Kijoita uudestaan: ")

    #laskea etäisyys ja päivitä tietoja game-taululle
    distance_between = calc_distance(current['ident'], icao)
    player_range = player_range - distance_between
    current = get_airport_info(icao)
    player_flight = player_flight - 1
    print(player_flight)
    update_game(player_id, player_range, player_flight, icao)

    if current['ident'] == diamond_airport['ident']:
        print("Wau! Löysit timantin! Olet hyvä etsijä!")
        if player_flight == 0:
            print('peli loppuu')

        game_win = True

else:
    print("se meni tähän----")
print(f"game win: {game_win}")
print(f"game lose: {game_lose}")
print("Onnea! Voitit pelin! " if game_win else "")
print("Hävisit!" if game_lose else "")












connection.close()