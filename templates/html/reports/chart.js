"var chart1;
chart1 = new Highcharts.Chart({

chart: {
  renderTo: '{{container}}',
  defaultSeriesType: '{{type}}'
},

{% if title %}
title: {
  text: '{{title}}'
},

xAxis: {
  categories: [

  {% for cat in categories %}
  '{{cat}}'
  {% if not loop.cycle.last() %},{% endif %}
  {% endfor %}

  ]
},

yAxis: {
  title: {
     text: '{{ytitle}}'
  }
},

series: [{

 {% for s in series %}
  {
  name: '{{s.name}}',
  data: [
  {% for d in s.data %}
  {{d}}
  {% if not loop.cycle.last() %},{% endif %}
  {% endfor %}
  ]
  }, 

]

credits: {
    enabled: false
}

});"