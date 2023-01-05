from src.domain.article import Article
from src.domain.article_dao import ArticleDao
from src.core.resources_mgr import ResourcesMgr
from src.domain.signup import lambda_handler
from src.domain.confirm_signup import confirm_signup_function
from src.domain.signin import signin_function

import logging
import json

logger = logging.getLogger()
print("create dynamodb resources")
resources_mgr = ResourcesMgr()


def create_article(event, context):
    print(event)

    body = json.loads(event["body"])

    article = Article(author_id=None, title=body["title"], tags=body["tags"], content=body["content"])

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


def find_articles(event, context):
    print(event)
    
    dao = ArticleDao(
        dynamodb_resource=resources_mgr.dynamodb_resource,
        dynamodb_client=resources_mgr.dynamodb_client,
        table_name=resources_mgr.table_name(),
    )
    
    query_params = event.get("queryStringParameters")
    
    if query_params and "tag" in query_params:
        articles = dao.find_by_tag(query_params.get("tag"))
    else:
        articles = dao.find_by_tag(None)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(articles),
    }

def signup(event, context):
    return lambda_handler(json.loads(event["body"]))

def confirm_signup(event, context):
    return confirm_signup_function(json.loads(event["body"]))

def signin(event, context):
    return signin_function(json.loads(event["body"]))