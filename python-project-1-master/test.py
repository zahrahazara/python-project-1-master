import mysql.connector
import random
from geopy import distance
yhteys = mysql.connector.connect(
         host='localhost',
         port= 3306,
         database='lentopeli',
         user='user2',
         password='sala2',
         autocommit=True
         )
def create_airport():
    sql_n = "select name, ident, longitude_deg, latitude_deg " \
            "from airport where iso_country = 'FI' " \
            "AND (TYPE = 'medium_airport' or TYPE = 'large_airport')"

    kursori = yhteys.cursor()
    kursori.execute(sql_n)
    nimet = kursori.fetchall()

    pelaaja = random.choice(nimet)
    timantti = random.choice(nimet)


    while pelaaja == timantti:
        pelaaja = random.choice(nimet)
        timantti = random.choice(nimet)
    print(pelaaja)

    koodi1 = pelaaja[2:]
    koodi2 = timantti[2:]
    matka = distance.distance(koodi1, koodi2).km
    print(f"Olet {pelaaja[0]} lentokentällä. Timantin välisen etäisyys on {matka:.0f} Km.")

    sql = "update game " \
          "set location = '" + pelaaja[0] + "'" \
            "where screen_name = '" + pelaajan_name + "'"

    kursori = yhteys.cursor()
    kursori.execute(sql)


    return

create_airport()