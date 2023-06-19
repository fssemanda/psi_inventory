
$(document).ready(function(){
    $('.halloha').click( function(){
        var $this = $(this);
        let td_val = $this.parents(".lower-table").find('td').eq(0).text();
        // var pk = document.getElementById('').value
        console.log(td_val)
        const myoutput = document.querySelector('.mytable-output')
            $.ajax({
                // url: '{% url "accept_asset" %}',
                url: '/accept_asset',
                type: 'GET',
                data: {'pk':td_val},
                dataType: 'JSON',
                success: function(data){
                    
                    console.log("data", data)

                    if(data.length === 0){

                    myoutput.innerHTML = "No results found";

                    }
                    else{
                        // $('.mytable-output').empty();
                        data.forEach((element) => {
                            myoutput.innerHTML += `<tr>
                    <td>${element.Ast_Tag}</td>
                    <td>${element.AstNo}</td>
                    <td>${element.Model_No}</td>
                    <td>${element.Serial_No}</td>
                    <td>${element.Asset_Type}</td>
                    <td>${element.Asset_Condition}</td>
                    
                                
                    </tr>`;
                });

                alert("User Accepted Device. See Respective Asset Manager to Receive Asset");
                    }
                }

            });
    

});

// Use Get method to send PK of device we wish to handover periof

$('#Checkme').click( function(){
    var $this = $(this);
    let td_val = $this.parents(".record2").find('td').eq(2).text();
    var dpbox = document.querySelector('#dp_view_box')
    // var pk = document.querySelector('.Checkme').value
    console.log(td_val)
    const myoutput = document.querySelector('.mytable-output')
        $.ajax({
            // url: '{% url "accept_asset" %}',
            url: '/handover',
            type: 'POST',
            data: {'pk':td_val},
            dataType: 'JSON',
            success: function(data){
                
                console.log("data", data)

                if(data.length === 0){

                myoutput.innerHTML = "No results found";

                }
                else{
                    // $('.mytable-output').empty();
                    data.forEach((element) => {
                        myoutput.innerHTML += `<tr>
                <td>${element.Ast_Tag}</td>
                <td>${element.AstNo}</td>
                <td>${element.Model_No}</td>
                <td>${element.Serial_No}</td>
                <td>${element.Asset_Type}</td>
                <td>${element.Asset_Condition}</td>
                
                            
                </tr>`;
            });

            alert("Device Handed over. Wait for confirmation from IT");
                }
            }

        });


});



});

