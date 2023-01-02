from src.domain.article import Article
from src.domain.article_dao import ArticleDao
from src.core.resources_mgr import ResourcesMgr

import logging
import json

logger = logging.getLogger()
print("create dynamodb resources")
resources_mgr = ResourcesMgr()


def create_article(event, context):
    print(event)

    body = json.loads(event["body"])

    article = Article(author_id="author_id", title=body["title"], tags=body["tags"], content=body["content"])

    dao = ArticleDao(
        dynamodb_resource=resources_mgr.dynamodb_resource,
        dynamodb_client=resources_mgr.dynamodb_client,
        table_name=resources_mgr.table_name(),
    )

    dao.create(article)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": article.to_json(),
    }


def delete_article(event, context):
    print(event)

    dao = ArticleDao(
        dynamodb_resource=resources_mgr.dynamodb_resource,
        dynamodb_client=resources_mgr.dynamodb_client,
        table_name=resources_mgr.table_name(),
    )

    article_id = event["pathParameters"]["article_id"]
    dao.delete(uuid=article_id)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": "",
    }


def get_by_uuid(event, context):
    print(event)

    dao = ArticleDao(
        dynamodb_resource=resources_mgr.dynamodb_resource,
        dynamodb_client=resources_mgr.dynamodb_client,
        table_name=resources_mgr.table_name(),
    )
    
    article_id = event["queryStringParameters"]["article_id"]
    entities = dao.get_by_uuid(article_id)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(entities, default=lambda entity: entity.to_json()),
    }