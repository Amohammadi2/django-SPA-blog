from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q,F
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import viewsets
from rest_framework.status import HTTP_511_NETWORK_AUTHENTICATION_REQUIRED, HTTP_201_CREATED
from .models import *
from .serializers import *
from .forms import *
from .blog_conf import PageDescription, PageHeaderImageAddr, PageTitle, CustomCss
# Create your views here.

# @param: msg_header:str the header of message
# @param: msg_body:Str the body of message
# @param: err:Excpetion | an exception containing an erro
# @example1:
#     return_res("completed", "your post has been created")
# @result1:
#     {"msg": {"header": "completed", "body": "your post has been created"}}
# @example2:
#     try:
#          post_headline = request.data["headline"]
#     except Excpetion as err:
#          return_res("error", "error while creation of post", err)
# @result2:
#     {"msg": {"header": "error", "body": "error while creation of post"}, "err": str(err)}
def return_res(msg_header:str , msg_body:str , err:Exception=None)->dict:
    context = {
        "msg": {"header": msg_header, "body": msg_body},
    }
    if err:
        context.update({"err": str(err)})
    return context


# renders all templates
# @param: request -> httpRequest object that djagno framework injects
# @param: template -> the template name to render. name of the files within blog/templates/blog/
def render_template(request, template):
    website_info = WebsiteInfo.objects.get(pk=1)
    PageTitle = website_info.header_title
    PageDescription = website_info.header_description
    PageHeaderImageAddr = website_info.header_image_addr
    NavbarBackgroundColor = website_info.navbar_background_color
    NavbarMagicLineColor = website_info.navbar_magic_line_color
    return render(request, "blog/"+template, {
        "post_form": PostForm(),
        "user_login_form": UserLoginForm(),
        "user_signup_form": UserSignupForm(),
        "comment_form": CommentForm(),
        "respond_form": RespondForm(),
        "feedback_form": FeedbackForm(),
        "profile_info_form": ProfileInfoForm(),
        "page_title": PageTitle,
        "page_description": PageDescription,
        "page_header_image_addr": PageHeaderImageAddr,
        "navbar_background_color": NavbarBackgroundColor,
        "navbar_magic_line_color": NavbarMagicLineColor,
    })

# start home page
def index(request):
    return render_template(request, "index.html")
	
#quick_start page
def quick_start(request):
	try:
		response = "<h1>quick start completed</h1>"
		info = WebsiteInfo.objects.filter(pk=1)
		# if there is no informations so create
		if not info:
			WebsiteInfo.objects.create(
				header_image_addr = "/media/website/img/site_wall-min.jpg",
				header_title = "Django blog",
				header_description = "another blog written in Django",
				navbar_background_color = "green",
				navbar_magic_line_color = "white",
			)
			User.objects.createsuperuser
		# check if there is at least one super user
		super_users = User.objects.filter(is_superuser=True)
		# if there isn' 
		if not super_users:
			user = User.objects.create_user("admin", password="admin")
			user.is_superuser = True
			user.is_staff = True
			user.save()
			profile = Profile.objects.create(user=user)
			profile.save()
			response += "<p>username: admin, password: admin</p>"
			response += "<p>to change your password go to admin panel</p>"
		
		return HttpResponse(response)
	except Exception as err:
		print(err)
		return HttpResponse((
			"<h1>database tables are not availibal</h1>"
			"<p>make sure you have made migrations and migrated the database :)</p>"
			"<p>run start.py and make migrations then migrate</p>"
		))

# posts
# this veiw set lets us to deal with post objects
# delete, create, retive them
# extra actions are added for more functionalities
#------------------------------------------------
# EXTRA ACTIONS:
    # @param: self -> python class instance
    # @param: request -> djagno httpRequest
    # @param: pk -> id of a specific post for actions on one post e.g /posts/5/update_post/, pk=5
class postsView(viewsets.ModelViewSet):
    serializer_class = PostSerial
    queryset = Post.objects.all()

    # get user liked posts
    @action(["GET"], False)
    def user_liked_posts(self, request):
        # get the user
        user = request.user if request.user.username else None
        if not user: return Response({"msg": {"header": "please login", "body":"you haven't logged in"}})

        # get the posts that user has liked them
        liked_posts = user.popular_posts.all()
        serial = PostSerial(liked_posts, many=True)

        return Response(serial.data)

    # use this function to examine that a user has liked a post or not
    @action(["GET"], True)
    def has_user_liked(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        # check if user has logged in or not
        if request.user.username:
            user = request.user
        # otherwise 
        else: 
            return Response({
                "has_liked": False,
            })
        
        # return the response
        return Response({
            "has_liked": True if user in post.likes.all() else False,
        })

    # this functions is for like and dislike functionalities
    # likes the post if the reuqest.user (current user) is not
    # in the post.likes -> ManyToMany with User object
    # otherwise removes user from relation ship
    @action(["POST"], True)
    def toggle_like(self, request, pk):
        # get the post with its id
        post = get_object_or_404(Post, pk=pk)
        # get the current user if has been logged in
        if request.user.username:
            user = request.user
        # otherwise 
        else: 
            return Response({
                "msg": {"header": "please login", "body": "you haven't logged in"}
            })
        # that's because we need a real User object to like a post

        # now add the user toggle_like . custom method in Post Class
        # gets a user objects adds it to likes
        post.toggle_like(user)
    
        # check weather the user has been removed or added
        if user in post.likes.all():
            return Response({
                "liked": True
            })
        else:
            return Response({
                "disliked": True
            })


    # this updates the post. it needs:
    # bodyText, headline, summery, categories[],
    # send them in an ajax request
    @action(["POST"], True)
    def update_post(self, request, pk):
        # get the exising post otherwise raise 404 error
        pst = get_object_or_404(Post, pk=pk)
        # try to get all informations
        try:
            bodyText = request.data["bodyText"]
            headline = request.data["headline"]
            summery = request.data["summery"]
            categories = request.data["categories[]"]
            author = request.user
        except Exception as err:
            return Response({
                "msg": {"header": "information not enough","body": "your information is not enough to update"},
                "err": str(err),
            })
        
        # now update the post
        try:
            pst.bodyText = bodyText
            pst.headline = headline
            pst.summery = summery
            pst.author = author
            pst.categories.set(categories)
            pst.save()
        except Exception as err:
            return Response({
                "msg": {"header": "can't update post","body": "faild to update the existing post"},
                "err": str(err),
            })

        #finally return Response
        return Response({
            "msg": {"header": "post updated", "body": "your post has been updated"}
        })


        
    # this functions gets the posts related to a specific user
    # you have to be logged in to use this function otherwise you'll get nothing
    @action(["GET"], False)
    def get_posts_related_to_user(self, request):
        posts = Post.objects.filter(author=request.user)
        serial = PostSerial(posts, many=True)
        return Response(serial.data)


    # newest posts
    @action(["GET"], False)
    def get_new_posts(self, request):
        new_posts = Post.objects.get_newest(6)
        serial = PostSerial(new_posts, many=True)
        return Response(serial.data)


    # popular posts
    @action(["GET"], False)
    def get_pop_posts(self, request):
        pop_posts = Post.objects.get_popular(6)
        serial = PostSerial(pop_posts, many=True)
        return Response(serial.data)

    # controversial posts
    @action(["GET"], False)
    def get_controversial_posts(self, request):
        cont_posts = Post.objects.get_controversial(6)
        serial = PostSerial(cont_posts, many=True)
        return Response(serial.data)


    # creat a new post
    # needs:  bodyText, summery, headline, author
    # send them in an ajax request
    @action(["POST"], False)
    def create_new_post(self, request):
        if request.user.username:
            try:
                new_post = Post(
                    bodyText = request.data["bodyText"],
                    summery = request.data["summery"],
                    headline = request.data["headline"],
                    author = request.user,
                )
                new_post.save()
                print(request.data)
                new_post.categories.set(request.data["categories[]"])
                new_post.save()
            except Exception as err:
                return Response({
                    "msg": {"header": "error", "body": "an error happend during creation of post"},
                    "err": str(err)
                })
            else:
                return Response({"msg": {"header": "created", "body": "your post successfully created"}})
        else:
            return Response({"msg": {
                "header": "login first",
                "body": "you need to have an account then you can send your posts"
            }}, HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)
    
    @action(["GET"], False)
    def search_for_post(self, request):
        try:
            query = request.GET["q"]
        except Exception as err:
            return Response(return_res("error", "q parameter not found", err))

        result = Post.objects.filter(
            Q(headline__icontains=query) | Q(bodyText__icontains=query)
        )

        if not result: # control the empty queryset
            return Response({
                "not_found": True, # we use this flag to determine the query has no result in js side
            })

        serial = PostSerial(result, many=True)
        return Response(serial.data)

# login a user
# needs: username, password
# send them in an ajax request
@api_view(["POST"])
def login_user(request):
    try:
        user = request.data["username"]
        Pass = request.data["password"]
    except Exception as err:
        return Response({"msg": {
            "header": "error parsing values",
            "body": "username and password arguments are not provided in the request",
        }, "err": err})

    user = authenticate(username=user, password=Pass)
    if user is not None:
        login(request, user)
        return Response({"msg": {"header": "login completed", "body": "you have been logged in"}})
    else:
        return Response({"msg": {"header": "login faild", "body": "your username or password is incorrect"}})

# logs out a user
# needs: nothing!
@api_view(["POST"])
def logout_user(request):
    logout(request)
    return Response({"msg": {"header": "logout completed", "body": "you have been logged out"}})


# checks weather user has account or not
# returns has = True if has otherwise has = False
# it is stores in a dictionary
@api_view(["POST"])
def has_account(request):
    if request.user.username:
        if request.user.is_superuser:
            return Response({"has": True, "admin": True})
        elif request.user.is_active:
            return Response({"has": True, "admin": False})
        else:
            return Response({
                "has": False,
                "admin": False,
                "msg": {"header": "accout not activated","body": "your account is not activate"},
            })
    else:
        return Response({"has": False})


# signup a new user
# needs: user, pass, first, last, email
# send them in an ajax request
@api_view(["POST"])
def signup(request):
    # gathering information
    try:
        data = request.POST
        user = data["user"]
        Pass = data["pass"]
        first = data["first"]
        last = data["last"]
        email = data["email"]
    # if an exception occured
    except Exception as err:
        # handle it
        return Response({
            "msg": {"header":"error parsing values", "body": "arguments are not provided", "err": str(err)}
        })
    # create a user
    try:
        usr = User.objects.create(
            username = user,
            first_name = first,
            last_name = last,
            email = email,
        )
        usr.set_password(Pass)
        usr.save()
    except Exception as err:
        return Response({
            "msg": {"header": "user not created", "body": "error during creation of user"}
        })
    # create profile for the user
    try:
        profile = Profile.objects.create(
            user = usr,
        )
        profile.save()
    except Exception as err:
        return Response({
            "msg": {"header": "profile not created", "body": "error during creation of profile"}
        })

    return Response({
        "msg": {"header": "signing up completed","body": "now login to your account"}
    })


# this is a view set for comments
#---------------------------------
# EXTRA ACTIONS
    # @param: self -> instance of CommentView class
    # @param: request -> HttpRequest django object
    # @param: pk -> primary key for detailed actions (working with a specific comment)
class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerial
    queryset = Comment.objects.all()

    @action(["DELETE"], True)
    def delete_comment(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        post = comment.post
        post.remove_comment(comment)
        return Response({
            "msg": {"header": "deleted", "body": "your comment has been deleted"}
        })

    @action(["POST"], False)
    def create_new_comment(self, request):
        # try to get the data
        try:
            text = request.data["text"]
            post_pk = request.GET["id"] # the id is avalibal in the url
            sender = request.user

        # if an error occured
        except Exception as err:
            return Response({
                "msg": {"header": "error", "body":"an error occured during information gathering"},
                "err": str(err)
            })

        # now try to create a new comment
        try:
            # create a comment
            new_comment = Comment.objects.create(
                text = text,
                sender = sender,
            )
            # get the post
            post = Post.objects.get(pk=post_pk)
            # assign it the comment
            post.add_comment(new_comment)
            

        # except any error
        except Exception as err:
            return Response({
                "msg": {"header", "comment not created", "body", "error during creation of comment"},
                "err": str(err),
            })


        # otherwise
        return Response({
            "msg": {"header": "successfully sent", "body": "your comment has been sent"}
        })

    # a new action to get the comments related to a post
    # this is used to update comments
    @action(["POST"], False)
    def get_comments_related_to(self, request):
        # we need to get the id of post
        try:
            post_pk = request.data["id"]

        # handle exceptions
        except Exception as err:
            return Response({
                "msg": {"header": "id of post not found", "body": "argument id is not provided"},
                "err": str(err)
            })

        # get the comments related to [post_pk](var)
        related_comments = Comment.objects.filter(post=post_pk)

        # serialize them
        serial = CommentSerial(related_comments, many=True)

        # return the response
        return Response(serial.data)

    @action(["GET"], False)
    def get_comments_of_user(self, request):
        # get the user
        user = request.user

        # get the comments which user is their sender
        comments = Comment.objects.filter(sender=user)

        # serialize the data as json structuer
        serial = CommentSerial(comments, many=True) # because we have more than one objects (maybe)

        # now return the response to the client
        return Response(serial.data) # serial.data contains the json data



# this is a view set for Responds
#---------------------------------
# EXTRA ACTIONS
    # @param: self -> instance of respondView class
    # @param: request -> HttpRequest django object
    # @param: pk -> primary key for detailed actions (working with a specific Respond)
class RespondView(viewsets.ModelViewSet):
    queryset = Respond.objects.all()
    serializer_class = RespondSerial

    @action(["POST"], False)
    def create_new_respond(self, request):
        # information gathering
        try:
            comment_pk = request.data["comment_id"]
            respond_text = request.data["text"]

        # handle any exceptions
        except Exception as err:
            return Response({
                "msg": {"header": "faild", "body": "information gathering faild"},
                "err": str(err)
            })

        # try to create the respond
        try:
            new_respond = Respond.objects.create(
                text = respond_text,
                comment = Comment.objects.get(pk=comment_pk),
                sender = request.user,
            )

        # handle any exceptions
        except Exception as err:
            return Response({
                "msg": {"header": "faild", "body": "error while creating the post"},
                "err": str(err)
            })

        # finally
        return Response({
            "msg": {"header": "successfully sent", "body": "your respond has been successfully sent"},
        })

    # get responds related to a comment
    @action(["GET"], False)
    def get_responds_related(self, request):
        # information gathering
        try:
            comment_pk = request.GET["comment_id"]
            comment = Comment.objects.get(pk=comment_pk)

        # handle any exceptions
        except Exception as err:
            return Response({
                "msg": {"header": "faild", "body": "information gathering faild"},
                "err": str(err)
            })

        # get the responds
        responds = Respond.objects.filter(comment=comment)

        # serialize the data
        serial = RespondSerial(responds, many=True)

        # finally
        return Response(serial.data)

# website's information
class WebsiteInfoView(viewsets.ModelViewSet):
    queryset = WebsiteInfo.objects.filter(pk=1)
    serializer_class = WebsiteInfoSerial

    # updates the informations on header section
    @action(["POST"], True)
    def update_header_section(self, request, pk):
        # getting the informations
        info = get_object_or_404(WebsiteInfo, pk=pk)
        try:
            title = request.data["title"]
            description = request.data["description"]
            image_addr = request.data["image_addr"]
        except Exception as err:
            return Response({
                "msg": {"header": "error", "body": "informations aren't provided"},
                "err": str(err),
            })

        # updating informations
        info.header_title = title
        info.header_description = description
        info.header_image_addr = image_addr
        # saving changes and commiting to database
        info.save()

        return Response({
            "msg": {"header": "successfully saved", "body": "your changes have been saved"},
        })

    # updates the navbar sections
    @action(["POST"], True)
    def update_navbar_section(self, request, pk):
        # gathering informations
        info = get_object_or_404(WebsiteInfo, pk=pk)
        try:
            navbar_color = request.data["navbar_color"]
            magic_color = request.data["magic_color"]
        except Exception as err:
            return Response(return_res("error" , "informations aren't provided", err))

        #updating info
        info.navbar_background_color = navbar_color
        info.navbar_magic_line_color = magic_color

        #saving and commiting to database
        info.save()

        return Response(return_res("successfully saved", "your changes have been saved"))


class FeedbackView(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerial

    @action(["POST"], False)
    def create_feedback(self, request):
        # informtaion gathering
        try:
            feedback_text = request.data["text"]
        # handles any exception
        except Exception as err:
            return Response(return_res("error", "arguments are not provided", err))

        Feedback.objects.create(text=feedback_text)

        return Response(return_res("sent", "we've recieved your feedback"))


# this is a view set for categories
# we'll use it to get posts by their categories
class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerial

    @action(["POST"], False)
    def create_new_category(self, request):
        # info gathering
        try:
            name = request.data["name"]
        # handle exceptions
        except Exception as err:
            return Response(return_res("error", "the name of category is not provided", err))
        # create the category
        category = Category.objects.create(name=name)
        # return the response
        serial = CategorySerial(category, many=False)
        # serialize the data
        return Response(serial.data)

    # use this function to update a category
    @action(["POST"], True)
    def update_category(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        try:
            name = request.data["name"]
        except Exception as err:
            return Response(return_res("error", "name is not provided", err))

        category.name = name
        category.save()

        return Response(return_res("saved", "category has been updated"))



class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerial

    @action(["POST"], True)
    def update_profile_image(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        try:
            profile.photo.delete(save=True)
            profile.photo = request.FILES["profile_image"]
            profile.save()
        except Exception as err:
            return Response(return_res("error", "erro while updating the profile", err))

        return Response({"url":  profile.photo.url})

    @action(["POST"], True)
    def update_profile_info(self, request, pk):

        profile = get_object_or_404(Profile, pk=pk)
        try:
           bio = request.data["bio"]
           phone = request.data["phone"]
        except Exception as err:
            return Response(return_res("error", "biography or phone is not provided", err))

        profile.bio = bio
        profile.phone = phone

        profile.save()

        return Response(return_res("changed", "your profile has been changed"))

    @action(["GET"], False)
    def get_user_profile(self, request):
        serial = UserInfoSerial(request.user) if request.user.username else None

        if not serial:
            return Response(
                return_res("login first", "you havn't logged in")
            )

        return Response(serial.data)