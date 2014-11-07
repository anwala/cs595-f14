 //OnClick event block
 var node = svg.selectAll(".node")
          .data(graph.nodes)
          .enter()
          .append("circle")
          .attr("class", "node")
          .on("click", specialNodeClick)
          .attr("id", function(d) { return d.name; })
          .attr("r", 5)
          .style("fill", function(d) { return color(d.color); })
          .call(force.drag);

function specialNodeClick(d) 
{
  if(globalClickFlag==1)
  {
    d3.selectAll('.node').style('fill', function(d) { return color(d.faction - 10); });
    globalClickFlag = 0;
  }
  else
  {
    d3.selectAll('.node').style('fill', function(d) { return color(d.color); });
    globalClickFlag = 1;
  }
}
