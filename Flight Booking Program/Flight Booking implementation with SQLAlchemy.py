import csv
from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import text


engine = create_engine(config('DATABASE_URL'))

db = scoped_session(sessionmaker(bind=engine))


def datainsertion():
    flightsfilepath = config('CSV_FILE_PATH')
    f = open(flightsfilepath)
    reader = csv.reader(f)
    for origin, destination, duration in reader:
        sql_query = text("INSERT INTO flightrecords (origin, destination, duration) VALUES (:origin, :destination, :duration)")
        db.execute(sql_query, {"origin": origin, "destination": destination, "duration": duration})
        print(f"Added flight from {origin} to {destination} lasting {duration} minutes.")
    db.commit()


def allflights():
    sql_query = text("SELECT id, origin, destination, duration FROM flightrecords")
    flights = db.execute(sql_query).fetchall()
    for flight in flights:
        print(f"flight {flight.id}: {flight.origin} to {flight.destination}, {flight.duration} minutes.")

    flight_id = int(input("\nFlight ID: "))
    name = input("Your Name: ")
    country = input("Your Country: ")

    # Save user details to CSV file
    passengersfilepath = config('CSV2_FILE_PATH')
    with open(passengersfilepath, "a", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([name, country, flight_id])

    print("Details saved sucessfully")

    # Retrieve flight information based on flight_id
    sql_query = text("SELECT origin, destination, duration FROM flightrecords WHERE id = :id")
    flight = db.execute(sql_query, {"id": flight_id}).fetchone()
    

    if flight is None:
        print("Error: No such flight.")
        return
    
    print(f"You have booked a flight from {flight.origin} to {flight.destination}, the trip will last {flight.duration} minutes.")

    # Insert passenger details into the database
    sql_query = text("INSERT INTO passengers (name, country, flight_id) VALUES (:name, :country, :flight_id)")

    # Execute the SQL query with parameters
    db.execute(sql_query, {"name": name, "country": country, "flight_id": flight_id})
    db.commit()


if __name__ == "__main__":
    datainsertion()
    allflights()



