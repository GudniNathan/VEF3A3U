(function() {

	// Create the renderer
	let renderD3 = new dagreD3.render();
	let g = new dagreD3.graphlib.Graph({compound:true})
		  .setGraph({rankdir: "LR", align: "DR", ranksep: "40", ranker: "tight-tree", acyclicer:"greedy", marginy:50, marginx:50})
		  .setDefaultEdgeLabel(function() { return {}; });

	let svg;

	function main(argument) {
		let treeJson = d3.json("data.json", function(error, data) {
			if (!error) {
				createGraph(data);
				postRender();
			}
			else{
				console.log("Error fetching JSON");
				render();
				postRender();
			}
		});
		function postRender(argument) {
			// body...
			if (!svg) {
				svg = d3.select("svg");
			}

			document.querySelectorAll("g.nodes");

			d3.select("g.nodes").node().addEventListener("mouseup", function( event ) {
			    // display the current click count inside the clicked div
			    let node = crawlToNode(event.target, "node")
			    console.log(node);

			    if (node && node.classList.contains("availableCourse")) {
			    	//do something
			    	node.classList.toggle("selectedCourse");
			    }
			  }, true);


			//d3.select("svg").selectAll("g.node").on("mouseup", function(id) { var _node = g.node(id); console.log("Clicked " + id,_node); });

			document.querySelector("main").addEventListener("contextmenu", function (event) {
				// body...
				event.preventDefault();
			});
		}

		document.querySelector("#submitCourses").addEventListener("click", function (event) {
			// body...
			collectSelectedCourses();

		});
	}

	function crawlToNode(node, expectedClass) {
		// body...
		while(!node.classList.contains(expectedClass)) {
			if (node.nodeName == "BODY") {
				return false;
			}
			node = node.parentNode;
		}
		return node;
	}
	function collectSelectedCourses(){
		//let textNode = document.querySelectorAll(".selectedCourse.availableCourse g g text tspan");
		//let nodes = d3.selectAll(".selectedCourse.availableCourse");
		//console.log(nodes);
		courses = [];
		g.nodes().forEach(function(v) {
	    	//console.log("Node " + v + ": " + JSON.stringify(g.node(v)));
	    	//console.log(g.node(v));
	    	if (g.node(v).elem.classList.contains("selectedCourse")){

	    		courses.push(v);
	    	}
		});
		console.log(courses);

	}

	function createGraph(jsonData) {
		// body...
		for (let i = jsonData.length - 1; i >= 0; i--) {
			let node = jsonData[i];
			let classes = "";
			console.log(node);
			if (node.completed) { classes += "completedCourse "; }
			if (node.precursors.length == 0) { classes += "availableCourse "}
			g.setNode(node.id, {label: node.id, class:classes});
			if (node.precursors.length > 0) {
				for (let j = node.precursors.length - 1; j >= 0; j--) {
					let parent = node.precursors[j];
					g.setEdge(parent, node.id, {curve: d3.curveBasis});
				}
			}
		}

		render();
	}

	function render() {

		// Set up an SVG group so that we can translate the final graph.
		let parent = d3.select(d3.select("svg").node().parentNode);
		//d3.select("svg").remove();
		//svg = parent.append("svg");
		svg = d3.select("svg");

		svg.attr("width", Math.min(svg.node().getBoundingClientRect().width, svg.node().parentNode.getBoundingClientRect().width))
		    
		let inner = svg.append("g");

		// Run the renderer. This is what draws the final graph.
		renderD3(inner, g);

		// Set up zoom support
		let zoom = d3.zoom().on("zoom", function() {
			inner.attr("transform", d3.event.transform);
		  });

		zoom.filter(function(i, j, k, l) {
			// body...
			if (event.type == 'mousedown') {
				return event.button;
			}
			return !event.button;
		})

		svg.call(zoom);



		// Center the graph

		var initialScale = 0.75;

		svg.attr('height', g.graph().height * initialScale + 40);

		let transform = d3.zoomTransform(svg.node()).translate((svg.attr("width") - g.graph().width * initialScale) / 2, 0)
													.scale(initialScale);
		svg.call(zoom.transform, transform);



		inner.selectAll("g.node").each(function(d, i, j) {
			// body...
			j[i].classList.add('course');
		});
	}

	window.addEventListener("load", main, true);
	//window.addEventListener("resize", render, true);
})();