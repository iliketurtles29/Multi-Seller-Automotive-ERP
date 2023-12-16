

console.log("working fine");

$("#comment_form").submit(function(e){
e.preventDefault();

$.ajax({
    data: $(this).serialize(),

    method: $(this).attr("method"),

    url:$(this).attr("action"),

    dataType: "json",

    success: function(res){
        console.log("comment Saved to db");

        if(res.bool == true){
            $("#review-res").html("Review Added Successfully.")
            $(".hide-comment-form").hide()
            $(".add-review").hide()
        }
    }
})
})

$(document).ready(function(){
$(".add-to-cart-btn").on("click", function(){  

    let this_val = $(this)
    let index = this_val.attr("data-index")


    let quantity = $(".product-quantity-" + index).val()
    let product_title = $(".product-title-" + index).val()
    let product_id = $(".product-id-" + index).val()
    let product_price = $(".current-product-price-" + index).text()
    let product_pid = $(".product-pid-" + index).val()
    let product_image = $(".product-image-" + index).val()

    console.log("quantity ", quantity);
    console.log("title ", product_title);
    console.log("id ", product_id);
    console.log("pid ", product_pid);
    console.log("price ", product_price);
    console.log("image ", product_image);
    console.log("index ", index);
    console.log("current element ", this_val);

    $.ajax({
        url: '/add-to-cart',
        data: {
            'id': product_id,
            'pid': product_pid,
            'image': product_image,
            'qty': quantity,
            'title': product_title,
            'price': product_price,
        },
        dataType: 'json',   
        beforeSend: function(){
            console.log("adding....")
        },
        success: function(response){
            this_val.html("Added ✔") 
            console.log("added...")
            $(".cart-items-count").text(response.totalcartitems)
        }
    })
})

$(".delete-product").on("click", function(){
    let product_id = $(this).attr("data-product")
    let this_val = $(this)

    console.log("product id:", product_id);

    $.ajax({
        url: "/delete-from-cart",
        data: {
            "id": product_id
        },
        dataType: "json",
        beforeSend: function(){
            this_val.hide()

        },
        success: function(response){
            this_val.show()
            $(".cart-items-count").text(response.totalcartitems)
            $("#cart-list").html(response.data) 
            location.reload();
        },
        
    })
})


$(".update-product").on("click", function(){
    let product_id = $(this).attr("data-product")
    let this_val = $(this)
    let product_quantity = $(".product-qty-"+product_id).val()

    console.log("product id:", product_id);
    console.log("product qty:", product_quantity);

    $.ajax({
        url: "/update-cart",
        data: {
            "id": product_id,
            "qty": product_quantity
        },
        dataType: "json",
        beforeSend: function(){

        },
        success: function(response){
            this_val.show()
            $(".cart-items-count").text(response.totalcartitems)
            $("#cart-list").html(response.data) 
            location.reload();
        },
        
    })
})
$(document).on("click", ".make-default-address", function(){
    let id = $(this).attr("data-address-id")
    let this_val = $(this)

    console.log("ID is:", id);
    console.log("Element is:", this_val);

    $.ajax({
        url: "/make-default-address",
        data: {
            "id": id
        },
        dataType: "json",
        success: function(response){
            console.log("Address made to deault")
            if (response.boolean == true){
                $(".check").hide()
                $(".action_btn").show()

                $(".check"+id).show()
                $(".button"+id).hide()
            }
        }
    })
})


$(document).on("click", ".add-to-wishlist", function(){
    let product_id = $(this).attr("data-product-item")
    let this_val = $(this)

    console.log("prod id", product_id);

    $.ajax({
        url: "/add-to-wishlist",
        data: {
            "id": product_id
        },
        dataType: "json",
        beforeSend: function(){
            console.log("adding")
        },
        success: function(response){
            this_val.html("✔")
            if (response.bool === true){
                console.log("Added to wishlist");
                location.reload();
            }
        }
    })
})

$('#addReviewModal').on('show.bs.modal', function (event) {
    var modal = $(this);
    var csrfToken = "{{ csrf_token }}";
    modal.find('#comment_form input[name="csrfmiddlewaretoken"]').val(csrfToken);
});

$(document).on("click", ".delete-wishlist-product", function(){
    let wishlist_id = $(this).attr("data-wishlist-product")
    let this_val = $(this)

    console.log("wishlist", wishlist_id);

    $.ajax({
        url: "/remove-from-wishlist",
        data:{
            "id": wishlist_id,
        },
        dataType: "json",
        beforeSend: function(){
            console.log("deleteting..")
        }, 
        success: function(response){
            $("#wishlist_list").html(response.data)
            location.reload();
        }
    })
})


$(".filter-checkbox, #price-filter-btn").on("click", function(){
    console.log("clicked");

    let filter_object = {}
    
    let min_price = $("#max_price").attr("min")
    let max_price = $("#max_price").val()


    filter_object.min_price = min_price;
    filter_object.max_price = max_price;

    $(".filter-checkbox").each(function(){
        let filter_value = $(this).val()
        let filter_key = $(this).data("filter")

        console.log("filter value: ", filter_value );
        console.log("filter key: ", filter_key );

        filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key +']:checked')).map(function(element){
            return element.value
        })
    })
    console.log("Filter object:", filter_object );
    $.ajax({
        url: '/filter-products',
        data: filter_object,
        dataType: 'json',
        beforeSend: function(){
            console.log("sending data");
        },
        success: function(response){ 
            console.log(response);
            console.log("success");
            $("#filtered-product").html(response.data)
        }
    })
    $("#max_price").on("blur", function(){
        console.log("clicked");
        let min_price = $(this).attr("min")
        let max_price= $(this).attr("max")
        let current_price = $(this).val()

        console.log("current price is:", current_price);
        console.log("current:", min_price);
        console.log("current:", max_price);
    })  
})  
})
window.onload = function(){
    document.getElementById("download").addEventListener("click", () => {
        const invoice = document.getElementById("invoice"); // Get the invoice element
        var opt = {
            margin: 1,
            filename: 'invoice.pdf',
            image: { type: 'png', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
        };

        html2pdf().from(invoice).save();
    });
}    