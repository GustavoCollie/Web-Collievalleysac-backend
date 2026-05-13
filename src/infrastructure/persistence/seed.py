"""
Seed script: creates default admin user and initial landing sections.

Run with: python -m infrastructure.persistence.seed
"""
import asyncio
import sys
from pathlib import Path
from uuid import uuid4

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy import select
from infrastructure.persistence.database import async_session_factory, engine, Base
from infrastructure.persistence.models.user_model import UserORM
from infrastructure.persistence.models.landing_model import LandingSectionORM
from infrastructure.persistence.models.product_model import ProductORM
from infrastructure.persistence.models.advisory_model import TechnicalArticleORM
from infrastructure.auth.jwt_auth_service import JwtAuthService


auth_service = JwtAuthService()

ADMIN_EMAIL = "admin@collievalley.com"
ADMIN_PASSWORD = "admin12345"
ADMIN_NAME = "Administrador Collie"

LANDING_SECTIONS = [
    {
        "section_key": "hero",
        "title": "Del campo peruano al mundo",
        "subtitle": "Palta Hass, mandarina, paprika y arándanos de la más alta calidad. Exportamos frescura, confianza y compromiso.",
        "content": {
            "cta_primary": "Comenzar ahora",
            "cta_secondary": "Ver productos",
            "background_image": "",
        },
        "display_order": 0,
    },
    {
        "section_key": "products",
        "title": "Nuestros Productos",
        "subtitle": "Productos agrícolas premium certificados para exportación",
        "content": {
            "items": [
                {"name": "Palta Hass", "desc": "Calibres premium, exportación todo el año", "image": ""},
                {"name": "Mandarina", "desc": "Dulce y jugosa, ideal para mercados europeos", "image": ""},
                {"name": "Paprika", "desc": "Seca y molida, alta concentración de color", "image": ""},
                {"name": "Arándanos", "desc": "Berries frescos de contraestación", "image": ""},
            ]
        },
        "display_order": 1,
    },
    {
        "section_key": "services",
        "title": "Servicios",
        "subtitle": "Soluciones integrales para el agronegocio internacional",
        "content": {
            "items": [
                {
                    "title": "Broker Internacional",
                    "desc": "Conectamos exportadores con compradores globales. Gestión de logística, documentación y certificaciones.",
                },
                {
                    "title": "Asesoría Agronómica",
                    "desc": "Expertos en campo que optimizan tu producción para cumplir estándares internacionales.",
                },
                {
                    "title": "Collie App",
                    "desc": "Sistema de gestión con IA para agroexportadores. Forecast, alertas y métricas en tiempo real.",
                },
            ]
        },
        "display_order": 2,
    },
    {
        "section_key": "testimonials",
        "title": "Lo que dicen nuestros clientes",
        "subtitle": "",
        "content": {
            "items": [
                {
                    "name": "Carlos M.",
                    "company": "FreshImports EU",
                    "quote": "La calidad de la palta Hass de Collie Valley es insuperable. Entregas puntuales y comunicación excelente.",
                },
                {
                    "name": "Ana R.",
                    "company": "Agrícola San Juan",
                    "quote": "Las asesorías agronómicas nos ayudaron a mejorar nuestro rendimiento en un 30%.",
                },
            ]
        },
        "display_order": 3,
    },
    {
        "section_key": "cta",
        "title": "¿Listo para exportar con nosotros?",
        "subtitle": "Regístrate y accede a nuestra plataforma de comercio internacional.",
        "content": {"button_text": "Crear cuenta gratis"},
        "display_order": 4,
    },
]


async def seed():
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        # Check if admin exists
        result = await session.execute(
            select(UserORM).where(UserORM.email == ADMIN_EMAIL)
        )
        admin = result.scalar_one_or_none()

        if not admin:
            admin = UserORM(
                id=uuid4(),
                email=ADMIN_EMAIL,
                hashed_password=auth_service.hash_password(ADMIN_PASSWORD),
                full_name=ADMIN_NAME,
                phone="+51999000000",
                role="admin",
                is_active=True,
            )
            session.add(admin)
            print(f"[SEED] Admin creado: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
        else:
            print(f"[SEED] Admin ya existe: {ADMIN_EMAIL}")

        # Seed landing sections
        for section_data in LANDING_SECTIONS:
            result = await session.execute(
                select(LandingSectionORM).where(
                    LandingSectionORM.section_key == section_data["section_key"]
                )
            )
            existing = result.scalar_one_or_none()

            if not existing:
                section = LandingSectionORM(
                    id=uuid4(),
                    section_key=section_data["section_key"],
                    title=section_data["title"],
                    subtitle=section_data["subtitle"],
                    content=section_data["content"],
                    display_order=section_data["display_order"],
                    is_visible=True,
                )
                session.add(section)
                print(f"[SEED] Sección creada: {section_data['section_key']}")
            else:
                print(f"[SEED] Sección ya existe: {section_data['section_key']}")

        # Seed products
        PRODUCTS = [
            {
                "name": "Palta Hass",
                "slug": "palta-hass",
                "description": "Palta Hass peruana de calibres premium. Exportación todo el año desde las principales zonas productoras.",
                "category": "fruta",
                "price_per_kg": 2.85,
                "season_start": 3,
                "season_end": 9,
            },
            {
                "name": "Mandarina W. Murcott",
                "slug": "mandarina-murcott",
                "description": "Mandarina dulce y jugosa, ideal para mercados europeos y norteamericanos.",
                "category": "fruta",
                "price_per_kg": 1.20,
                "season_start": 4,
                "season_end": 9,
            },
            {
                "name": "Paprika Seca",
                "slug": "paprika-seca",
                "description": "Paprika seca y molida con alta concentración de color ASTA 120+.",
                "category": "hortaliza",
                "price_per_kg": 4.50,
                "season_start": 1,
                "season_end": 12,
            },
            {
                "name": "Arándanos Frescos",
                "slug": "arandanos-frescos",
                "description": "Berries frescos de contraestación. Calibre 12-18mm, empaque clamshell.",
                "category": "berry",
                "price_per_kg": 8.90,
                "season_start": 8,
                "season_end": 12,
            },
            {
                "name": "Uva Red Globe",
                "slug": "uva-red-globe",
                "description": "Uva de mesa variedad Red Globe, calibre XL, ideal para mercados asiáticos.",
                "category": "fruta",
                "price_per_kg": 2.10,
                "season_start": 11,
                "season_end": 3,
            },
            {
                "name": "Espárrago Verde",
                "slug": "esparrago-verde",
                "description": "Espárrago verde fresco, calibre Standard y Large. Producción continua.",
                "category": "hortaliza",
                "price_per_kg": 3.75,
                "season_start": 1,
                "season_end": 12,
            },
        ]

        for prod_data in PRODUCTS:
            result = await session.execute(
                select(ProductORM).where(ProductORM.slug == prod_data["slug"])
            )
            existing = result.scalar_one_or_none()
            if not existing:
                product = ProductORM(
                    id=uuid4(),
                    name=prod_data["name"],
                    slug=prod_data["slug"],
                    description=prod_data["description"],
                    category=prod_data["category"],
                    price_per_kg=prod_data["price_per_kg"],
                    season_start=prod_data["season_start"],
                    season_end=prod_data["season_end"],
                    is_available=True,
                )
                session.add(product)
                print(f"[SEED] Producto creado: {prod_data['name']}")
            else:
                print(f"[SEED] Producto ya existe: {prod_data['name']}")

        # Seed technical articles
        from datetime import datetime
        ARTICLES = [
            {
                "title": "Manejo integrado de plagas en palta Hass",
                "slug": "mip-palta-hass",
                "content": "El Manejo Integrado de Plagas (MIP) en palta Hass combina métodos culturales, biológicos y químicos para mantener las poblaciones de plagas por debajo del umbral económico de daño.\n\nPrincipales plagas:\n- Trips del palto (Heliothrips haemorrhoidalis)\n- Arañita roja (Oligonychus punicae)\n- Queresas (Fiorinia fioriniae)\n\nEstrategias recomendadas:\n1. Monitoreo semanal con trampas cromáticas amarillas\n2. Liberación de controladores biológicos (Chrysoperla carnea)\n3. Aplicación de productos biológicos antes que químicos\n4. Rotación de ingredientes activos para evitar resistencia\n\nEl monitoreo constante es la base de un MIP exitoso. Registre sus observaciones para identificar tendencias estacionales.",
                "crop_tags": ["palta", "palta hass"],
                "author": "Ing. María López",
            },
            {
                "title": "Fertilización foliar en cítricos: guía práctica",
                "slug": "fertilizacion-foliar-citricos",
                "content": "La fertilización foliar complementa la nutrición radicular y corrige deficiencias de micronutrientes rápidamente.\n\nMomentos clave:\n- Pre-floración: aplicar Boro (150 ppm) + Zinc (200 ppm)\n- Cuajado de frutos: Calcio (400 ppm) para firmeza\n- Desarrollo de fruto: Potasio (500 ppm) para calibre y dulzura\n\nRecomendaciones generales:\n- Aplicar temprano en la mañana o al atardecer\n- Usar coadyuvantes para mejorar la absorción\n- No mezclar Calcio con Fósforo en el mismo tanque\n- pH de la solución entre 5.5 y 6.5\n\nUn programa de fertilización foliar bien diseñado puede incrementar la producción en un 15-20%.",
                "crop_tags": ["mandarina", "cítricos"],
                "author": "Ing. Carlos Mendoza",
            },
            {
                "title": "Buenas prácticas de cosecha para arándanos de exportación",
                "slug": "cosecha-arandanos-exportacion",
                "content": "La calidad del arándano se define en gran parte durante la cosecha. Seguir estas prácticas asegura fruta de exportación premium.\n\nIndicadores de madurez:\n- Color azul uniforme con bloom (pruina) intacta\n- Calibre mínimo 12mm\n- Firmeza > 150g en penetrómetro\n\nProtocolo de cosecha:\n1. Cosechar en horas frescas (6-10 AM)\n2. Manipulación mínima — usar cosechadores capacitados\n3. No más de 3 capas de fruta por clamshell\n4. Pre-enfriamiento (forced air cooling) dentro de 2 horas\n5. Temperatura de transporte: 0-1°C\n\nRegistrar la trazabilidad por lote: fecha, sector, cosechador, hora de ingreso a packing.",
                "crop_tags": ["arándano", "berry"],
                "author": "Ing. Ana Rodríguez",
            },
            {
                "title": "Manejo del riego por goteo en espárrago",
                "slug": "riego-goteo-esparrago",
                "content": "El espárrago requiere un manejo hídrico preciso para maximizar el rendimiento de turiones.\n\nFases críticas:\n- Brotación (sep-oct): incrementar frecuencia, 4-6 mm/día\n- Cosecha: mantener humedad constante, 6-8 mm/día\n- Agoste (abr-may): reducir gradualmente hasta suspender\n- Descanso: riego mínimo de mantenimiento\n\nRecomendaciones técnicas:\n- Sensores de humedad a 30cm y 60cm de profundidad\n- Coeficiente de cultivo (Kc): 0.3 (brotación) a 1.0 (máximo follaje)\n- Fertirrigación: N-P-K según análisis foliar mensual\n\nEl exceso de agua durante el agoste reduce la calidad de la siguiente campaña.",
                "crop_tags": ["espárrago", "hortaliza"],
                "author": "Ing. Pedro Gutiérrez",
            },
            {
                "title": "Certificación GlobalGAP: checklist para pequeños agricultores",
                "slug": "certificacion-globalgap-checklist",
                "content": "GlobalGAP es requisito para exportar a la Unión Europea. Esta guía simplifica los puntos críticos.\n\nPuntos obligatorios principales:\n1. Trazabilidad: identificar cada lote desde siembra hasta despacho\n2. Manejo de fitosanitarios: registro de aplicaciones con productos autorizados\n3. Higiene del trabajador: baños, lavamanos, capacitación\n4. Manejo de residuos: plan de disposición documentado\n5. Gestión del agua: análisis microbiológico anual\n\nDocumentación mínima:\n- Mapa del predio con identificación de parcelas\n- Registros de siembra, aplicaciones y cosecha\n- Evaluación de riesgos del sitio\n- Plan de acción para no conformidades\n\nTip: iniciar la documentación al menos 6 meses antes de la auditoría.",
                "crop_tags": ["general", "certificación"],
                "author": "Ing. María López",
            },
        ]

        for art_data in ARTICLES:
            result = await session.execute(
                select(TechnicalArticleORM).where(TechnicalArticleORM.slug == art_data["slug"])
            )
            existing = result.scalar_one_or_none()
            if not existing:
                article = TechnicalArticleORM(
                    id=uuid4(),
                    title=art_data["title"],
                    slug=art_data["slug"],
                    content=art_data["content"],
                    crop_tags=art_data["crop_tags"],
                    author=art_data["author"],
                    published_at=datetime.utcnow(),
                )
                session.add(article)
                print(f"[SEED] Artículo creado: {art_data['title']}")
            else:
                print(f"[SEED] Artículo ya existe: {art_data['title']}")

        await session.commit()
        print("[SEED] Seed completado exitosamente.")


if __name__ == "__main__":
    asyncio.run(seed())
