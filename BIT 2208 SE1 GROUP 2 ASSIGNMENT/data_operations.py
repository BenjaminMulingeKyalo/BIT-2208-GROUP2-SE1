from firebaseConfig import db
from typing import Optional, List, Dict

COLLECTION_NAME = 'items'
ORDERS_COLLECTION = 'orders'

def add_item(name: str, category: str, price: float, offer: Optional[str] = None) -> None:
    """
    Adds an item to the Firestore database.

    :param name: Name of the item
    :param category: Category of the item
    :param price: Price of the item
    :param offer: Offer details for the item, if any
    :raises ValueError: If name, category, or price are not provided or if price is not a number
    """
    if not all([name, category, price]):
        raise ValueError("Name, category, and price are required fields.")
    
    try:
        price = float(price)
    except ValueError:
        raise ValueError("Price must be a number.")

    doc_ref = db.collection(COLLECTION_NAME).document(name)
    doc_ref.set({
        'name': name,
        'category': category,
        'price': price,
        'offer': offer or 'No offer'
    })

def get_items() -> List[Dict[str, any]]:
    """
    Retrieves all items from the Firestore database.

    :return: List of items as dictionaries
    """
    items_ref = db.collection(COLLECTION_NAME)
    docs = items_ref.stream()
    return [doc.to_dict() for doc in docs]

def add_order(user_id: str, items: Dict[str, int], total_amount: float) -> None:
    """
    Adds an order to the Firestore database.

    :param user_id: ID of the user placing the order
    :param items: Dictionary with item names as keys and quantities as values
    :param total_amount: Total amount for the order
    """
    if not user_id or not items or not total_amount:
        raise ValueError("User ID, items, and total amount are required fields.")

    order_ref = db.collection(ORDERS_COLLECTION).document()
    order_ref.set({
        'user_id': user_id,
        'items': items,
        'total_amount': total_amount,
        'status': 'pending'  # Initial status of the order
    })

def main() -> None:
    """
    Main function to add items and retrieve the list of items.
    """
    try:
        add_item('Chocolate Bar', 'Snacks', 250.0, '10% off')
        add_item('Soda', 'Drinks', 70.0, None)
        add_item('Smocha', 'Snacks', 60.0, '5% off')
        add_item('BIC Biro Pen', 'Stationery', 50, None)
        add_item('Notebook', 'Stationery', 100.0, None)
        add_item('Water', 'Drinks', 80.0, None)
        add_item('Printing', 'Stationery', 2.00, None)
        add_item('Chapati', 'Snacks', 30.0, 'None')  
        add_item('Bread', 'Snacks', 70.0, 'None')
        add_item('Juice', 'Snacks', 85.0, 'None')
        add_item('Cake', 'Snacks', '100', 'None')
        add_item('Red Bull', 'Snacks', 250.0, 'None')
        
        items = get_items()
        for item in items:
            print(item)

        # Example usage of add_order function
        add_order('user123', {'Chocolate Bar': 2, 'Soda': 1}, 570.0)
    
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
