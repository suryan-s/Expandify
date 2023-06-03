import pynecone as pc


class ExpandifyConfig(pc.Config):
    pass


config = ExpandifyConfig(
    app_name="Expandify",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)
