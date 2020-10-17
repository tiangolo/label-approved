import logging
from typing import Dict, Optional

from github import Github
from github.PullRequestReview import PullRequestReview
from pydantic import BaseSettings, SecretStr
from pydantic.main import BaseModel


class LabelSettings(BaseModel):
    await_label: Optional[str] = None
    number: int


class Settings(BaseSettings):
    github_repository: str
    input_token: SecretStr
    input_debug: Optional[bool] = False
    input_config: Dict[str, LabelSettings] = {
        "approved-2": LabelSettings(await_label="awaiting review", number=2)
    }


settings = Settings()
if settings.input_debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
logging.debug(f"Using config: {settings.json()}")
g = Github(settings.input_token.get_secret_value())
repo = g.get_repo(settings.github_repository)
for pr in repo.get_pulls(state="open"):
    logging.info(f"Checking PR: #{pr.number}")
    pr_labels = list(pr.get_labels())
    pr_label_by_name = {label.name: label for label in pr_labels}
    reviews = list(pr.get_reviews())
    review_by_user: Dict[str, PullRequestReview] = {}
    for review in reviews:
        if review.user.login in review_by_user:
            stored_review = review_by_user[review.user.login]
            if review.submitted_at >= stored_review.submitted_at:
                review_by_user[review.user.login] = review
        else:
            review_by_user[review.user.login] = review
    approved_reviews = [
        review for review in review_by_user.values() if review.state == "APPROVED"
    ]
    for approved_label, conf in settings.input_config.items():
        logging.debug(f"Processing config: {conf.json()}")
        if conf.await_label is None or (conf.await_label in pr_label_by_name):
            logging.debug(f"Processable PR: {pr.number}")
            if len(approved_reviews) >= conf.number:
                logging.info(f"Adding label to PR: {pr.number}")
                pr.add_to_labels(approved_label)
                if conf.await_label:
                    logging.info(f"Removing label from PR: {pr.number}")
                    pr.remove_from_labels(conf.await_label)
logging.info("Finished")
