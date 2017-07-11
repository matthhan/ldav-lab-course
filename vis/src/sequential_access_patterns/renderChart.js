import * as d3 from 'd3';
import './style.css'


function hasRep(arr) {
  for(let i = 1;i < arr.length;i++) {
    if(arr[i] === arr[i-1]) return true;
  }
  return false;
}
export default function renderChart(data,chartcontainer) {
  const patterns = data.filter(x => !hasRep(x.pattern)).filter(x => x.pattern.length > 1).slice(1);
  d3.select('#'+ chartcontainer).append('svg').attr('width','100%').attr('height',10000)
  let svg = d3.select('svg')

  const patternstring = pattern => pattern.join("<br>")

  const widthscale = d3.scaleLog().domain([0.1,Math.max(...(patterns.map(x => x.badness)))]).range([0,300])
  let colorcounter = 0;
  const color = () => {
      colorcounter++;
      return d3.schemeCategory20[colorcounter % 20]
  }
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
  //g.selectAll('g').append('text').text(d => d.badness).attr('y',(d,i) => 15+i*20).attr('x',300).style('font-size','14px')
}
