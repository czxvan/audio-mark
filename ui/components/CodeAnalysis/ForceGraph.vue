<template>
    <div ref="chartContainer"></div>
  </template>
  
  <script>
  import * as d3 from "d3";
  
  export default {
    async mounted() {
      try {
        // 使用 fetch 通过 HTTP 请求加载 CSV 文件
        const response = await fetch('/suits.csv');
        const csvText = await response.text();
  
        // 使用 d3.csvParse 解析 CSV 数据
        const suits = d3.csvParse(csvText, d => ({
          source: d.source,
          target: d.target,
          type: d.type
        }));
  
        this.createForceGraph(suits);
      } catch (error) {
        console.error("Error loading CSV data:", error);
      }
    },
    methods: {
      createForceGraph(suits) {
        const width = 928;
        const height = 600;
        const types = Array.from(new Set(suits.map(d => d.type)));
        const nodes = Array.from(new Set(suits.flatMap(l => [l.source, l.target])), id => ({ id }));
        const links = suits.map(d => Object.create(d));
  
        const color = d3.scaleOrdinal(types, d3.schemeCategory10);
  
        const simulation = d3.forceSimulation(nodes)
          .force("link", d3.forceLink(links).id(d => d.id))
          .force("charge", d3.forceManyBody().strength(-400))
          .force("x", d3.forceX())
          .force("y", d3.forceY());
  
          const svg = d3.select(this.$refs.chartContainer)
                        .append("svg")
                        .attr("viewBox", [-width / 2, -height / 2, width, height])
                        .attr("width", "100%")   // 设置为 100%，自适应父容器
                        .attr("height", "100%")  // 设置为 100%，自适应父容器
                        .attr("style", "max-width: 100%; height: auto; font: 12px sans-serif;");

  
        svg.append("defs").selectAll("marker")
          .data(types)
          .join("marker")
          .attr("id", d => `arrow-${d}`)
          .attr("viewBox", "0 -5 10 10")
          .attr("refX", 15)
          .attr("refY", -0.5)
          .attr("markerWidth", 6)
          .attr("markerHeight", 6)
          .attr("orient", "auto")
          .append("path")
          .attr("fill", color)
          .attr("d", "M0,-5L10,0L0,5");
  
        const link = svg.append("g")
          .attr("fill", "none")
          .attr("stroke-width", 1.5)
          .selectAll("path")
          .data(links)
          .join("path")
          .attr("stroke", d => color(d.type))
          .attr("marker-end", d => `url(#arrow-${d.type})`);
  
        const node = svg.append("g")
          .attr("fill", "currentColor")
          .attr("stroke-linecap", "round")
          .attr("stroke-linejoin", "round")
          .selectAll("g")
          .data(nodes)
          .join("g")
          .call(this.drag(simulation));
  
        node.append("circle")
          .attr("stroke", "white")
          .attr("stroke-width", 1.5)
          .attr("r", 4);
  
        node.append("text")
          .attr("x", 8)
          .attr("y", "0.31em")
          .text(d => d.id)
          .clone(true).lower()
          .attr("fill", "none")
          .attr("stroke", "white")
          .attr("stroke-width", 3);
  
        simulation.on("tick", () => {
          link.attr("d", this.linkArc);
          node.attr("transform", d => `translate(${d.x},${d.y})`);
        });
      },
      linkArc(d) {
        const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y);
        return `
          M${d.source.x},${d.source.y}
          A${r},${r} 0 0,1 ${d.target.x},${d.target.y}
        `;
      },
      drag(simulation) {
        function dragstarted(event, d) {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        }
        function dragged(event, d) {
          d.fx = event.x;
          d.fy = event.y;
        }
        function dragended(event, d) {
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        }
        return d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended);
      }
    }
  };
  </script>
  
  <style scoped>
  /* 适当的样式来美化图表的显示 */
  </style>
  