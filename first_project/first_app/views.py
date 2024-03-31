import os
from os import listdir

import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CreateNewList

# Create your views here.


def index(request):
    tv_shows_list = {
        "tv_shows": {
            "Game of Thrones": "9.3",
            "Blacklist": "8",
            "Suits": "8.5",
            "The Witcher": "8.5",
        }
    }
    return render(request, "first_app/index.html", context=tv_shows_list)


def home(request):
    return HttpResponse("Welcome to home page!")


def create(request):
    if request.method == "POST":
        form = CreateNewList(request.POST)

        if form.is_valid():
            job_title_value = form.cleaned_data["job_title"]
            job_description_value = form.cleaned_data["job_description"]

            ENDPOINT_COMPLETIONS = "https://api.openai.com/v1/chat/completions"

            # Global variables
            API_KEY = "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"

            prompt = f"Give 5 behavioural interview questions for the role of {job_title_value} with the following job description: {job_description_value}. Answer them too. Questions in single quotes and Answers in double quotes"
            GPT3 = "gpt-3.5-turbo"

            # Sends the request to the API
            response = requests.post(
                ENDPOINT_COMPLETIONS,
                json={"model": GPT3, "messages": [{"role": "user", "content": prompt}]},
                headers={
                    "Content-type": "application/json",
                    "Authorization": f"Bearer {API_KEY}",
                },
            )

            # Extracts the data from the response
            data = response.json()

            sections = data["choices"][0]["message"]["content"].split(
                "\n\n"
            )  # Assuming each section is separated by two newline characters
            global qa_pairs
            qa_pairs = {}
            for section in sections:
                if section.strip():  # Ignore empty sections
                    lines = section.split("\n")
                    question = lines[0].strip()
                    answer = "\n".join(lines[1:]).strip()
                    qa_pairs[question] = answer

            for question, answer in qa_pairs.items():
                print("Question:", question)
                print("Answer:", answer)
                print()
            return HttpResponseRedirect(reverse("jobshow"))

    else:
        form = CreateNewList()

        return render(request, "first_app/create.html", {"form": form})


def jobshow(request):
    print(qa_pairs)
    return render(request, "first_app/jobshow.html", context={"questions": qa_pairs})
