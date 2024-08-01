$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 4,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];

    $.ajax({
        type: "GET",
        url: "/pluscart/",  // Ensure this URL matches your Django URL configuration
        data: {
            prod_id: id
        },
        success: function(data) {
            if (data.quantity >= 1) {
                eml.innerText = data.quantity;
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX error:", status, error);
            // Optionally, display an error message to the user
            alert("An error occurred. Please try again.");
        }
    });
});

$('.minus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    console.log("pid =", id);

    $.ajax({
        type: "GET",
        url: "/minuscart/",  // Ensure this URL matches your Django URL configuration
        data: {
            prod_id: id
        },
        success: function(data) {
            console.log("data =", data);
            if (data.quantity >= 1) {
                eml.innerText = data.quantity;
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX error:", status, error);
            // Optionally, display an error message to the user
            alert("An error occurred. Please try again.");
        }
    });
});



$('.remove-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var row = this.parentNode.parentNode;

    $.ajax({
        type: "GET",
        url: "/removecart/",  // Ensure this URL matches your Django URL configuration
        data: {
            prod_id: id
        },
        success: function(data) {
            row.remove();
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        },
        error: function(xhr, status, error) {
            console.error("AJAX error:", status, error);
            // Optionally, display an error message to the user
            alert("An error occurred. Please try again.");
        }
    });
});


$('.plus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/pluswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            //alert(data.message)
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})


$('.minus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/minuswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})