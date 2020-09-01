import urllib
import asyncio
import src.copart as copart

from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, request

# from src.spider import Spider

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    return make_response("OK", 200)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.route("/car/member/lot/<string:lot_number>", methods=["GET"])
def member(lot_number):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    car_info = loop.run_until_complete(copart.get_lot_details(lot_number, True))
    if car_info == 404:
        return make_response(
            jsonify({"error": "Result not found. Check your query"}), 404
        )
    else:
        return jsonify({"success": True, "result": car_info})


@app.route("/car/lot/<string:lot_number>", methods=["GET"])
def car_info(lot_number):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    car_info = loop.run_until_complete(copart.get_lot_details(lot_number))
    if car_info == 404:
        return make_response(
            jsonify({"error": "Result not found. Check your query"}), 404
        )
    else:
        return jsonify({"success": True, "result": car_info})


@app.route("/car/query", methods=["GET"])
def search_car():
    args = request.args

    make = ""
    if "make" in args:
        make = urllib.parse.quote(args.get("make"))
        make_query = f"%22MAKE%22:%5B%22lot_make_desc:%5C%22{make.upper()}%5C%22%22%5D"
    else:
        make_query = ""

    model = ""
    if "model" in args:
        model = urllib.parse.quote(args.get("model"))
        model_query = (
            f"%22MODL%22:%5B%22lot_model_desc:%5C%22{model.upper()}%5C%22%22%5D"
        )
    else:
        model_query = ""

    years = []
    if "year" in args:
        years = request.args.getlist("year")
        if len(years) == 1:
            years_query = f"%22YEAR%22:%5B%22lot_year:%5C%22{years[0]}%5C%22%22%5D"
        elif len(years) > 1:
            years_list = []
            for y in years:
                year = f"%22lot_year:%5C%22{y}%5C%22%22"
                years_list.append(year)
            years_query = "%22YEAR%22:%5B" + ",".join(years_list) + "%5D"
        else:
            years_query = ""
    else:
        years_query = ""

    referer_url = (
        "https://www.copart.com/lotSearchResults/?searchCriteria=%7B%22query%22:%5B%22*%22%5D,"
        "%22filter%22:%7B"
        + ",".join(filter(lambda x: x != "", [make_query, model_query, years_query]))
        + "%7D,%22sort%22:%5B%22auction_date_type%20desc%22,"
        "%22auction_date_utc%20asc%22%5D,"
        "%22watchListOnly%22:false,"
        "%22searchName%22:%22%22,"
        "%22freeFormSearch%22:false%7D"
    )

    all_page_query = True if "all" in args else False

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    car_list = loop.run_until_complete(copart.get_car_list(referer_url, all_page_query))

    if car_list == 404:
        return make_response(
            jsonify({"error": "Result not found. Check your query"}), 404
        )
    else:
        return jsonify(
            {"success": True, "resultCount": len(car_list), "result": car_list}
        )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
    # app.run(debug=True, host="0.0.0.0")
