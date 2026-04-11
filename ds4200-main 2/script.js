const svg = d3.select("#chart");
const tooltip = d3.select("#tooltip");

const width = +svg.attr("width");
const height = +svg.attr("height");

const margin = { top: 110, right: 180, bottom: 60, left: 170 };
const innerWidth = width - margin.left - margin.right;
const innerHeight = height - margin.top - margin.bottom;

const g = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

const questionMap = {
  Q2_1: "Voting in elections",
  Q2_2: "Participating in Census",
  Q2_3: "Supporting military",
  Q2_4: "Respecting opposing opinions",
  Q2_5: "Knowing Pledge of Allegiance",
  Q2_6: "Serving on a jury",
  Q2_7: "Following politics",
  Q2_8: "Believing in God",
  Q2_9: "Displaying the flag",
  Q2_10: "Protesting government actions"
};

const partyMap = {
  1: "Republican",
  2: "Democrat",
  3: "Independent",
  4: "Other",
  5: "None"
};

const responseMap = {
  1: "Very important",
  2: "Somewhat important",
  3: "Not so important",
  4: "Not at all important"
};

const responseOrder = [
  "Very important",
  "Somewhat important",
  "Not so important",
  "Not at all important"
];

const partyOrder = [
  "Republican",
  "Democrat",
  "Independent",
  "Other",
  "None"
];

const color = d3.scaleOrdinal()
  .domain(responseOrder)
  .range(["#440154", "#31688e", "#35b779", "#fde725"]);

const x = d3.scaleLinear()
  .domain([0, 100])
  .range([0, innerWidth]);

const y = d3.scaleBand()
  .domain(partyOrder)
  .range([0, innerHeight])
  .padding(0.22);

svg.append("text")
  .attr("class", "title")
  .attr("x", margin.left)
  .attr("y", 35)
  .text("Importance of Civic Activities by Political Party");

const subtitle = svg.append("text")
  .attr("class", "subtitle")
  .attr("x", margin.left)
  .attr("y", 62)
  .text("");

const xAxisGroup = g.append("g")
  .attr("class", "axis")
  .attr("transform", `translate(0, ${innerHeight})`);

const yAxisGroup = g.append("g")
  .attr("class", "axis");

g.append("text")
  .attr("x", innerWidth / 2)
  .attr("y", innerHeight + 45)
  .attr("text-anchor", "middle")
  .style("font-size", "13px")
  .text("Percent within party");

const legend = svg.append("g")
  .attr("class", "legend")
  .attr("transform", `translate(${width - 165}, ${margin.top})`);

responseOrder.forEach((label, i) => {
  const row = legend.append("g")
    .attr("transform", `translate(0, ${i * 26})`);

  row.append("rect")
    .attr("width", 16)
    .attr("height", 16)
    .attr("fill", color(label));

  row.append("text")
    .attr("x", 24)
    .attr("y", 12)
    .text(label);
});

svg.append("text")
  .attr("x", width - 165)
  .attr("y", margin.top - 16)
  .style("font-size", "13px")
  .style("font-weight", "bold")
  .text("Response");

const select = d3.select("#question-select");

Object.entries(questionMap).forEach(([key, label]) => {
  select.append("option")
    .attr("value", key)
    .text(label);
});

d3.csv("nonvoters_clean.csv", d3.autoType).then(data => {
  const filtered = data.filter(d => partyMap[d.Q30]);

  function buildChartData(questionKey) {
    const valid = filtered.filter(d => d[questionKey] >= 1 && d[questionKey] <= 4);

    const counts = d3.rollup(
      valid,
      v => v.length,
      d => partyMap[d.Q30],
      d => responseMap[d[questionKey]]
    );

    return partyOrder.map(party => {
      const responseCounts = counts.get(party) || new Map();
      const total = d3.sum(responseOrder, r => responseCounts.get(r) || 0);

      const row = { party };

      responseOrder.forEach(r => {
        row[r] = total === 0 ? 0 : ((responseCounts.get(r) || 0) / total) * 100;
      });

      return row;
    });
  }

  function update(questionKey) {
    const chartData = buildChartData(questionKey);

    subtitle.text(`Selected question: ${questionMap[questionKey]}`);

    const stacked = d3.stack()
      .keys(responseOrder)(chartData);

    xAxisGroup.transition()
      .duration(750)
      .call(
        d3.axisBottom(x)
          .ticks(10)
          .tickFormat(d => `${d}%`)
      );

    yAxisGroup.transition()
      .duration(750)
      .call(d3.axisLeft(y));

    const groups = g.selectAll(".stack-group")
      .data(stacked, d => d.key);

    const groupsEnter = groups.enter()
      .append("g")
      .attr("class", "stack-group")
      .attr("fill", d => color(d.key));

    groupsEnter.merge(groups);
    groups.exit().remove();

    const rects = g.selectAll(".stack-group")
      .selectAll("rect")
      .data(d => d.map(v => ({ ...v, key: d.key })), d => d.data.party);

    rects.enter()
      .append("rect")
      .attr("x", x(0))
      .attr("y", d => y(d.data.party))
      .attr("height", y.bandwidth())
      .attr("width", 0)
      .on("mousemove", function(event, d) {
        const value = d.data[d.key];
        tooltip
          .style("opacity", 1)
          .html(`
            <strong>Party:</strong> ${d.data.party}<br>
            <strong>Response:</strong> ${d.key}<br>
            <strong>Percent:</strong> ${value.toFixed(1)}%
          `)
          .style("left", `${event.pageX + 12}px`)
          .style("top", `${event.pageY - 28}px`);
      })
      .on("mouseleave", function() {
        tooltip.style("opacity", 0);
      })
      .merge(rects)
      .transition()
      .duration(750)
      .attr("x", d => x(d[0]))
      .attr("y", d => y(d.data.party))
      .attr("height", y.bandwidth())
      .attr("width", d => x(d[1]) - x(d[0]));

    rects.exit()
      .transition()
      .duration(500)
      .attr("width", 0)
      .remove();
  }

  select.on("change", function() {
    update(this.value);
  });

  update("Q2_1");
}).catch(error => {
  console.error("Error loading CSV:", error);

  svg.append("text")
    .attr("x", 40)
    .attr("y", 120)
    .style("fill", "red")
    .style("font-size", "16px");
});