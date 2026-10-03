from decimal import Decimal, InvalidOperation

from .models import Consolas, Accsesorios, Juegos

# Tipos de producto que se pueden agregar al carrito
MODELOS = {
    "consola": Consolas,
    "accesorio": Accsesorios,
    "juego": Juegos,
}

URL_CATEGORIA = {"consola": "consolas", "accesorio": "accesorios", "juego": "juegos"}

MAX_POR_PRODUCTO = 10


def a_decimal(valor):
    """Convierte precios como 540, '540.00$' o '$ 449,50' a Decimal."""
    texto = str(valor).replace("$", "").replace(",", ".").strip()
    try:
        return Decimal(texto)
    except (InvalidOperation, ValueError):
        return Decimal("0")


class Cart:
    """Carrito guardado en la sesión. Clave: '<tipo>-<id>' (ej. 'consola-3').

    En la sesión solo se guarda tipo, id y cantidad. Precio y descuento se leen
    siempre de la base de datos, así el cliente paga el precio vigente.
    """

    SESSION_KEY = "cart"

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(self.SESSION_KEY, {})

    @staticmethod
    def _key(tipo, product_id):
        return f"{tipo}-{product_id}"

    def add(self, tipo, product, cantidad=1):
        key = self._key(tipo, product.id)
        item = self.cart.setdefault(key, {"tipo": tipo, "id": product.id, "cantidad": 0})
        item["cantidad"] = min(item["cantidad"] + cantidad, MAX_POR_PRODUCTO)
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

    def items(self):
        """Lista de items con datos actuales de la BD. Quita productos que ya no existen."""
        resultado, borrar = [], []
        for key, item in self.cart.items():
            modelo = MODELOS.get(item.get("tipo"))
            producto = modelo.objects.filter(id=item.get("id")).first() if modelo else None
            if producto is None:
                borrar.append(key)
                continue
            cantidad = item["cantidad"]
            resultado.append({
                "tipo": item["tipo"],
                "id": producto.id,
                "nombre": str(producto),
                "precio_base": producto.precio,
                "descuento": producto.descuento,
                "precio": producto.precio_final,
                "cantidad": cantidad,
                "subtotal_base": producto.precio * cantidad,
                "total": producto.precio_final * cantidad,
                "url_categoria": URL_CATEGORIA.get(item["tipo"], "home"),
            })
        for key in borrar:
            del self.cart[key]
        if borrar:
            self.save()
        return resultado

    def __iter__(self):
        return iter(self.items())

    def __len__(self):
        return sum(item["cantidad"] for item in self.cart.values())

    def resumen(self):
        """Montos del carrito: base, ahorro, total y % de descuento global."""
        items = self.items()
        base = sum((i["subtotal_base"] for i in items), Decimal("0"))
        total = sum((i["total"] for i in items), Decimal("0"))
        ahorro = base - total
        pct = round(ahorro * 100 / base) if base else 0
        return {"items": items, "base": base, "ahorro": ahorro, "total": total, "porcentaje": pct}

    def get_total_price(self):
        return self.resumen()["total"]
