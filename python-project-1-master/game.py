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
    query = """SELECT municipality, ident, name, latitude_deg, longitude_deg
FROM airport
WHERE iso_country = 'FI' AND (type = 'large_airport'
OR type = 'medium_airport');"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    return result


#saada 29 tehtävää satunnaisesti tietokannasta
def get_tasks():
    query = "SELECT * FROM task ORDER BY RAND();"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

#luoda uusi peli: insert pelaajan nimi, current airport, player range, player flight --> game taulu
"""
def create_game(all_airports, p_range, p_flight, p_airport, p_name):
    #peli arpoo aloituslentokentä ja lentokentä, joka timantti sijaitsee
    #a = random.sample(all_airports, k=2)
    #(starting_airport, diamond_airport)
    query1 = "INSERT INTO game (player_range, player_flight, location, screen_name)
VALUES(200, 15, %s, %s);"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query1, (p_airport, p_name))
    p_id = cursor.lastrowid
    tasks = get_tasks()
    query2 = "INSERT INTO"
#create_game(300, 15, 'EFHA', 'Martti')
"""

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

#print(calc_distance("vvts", "efhk"))

#saada lentokentät, joille pelaaja voi lentää kilo
# metrimäärällään
def get_airports_in_range(airports, cur_airport, p_range):
    airports_in_range = []
    for airport in airports:
        distance_km = calc_distance(cur_airport['ident'], airport['ident'])
        if distance_km <= p_range and distance_km != 0:
            airports_in_range.append(airport)
    return airports_in_range

#päivitä location, player_range, player_flight,  game-taulussa
def update_location(game_id, icao, p_range, p_flight):
    query = f"UPDATE game SET location = '{icao}', player_range = {p_range}, player_flight = {p_flight} WHERE id = {game_id}"
    #print(query)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)




#PELI ALKAA
#kysy tarvitseko näyttää pelin sääntö
show_rules = input("Haluatko lukea pelin sääntöjä? Yes/No: ")
if show_rules.lower().strip() != "no":
    rule.play_rules()




player_name = input("Anna nimesi: ")
player_range = 200
player_flight = 15


#pelin lentokentät
all_airports = get_airports()

#pelaajan aloitus lentokentä
starting = all_airports[0]

#pelin lentokentä, jossa timantti
diamond_airport = all_airports[5]
print(f"diamond: {diamond_airport}")
#pelaajan nytkuinen lentokentä
current = starting
print(f"starting: {starting['name'], starting['ident']}")

#pelin kaikki tehtävät
tasks = get_tasks()


#Boolean kun timantti on löytynyt
diamond_found = False
game_lose = False

#luoda peli pelaajalle:
#create_game()
#kun tämä funktio on suoritettu, saamme player_id
player_id = 1


#pelin loopi
while game_lose == False:
    #näyttää kenttien tiedot, etäiisyys ja pelaajan oma kmmäärä sekä lentokertaa jäljellä pelaajalle
    current_name = get_airport_info(current['ident'])['name']
    current_to_diamond = calc_distance(current['ident'], diamond_airport['ident'])
    print(f"{player_name}, olet nyt {current_name} lentokentällä.")

    print(f"Sinulla on nyt {player_range} km ja {player_flight} lentokertaa jäljellä.")
    print(f"Etäisyys timanttiin on noin yli {round(current_to_diamond - 100)} km.")
    input("Jatkamaan painamalla Enter-näppäintä...")


    #kysy jos pelaaja halua lisätä kmmäärä tekemällä tehtävä
    question = input("Haluatko voittaa lisä kilometrimäärä tai jatka matka? Y = Haluan, Enter-näppäin: Ohita")
    # if question = Y niin tässä pitää yhdistaa Annan task funktio tai jotain tehtävästä
    # vastaus oiken saa lisää km, muuten miinus
    # player_range += km jos voitti, -= km jos vastaus oli väärin
    #päivitä game taulu (+ tai - km)

    #laskea etäisyys ja näyttää lentokentät, joihin pelaaja on mahdollista lentää
    in_range = get_airports_in_range(all_airports, current, player_range)
    if len(in_range) == 0:
        print("Sinun kilometrimäärä ei riittää lentämiseksi. Game over!")
        game_lose == True
        break
    print(f"Mihin haluat matka? On {len(in_range)} lentokenttää, mihin voit lentää kilometrimäärälläsi.")
    input("Lentokentät:")
    in_range_icao_list = []
    for airport in in_range:
        in_range_icao_list.append(airport['ident'])
        distance_km = calc_distance(current['ident'], airport['ident'])
        print(f"{airport['name']}, ICAO-koodi: {airport['ident']}, etäisyys: {distance_km} km")
    print(in_range_icao_list)
    #kysy
    icao = input("Anna lentokentän ICAO-koodi: ")
    #Oletetaan että pelaaja valitse Rovaniemi airport
    #Pyytä uudelleen ICAO-koodi, jos se ei ole yllä olevassa luettelossa
    while icao not in in_range_icao_list:
        icao = input("Anna lentokentän ICAO-koodi: ")
    #laskea ja päivitä tietoja game-taululle
    distance_between = calc_distance(current['ident'], icao)
    player_range = player_range - distance_between
    current = get_airport_info(icao)
    player_flight = player_flight -1
    print(player_flight)
    update_location(player_id, icao, player_range, player_flight)
    if player_flight == 0:
        print('peli loppuu')














connection.close()