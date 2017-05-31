import * as d3 from 'd3';
import test_data from './test_data.json'
import './style.css'



//console.log(JSON.stringify(test_data))

d3.select('#app').append('svg').attr('width',500).attr('height',500)
let svg = d3.select('svg')

const g = svg.append('g').attr('transform','translate(200,50)')

const pie = d3.pie().value(d => d.seconds_spent)
const slices = pie(test_data)
const arc = d3.arc().innerRadius(30).outerRadius(50)
const color = d3.scaleOrdinal(d3.schemeCategory10)
const ttdiv = d3.select('body').append('div').attr('id','tooltip').style('opacity',0)

g
  .selectAll('path.slice').data(slices).enter().append('path')
  .attr('class','slice')
  .attr('d',arc)
  .attr('fill',d => color(d.data.name))
  .on('mouseover', d => {
    ttdiv.transition().duration(200).style('opacity',.9)    
    ttdiv.html(d.data.name)
      .style('left',d3.event.pageX + 'px')
      .style('top',(d3.event.pageY -28) + 'px')
  })
  .on('mouseout',d => {
    ttdiv.transition().duration(200).style('opacity',0)    
  })

