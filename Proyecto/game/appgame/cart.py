from decimal import Decimal, InvalidOperation

from .models import Consolas, Accsesorios, Juegos

# Tipos de producto que se pueden agregar al carrito
MODELOS = {
    "consola": Consolas,
    "accesorio": Accsesorios,
    "juego": Juegos,
}

URL_CATEGORIA = {"consola": "consolas", "accesorio": "accesorios", "juego": "juegos"}


def a_decimal(valor):
    """Convierte precios como 540, '540.00$' o '$ 449,50' a Decimal."""
    texto = str(valor).replace("$", "").replace(",", ".").strip()
    try:
        return Decimal(texto)
    except (InvalidOperation, ValueError):
        return Decimal("0")


class Cart:
    """Carrito guardado en la sesión. Clave: '<tipo>-<id>' (ej. 'consola-3')."""

    SESSION_KEY = "cart"

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(self.SESSION_KEY, {})

    @staticmethod
    def _key(tipo, product_id):
        return f"{tipo}-{product_id}"

    def add(self, tipo, product, cantidad=1):
        key = self._key(tipo, product.id)
        if key not in self.cart:
            self.cart[key] = {
                "tipo": tipo,
                "id": product.id,
                "nombre": str(product),
                "precio": str(a_decimal(product.precio)),  # JSON-serializable
                "cantidad": 0,
            }
        self.cart[key]["cantidad"] += cantidad
        self.save()

    def decrease(self, tipo, product_id):
        key = self._key(tipo, product_id)
        if key in self.cart:
            self.cart[key]["cantidad"] -= 1
            if self.cart[key]["cantidad"] <= 0:
                del self.cart[key]
            self.save()

    def remove(self, tipo, product_id):
        if self.cart.pop(self._key(tipo, product_id), None) is not None:
            self.save()

    def clear(self):
        self.session[self.SESSION_KEY] = {}
        self.cart = self.session[self.SESSION_KEY]
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        # Copias: nunca se mete un objeto no serializable en la sesión
        for item in self.cart.values():
            precio = Decimal(item["precio"])
            yield {
                **item,
                "precio": precio,
                "total": precio * item["cantidad"],
                "url_categoria": URL_CATEGORIA.get(item["tipo"], "home"),
            }

    def __len__(self):
        return sum(item["cantidad"] for item in self.cart.values())

    def get_total_price(self):
        return sum((Decimal(i["precio"]) * i["cantidad"] for i in self.cart.values()), Decimal("0"))
