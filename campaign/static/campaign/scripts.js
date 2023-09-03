const modal = document.getElementById("modal")
    const donate_modal = document.getElementById("donate_modal")
    
    const donate_ok = document.getElementById("donate_ok")
    // const delete_event_ok = document.getElementById("delete_event_ok")
    // const delete_event = document.getElementById("delete_event")
    // const donate_form = document.getElementById("donation_form")

    let open_delet_model = (e) => {
        if (modal.classList.contains("hidden")) {
            modal.classList.remove("hidden")
            modal.classList.add("block")
        }
    }

    let donate_form = () => {
        event.preventDefault()
        if($("#id_amount").val() === "" || $("#id_amount").val() < 10)
        {
            alert("The amount you want to donate should be greater than R10!")
        }else{
            if (donate_modal.classList.contains("hidden")) {
                donate_modal.classList.remove("hidden")
                donate_modal.classList.add("block")
            }
        }
        
    }
    
    function close_modal(){
        if (modal.classList.contains("block")) {
            modal.classList.remove("block")
            modal.classList.add("hidden")
        }
    }
    function close__donatemodal(){
        if (donate_modal.classList.contains("block")) {
            donate_modal.classList.remove("block")
            donate_modal.classList.add("hidden")
        }
    }

    const delete_campaign_i = () => {
        event.preventDefault()
        $.ajax({
            type: "POST",
            beforeSend: function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
                $("#inner_model").empty()
                $("#inner_model").html(
                    `<div id="inner_model_child_2" class="space-y-3 text-center font-sans">
                    <h6 class="text-black text-2xl font-bold">deleting...</h6>
                    <i class="fa-solid fa-spinner fa-spin text-8xl text-custom-primary"></i>
                </div>
                `
                )
            },
            url: $("#inner_model").attr("data-href"),
            data: {

            },
            contentType: 'application/json; charset=utf-8',
            cache: false,
            success: function (data) {
                $("#inner_model").empty();
                if (data.success) {
                    
                    $("#inner_model").html(
                    `<div id="inner_model_child" class="space-y-3 text-center font-sans">
                        <h6 class="text-black text-2xl font-bold">Deleted!!</h6>
            
                        <i class="fa-solid fa-check fa-bounce text-red-500 text-5xl"></i>
                        <p class="text-gray-500 text-base font-normal">
                            ${data.message}
                        </p>
                        <p class="text-gray-500 text-base font-normal">
                            redirect in 3 seconds
                        </p>
                    </div>
                    =
                    `
                );
                window.setTimeout(() => {
                    window.location.href = data.url
                }, 3000)
                } else {
                    $("#inner_model").html(
                        `<div id="inner_model_child" class="space-y-3 text-center font-sans">
                            <h6 class="text-black text-2xl font-bold">Delete failed!!</h6>
                
                            <i class="fa-solid fa-trash fa-shake text-red-500 text-5xl"></i>
                            <p class="text-gray-500 text-base font-normal">
                                ${data.message}
                            </p>
                        </div>
                        <div onclick="close_modal()" class="absolute right-4 top-4 w-8 h-8 flex items-center justify-center">
                            <p class="text-gray-600 text-base font-bold">X</p>
                        </div>
                    `
                )
                }
                },
            error: function (error) {
                $("#inner_model").empty();
                $("#inner_model").html(
                    `<div id="inner_model_child" class="space-y-3 text-center font-sans">
                        <h6 class="text-black text-2xl font-bold">Error on our side</h6>
            
                        <i class="fa-solid fa-trash fa-shake text-red-500 text-5xl"></i>
                        <p class="text-gray-500 text-base font-normal">
                            ${error.statusText}
                        </p>
                        <p class="text-gray-500 text-base font-normal">
                            Okay, we did this. Will fix it!
                        </p>
                    </div>
                    
                    `
                );
                window.setTimeout(() => {
                    window.location.href = data.url
                }, 1000)
            },
            complete : function(){
                
            }
        })
    }

    function donate(){
        event.preventDefault()
        $.ajax({
            type: "POST",
            beforeSend: function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
                $("#inner_donatemodel").empty()
                $("#inner_donatemodel").html(
                    `<div id="inner_donatemodel_child" class="space-y-3 text-center font-sans">
                    <h6 class="text-black text-2xl font-bold">donating...</h6>
                    <i class="fa-solid fa-spinner fa-spin text-8xl text-custom-primary"></i>
                </div>
                `
                )
            },
            url: $("#inner_donatemodel").attr("data-href"),
            data: {
                id: $(this).data("id"),
                amount_donated: $("#id_amount").val(),
            },
            dataType: "json",
            cache: false,
            success: function (data) {
                $("#inner_donatemodel").empty();
                if (data.success) {
                    
                    $("#inner_donatemodel").html(
                    `<div id="inner_donatemodel_child" class="space-y-3 text-center font-sans">
                        <h6 class="text-black text-2xl font-bold">Donated!!</h6>
            
                        <i class="fa-solid fa-check fa-bounce text-red-500 text-5xl"></i>
                        <p class="text-gray-500 text-base font-normal">
                            ${data.message}
                        </p>
                        <p class="text-gray-500 text-base font-normal">
                            redirect to checkout in 3 seconds
                        </p>
                    </div>
                    
                    `
                );
                window.setTimeout(() => {
                    window.location.href = data.url
                }, 3000)
                } else {
                    $("#inner_donatemodel").html(
                        `<div id="inner_donatemodel_child" class="space-y-3 text-center font-sans">
                            <h6 class="text-black text-2xl font-bold">Delete failed!!</h6>
                
                            <i class="fa-solid fa-trash fa-shake text-red-500 text-5xl"></i>
                            <p class="text-gray-500 text-base font-normal">
                                ${data.message}
                            </p>
                        </div>
                        <div onclick="close__donatemodal()" class="absolute right-4 top-4 w-8 h-8 flex items-center justify-center">
                            <p class="text-gray-600 text-base font-bold">X</p>
                        </div>
                    `
                );
                window.setTimeout(() => {
                    window.location.href = $("#campaign_container").attr("data-url")
                }, 1000)
                }
                },
            error: function (error) {
                $("#inner_donatemodel").empty();
                $("#inner_donatemodel").html(
                    `<div id="inner_donatemodel_child" class="space-y-3 text-center font-sans">
                        <h6 class="text-black text-2xl font-bold">Error on our side</h6>
            
                        <i class="fa-solid fa-trash fa-shake text-red-500 text-5xl"></i>
                        <p class="text-gray-500 text-base font-normal">
                            ${error.statusText}
                        </p>
                        <p class="text-gray-500 text-base font-normal">
                            Okay, we did this. Will fix it!
                        </p>
                    </div>
                    
                    `
                );
                window.setTimeout(() => {
                    window.location.href = $("#campaign_container").attr("data-url")
                }, 1000)
            },
            complete : function(){
                
            }
        })
    }
