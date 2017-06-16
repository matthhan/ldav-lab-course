import * as d3 from 'd3';
import patterns from './patterns.json'
import './style.css'



d3.select('#app').append('svg').attr('width',700).attr('height',10000)
let svg = d3.select('svg')

const patternstring = pattern => pattern.join("<br>")

const widthscale = d3.scaleLinear().domain([0,10000]).range([0,300])
const color = d3.scaleOrdinal(d3.schemeCategory10)
const ttdiv = d3.select('body').append('div').attr('id','tooltip').style('opacity',0)
const g = svg.append('g').attr('transform','scale(2,2)')
g.selectAll('rect').data(patterns).enter()
 .append('g')
   .append('rect')
   .attr('x',0)
   .attr('y',(d,i) => i*20)
   .attr('height',20)
   .attr('width',d => widthscale(d.badness))
   .attr('fill',d => color(d.pattern[0]))
   .on('mouseover', d => {
     ttdiv.transition().duration(200).style('opacity',.9)    
     ttdiv.html(patternstring(d.pattern))
       .style('left',d3.event.pageX + 'px')
       .style('top',(d3.event.pageY -28) + 'px')
   })
   .on('mouseout',d => {
     ttdiv.transition().duration(200).style('opacity',0)    
  })
g.selectAll('g').append('text').text(d => d.badness).attr('y',(d,i) => 15+i*20).attr('x',300).style('font-size','14px')

