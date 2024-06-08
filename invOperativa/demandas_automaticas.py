from datetime import date
from stock.models import *
import os
import django

# Configurar el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invOperativa.settings')
django.setup()

# Lógica para crear demandas al inicio del año con demanda real inicializada en 0
def crear_demandas_anuales():
    current_year = date.today().year

    # Obtener todos los artículos
    articulos = Articulo.objects.all()

    for year in range(current_year - 3, current_year + 1):
        for month in range(1, 13):
            for articulo in articulos:
                if not Demanda.objects.filter(mesDemanda=month, anioDemanda=year, articulo=articulo).exists():
                    nueva_demanda = Demanda.objects.create(
                        mesDemanda=month,
                        anioDemanda=year,
                        demandaReal=0,
                        articulo=articulo
                    )
                    nueva_demanda.save()

if __name__ == "__main__":
    crear_demandas_anuales()
