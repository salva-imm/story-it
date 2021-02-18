from tortoise import Tortoise, run_async

db_arguments = dict(
    db_url='sqlite://db.sqlite3',
    modules={'models': [
        'user.models',
        'story.models',
        'comment.models',
    ]}
)


async def init(generate_schema=False):
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(**db_arguments)
    # Generate the schema
    if generate_schema:
        await Tortoise.generate_schemas()

if __name__ == "__main__":
    run_async(init(True))
