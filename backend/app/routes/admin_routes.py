# from flask import Blueprint, jsonify, request
# # from flask_jwt_extended import jwt_required
# from app.services.admin_service import get_dashboard_stats
# from app.services.tower_service import (create_tower,
#                                          get_all_towers,
#                                         #    get_tower_by_code,
#                                              update_tower,
#                                                delete_tower,
#                                                get_tower_by_code_service)
                                        
                                        
# from app.utils.decorators import admin_required
# admin_bp = Blueprint("admin", __name__)




# @admin_bp.route("/dashboard",methods=["GET"])
# @admin_required
# def dashboard():
#     return jsonify({"message": "Welcome Admin"})


# @admin_bp.route("/towers", methods=["POST"])
# @admin_required
# def add_tower():
#     try:
#         data = request.get_json()
#         tower = create_tower(data)
#         return jsonify({"message": "Tower created",
#                          "tower": {"id": tower.id, "name": tower.name,"code":tower.code,"locality":tower.locality}}), 201

#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
    


# @admin_bp.route("/towers", methods=["GET"])
# @admin_required
# def list_towers():
#     towers = get_all_towers()

#     return jsonify([
#         {
#             "id":t.id,
#             "name":t.name,
#             "code":t.code,
#             "locality":t.locality
#         }
#         for t in towers
#     ])


# # @admin_bp.route("/towers/<string:code>", methods=["GET"])
# # @admin_required
# # def get_tower(code):
# #     tower = get_tower_by_code(code)

# #     if not tower:
# #         return jsonify({"error": "Tower not found"}), 404

# #     return jsonify({
# #         "id":tower.id,
# #         "name":tower.name,
# #         "code":tower.code,
# #         "locality":tower.locality
# #     })


# @admin_bp.route("/towers/<string:code>", methods=["GET"])
# @admin_required
# def get_tower_by_code(code):
#     print(f"Received request for tower with code: {code}")
#     # return jsonify({"code":code})
#     tower = get_tower_by_code_service(code)

#     if not tower:
#         return jsonify({"error": "Tower not found"}), 404

#     return jsonify({
#         "id": tower.id,
#         "name": tower.name,
#         "code": tower.code,
#         "locality": tower.locality
#     })



# @admin_bp.route("/towers/<string:code>", methods=["PUT"])
# @admin_required
# def edit_tower(code):
#     try:
#         data=request.get_json()
#         tower = update_tower(code,data)

#         return jsonify({"message":"tower updated",
#                         "id":tower.id,
#                         "name":tower.name,
#                         "code":tower.code,
#                         "locality":tower.locality})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
    

# @admin_bp.route("/towers/<string:code>", methods=["DELETE"])
# @admin_required
# def remove_tower(code):
#     try:
#         delete_tower(code)
#         return jsonify({"message": "Tower deleted"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400