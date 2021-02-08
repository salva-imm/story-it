from tortoise import Tortoise, run_async
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': [
            'user.models',
            'story.models',
            'comment.models',
        ]}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


run_async(init())
