from django.urls import path

from . import views

app_name = "learning_logs"

urlpatterns = [
    # Render homepage
    path("", views.index, name="index"),
    # Render topics
    path("topics", views.topics, name="topics"),
    # Render topic entries
    path("topics/<int:topic_id>", views.topic, name="topic"),
    # Render new topic form
    path("new_topic/", views.new_topic, name="new_topic"),
    # Render new entry
    path("new_entry/<int:topic_id>/", views.new_enetry, name="new_entry"),
    # Render edit entry
    path("edit_entry/<int:entry_id>/", views.edit_entry, name="edit_entry"),
]
