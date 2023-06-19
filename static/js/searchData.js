
$(document).ready(function(){
    $('#searchHere').change(function(e){


        
    const searchHere =  document.querySelector("#searchHere");
    const tableOutput =  document.querySelector(".table-output");
    const originalTable =  document.querySelector(".original-table");
    const paginate =  document.querySelector(".pagination-container");
    const tbody = document.querySelector(".table-body");

    tableOutput.style.display = "none";
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0 ){

        paginate.style.display = "none";
        tbody.innerHTML = "";
        console.log("searchValue", searchValue);


        fetch("/search",{
            body: JSON.stringify({searchText : searchValue}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => { 
                console.log("data", data);
                
                originalTable.style.display = "none";
                
                tableOutput.style.display = "block";
               

                if(data.length === 0){

                    tableOutput.innerHTML = "No results found";

                }
                else{
                    
                    data.forEach((element) => {
                        tbody.innerHTML += `<tr>
                        <td><a href="/detail/${element.Ast_Tag_nbr}">${element.Ast_Tag_nbr}</a></td>
                        <td>${element.Serial_No}</td>
                        <td>${element.Model_No}</td>
                        <td>${element.Location}</td>
                        <td>${element.Asset_Type}</td>
                        <td>${element.Asset_Condition}</td>
                        <td>${element.Availability}</td>
                        <td>${element.PurchaseDate}</td>
                        <td>${element.Item_Cost_UGX}</td>
                        <td>${element.Item_Cost_USD}</td>
                        <td>${element.Project}</td>
                        <td>${element.Project_Name}</td>
                        <td><a class="btn-success btn-sm" href="/edit-item/${element.Ast_Tag_nbr}">Edit</a></td>
                        <td><a class="btn-success btn-sm" href="/assign/${element.Ast_Tag_nbr}">Assign</a></td>
                        <td><a class="btn-danger btn-sm" href="/deleteitem/${element.Ast_Tag_nbr}">Delete</a></td>              
                        </tr>`;
                    });

                          
                }
        });
    }
    else{
        tableOutput.style.display = "none";
        originalTable.style.display = "block";
        paginate.style.display = "block";
    }
    });
});

