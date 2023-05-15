from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost

# Create your views here.


def index(request):
    allblog = Blogpost.objects.values(
        "post_id", "title", "pub_date", "head0", "chead0", "thumnbnaile", "topic"
    )
    AllAboutblog = {
        "Blogdetils": allblog,
        "numberofblog": range(len(allblog) % 2 + len(allblog) // 2),
    }
    # print(AllAboutblog["numberofblog"])
    # print(AllAboutblog["Blogdetils"])
    return render(request, "blog/index.html", {"AllBlogs": AllAboutblog})


def blogPost(request, blogid):
    # print(blogid)
    relatedBlogDetails = []
    blogdetails = Blogpost.objects.filter(post_id=blogid)
    # if Blogpost.objects.filter(post_id=blogid - 1) != {}:
    relatedBlogDetails.append(Blogpost.objects.filter(post_id=blogid - 1))
    # if Blogpost.objects.filter(post_id=blogid + 1) != {}:
    relatedBlogDetails.append(Blogpost.objects.filter(post_id=blogid + 1))
    return render(
        request,
        "blog/blogpost.html",
        {"BlogDetails": blogdetails[0], "RelatedBlogDetails1": relatedBlogDetails},
    )
