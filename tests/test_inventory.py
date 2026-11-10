import pytest
import inventory 

@pytest.fixture(autouse=True)
def setup_test_data():
    inventory.inventory = [
        {"id": 1, 
         "type": "ПК", 
         "name": "Test", 
         "room": "101", 
         "status": "исправно"}
    ]

def test_add_item_success():
    result, text = inventory.add_item({"id":2, "type":"Монитор", "name":"Samsung 24", "room":"102", "status":"исправно"})
    
    assert result is True
    
    items = inventory.get()
    assert len(items) == 2
    assert items[1]["id"] == 2

def test_add_item_duplicate_id():
    result, text = inventory.add_item({"id":1, "type":"Принтер", "name":"HP", "room":"103", "status":"исправно"})
    
    assert result is False 
    
    assert len(inventory.get()) == 1

def test_add_item_empty_fields():
    result, text = inventory.add_item({"id":3, "type":"", "name":"Без имени", "room":"101", "status":"исправно"})
    
    assert result is False
