import * as d3 from 'd3';
import test_data from './test_data.json'
import './style.css'

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
const preprocessed_data = withLevels(test_data,0)


d3.select('#app').append('svg').attr('width',500).attr('height',500)
let svg = d3.select('svg')

const g = svg.append('g').attr('transform','translate(200,100)')

const pie = d3.pie().value(d => d.seconds_spent).padAngle(0.03)
const first_level_slices = pie(preprocessed_data)
let slices = first_level_slices
for (let i = 0;i < slices.length;i++ ){
  const s = slices[i]
  if(s.data.children) {
    const endAngle = s.startAngle + (s.endAngle - s.startAngle) * (sum(s.data.children.map(x => x.seconds_spent))/s.data.seconds_spent)
    slices = slices.concat(d3.pie().value(d => d.seconds_spent).startAngle(s.startAngle).endAngle(endAngle).padAngle(0.03)(s.data.children))
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
    ttdiv.html(d.data.name + '<br>' + d.data.seconds_spent + 's')
      .style('left',d3.event.pageX + 'px')
      .style('top',(d3.event.pageY -28) + 'px')
  })
  .on('mouseout',d => {
    ttdiv.transition().duration(200).style('opacity',0)    
  })

