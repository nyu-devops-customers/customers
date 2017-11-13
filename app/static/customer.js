$(function () {

    // create customer 

    $("#create-btn").click(function () {

        var firstName = $(this).parent().find("#create_first_name").val();
        var lastName = $(this).parent().find("#create_last_name").val();

        var data = {
            "firstname": firstName,
            "lastname": lastName
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType:"application/json;charset=UTF-8",
            data: JSON.stringify(data),
        });
        ajax.done(function(res){
            var id = res.id;
            var fn = res.firstname;
            var ln = res.lastname;

            $("#create_result_id").empty();
            $("#create_result_name").empty();
            $("#create_result_id").append(id);
            $("#create_result_name").append(fn +" " +  ln);

        });
        ajax.fail(function(res){

            $("#create_result_id").empty();
            $("#create_result_name").empty();
            $("#create_result_id").append("server error!");
        });

    });


    // update customer id

    $("#update-btn").click(function () {

        var customer_id = $(this).parent().find("#update_id").val();
        var firstName = $(this).parent().find("#update_first_name").val();
        var lastName = $(this).parent().find("#update_last_name").val();

        var data = {
            "customer_id": customer_id,
            "firstname": firstName,
            "lastname" : lastName
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + customer_id,
                contentType:"application/json;charset=UTF-8",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            var id = res.id;
            var fn = res.firstname;
            var ln = res.lastname;

            $("#update_result_id").empty();
            $("#update_result_name").empty();
            $("#update_result_id").append(id);
            $("#update_result_name").append(fn +" " +  ln);

        });
        ajax.fail(function(res){

            $("#update_result_id").empty();
            $("#update_result_name").empty();
            $("#update_result_id").append("user id does not exist");
        });
    });

    // retrive customer information

    $("#retrive-btn").click(function () {

        var customer_id = $("#retrive_id").val();
        var data = {
            "customer_id": customer_id
        };

        var ajax = $.ajax({
            type: "GET",
            url: "/customers/" + customer_id,
            contentType:"application/json;charset=UTF-8",
            data: JSON.stringify(data)
        })
        ajax.done(function(res){
            var id = res.id;
            var fn = res.firstname;
            var ln = res.lastname;

            $("#retrive_result_id").empty();
            $("#retrive_result_name").empty();
            $("#retrive_result_id").append(id);
            $("#retrive_result_name").append(fn +" " +  ln);

        });
        ajax.fail(function(res){

            $("#retrive_result_id").empty();
            $("#retrive_result_name").empty();
            $("#retrive_result_id").append("user id does not exist!");
        });
    });

    // delete a customer

    $("#delete-btn").click(function () {

        var customer_id = $("#delete_id").val();
        var data = {
            "customer_id": customer_id
        };

        var ajax = $.ajax({
            type: "DELETE",
            url: "/customers/" + customer_id,
            contentType:"application/json;charset=UTF-8",
            data: JSON.stringify(data),
        })

        ajax.done(function(res){

            $("#delete_result").empty();
            $("#delete_result").append("Deleted!");

        });
        ajax.fail(function(res){

            $("#delete_result").empty();
            $("#delete_result").append("server error!");
        });
    });


})
