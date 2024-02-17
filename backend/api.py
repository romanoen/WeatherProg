from flask import Flask, jsonify
import runner

app = Flask(__name__)

@app.route("/get-data/<startdate>/<enddate>/<int:periods>/<latitude>/<longitude>/<hourlyParameters>/<dailyParameters>/<dataSelector>")
def get_data(startdate, enddate, periods, latitude, longitude, hourlyParameters, dailyParameters, dataSelector):

    hourlyParameters_list = hourlyParameters.split(',')
    dailyParameters_list = dailyParameters.split(',')

    try:
        ru = runner.Runner(startdate, enddate, int(periods), latitude, longitude, hourlyParameters_list, dailyParameters_list, int(dataSelector))
        df = ru.run()
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)