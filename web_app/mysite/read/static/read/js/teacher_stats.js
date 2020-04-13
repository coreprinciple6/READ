function graph(ctx, labels, data, x_axis_label, title){
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: title,
                data: data,
                backgroundColor: [
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
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Time in Seconds'
                    },
                    ticks: {
                        beginAtZero: true
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: x_axis_label
                    },
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function showStudentGraph(){
    var ctx = document.getElementById('studentChart').getContext('2d');
    graph(ctx, student_labels, student_time_data, 'Student Username', 'Total Time Spent On All Documents By Each Student');
}

function showDocumentGraph(){
    var ctx = document.getElementById('docChart').getContext('2d');
    graph(ctx, doc_labels, doc_time_data, 'Document Name', 'Total Time Spent On Each Document By All Students');
}

showStudentGraph();
showDocumentGraph();
