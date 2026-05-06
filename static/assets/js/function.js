$(document).ready(function () {
    $('#post-form').submit(function (e) {
        e.preventDefault();

        let post_caption = $("#post-caption").val();
        let post_visibility = $("#visibility").val();

        var fileInput = $('#post-thumbnail')[0];
        var file = fileInput.files[0];
        if (!file) {
            alert("Please select an image");
            return;
        }
        var fileName = file.name;

        var formData = new FormData();
        formData.append('post-caption', post_caption);
        formData.append('visibility', post_visibility);
        formData.append('post-thumbnail', file, fileName);

        $.ajax({
            url: '/create-post/',


            type: 'POST',
            dataType: 'json',
            data: formData,
            processData: false,
            contentType: false,


            success: function (res) {
                console.log("Post Saved to DB...");
                console.log(res);

                let _html = `
            <div class="card lg:mx-0 uk-animation-slide-bottom-small mt-3 mb-3">

                <!-- Post Header -->
                <div class="flex justify-between items-center lg:p-4 p-2.5">
                    <div class="flex flex-1 items-center space-x-4">

                        <a href="#">
                            <img 
                                src="${res.post.profile_image}" 
                                style="width:40px; height:40px;"
                                class="bg-gray-200 border border-white rounded-full w-10 h-10"
                            />
                        </a>

                        <div class="flex-1 font-semibold capitalize">
                            <a href="#" class="text-black dark:text-gray-100">
                                ${res.post.full_name}
                            </a>

                            <div class="text-gray-700 flex items-center space-x-2">
                                <span>${res.post.date} ago</span>
                                <ion-icon name="time-outline"></ion-icon>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Post Caption -->
                <div class="p-5 pt-0 border-b dark:border-gray-700 pb-3">
                    ${res.post.title}
                </div>

                <!-- Post Image -->
                <div class="grid grid-cols-2 gap-2 px-5">
                    <a href="${res.post.image_url}" class="col-span-2">
                        <img 
                            src="${res.post.image_url}" 
                            style="width:100%; height:300px; object-fit:cover;"
                            class="rounded-md w-full"
                        />
                    </a>
                </div>

                <!-- Like / Comment -->
                <div class="p-4 space-y-3">

                    <div class="flex space-x-4 lg:font-bold">

                        <!-- Like -->
                        <a class="flex items-center space-x-2" style="cursor:pointer;">
                            <div 
                                class="p-2 rounded-full like-btn${res.post.id} text-black"
                                id="like-btn"
                                data-like-btn="${res.post.id}"
                            >
                                <i class="fas fa-thumbs-up"></i>
                            </div>
                            <div>Like</div>
                        </a>

                        <!-- Comment -->
                        <a class="flex items-center space-x-2">
                            <div class="p-2 rounded-full text-black">
                                <i class="fas fa-comment"></i>
                            </div>
                            <div>
                                <b>
                                    <span id="comment-count${res.post.id}">0</span>
                                </b>
                                Comment
                            </div>
                        </a>
                    </div>

                    <!-- Like Count -->
                    <div class="dark:text-gray-100">
                        <strong>
                            <span id="like-count${res.post.id}">0</span>
                        </strong>
                        Likes
                    </div>

                    <!-- Comment List -->
                    <div 
                        class="border-t py-4 space-y-4 dark:border-gray-600"
                        id="comment-div${res.post.id}">
                    </div>

                    <!-- Add Comment -->
                    <div class="bg-gray-100 rounded-full relative border-t">
                        <input
                            placeholder="Add your Comment..."
                            id="comment-input${res.post.id}"
                            data-comment-input="${res.post.id}"
                            class="bg-transparent max-h-10 shadow-none px-5 w-full"
                        />

                        <div class="absolute bottom-0 right-3 text-xl">
                            <a
                                style="cursor:pointer;"
                                id="comment-btn"
                                class="comment-btn${res.post.id}"
                                data-comment-btn="${res.post.id}"
                            >
                                <ion-icon 
                                    name="send-outline"
                                    class="hover:bg-gray-200 p-1.5 rounded-full">
                                </ion-icon>
                            </a>
                        </div>
                    </div>

                </div>
            </div>
            `;

                // Add new post at top instantly
                $("#post-list").prepend(_html);

                // Properly close modal
                UIkit.modal("#create-post-modal").hide();

                $("body").removeClass("uk-modal-page");
                $("html").css("overflow", "auto");
                $("body").css("overflow", "auto");

                $(".uk-modal").removeClass("uk-open");


                // Reset form
                $("#post-form")[0].reset();

                // Reset preview image
                $("#preview_post_thumbnail").attr(
                    "src",
                    "/static/images/no-image.jpg"
                );
            }
        });
    });
});

// Loading old into model
$(document).on("click", "#edit-post-btn", function () {

    let post_id = $(this).attr("data-post-id");

    $.ajax({
        url: "/get-post-data/",
        data: {
            "id": post_id
        },

        success: function (response) {
            $("#edit-post-id").val(response.id);
            $("#edit-post-caption").val(response.title);
            $("#edit-visibility").val(response.visibility);
            $("#edit_preview_post_thumbnail").attr("src", response.image_url);
            UIkit.modal("#edit-post-modal").show();
        }
    });

});


$("#edit-post-form").submit(function (e) {
    e.preventDefault();

    let formData = new FormData(this);

    $.ajax({
        url: "/edit-post/",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,

        success: function (response) {
            if (response.status === "success") {

                let postId = response.post.id;
                $("#post-title-" + postId).text(response.post.title);
                $("#post-image-" + postId).attr("src", response.post.image_url);
                $("#post-visibility-" + postId).text(
                    response.post.visibility
                );
                UIkit.modal("#edit-post-modal").hide();
                $("#edit-post-form")[0].reset();

                alert("Post updated successfully");
            } else {
                alert(response.message);
            }
        }
    });
});


$(document).on("click", ".delete-post-btn", function () {
    let post_id = $(this).attr("data-post-id");

    let confirmDelete = confirm("Do you want to delete this post?");

    if (confirmDelete) {
        $.ajax({
            url: "/delete-post/",
            data: {
                "id": post_id
            },

            success: function (response) {
                if (response.status === "success") {
                    $("#post-wrapper-" + post_id).remove();

                    alert(response.message);
                } else {
                    alert(response.message);
                }
            }
        });
    }
});


$(document).on("click", "#like-btn", function () {
    let btn_val = $(this).attr("data-like-btn")
    console.log(btn_val);

    $.ajax({
        url: "/like-post/",
        dataType: "json",
        data: {
            "id": btn_val
        },
        success: function (response) {
            if (response.data.bool === true) {
                console.log("Liked");
                console.log(response.data.likes);
                $("#like-count" + btn_val).text(response.data.likes)
                $(".like-btn" + btn_val).addClass("text-blue-500")
                $(".like-btn" + btn_val).removeClass("text-black")
            } else {
                console.log("Unliked");
                console.log(response.data.likes);
                $("#like-count" + btn_val).text(response.data.likes)
                $("#like-count" + btn_val).text(response.data.likes)
                $(".like-btn" + btn_val).addClass("text-black")
                $(".like-btn" + btn_val).removeClass("text-blue-500")

            }
            console.log(response.data.bool);
        }
    })
})



// Comment on post
$(document).on("click", "#comment-btn", function () {
    let id = $(this).attr("data-comment-btn")
    let comment = $("#comment-input" + id).val()

    console.log(id);
    console.log(comment);

    $.ajax({
        url: "/comment-post/",
        dataType: "json",
        data: {
            "id": id,
            "comment": comment,
        },
        success: function (res) {
            console.log(res)
            let newComment = '<div class="flex card shadow p-2" id="comment-div' + res.data.comment_id + '">\
                    <div class="w-10 h-10 rounded-full relative flex-shrink-0">\
                        <img src="' + res.data.profile_image + '" alt="" class="absolute h-full rounded-full w-full">\
                    </div>\
                    <div>\
                        <div class="text-gray-700 py-2 px-3 rounded-md bg-gray-100 relative lg:ml-5 ml-2 lg:mr-12 dark:bg-gray-800 dark:text-gray-100 flex items-center">\
                            <p class="leading-6 flex-grow">'+ res.data.comment + '</p>\
                                <button class="ml-auto text-xs ml-3 mr-3" id="delete-comment" data-delete-comment="'+ res.data.comment_id + '"> <i class="fas fa-trash text-red-500"></i> </button>\
                        </div>\
                        <div class="text-sm flex items-center space-x-3 mt-2 ml-5">\
                            <a id="like-comment-btn" data-like-comment="'+ res.data.comment_id + '" class="like-comment' + res.data.comment_id + ' text-red-500" style="color: gray;" > <i id="comment-icon' + res.data.comment_id + '" class=" fas fa-heart  "></i></a> <small><span class="" id="comment-likes-count' + res.data.comment_id + '">0</span></small>\
                            <details >\
                                <summary><div class="">Reply</div></summary>\
                                <details-menu role="menu" class="origin-topf-right relative right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">\
                                    <div class="pyf-1" role="none">\
                                        <div method="POST" class="p-1 d-flex" action="#" role="none">\
                                            <input type="text" class="with-border" name="" id="reply-input'+ res.data.comment_id + '">\
                                            <button id="reply-comment-btn" data-reply-comment-btn="'+ res.data.comment_id + '" class="block w-fulfl text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 reply-comment-btn' + res.data.comment_id + '" role="menuitem">\
                                            <ion-icon name="send"></ion-icon>\
                                        </button>\
                                        </div>\
                                    </div>\
                                </details-menu>\
                            </details>\
                            <span> <small>' + res.data.date + ' ago</small> </span>\
                        </div>\
                        <div class="reply-div'+ res.data.comment_id + '">\
                        </div>\
                    </div>\
                </div>\
            '
            $("#comment-div" + id).prepend(newComment);
            $("#comment-count" + id).text(res.data.comment_count);
            $("#comment-input" + id).val("")

            console.log(response.data.bool);
        }
    })
})

//   LIke Comment
$(document).on("click", "#like-comment-btn", function () {
    let id = $(this).attr("data-like-comment")
    console.log(id);

    $.ajax({
        url: "/like-comment/",
        dataType: "json",
        data: {
            "id": id
        },
        success: function (response) {
            console.log(response.data.bool);
            console.log(response.data.likes);

            if (response.data.bool === true) {

                $("#comment-likes-count" + id).text(response.data.likes)
                $(".like-comment" + id).css("color", "red")

            } else {
                console.log("Unliked");
                console.log(response.data.likes);
                $("#comment-likes-count" + id).text(response.data.likes)
                $('#comment-icon' + id).removeClass(' text-red-600 ');
                console.log($('.comment-icon' + id));
                $("#comment-likes-count" + id).removeClass(' text-red-600 ');
                $(".like-comment" + id).css("color", "gray")


            }
        }
    })
})


// Reply Comment
$(document).on("click", "#reply-comment-btn", function () {
    let id = $(this).attr("data-reply-comment-btn")
    let reply = $("#reply-input" + id).val()

    console.log(id);
    console.log(reply);

    $.ajax({
        url: "/reply-comment/",
        dataType: "json",
        data: {
            "id": id,
            "reply": reply,
        },
        success: function (res) {

            let newReply = ' <div class="flex mr-12 mb-2 mt-2" style="margin-right: 20px;">\
                <div class="w-10 h-10 rounded-full relative flex-shrink-0">\
                    <img src="'+ res.data.profile_image + '" style="width: 40px; height: 40px;" alt="" class="absolute h-full rounded-full w-full">\
                </div>\
                <div>\
                    <div class="text-gray-700 py-2 px-3 rounded-md bg-gray-100 relative lg:ml-5 ml-2 lg:mr-12 dark:bg-gray-800 dark:text-gray-100">\
                        <p class="leading-6">'+ res.data.reply + '</p>\
                        <div class="absolute w-3 h-3 top-3 -left-1 bg-gray-100 transform rotate-45 dark:bg-gray-800"></div>\
                    </div>\
                    <span> <small>'+ res.data.date + ' ago</small> </span>\
                    \
                </div>\
            </div>\
            '
            $(".reply-div" + id).prepend(newReply);
            $("#reply-input" + id).val("")

            console.log(res.data.bool);
        }
    })
})


$(document).on("click", "#delete-comment", function () {
    let id = $(this).attr("data-delete-comment")

    $.ajax({
        url: "/delete-comment/",
        dataType: "json",
        data: {
            "id": id
        },
        success: function (response) {
            $("#comment-div" + id).addClass("d-none")
        }
    })
})

// Add Freind
$(document).on("click", "#add-friend", function () {
    let id = $(this).attr("data-friend-id")
    console.log(id);

    $.ajax({
        url: "/add-friend/",
        dataType: "json",
        data: {
            "id": id
        },
        success: function (response) {
            console.log("Bool ==", response.bool);
            if (response.bool == true) {
                $("#friend-text").html("<i class='fas fa-user-minus'></i> Cancel Request ")
                $(".add-friend" + id).addClass("bg-red-600")
                $(".add-friend" + id).removeClass("bg-blue-600")
            }
            if (response.bool == false) {
                $("#friend-text").html("<i class='fas fa-user-plus'></i> Add Friend ")
                $(".add-friend" + id).addClass("bg-blue-600")
                $(".add-friend" + id).removeClass("bg-red-600")
            }
        }
    })
})


// Accept Friend Request
$(document).on("click", "#accept-friend-request", function () {
    let id = $(this).attr("data-request-id")
    console.log(id);

    $.ajax({
        url: "/accept-friend-request/",
        dataType: "json",
        data: {
            "id": id
        },
        success: function (response) {
            console.log(response.data);
            $(".reject-friend-request-hide" + id).hide()
            $(".accept-friend-request" + id).html("<i class='fas fa-check-circle'></i> Friend Request Accepted")
            $(".accept-friend-request" + id).addClass("text-white")
        }
    })
})

// Reject Friend Request
$(document).on("click", "#reject-friend-request", function () {
    let id = $(this).attr("data-request-id")
    console.log(id);

    $.ajax({
        url: "/reject-friend-request/",
        dataType: "json",
        data: {
            "id": id
        },
        success: function (response) {
            console.log(response.data);
            $(".accept-friend-request-hide" + id).hide()
            $(".reject-friend-request" + id).html("<i class='fas fa-check-circle'></i> Friend Request Rejected")
            $(".reject-friend-request" + id).addClass("text-white")
        }
    })
})

// UnFriend User
$(document).on("click", "#unfriend", function () {
    let id = $(this).attr("data-friend-id")
    console.log(id);

    $.ajax({
        url: "/unfriend/",
        dataType: "json",
        data: {
            "id": id
        },
        success: function (response) {
            console.log(response);
            $("#unfriend-text").html("<i class='fas fa-check-circle'></i> Friend Removed ")
            $(".unfriend" + id).addClass("bg-green-600")
            $(".unfriend" + id).removeClass("bg-red-600")
        }
    })
})


$(document).on("click", "#block-user-btn", function () {
    let id = $(this).attr("data-block-user")

    $.ajax({
        url: "/block-user/",
        dataType: "json",
        data: {
            "id": id
        },
        success: function (response) {
            console.log(response);
            $(".block-text" + id).html("<i class='fas fa-check-circle'></i> User Blocked Successfully. ")
        }
    })
})
