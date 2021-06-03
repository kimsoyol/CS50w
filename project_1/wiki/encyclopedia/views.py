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
    # c
    entry = util.get_entry(title)

    if not entry:
        return render(request, "encyclopedia/entry.html", {
            "ttile" : "error",
            "context" : "Sorry, the page you are looking for could not be found.",
        })

    else:     
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "context" : md.convert(entry),
        })


def search(request):
    #if request.method == "GET":
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
            if title.upper() in entries:
                return render(request, "encyclopedia/create_page.html",{
                        'pageForm': forms.CreatePageForm(),
                        'error': "Page Already exit!"
                    })
            else:
                contentData = ('#' + title) + '\n' + content
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
        oldForm = forms.EditPageForm(initial={'title': title, 'content': oldContent})
        return render(request, "encyclopedia/edit_page.html", {
            'editForm': oldForm,
        })   

    else:
        form = forms.EditPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html",{
                'title': title,
                'context': md.convert(content)
            })
            

def random_page(request):
    title = choice(util.list_entries())
    page = util.get_entry(title)
    return render(request, "encyclopedia/entry.html",{
        'title': title,
        'context': md.convert(page)
    })
            