from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import EntryForm, TopicForm
from .models import Entry, Topic


def index(request):
    """Render homepage"""
    return render(request, "index.html")


@login_required
def topics(request):
    """Render all topics, page"""
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {"topics": topics}
    return render(request, "topics.html", context)


@login_required
def topic(request, topic_id):
    """Render all entries of a topic, page"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entries_set.order_by("-date_added")

    if request.user != topic.owner:
        raise Http404

    context = {"topic": topic, "entries": entries}
    return render(request, "entries.html", context)


@login_required
def new_topic(request):
    """Enter a new topic, page"""
    if request.method != "POST":
        # No data submitted create new empty form
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect("learning_logs:topics")

    context = {"form": form}
    return render(request, "new_topic.html", context)


@login_required
def new_entry(request, topic_id):
    """Enter a new entry, page"""
    topic = Topic.objects.filter(owner=request.user).get(id=topic_id)
    entry = topic.text

    if topic.owner != request.user:
        return Http404

    if request.method != "POST":
        # No data submitted create new empty fo
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)

    context = {"form": form, "topic": topic}
    return render(request, "new_entry.html", context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=topic.id)

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "edit_entry.html", context)
