from typing import TypedDict


class DailyLearningErrorDefinitions(TypedDict):
    invalid_date: str
    invalid_description: str


DAILY_LEARNING_ERRORS: DailyLearningErrorDefinitions = {
    "invalid_date": "The date cannot be in the future.",
    "invalid_description": "Description must be at least 5 characters.",
}


class TagsErrorDefinitions(TypedDict):
    duplicate_name: str


TAG_ERRORS: TagsErrorDefinitions = {
    "duplicate_name": "A tag with this name already exists for this user."
}
