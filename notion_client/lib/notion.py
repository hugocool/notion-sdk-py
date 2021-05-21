import os
from typing import Dict, List

from notion_client.client import Client
from notion_client.api_endpoints import (
    BlocksChildrenEndpoint,
    BlocksEndpoint,
    DatabasesEndpoint,
    PagesEndpoint,
    SearchEndpoint,
    UsersEndpoint
)
from .api_objects import APIObject, User, Page, Block
from .database import Database

if not os.environ.get("NOTION_KEY"):
    raise EnvironmentError("Please specify your notion key as an environment variable `NOTION_KEY`.")

else:
    _client = Client(os.environ["NOTION_KEY"])
    _block_children = BlocksChildrenEndpoint(_client)
    _block = BlocksEndpoint(_client)
    _database = DatabasesEndpoint(_client)
    _page = PagesEndpoint(_client)
    _search = SearchEndpoint(_client)
    _user = UsersEndpoint


# TODO: convert all Class objects passed into api into standard Dict format.
class Notion(object):


    def get_object_from_response(self, o: Dict[str, object]) -> APIObject:
        return {
            "database": Database.from_json,
            "user": User.from_json,
            "page": Page.from_json,
            "block": Block.from_json
        }[o["object"]](o)


    @staticmethod
    def retrieve_database(database_id: str, **kwargs) -> Database:
        return Database.from_json(
            _database.retrieve(database_id, **kwargs).json()
        )

    @staticmethod
    def query_database(database_id: str, **kwargs) -> List[Page]:
        return [
            Page.from_json(p.json()) for p in _database.query(database_id, **kwargs)
        ]

    @staticmethod
    def list_databases(**kwargs) -> List[Database]:
        return [
            Database.from_json(d) for d in _database.list(**kwargs)
        ]

    @staticmethod
    def retrieve_page(page_id: str, **kwargs) -> Page:
        return Page.from_json(_page.retrieve(page_id).json())

    @staticmethod
    def create_page(page: Page, children: List[Block]) -> Page:
        return Page.from_json(_page.create(
            parent=page.parent,
            properties=page.properties,
            children=children
        ).json())

    @staticmethod
    def retrieve_block_children(block_id: str) -> List[Block]:
        return Block.from_json(
            Block.from_json(b) for b in _block_children.list(block_id)
        )

    @staticmethod
    def append_block_children(block_id: str, children: List[Block]) -> Block:
        return Block.from_json(
            _block_children.append(
                block_id,
                children=children
            )
        )

    @staticmethod
    def update_page(page_id: str, properties: Dict[str, "PropertyValue"]) -> Page:
        return Page.from_json(
            _page.update(
                page_id,
                properties=properties
            )
        )

    @staticmethod
    def retrieve_user(user_id: str) -> User:
        return User.from_json(
            _user.retrieve(
                user_id
            ).json()
        )

    @staticmethod
    def list_users():
        return [
            User.from_json(u) for u in _user.list().json()
        ]

    @staticmethod
    def search(**kwargs) -> List[APIObject]:
        return [
            Notion.get_object_from_response(o) for o in _search.__call__(**kwargs)
        ]