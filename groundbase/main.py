import os

import fastapi
import fastapi.middleware.cors

from groundbase import check_dependencies, initialize_database, initialize_dependency_injection
from groundbase.routers import root

# to be removed in a proper scenario
os.environ["DB_CONNECTION_STRING"] = "sqlite+aiosqlite:///db.sqlite"
os.environ["DB_SQL_LOGGING"] = "True"

check_dependencies()
initialize_database()
initialize_dependency_injection()

# here add middlewares
middlewares = {
    fastapi.middleware.cors.CORSMiddleware: {
        "allow_origins": ["*"],
        "allow_methods": ["*"],
        "allow_headers": ["*"],
        "allow_credentials": True,
    },
}

# here add routers
routers = [
    root.router,
]

app = fastapi.FastAPI()

for middleware_class, options in middlewares.items():
    app.add_middleware(middleware_class, **options)

for router in routers:
    app.include_router(router)
