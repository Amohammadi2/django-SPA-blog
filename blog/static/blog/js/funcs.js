/* dealing with notifications */

// shows notifications
// @param: msg -> the message :sring e.g -> "hello this is msg"
// @param: header -> the header :string -> "hello this is header"
// @param: delay -> how many miliseconds to show the notification :int e.g -> 2000 (2 seconds)
function show_notification(msg, header, delay=1500){
    $(".notification-header").text(header);
    $(".notification-body").text(msg);
    $(".notification").css({
        "opacity": "1",
        "left": "50px",
        "bottom": "50px",
    });
    setTimeout(() => {
        hide_notification();
    }, delay);
}


// hides the notification
// this function accepts no arguments
function hide_notification(){
    $(".notification").css({
        "opacity": "0",
        "left": "-50%",
        "bottom": "-50%",
    });
}

// shoes page preloader (bootstrap spinner)
// accepts no arguments
function show_preloader(){
    $(".page-preloader").fadeIn(100);
}

// hides page preloader
// accepts no arguments
function hide_preloader(){
    $(".page-preloader").fadeOut(100);
}



function upload_file(form, url, type, callback= data => console.log("callback")){
    // we have file to be sent
    var form_data = new FormData(document.getElementById(form));

    $.ajax({
        url: url,
        type: type,
        data: form_data,
        contentType: false,
        processData: false,
        headers: {
            "x-csrftoken": getCookie("csrftoken"),
        },
        xhr: function(){
            // we want to show the user percentage
            var xhr = new window.XMLHttpRequest();
            xhr.addEventListener("loadstart", event => {
                $(".upload_progress_bar").fadeIn(600);
            });
            xhr.addEventListener("progress", event => {
                var percent_counter = $(".precent_count");
                if(event.lengthComputable){
                    var percent = Math.round(event.loaded / (event.total / 100));
                    percent_counter.text(percent + "%");
                }
                else{
                    percent_counter.text("size-unknown");
                }
            });
            xhr.addEventListener("load", event => {
                $(".upload_progress_bar").fadeOut(600);
            });
            return xhr;
        }
    })
    .fail(function() {
        console.log("operation failed");
    })
    .always(function (data){
        callback(data);
    });

}


/* performing ajax (base level) of all ajax calls*/
// for POST request you will need xcsrf-token that is handled by this function
// @param : url:str -> the page address to send ajax request e.g -> /posts
// @param : type:str -> the type of ajax request e.g -> POST, GET, DELETE, PUT and etc...
// @param : data:object -> the data to be sent e.g -> {"firstname": "ashkan", "lastname": "mohammadi"}
// @param : callBack:function -> a function to be called after the ajaxrequest
    //@sub-param: data:objec ->
        //data returned from server will be passed in the function as its first
        //argument. the function should have data parameter
function callApi(url, type, data, callBack=function(data){}){
    // shows preloader after 500 miliseconds
    var id = setTimeout(() => {
        show_preloader();
    }, 200);

    $.ajax({
        url: url,
        type: type,
        data: data,
        headers: {
            "x-csrftoken": getCookie("csrftoken"),
        },
    })
    .done(function() {
        //("success");
    })
    .fail(function() {
        //("error");
    })
    .always(function(d) {
        // clear the timeout
        clearTimeout(id);
        // finally hide the preloader
        hide_preloader();
        // call the callback function
        callBack(d);
        // if data has a message
        if (d.msg){
            // then show it as a notification
            show_notification(d.msg.body, d.msg.header, 6000);
        }
        // if data has an error
        if(d.err){
            // give me more detail in console
            console.log(d.err);
        }
    });
}

/* load a page */
// this function loads pages by sending a GET ajax request
// @param: url:string -> the url to send the ajax request (template name)
// data returned gets in div.container in index.html file
function render(url, delete_parameters=false){

    function callback(data){
        $(".container").css("display", "none");
        $(".container").html(data);
        $(".container").fadeIn(200);
    }

    callApi(url, "GET", {}, callback);

    if (delete_parameters){
        del_params();
    }

    add_param("render", url);
}

/* working with cookies*/
// this function sets a cookie
// @param: cname:string -> the cookie name
// @param: cvalue:sring -> the cookie's value
// @param: exdays:number -> cookie's expiration date
// no returning value [code snippet from w3schools.com]
function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}


// this function get's the cookie's value by the cookie name
// @param: cname:string -> name of cookie
// returns value of cname if exists otherwise an empty string will be returned
// [code snippet from w3schools.com]
function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

// checks if a cookie exists or not
// @param: cname -> name of the cookie to be looking for
// returns a boolean: true if it exists otherwise false
function hasCookie(cname){
    if(getCookie(cname)){
        return true;
    }else{
        return false;
    }
}

// a simple html template to use to insert a post to document
// @param: dist -> String [css selector] e.g.: "#contrbue", ".note > #my_id", "span" and ..
// @param: post -> a JSON containing a post content you can get it from url-> "/posts/"
// see the views.py file for more details
function insertPost(post, dist=".container"){
    var $new_post = $(`
    <div class="note col-lg-6">
        <input type="hidden" value="${post.id}">
        <div class="note-header">${post.headline}</div>
        <div class="note-body">
            ${post.summery}
        </div>
        <div class="note-footer">
            <span class="material-icons">comment</span>
            <span>${post.comments_count}</span>
            <span class="material-icons">loyalty</span>
            <span>${post.likes_count}</span>
            <span class="material-icons">insert_drive_file</span>
            <span>${post.author.username}</span>
        </div>
    </div>
    `);
    $new_post.children(".note-header").on("click", event => {

        // adding event listener to render the post
        //("note header clicked rendering the page");
        // render the renderer page
        render("render_post.html");
        // add id to id parameters
        add_param("id", $(event.target).siblings("input").val());
        
    });
    $new_post.appendTo(dist);
}

/**
 * this function adds a section
 * @param {str} id id of the section
 * @param {str} dist where to add the section default -> .container
 */
function insertSection(id, dist=".container" ){
    $(`
    <div class="cus-section mb-5">
        <div class="row" id="${id}">

        </div>  
    </div>
    `).appendTo(dist);
}

function insertCategory(category, dist=".container"){
    $(`
    <div class="cus-header mb-5 mt-5">
        <div class="cus-indicator"></div>
        <h1>${category.name}</h1>
    </div>
    `).appendTo(dist);
    // create a section for the category posts
    insertSection(category.name.replace(/ /g, "-") + "-posts");
    // a category object has a reverse relation to its posts
    // and it is accessible via category.posts it consists of
    // json data including post data which is compatible with
    // insertPost function
    // iterate over the category
    for (var p in category.posts){
        // get the post data
        var post = category.posts[p];
        // now add the post to the section which we just
        // created before
        insertPost(post, "#" + category.name.replace(/ /g, "-") + "-posts");
    }
}


function insert_comment(comment, dist="#post-comments"){
    // insert comment itself
    var $new_comment = $(`
        <div class="cus-section mt-3 mb-3 relative-comment">
            <span class="material-icons reply-button">reply</span>
            <input type="hidden" value="${comment.id}">
            <div class="comment-text mb-5">
                <span>
                    <img class="profile_small_image" src="${comment.sender.profile.photo}" alt="">
                </span>
                <strong>${comment.sender.username}</strong>: ${comment.text}
            </div>
            <form class="collapse">
                <div class="user-login">
                    <textarea class="form-control"></textarea>
                    <input type="submit" class="btn btn-primary" value="reply">
                </div>
                <div class="no-user-login">
                    <p> please login first then you can reply </p>
                </div>
            </form>
            <div class="comment-respond">
            </div>
        </div>
    `)
    $new_comment.appendTo(dist);
    // send reply to a comment
    $new_comment.children("form").on("submit", event => {
        // prevent the post from being sent
        event.preventDefault();
        
        // get the respond comment text
        var comment_text = $(event.target).children(".user-login").children("textarea").val();
        
        // make ajax call to the backend
        callApi("/responds/create_new_respond/", "POST", {
            "text": comment_text,
            "comment_id": comment.id,
        }, data => {

            // after sending the request, now update the commentList
            // getting all new responds related to the comment
            callApi(`/responds/get_responds_related/?comment_id=${comment.id}`, "GET",{} , data => {
                // clear the responds
                related_comment.html(" ");
                // now update them
                for (var i in data){
                    var r = data[i]; // this is a respond object
                    $(`
                        <div class="cus-section mt-2 mb-2"><strong>${r.sender.username}</strong>: ${r.text}</div>
                    `).appendTo(related_comment);
                }
            }); 

        });

        // reset the form
        event.target.reset();

    });

    // get the related comment
    var related_comment = $('input[value="'+comment.id+'"]')
    .parent()
    .children(".comment-respond");

    // now insert the responses to it
    for (i in comment.respond_set){
        // get the respond data
        var respond = comment.respond_set[i];
        $(`
            <div class="cus-section mt-2 mb-2"><strong>${respond.sender.username}</strong>: ${respond.text}</div>
        `).appendTo(related_comment);
    }

    // hide and show the collapsed forms to send reply to comments
    $(".reply-button").on("click", event => {
        // toggles the collapsible forms
        $(event.target).siblings("form.collapse").collapse("toggle");
    });
    
}


function getPosts(data, dist){
    // insert the posts into the document
    for (let i = 0; i < data.length; i++) {
        const post = data[i];
        insertPost(post, dist);
    }
}

function getNewPosts(data){
    getPosts(data, "#news");
}

function getPopPosts(data){
    getPosts(data, "#pops");
}

function getContPosts(data){
    getPosts(data, "#conts");
}

function getMyPosts(data){
    getPosts(data, "#myposts");
}

function getAllPosts(data){
    getPosts(data, "#allPosts");
}

function formHandle(data){
    //(data);
}

// checks user authentication
// hides user-login elements if user doesn't have account
// other wise shows
// use user-login and no-userlogin classes in elements
function check_auth(){
    callApi("/has_account/", "POST", {}, function(data){
        $(".admin-login").css("display", "none");
        if (data.admin){
            $(".admin-login").css("display", "block");
            $(".user-login").css("display", "block");
            $(".no-user-login").css("display", "none");
        }
        else if (data.has){
            $(".user-login").css("display", "block");
            $(".no-user-login").css("display", "none");
        }else{
            $(".no-user-login").css("display", "block");
            $(".user-login").css("display", "none");
        }
    });
}

// rendering markdown text
// @param: text:string -> a string containing markdown data
// returns html code according to (@param: text)
// e.g -> text="# this is heading" will produce <h1> this is heading </h1>
function render_markdown(text){
    var transformed_text = marked(text);
    return transformed_text;
}

// user actions
// logs in a user with password and username then checks the user authentication
// @param: user -> username
// @param: pass -> password
// no returning value
function user_login(user, pass){
    callApi("/login/", "POST", {
        username: user,
        password: pass,
    }, function (data) {
        check_auth();
    });
}


// logs out user
// no arguments
// no returning value
function user_logout(){
    callApi("/logout/", "POST", {}, function () {
        check_auth();
    });
}


// signup a new account
// @param: user -> username
// @param: pass -> password 
// @param: first -> firstname
// @param: last -> lastname
// @param: email -> email
// no returning value
function user_signup(user,pass,first,last,email){
    callApi("/signup/", "POST", {
        user,
        pass,
        first,
        last,
        email,
    }, function (data) {
        check_auth();
    });
}

// working with url witout refreshing the whole page
// this function adds parameters to page url without refresing the page
// @param: key -> string
// @param: value -> string
function add_param(key, value){
    // endcode them as valid text
    key = encodeURIComponent(key);
    value = encodeURIComponent(value);
    // get the existing params
    var existing_params = window.location.search;
    // replace ? with a ""
    existing_params = existing_params.replace("?", "");
    // perform a valid url key|value pairs
    var new_param = key + "=" + value;
    // check if the parameter exists or not
    if (get_param(key)){
        // if exists don't add it instead update it
        var existing_params_array = existing_params.split("&"); // -> ["key=value", "key2=value2"]
        // iterate over the array
        for (var i=0; i<existing_params_array.length; i++){
            // find the param that starts with key
            if (existing_params_array[i].split("=")[0] == key){ // if ["key", "value"][0] == key
                var item = existing_params_array[i].split("=");
                // change the value item[0] is the key
                item[1] = value;
                // make a new string key=value
                var item_string  = item[0] + "=" + item[1];
                // now replace the new param
                existing_params = existing_params.replace(key+"="+get_param(key),item_string);
            }
        }
        window.history.replaceState(null, null, "?"+existing_params);
    }else{
        // otherwise add it to url
        window.history.replaceState(null, null, "?"+existing_params+"&"+new_param);
    }
}


function del_param(key){
    // check if the key exists
    var value = get_param(key);
    if (value){
        var query = window.location.search;
        query = query.replace(`${key}=${value}`, "");
        query = query.replace(/&&/g, "&");
        console.log("i am working");
        window.history.replaceState(null, null, query);
    }
}


// this function gets parameters from page url
// @param: key -> string
function get_param(key){
    // get all params
    var params = window.location.search;
    // remove ? with ""
    params = params.replace("?", "");
    // split them into an array -> ["key=value", "key2=value2"] with & seperator
    var args = params.split("&");
    // now find the value for key
    for (var i=0; i < args.length; i++){
        // [key|value] pairs
        var item = args[i].split("=");
        // if item starts with key
        if (item[0] == key){
            // then split them with "="(equal-sign) seperator and take the second part
            var value = item[1];
            // return the value of key
            return value;
        }
    }
    // if there was no value return false
    return false;
}


// clear all params
// this function accepts no arguments
function del_params(){
    window.history.replaceState(null, null, "/");
}

// used to create html elements with node interface
// for example to create a span tag
// @param: tag_name:str -> a string containing tag name |span, div, etc ...|
// @param: children:array -> array containing children
// @usage_example:
/**
 * create_node("div",
 *  [create_node("span"), create_node("h1", [create_text_node("hello")])]
 * )
 */
function create_node(tag_name, children=[], Class=null, Id=null){
    var node = document.createElement(tag_name);
    if (Class !== null) node.className = Class;
    if (Id !== null) node.id = Id;
    // iterates over children array and appends them to the node
    for (var c in children){
        child = children[c];
        node.appendChild(child);
    }
    return node;
}

// this can be used beside create_node function
// to create text nodes and append them to elements
// @param: text:str -> a string containing the text
function create_text_node(text){
    return document.createTextNode(text);
}


function check_if_contains(str, exp){
    exp = exp.split(";");
    for (var i in exp){
        var word = exp[i];
        if (str.includes(word)){
            return true;
        }
    }
    return false; 
}

function search_post(callback){
    query = $("#search").val()
    callApi(`/posts/search_for_post/?q=${ query }`, "GET", {}, data => {
        callback(data);
    });
}

function render_search_page(){
    console.log("invoked");
    var target = $("#search");
    if (!target.val()) return;
    render('search.html');
}

// document event oriented works
$(document).ready(function() {
    'use strict';

    // check if user wants a specific page with * render * parameter
    // @urlParam: 127.0.0.1:8000/?render=upload.html -> will render 127.0.0.1:8000/upload.html
    // if there is render in url parameters
    if (get_param("render")){
        //("entered the render parmeter if loop")
        // get the value. the value is address of a page (actually template name)
        var page = get_param("render");
        // render the page with render method
        render(page, false); // don't delete the url get arguments e.g -> ?render=render_post.html&id=5
    }else{
        // load the default page
        render("home.html");
    }
    // check the user authentication
    check_auth();

});