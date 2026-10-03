from django.contrib import admin

from .models import Consolas, Accsesorios, Juegos, Avatar, Pedido, PedidoItem


@admin.register(Consolas, Accsesorios, Juegos)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "empresa", "precio", "descuento", "precio_final")
    list_editable = ("precio", "descuento")
    search_fields = ("nombre", "empresa")


admin.site.register(Avatar)


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0
    readonly_fields = ("tipo", "producto_id", "nombre", "precio_base", "descuento", "precio_final", "cantidad")
    can_delete = False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """El staff cambia el estado aquí y el cliente lo ve en su historial."""
    list_display = ("numero", "user", "creado", "total", "estado")
    list_editable = ("estado",)
    list_filter = ("estado", "creado")
    search_fields = ("id", "user__username", "numero_documento")
    inlines = [PedidoItemInline]
    readonly_fields = ("user", "creado", "actualizado", "subtotal", "descuento", "total",
                       "marca_tarjeta", "ultimos4", "vencimiento")
