import markdown2
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django import forms
from . import util
import random

# Renders the home page of the wiki
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),  
    })

# Provided a title the function will check if the entry exists. If it does then the page is converted to HTML and returned.
def convertToHtml(title):
    page = util.get_entry(title)
    # Performs a check to see that entry exists
    if page == None:
        return None
    else:
        markdowner = Markdown()
        return markdowner.convert(f"{page}")

# Renders the HTML page if the entry exists
def entry(request, title):
    html = convertToHtml(title)
    if html == None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "html": html
        })

# Takes the queried entry and displays the page or a list of pages with the substring in its title
def search(request):
    if request.method == "POST":
        title = request.POST['q']
        html = convertToHtml(title)
        if html != None:
            return render(request, "encyclopedia/entry.html", {
            "title": title,
            "html": html
            })
        else:
            substringEntries = []

            # Searches through list of all entries for titles with the substring
            for name in util.list_entries():
                if title.lower() in name.lower():
                    substringEntries.append(name)

            return render(request, "encyclopedia/search_results.html", {
            "entries": substringEntries
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),  
    })

# Retrieves a random entry from the list of entries and renders the page
def randomPage(request):
    randomIndex = random.randrange(len(util.list_entries()))
    title = util.list_entries()[randomIndex]
    html = convertToHtml(title)
    return render(request, "encyclopedia/entry.html", {
            "title": title,
            "html": html
        })

# Converts all strings in list to lowercase
def all_lower(list):
    return [x.lower() for x in list]

# Renders the html page to create a new entry within the wiki
def createNewPage(request):
    if request.method == "POST":
        title = request.POST['title']
        # Checks for unique title by searching through titles list
        if title.lower() not in all_lower(util.list_entries()):
            content = request.POST['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'title': title}))
        else:
            return render(request, "encyclopedia/createPage.html", {
                "content": request.POST['content'],
                "title": "",
                "errorVis": '<p style="color: red;">Entry with provided title already exists. Try again.</p>'
            })

    return render(request, "encyclopedia/createPage.html", {
        "content": "",
        "title": "",
        "errorVis": "<br></br>"
    })

# Allows the user to edit markdown content of an existing page
def editPage(request, title):
    if request.method == "POST":
        postTitle = request.POST['title']
        content = request.POST['content']
        util.save_entry(postTitle, content)
        return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'title': postTitle}))

    return render(request, "encyclopedia/editPage.html", {
        "content": util.get_entry(title),
        "title": title,
        "errorVis": "<br></br>",
        "url": "{% url 'encyclopedia:editPage' {title} %}"
    })
