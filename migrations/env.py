"""Alembic integration for the Flask-SQLAlchemy application."""

import logging
from logging.config import fileConfig

from alembic import context
from flask import current_app

config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")
extension = current_app.extensions["migrate"]
target_metadata = extension.db.metadata


def process_revision_directives(_context, _revision, directives):
    if getattr(config.cmd_opts, "autogenerate", False):
        if directives[0].upgrade_ops.is_empty():
            directives[:] = []
            logger.info("No changes in schema detected.")


def run_migrations_offline():
    context.configure(
        url=extension.db.engine.url,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    options = dict(extension.configure_args)
    if options.get("process_revision_directives") is None:
        options["process_revision_directives"] = process_revision_directives
    with extension.db.engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            **options,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
