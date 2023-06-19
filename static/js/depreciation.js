
const renderChart = (data, labels) =>{
    var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Depreciation',
            data: data,
            backgroundColor: [
                // 'rgba(1, 184, 170, 1)',
                'rgba(55, 70, 73, 1)',
                'rgba(253, 98, 94, 1)',
                'rgba(242, 200, 15, 1)',
                'rgba(95, 107, 109, 1)',
                'rgba(138, 212, 235, 1)',
                'rgba(254, 150, 102, 1)',
                'rgba(166, 105, 153, 1)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
                
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        title:{
            display:true,
            text: 'Asset Depriciation',
        }
    }
});
    
}

const getChartData=()=>{
    console.log("fetching");
    fetch('/depreciation_stats')
    .then((res) => res.json()).then((results) =>{

        console.log("results",results);

        const assetTypeData = results.myDict;

        const [labels, data] =[
            Object.keys(assetTypeData),
            Object.values(assetTypeData )
        
        ];

        renderChart(data,labels);
    }
    );

};

document.onload = getChartData();