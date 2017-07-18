import * as d3 from 'd3';
import './style.css';

export default function renderChart(data,containerid) {
  if(!data) return;
  function withLevels(arr,n) {
    if(!arr) return arr
    return arr.map(d => {return {...d,level:n,children:withLevels(d.children,n+1)}})
  }
  function sum(arr) {
    let res = 0
    for(let val of arr) {
      res += val 
    }
    return res
  }
  //preprocess
  const preprocessed_data = withLevels(data,0)


  d3.select('svg').remove();
  d3.select('#'+ containerid).append('svg').attr('width','100%').attr('height',500).attr('preserveAspectRatio','xMidYMid meet').attr('viewBox','0 0 500 500')
  let svg = d3.select('svg').style('display','block').style('margin','auto')

  const g = svg.append('g').attr('transform','translate(200,250) scale(2.5,2.5)')

  const pie = d3.pie().value(d => d.seconds_spent).padAngle(0.03)
  const first_level_slices = pie(preprocessed_data)
  let slices = first_level_slices
  for (let i = 0;i < slices.length;i++ ){
    const s = slices[i]
    if(s.data.children) {
      const endAngle = s.startAngle + (s.endAngle - s.startAngle) * (sum(s.data.children.map(x => x.seconds_spent))/s.data.seconds_spent)
      slices = slices.concat(d3.pie().value(d => d.seconds_spent).startAngle(s.startAngle).endAngle(endAngle).padAngle(0.005)(s.data.children))
    }
  }


  const color = d3.scaleOrdinal(d3.schemeCategory10)
  const ttdiv = d3.select('body').append('div').attr('id','tooltip').style('opacity',0)

  g
    .selectAll('path.slice').data(slices).enter().append('path')
    .attr('class','slice')
    .attr('d',(d,i) => d3.arc().innerRadius(20 + 20 * d.data.level).outerRadius(39 + 20 * d.data.level)(d,i))
    .attr('fill',d => color(d.data.name))
    .on('mouseover', d => {
      ttdiv.transition().duration(200).style('opacity',.9)    
      ttdiv.html(decodeURIComponent(d.data.name) + '<br>' + format_time_amount(d.data.seconds_spent))
        .style('left',d3.event.pageX + 'px')
        .style('top',(d3.event.pageY -28) + 'px')
    })
    .on('mouseout',d => {
      ttdiv.transition().duration(200).style('opacity',0)    
    })

}

const format_time_amount = (seconds) => Math.round(seconds / (60 * 60)) + " hours " + Math.round((seconds % (60*60)) / 60) +  " minutes " 
