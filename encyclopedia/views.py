from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
import markdown2
import random 
from django.urls import reverse
from . import util
from .forms import CreatePageForm

def index(request):
    """Returns all entries to the index-/homepage."""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    """Loads an entry page by converting markdown files to html 
        and passing them into the entry html template."""
    entry_markdown = util.get_entry(title)

    if entry_markdown:
        entry_html = markdown2.markdown(entry_markdown)

        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "entry" : entry_html
        })
    else:
        return render(request, "encyclopedia/error.html")
    
def search(request):
    """Takes as input the query entered in the search bar 
        and as output the entry page, all possible entries meant or the error page."""
    all_entries = util.list_entries()
    possibilities = []

    if request.method == 'GET':
        search_query = request.GET.get('q')
        
    for entry in all_entries:
        if search_query.lower() == entry.lower():
            entry_html = markdown2.markdown(util.get_entry(search_query)) 
            return render(request, "encyclopedia/entry.html", {
                "title" : search_query,
                "entry" : entry_html
            })
        if search_query.lower() in entry.lower():
            possibilities.append(entry)

    if possibilities:
        return render(request, "encyclopedia/search_results.html",{
            "all_entries": possibilities
            })
    return render(request, "encyclopedia/error.html")

def new_page(request):
    """Creates a new entry, when the title already exists an error message is given"""
    all_entries = util.list_entries()

    # When user submits entry, clean data
    if request.method == "POST":
        form = CreatePageForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data['entry_title']
            entry_body = form.cleaned_data['entry_body']
            
            # Give error message when entry (title) already exists, else save entry and go to page
            for entry in all_entries:
                if entry_title.lower() == entry.lower():
                    return render(request, "encyclopedia/new_page.html", {
                            "form" : form,
                            "error_message" : "Entry already exists, create a new entry"
                            })
                else:
                    content = util.save_entry(entry_title, entry_body)
                    page = util.get_entry(entry_title)
                    html_page = markdown2.markdown(page)
                    return render(request, "encyclopedia/entry.html", {
                        "title" : entry_title,
                        "entry" : html_page
                    })

    form = CreatePageForm()
    return render(request, "encyclopedia/new_page.html", {
        "form" : form
    })

def random_entry(request):
    """Returns a random entry page."""
    all_entries = util.list_entries()
    random_entry = random.choice(all_entries)

    return redirect(reverse('entry', args=[random_entry]))
