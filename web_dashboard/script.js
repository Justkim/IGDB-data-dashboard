const ctx = document.getElementById('chart').getContext('2d');
const ctx_pie = document.getElementById('pie-chart').getContext('2d');

fetch('../jsons/num_games_per_year.json')
.then ( response => {if (!response.ok)
{
    throw new Error("no file found");
}
return response.json()
})
.then(data =>
{
    console.log(Array.isArray(data))
    const labels = data.map(item => item.year);
    const gameCounts = data.map(item => item.num_games);
    const myChart = new Chart(ctx, 
    {
        type: 'bar',
        data: {
            labels : labels,
            datasets : [
                {
                    label: 'Number of games per year',
                    data: gameCounts,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgb(54, 235, 69)'

                }

            ]
        },
    }



);
}
)

fetch('../jsons/platforms_count.json')
.then ( response => {if (!response.ok)
{
    throw new Error("no file found");
}
return response.json()
})
.then(data =>
{
    console.log(Array.isArray(data))
    const labels = data.map(item => item.name);
    const platformCount = data.map(item => item.count);
    const myChart = new Chart(ctx_pie, 
    {
        type: 'pie',
        data: {
            labels : labels,
            datasets : [
                {
                    label: 'Platform Distribution',
                    data: platformCount,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgb(54, 235, 69)'

                }

            ]
        },
    }



);
}
)

async function getRecommendations()
{
    const text = document.getElementById("userInput").value;
    try
    {
        const response = await fetch('http://localhost:5001/recommend', {
            method:'POST',
            headers:
            {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text }),


        });
        const data = await response.json;
        if (response.ok)
        {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = 'WHAAAT?';

            console.log("got the data!")
        }
        else
        {
            document.getElementById('results').innerHTML = "error";
             console.log("got data!")
        }
    }
        catch (error)
        {
            document.getElementById('results').innerHTML = "Network error";
        }
    }
