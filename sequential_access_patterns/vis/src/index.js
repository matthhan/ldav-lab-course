import * as d3 from 'd3';
import test_data from './test_data.json'
import './style.css'



d3.select('#app').append('svg').attr('width',700).attr('height',500)
let svg = d3.select('svg')


const color = d3.scaleOrdinal(d3.schemeCategory10)
const ttdiv = d3.select('body').append('div').attr('id','tooltip').style('opacity',0)
const g = svg.append('g').attr('transform','scale(2,2)')
g.selectAll('rect').data(test_data).enter()
 .append('g')
   .append('rect')
   .attr('x',0)
   .attr('y',(d,i) => i*20)
   .attr('height',20)
   .attr('width',d => d.badness * 3)
   .attr('fill',d => color(d.pattern[0]))
   .on('mouseover', d => {
     ttdiv.transition().duration(200).style('opacity',.9)    
     ttdiv.html(JSON.stringify(d.pattern))
       .style('left',d3.event.pageX + 'px')
       .style('top',(d3.event.pageY -28) + 'px')
   })
   .on('mouseout',d => {
     ttdiv.transition().duration(200).style('opacity',0)    
  })
g.selectAll('g').append('text').text(d => d.badness).attr('y',(d,i) => 15+i*20).attr('x',300).style('font-size','14px')

