from .cart import Cart


def carrito(request):
    """Expone el número de items del carrito en todas las plantillas (badge del navbar)."""
    return {"cart_items_count": len(Cart(request))}
