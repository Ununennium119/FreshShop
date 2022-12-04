const base_url = "http://127.0.0.1:8000/";

(function ($) {
    "use strict";


    /* ..............................................
       Loader
       ................................................. */

    $(window).on('load', function () {
        $('.preloader').fadeOut();
        $('#preloader').delay(550).fadeOut('slow');
        $('body').delay(450).css({
            'overflow': 'visible'
        });
    });


    /* ..............................................
       Fixed Menu
       ................................................. */

    $(window).on('scroll', function () {
        if ($(window).scrollTop() > 50) {
            $('.main-header').addClass('fixed-menu');
        } else {
            $('.main-header').removeClass('fixed-menu');
        }
    });


    /* ..............................................
       Gallery
       ................................................. */

    $('#slides-shop').superslides({
        inherit_width_from: '.cover-slides',
        inherit_height_from: '.cover-slides',
        play: 5000,
        animation: 'fade',
    });

    $(".cover-slides ul li").append("<div class='overlay-background'></div>");


    /* ..............................................
       Special Menu
       ................................................. */

    let Container = $('.container');
    Container.imagesLoaded(function () {
        let portfolio = $('.special-menu');
        portfolio.on('click', 'button', function () {
            $(this).addClass('active').siblings().removeClass('active');
            let filterValue = $(this).attr('data-filter');
            $grid.isotope({
                filter: filterValue
            });
        });
        let $grid = $('.special-list').isotope({
            itemSelector: '.special-grid'
        });
    });


    /* ..............................................
       BaguetteBox
       ................................................. */

    baguetteBox.run('.tz-gallery', {
        animation: 'fadeIn',
        noScrollbars: true
    });


    /* ..............................................
       Offer Box
       ................................................. */

    $('.offer-box').inewsticker({
        speed: 3000,
        effect: 'fade',
        dir: 'ltr',
        font_size: 13,
        color: '#ffffff',
        font_family: 'Montserrat, sans-serif',
        delay_after: 1000
    });


    /* ..............................................
       Tooltip
       ................................................. */

    $(document).ready(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });


    /* ..............................................
       Owl Carousel Instagram Feed
       ................................................. */

    $('.main-instagram').owlCarousel({
        loop: true,
        margin: 0,
        dots: false,
        autoplay: true,
        autoplayTimeout: 3000,
        autoplayHoverPause: true,
        navText: ["<i class='fas fa-arrow-left'></i>", "<i class='fas fa-arrow-right'></i>"],
        responsive: {
            0: {
                items: 2,
                nav: true
            },
            600: {
                items: 3,
                nav: true
            },
            1000: {
                items: 5,
                nav: true,
                loop: true
            }
        }
    });


    /* ..............................................
       Featured Products
       ................................................. */

    $('.featured-products-box').owlCarousel({
        loop: true,
        margin: 15,
        dots: false,
        autoplay: true,
        autoplayTimeout: 3000,
        autoplayHoverPause: true,
        navText: ["<i class='fas fa-arrow-left'></i>", "<i class='fas fa-arrow-right'></i>"],
        responsive: {
            0: {
                items: 1,
                nav: true
            },
            600: {
                items: 3,
                nav: true
            },
            1000: {
                items: 4,
                nav: true,
                loop: true
            }
        }
    });


    /* ..............................................
       Scroll
       ................................................. */

    $(document).ready(function () {
        $(window).on('scroll', function () {
            if ($(this).scrollTop() > 100) {
                $('#back-to-top').fadeIn();
            } else {
                $('#back-to-top').fadeOut();
            }
        });
        $('#back-to-top').click(function () {
            $("html, body").animate({
                scrollTop: 0
            }, 600);
            return false;
        });
    });


    /* ..............................................
       NiceScroll
       ................................................. */

    $(".brand-box").niceScroll({
        cursorcolor: "#9b9b9c",
    });


    /* ..............................................
       Filter Form
       ................................................. */

    $(function () {
        let start_price = $("#start_price")
        let end_price = $("#end_price")
        let slider_range = $("#slider-range")
        slider_range.slider({
            range: true,
            min: 0,
            max: 100,
            values: [start_price.val(), end_price.val()],
            slide: function (event, ui) {
                $("#amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
                $("#start_price").val(ui.values[0]);
                $("#end_price").val(ui.values[1]);
            }
        });
        $("#amount").val("$" + slider_range.slider("values", 0) + " - $" + slider_range.slider("values", 1));
        start_price.val(slider_range.slider("values", 0));
        end_price.val(slider_range.slider("values", 1));
    });

    $(function () {
        let search_input = $("#search_input")
        $("#search_query").val(search_input.val());
        search_input.change(function () {
            $("#search_query").val($("#search_input").val());
        });
    });

    $(document).ready(function () {
        $("#search_input").change(function () {
            $("#search_query").val($("#search_input").val());
        });
    });

    $(document).ready(function () {
        $("#price-slider-btn").click(function () {
            $("#filter_form").submit();
        });
    });

    $(document).ready(function () {
        let sort_select = $("#sort-select");
        sort_select.val($("#sort").val());
        sort_select.on("change", function () {
            $("#sort").val($(this).val())
        });
    });

    $(document).ready(function () {
        $(".alert__close").each(function () {
            $(this).click(function (e) {
                closeMessage(e.target);
            })
        });
        $(".alert").each(function () {
                setTimeout(() => {
                    if ($(this)) {
                        $(this).remove();
                    }
                }, 5000)
            }
        );
    });
}(jQuery));


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// JavaScript wrapper function to send HTTP requests using Django's "X-CSRFToken" request header
function sendHttpAsync(path, method, body) {
    let props = {
        method: method,
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        mode: "same-origin",
    }

    if (body !== null && body !== undefined) {
        props.body = JSON.stringify(body);
    }

    return fetch(path, props)
        .then(response => {
            return response.json()
                .then(result => {
                    return {
                        ok: response.ok,
                        body: result
                    }
                });
        })
        .then(resultObj => {
            return resultObj;
        })
        .catch(error => {
            throw error;
        });
}

function closeMessage(closeBtn) {
    closeBtn.parentElement.remove();
}

function showMessage(messageText, messageTag) {
    let message = document.createElement("div");
    message.innerHTML = `<div class="alert alert--${messageTag}">
                            <p class="alert__message">${messageText}</p>
                            <button onclick="closeMessage(this)" class="alert__close">⨯</button>
                        </div>`;
    $("#messages-container").prepend(message);
    setTimeout(() => {
        if (message) {
            message.remove();
        }
    }, 5000);
}


function fillCategory(category) {
    $("#category").val(category);
    $("#filter_form").submit();
}

function fillSearch() {
    $("#search_query").val($("#search_input").val());
    $("#filter_form").submit();
}

function fillPage(pageNumber) {
    $("#page").val(pageNumber);
    $("#filter_form").submit();
}


function removeOrderItem(orderItemId) {
    sendHttpAsync(base_url + "orders/remove-order-item/" + orderItemId, "DELETE", "")
        .then(response => {
            if (response.body.status === "success") {
                let orderItem = $("#order-item-" + orderItemId);
                orderItem.remove();
                showMessage("Product removed from your cart!", "success");
            } else if (response.body.status === "failed") {
                showMessage("Failed to remove product from your cart!", "error");
            }
        });
}

function updateOrderItems() {
    let counts = [];
    let body = {
        order_items_counts: counts
    };

    $(".count-input").each(function () {
        counts.push({
            id: $(this).data("order-item-id"),
            count: $(this).val()
        });
    });

    sendHttpAsync(base_url + "orders/update-order-items-count/", "POST", body)
        .then(response => {
            console.log(response)
            if (response.body.status === "success") {
                location.replace(base_url + "orders/cart/");
            } else if (response.body.status === "failed") {
                showMessage("Failed to update quantities!", "error");
            }
        });
}

function applyCoupon() {
    let coupon_code = $("#coupon-input").val();
    let body = {
        coupon_code: coupon_code
    };

    sendHttpAsync(base_url + "orders/apply-coupon/", "POST", body)
        .then(response => {
            let body = response.body
            let status = body.status
            if (status === "success") {
                location.replace(base_url + "orders/cart/");
            } else if (status === "failed") {
                showMessage(body.message, "error");
            }
        });
}


function addProductToCart(productId) {
    let quantityInput = $("#quantity-input")
    let quantity = 1;
    if (quantityInput.length > 0) {
        quantity = quantityInput.val()
    }
    let body = {
        productId: productId,
        quantity: quantity
    };

    sendHttpAsync(base_url + "orders/add-product-to-cart/", "POST", body)
        .then(response => {
            let body = response.body;
            let status = body.status;
            if (status === "success") {
                showMessage(body.message, "success");
            } else if (status === "failed") {
                showMessage(body.message, "error");
            } else if (status === "login") {
                window.location.href = body.login_path + "?next=" + window.location.pathname
            }
        });
}


function submitReview(productId) {
    let reviewInput = $("#review-input");
    if (reviewInput.length < 1) {
        return;
    }

    let body = {
        productId: productId,
        review: reviewInput.val()
    };

    sendHttpAsync(base_url + "products/submit-review/", "POST", body)
        .then(response => {
            let body = response.body;
            let status = body.status;
            if (status === "success") {
                showMessage(body.message, "success");
                let review = body.review;
                let reviewsContainer = $("#reviews-container");
                let reviewElement = `<div class="media mb-3">
                                        <div class="mr-2">
                                            <img class="rounded-circle border p-1" 
                                                src="/static/images/${review.image}" alt="User Image">
                                        </div>
                                        <div class="media-body">
                                            <p>${review.content}</p>
                                            <small class="text-muted">
                                                Posted by ${review.username} on ${review.create_time}
                                            </small>
                                        </div>
                                    </div>
                                    <hr>`;

                reviewsContainer.prepend(reviewElement);
                $([document.documentElement, document.body]).animate({
                    scrollTop: reviewsContainer.offset().top - 250
                }, 1000);
                reviewInput.val("")
            } else if (status === "failed") {
                showMessage(body.message, "error");
            }
        });
}


function removeWishlistItem(wishlistItemId) {
    sendHttpAsync(base_url + "users/remove-wishlist-item/" + wishlistItemId, "DELETE", "")
        .then(response => {
            if (response.body.status === "success") {
                let wishlistItem = $("#wishlist-item-" + wishlistItemId);
                wishlistItem.remove();
                showMessage("Product removed from your wishlist!", "success");
            } else if (response.body.status === "failed") {
                showMessage("Failed to remove product from your wishlist!", "error");
            }
        });
}

function addProductToWishlist(productId) {
    let body = {
        productId: productId
    };

    sendHttpAsync(base_url + "users/add-product-to-wishlist/", "POST", body)
        .then(response => {
            let body = response.body;
            let status = body.status;
            if (status === "success") {
                showMessage(body.message, "success");
            } else if (status === "failed") {
                showMessage(body.message, "error");
            } else if (status === "login") {
                window.location.href = body.login_path + "?next=" + window.location.pathname
            }
        });
}
