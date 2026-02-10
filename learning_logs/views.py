from django.http import Http404
from django.shortcuts import redirect, render

from .forms import EntriesForm, TopicForm
from .models import Entries, Topic


def index(request):
    return render(request, "index.html")


def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {"topics": topics}
    return render(request, "topics.html", context)


def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entries_set.order_by("-date_added")

    if topic.owner != request.user:
        raise Http404

    context = {"topic": topic, "entries": entries}
    return render(request, "entries.html", context)


def new_topic(request):
    if request.method != "POST":
        # No data is sent, create empty data
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


def new_enetry(request, topic_id):
    topic = Topic.objects.filter(owner=request.user).get(id=topic_id)
    entry = topic.text

    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        form = EntriesForm()
    else:
        form = EntriesForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)

    context = {"form": form, "topic": topic}
    return render(request, "new_entry.html", context)


def edit_entry(request, entry_id):
    entry = Entries.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        form = EntriesForm(instance=entry)
    else:
        form = EntriesForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=topic.id)

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "edit_entry.html", context)
