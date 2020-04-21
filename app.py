# Import sql dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import flask api 
from flask import Flask, jsonify


# Set up the database
engine = create_engine("sqlite:///10-Advanced-Data-Storage-and-Retrieval_homework_assignment_Resources_hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Set up flask
app = Flask(__name__)

# Home Route 
@app.route("/")
def home():
    print('List all the routes')
    return (
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs<br/>"
        f"for ranges you can put just a start date till the end of our data,or you can give a specfic range <br/>"
        f"Example of /api/v1.0/start = /api/v1.0/2016-08-07 <br/>"
        f"/api/v1.0/start<br/>"
        f"Example of /api/v1.0/start/end = /api/v1.0/2016-08-07/2017-01-01 <br/> "
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    
    print('Print all the percipitation data')
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query 
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Close session
    session.close()

    # Create dictionary 
    prcp_list = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def station():
    print('List of all stations')

     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query 
    results = session.query(Station.station).all()

    # Close session
    session.close()

    # Create list
    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    print('List all Tempereatures for most active station of last year')

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to find the station with the most measurments and then we query by that station id 
    # then we query to get tehe date and temperature for the last year of information
    result = engine.execute("SELECT COUNT(station) AS c,station FROM measurement GROUP BY station ORDER BY c DESC LIMIT 1 ")
    for row in result:
        tobs_data = (session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == row[1]).order_by(Measurement.id.desc()).limit(365).all())
    
    # Create list of the query 
    tobs_list = []
    tobs_list = list(np.ravel(tobs_data))

    # Close session
    session.close()

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start(start):
    print('print all the data for the start date to our last data entry')

     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to get max, avg, min 
    summary_tobs = session.query(func.max(Measurement.tobs), func.avg(Measurement.tobs), func.min(Measurement.tobs)).filter(Measurement.date >= start).all()
    summary_tobs_list = []
    summary_tobs_list = list(np.ravel(summary_tobs))

    # Close session
    session.close()

    return jsonify(summary_tobs_list)

@app.route("/api/v1.0/<start>/<end>")
def date_range(start, end):
    print('get the range of temperature from start date to end date')

    # Create our session (link) from python to the DB
    session = Session(engine)

    #Query 
    inclusive_summ = session.query(func.max(Measurement.tobs), func.avg(Measurement.tobs), func.min(Measurement.tobs)).filter(Measurement.date.between(start,end)).all()
    inclusive_summ_list = []
    inclusive_summ_list = list(np.ravel(inclusive_summ))

    session.close()

    return jsonify(inclusive_summ_list)


if __name__ == '__main__':
    app.run(debug=True)

