import uuid
from flask import request
from flask.views import MethodView
from schemas import ItemSchema, ItemUpdateSchema
from flask_smorest import Blueprint, abort
from db import items, stores


blp = Blueprint("items", __name__, description = "operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message = "item not found")


    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "item deleted."}
        except KeyError:
            abort(404, message="item not found.")
    

    @blp.arguments(ItemUpdateSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data

            return item
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    @blp.arguments(ItemSchema)
    def post(self, item_data):
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message=f"Item already exists.")

        
        if item_data["store_id"] not in stores:
            abort(404, message = "Store not found")
        
        item_id = uuid.uuid4().hex
        new_item = {**item_data, "id": item_id}
        items[item_id], = new_item
        
        return new_item, 201