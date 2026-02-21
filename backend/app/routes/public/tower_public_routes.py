from app.routes.public import public_bp
from app.models.tower import Tower
from flask import jsonify, request
from sqlalchemy import func
# @public_bp.route("/towers", methods=["GET"])
# def list_public_towers():

#     towers = Tower.query.all()

#     return jsonify([
#         {
#             "name":t.name,
#             "code":t.code,
#             "locality":t.locality
#         }
#         for t in towers
#     ])



# @public_bp.route("/towers", methods=["GET"])
# def list_public_towers():

#     locality = request.args.get("locality")

#     query = Tower.query

#     # If locality filter applied
#     if locality:
#         query = query.filter(Tower.locality == locality)

#     towers = query.all()

#     return jsonify([
#         {
#             "name": t.name,
#             "code": t.code,
#             "locality": t.locality
#         }
#         for t in towers
#     ])
from flask import request
from sqlalchemy import func

@public_bp.route("/towers", methods=["GET"])
def list_public_towers():

    locality = request.args.get("locality")

    query = Tower.query

    if locality:
        query = query.filter(
            func.lower(Tower.locality) == locality.lower()
        )

    towers = query.all()

    return jsonify([
        {
            "name": t.name,
            "code": t.code,
            "locality": t.locality
        }
        for t in towers
    ])