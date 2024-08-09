from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Sample static data
data = [
    {"id": 1, "name": "Item 1", "description": "This is item 1"},
    {"id": 2, "name": "Item 2", "description": "This is item 2"},
    {"id": 3, "name": "Item 3", "description": "This is item 3"},
]

# Pydantic model for the data structure
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: str

# Read all items
@app.get("/items", response_model=List[Item])
def read_items():
    return data

# Read single item by ID
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    item = next((item for item in data if item["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Create a new item
@app.post("/items", response_model=Item)
def create_item(item: Item):
    item.id = max([i["id"] for i in data]) + 1 if data else 1
    data.append(item.dict())
    return item

# Update an existing item by ID
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    item = next((item for item in data if item["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item.update(updated_item.dict(exclude_unset=True))
    return item

# Delete an item by ID
@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int):
    global data
    data = [item for item in data if item["id"] != item_id]
    return {"message": "Item deleted successfully"}
