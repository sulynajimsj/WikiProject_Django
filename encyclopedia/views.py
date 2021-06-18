from logging import PlaceHolder
from django.shortcuts import render
from django.http import HttpResponse
import markdown2
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from django.urls import resolve
from . import util
import random


class findWikiForm (forms.Form):
    entry = forms.CharField(label="", widget=forms.TextInput(attrs={
            'placeholder': 'Search for entry...'}))

class createForm (forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
            'placeholder': 'Enter title', 'id': 'new-entry-title'}))
    
    data = forms.CharField(label="", widget=forms.Textarea(attrs={
        'id': 'new-entry'}))

class EditForm (forms.Form):
    data = forms.CharField(label="",widget=forms.Textarea(attrs={
        'id': 'new-entry'}))


def edit(request, title):
    if request.method == "GET":
        editForm = EditForm(initial = {'data': util.get_entry(title)})
        return render(request, "encyclopedia/edit.html", {
            "theform": editForm,
            "form": findWikiForm()
        })
    else:
        saveForm = EditForm(request.POST)
        if saveForm.is_valid():
            newcontent = saveForm.cleaned_data["data"]
            util.save_entry(title, newcontent)
            return render(request, "encyclopedia/entry.html", {
                "content": markdown2.markdown(newcontent),
                "title": title,
                "form": findWikiForm()
            })

        

def random_entry(request):
    all_entries = util.list_entries()
    random_entry = random.choice(all_entries)
    random_content = util.get_entry(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "content": markdown2.markdown(random_content),
        "title": random_entry,
        "form": findWikiForm()
    })








def create(request):
    if request.method == "POST":
        createform = createForm(request.POST)
        if createform.is_valid():
            thetitle = createform.cleaned_data["title"]
            thecontent = createform.cleaned_data["data"]
            if thetitle in util.list_entries():
                return render(request, "encyclopedia/create.html", {
                    "isExist": True,
                    "theform": createForm(request.POST)

                })
            else:  
                util.save_entry(thetitle, thecontent)
                return render(request, "encyclopedia/entry.html", {
                    "content": markdown2.markdown(util.get_entry(thetitle)),
                    "title": thetitle,
                    "form": findWikiForm()
                })
            
            
    return render(request, "encyclopedia/create.html", {
        "theform": createForm(),
    })


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": findWikiForm()
    })

def title(request, title):
    
    return render(request, "encyclopedia/entry.html", {
        "content": markdown2.markdown(util.get_entry(title)),
        "title": title,
        "form": findWikiForm()
    })


def search(request): 
    if request.method == "POST":
        form = findWikiForm(request.POST)
        all_entries = util.list_entries()
        count_found = 0
        #Check if the form is valid
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            similar_entries = []
            for data in all_entries:
                if entry.lower() == data.lower():
                    return HttpResponseRedirect(f"wiki/{entry.lower().capitalize()}")
                #If a letter or word is in the list
                #We then list them
                elif (entry.lower() in data.lower()):
                    similar_entries.append(data)
                    count_found+=1
        
        
            #If we found at least one similar result
            return render(request,'encyclopedia/search.html', {
                "form": findWikiForm(),
                "similar_entries": similar_entries,
                "isnotEmpty": count_found > 0
            })
    

                   

    return render(request,'encyclopedia/index.html', {
        "form": findWikiForm()  
    })


    

