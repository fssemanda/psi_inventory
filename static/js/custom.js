const renderOtherChart = (data1,data2, data3, labels) =>{
    var ctx = document.getElementById('myChart2').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [
            {
            label: 'Over One Year',
            data: data1,
            backgroundColor: [
                'rgba(1, 184, 170, 1)',
                'rgba(1, 184, 170, 1)',

            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
            ],
            borderWidth: 1
        },{
            label: 'Over Three Years',
            data: data2,
            backgroundColor: [
                'rgba(253, 98, 94, 1)',
                'rgba(253, 98, 94, 1)',
                'rgba(253, 98, 94, 1)',

            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',

            ],
            borderWidth: 1

        },{
            label: 'Over Five Years',
            data: data3,
            backgroundColor: [
                'rgba(242, 200, 15, 1)',
                'rgba(242, 200, 15, 1)',
                'rgba(242, 200, 15, 1)',

            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',

            ],
            borderWidth: 1

        }]
    },
    options: {
        title:{
            display:true,
            text: 'Laptops Aging Report',
        }
    }
});

}
const fetchData=()=>{
    console.log("fetching");
    fetch('/aging')
    .then((res) => res.json()).then((results) =>{

        console.log("results",results);

//        const labels = ['Less the One Year','Between 1-3 Years','Above 5 Years'];
        const Dataset1 = results.data1;
        const Dataset2 = results.data2;
        const Dataset3 = results.data3;

        // const [labels, data] =[
        //     Object.keys(Department),
        //     Object.values(Department)

        // ];
        // console.log(labels)
        const [labels, data1] =[
            Object. keys(Dataset2),
            Object.values(Dataset2 )

        ];

        renderOtherChart(data1, labels);
    }
    );

};

document.onload = fetchData();

