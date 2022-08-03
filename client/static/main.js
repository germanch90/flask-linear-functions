//const domain = window.location.host
const api_version = "/api_v1/"
//const base_url = domain + api_version

function clearValue(el) {
    return el.value = "";
}



let cache = {};
const request = (endpoint, params, method) =>  {
    const url = api_version + endpoint
    console.log(url)
    // Quick return from cache.
    let cacheKey = JSON.stringify( { url, params, method } );
    if ( cache[ cacheKey ] ) {
        return cache[ cacheKey ];
    }

    let options = {
        method
    };
    if ( 'GET' === method ) {
        url += '?' + ( new URLSearchParams( params ) ).toString();
    } else {
        options.body = JSON.stringify( params );
        options.headers = {'Content-Type': 'application/json;charset=utf-8'};
    }

    const result = fetch( url, options )
    .then(response => {
        if(response.ok){
            return response.json()
        } else{
            alert("Server returned " + response.status + " : " + response.statusText);
        }
    })
    .catch(err => {
        console.log(err);
    });

    cache[ cacheKey ] = result;

    return result;
};

const get = ( url, params ) => request( url, params, 'GET' );
const post = ( url, params ) => request( url, params, 'POST' );

const vm = new Vue({
    el: '#vm',
    delimiters: ['[[', ']]'],
    data: {
        result: "",
        elementIds: ["function-name", "X1",  "Y1",  "X2",  "Y2"],
        linear_functions: []
    },
    methods:{
        getElements: function () {
            return this.elementIds.map(item => document.getElementById(item));
        },
        addFunction: function () {
            let container = document.getElementById("data");
            let obj = {}
            this.getElements().forEach((item, index, array) => {
                let value = null;
                if (item.type == "number") {
                    value = parseInt(item.value)
                } else {
                    value = item.value
                }
                obj[item.id] = value;
            });
            post('linear/points', obj)
                .then( response => {
                    this.linear_functions.push(
                        {
                            ...response,
                            ...obj
                        }
                    );
                    console.log(this.linear_functions)
                    let linearFuncElement = document.createElement('p');
                    let text = document.createTextNode(response.equation);
                    linearFuncElement.appendChild(text);
                    container.appendChild(linearFuncElement);
                    this.graphAll();
                });
        },
        clearInputs: function () {
            this.getElements().forEach( (item) => {
                clearValue(item);
            });
        },
        graphFunction: function (item) {
            post('linear/single/graph', item)
                .then( response => {
                    console.log(response);
                    Plotly.newPlot( 'graphic', response, {});
                })
        },
        graphAll: function () {
            post('linear/multiple/graph', this.linear_functions)
                .then( response => {
                    console.log(response);
                    Plotly.newPlot( 'graphic', response, {});
                })
        }
   }
});

//post('linear/multiple/graph', this.linear_functions)
//                .then( response => {
//                    console.log(response);
//                    var config = {responsive: true}
//                    Plotly.newPlot( 'graphic', response, {}, config);
//                })