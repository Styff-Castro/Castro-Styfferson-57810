from django.db import migrations, models

TABLAS = ["appgame_consolas", "appgame_accsesorios", "appgame_juegos"]


def limpiar_precios(apps, schema_editor):
    """Convierte textos como '540.00$' o '$ 1.234,50' en números antes de cambiar el tipo."""
    from decimal import Decimal, InvalidOperation

    with schema_editor.connection.cursor() as cur:
        for tabla in TABLAS:
            cur.execute(f"SELECT id, precio FROM {tabla}")
            for pk, valor in cur.fetchall():
                texto = str(valor if valor is not None else "0").replace("$", "").replace(" ", "")
                if "," in texto:  # formato 1.234,50 -> 1234.50
                    texto = texto.replace(".", "").replace(",", ".")
                try:
                    limpio = Decimal(texto)
                except (InvalidOperation, ValueError):
                    limpio = Decimal("0")
                cur.execute(f"UPDATE {tabla} SET precio = %s WHERE id = %s", [str(limpio), pk])


class Migration(migrations.Migration):

    dependencies = [
        ("appgame", "0002_alter_accsesorios_options_alter_consolas_options_and_more"),
    ]

    operations = [
        migrations.RunPython(limpiar_precios, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="consolas",
            name="precio",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="accsesorios",
            name="precio",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="juegos",
            name="precio",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
