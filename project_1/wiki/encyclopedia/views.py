from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util, forms
from markdown2 import Markdown 
from random import choice

md = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": forms.SearchForm(),
    })


def entry(request, title):
    entry = util.get_entry(title)

    if entry is None:
        return render(request, "encyclopedia/entry.html", {
            "title" : "Error",
            "message" : "Sorry, the page you are looking for could not be found.",
        })

    else:     
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "context" : md.convert(entry),
        })


def search(request):
    titles = util.list_entries()
    results = []

    form = forms.SearchForm(request.GET)
    if form.is_valid():
        title = form.cleaned_data["title"]
        for i in titles:
            if i.lower() == title.lower():
                return redirect(f"wiki/{title}")
        
            if title.lower() in i.lower():
                results.append(i)
        return render(request, "encyclopedia/search_result.html",{
            "results": results,
        })    
              

def create_page(request):
    if request.method == 'POST':
        form = forms.CreatePageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/create_page.html",{
                        'pageForm': forms.CreatePageForm(),
                        'error': "Page Already exit!"
                    })
            else:
                contentData = ('#' + ' ' + title) + '\n' + '\n'+ content
                util.save_entry(title, contentData)
                page = util.get_entry(title)
                pageConvert = md.convert(page)
                return redirect(f"wiki/{title}")

    else:
        form = forms.CreatePageForm()
        return render(request, "encyclopedia/create_page.html",{
            'pageForm': form
        })

        
def edit_page(request, title):
    if request.method == "GET":
        oldContent = util.get_entry(title)

        if oldContent is None:
            return render(request, "encyclopedia/entry.html", {
            "title" : "Error",
            "context" : "Sorry, the page you are looking for could not be found.",
        })
        else:
            editContent = oldContent.split("\n",2)[2]
            oldForm = forms.EditPageForm(initial={'title': title, 'content': editContent})
            return render(request, "encyclopedia/edit_page.html", {
                'editForm': oldForm,
            })   

    else:
        form = forms.EditPageForm(request.POST)
        if form.is_valid():
            newtitle = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            contentData = ('#' + ' ' + newtitle) + '\n' + '\n'+ content
            if newtitle != title:
                filename = f"entries/{title}.md"
                if default_storage.exists(filename):
                    default_storage.delete(filename)
            util.save_entry(newtitle, contentData)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[newtitle]))


def random_page(request):
    title = choice(util.list_entries())
    page = util.get_entry(title)
    return render(request, "encyclopedia/entry.html",{
        'title': title,
        'context': md.convert(page)
    })
            