(function() {

	// Create the renderer
	let renderD3 = new dagreD3.render();
	let g = new dagreD3.graphlib.Graph({compound:true})
		  .setGraph({rankdir: "TB",align: "UL", ranksep: 40, ranker: "longest-path", acyclicer:"greedy", marginy:50, marginx:50, edgesep: 40})
		  .setDefaultEdgeLabel(function() { return {}; });

	let svg;
	let jsonData;

	function main(argument) {
		let treeJson = d3.json("data.json", function(error, data) {
			if (!error) {
				jsonData = data;
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

			    let node = crawlToNode(event.target, "node")
			    if (node && node.classList.contains("availableCourse")) {
			    	//do something
			    	courseUpdate(node);
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

	function courseUpdate(courseNode) {
		// body...
		courseNode.classList.toggle("selectedCourse");

		let jsonNode;

		for (let i = jsonData.length - 1; i >= 0; i--) {
			if (jsonData[i].node == courseNode){
				jsonNode = jsonData[i];
				break;
			}
		}
		for (var i = jsonNode.precursors.length - 1; i >= 0; i--) {
			let precursor = jsonNode.precursors[i]
			switch(precursor.type){
				case '3':
					let pre_node = getJSONNodeByID(precursor.id);
					pre_node.node.classList.remove("selectedCourse");
					courseNode.classList.remove("selectedCourse", "availableCourse");
				default:
					break;
			}
		}


		for (var i = jsonNode.children.length - 1; i >= 0; i--) {
			let child = jsonNode.children[i];
			let child_node;
			switch(child.type){
				case '2':
					child_node = getJSONNodeByID(child.id);
					console.log(child_node.precursors);
					let this_pre = child_node.precursors.find(function (x) {
						// body...
						return x.id == jsonNode.id;
					});
					if (this_pre) {
						child_node.precursors = child_node.precursors.filter(item => item !== this_pre);
					}
					else{
						child_node.precursors.push({"id": jsonNode.id, "type": "2"});
					}
					console.log(child_node.precursors);
					break;
				case '3':
					child_node = getJSONNodeByID(child.id);
					child_node.node.classList.toggle("selectedCourse", "availableCourse");
					break;
				default:
					break;
			}
		}

	}

	function getJSONNodeByID(ID) {
		// body...
		for (let i = jsonData.length - 1; i >= 0; i--) {
			if(jsonData[i].id == ID){
				return jsonData[i];
			}
		}
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

		for (let k = jsonData.length - 1; k >= 0; k--) {
			if (!jsonData[k].children) {
				jsonData[k].children = [];
			}
			for (var l = jsonData[k].precursors.length - 1; l >= 0; l--) {
				let pre = jsonData[k].precursors[l];
				let pre_node = getJSONNodeByID(pre.id);
				if (!pre_node.children) {
					pre_node.children = [];
				}
				pre_node.children.push({'id': jsonData[k].id, 'type': pre.type});
			}
		}


		for (let i = jsonData.length - 1; i >= 0; i--) {
			let node = jsonData[i];
			let classes = "";
			if (node.completed) { classes += "completedCourse "; }
			else if (node.precursors.length == 0) { classes += "availableCourse "}
			g.setNode(node.id, {label: node.id, class:classes});
			if (node.precursors.length > 0) {
				let clustered = false;
				for (let j = node.precursors.length - 1; j >= 0; j--) {
					let parent = node.precursors[j].id;
					if (node.precursors[j].type == '3') {
						let tempid;
						tempid = `${node.id}-${node.precursors[j].id}`;
						//g.setNode(tempid, {});
						console.log(tempid);
						//g.setParent(node.id, tempid);
						//g.setParent(node.precursors[j].id, tempid);
						g.setEdge(parent, node.id, {curve: d3.curveBasis});
						//g.setEdge(node.id, parent, {curve: d3.curveBasis});
						node.child = parent;
					}
				}
				for (var j = node.children.length - 1; j >= 0; j--) {
					if (node.children[j].type == '3') {
						let child = node.children[j].id;
						node.parent = child;
					}
				}
			}
		}
		for (let i = jsonData.length - 1; i >= 0; i--) {
			let node = jsonData[i];
			for (let j = node.precursors.length - 1; j >= 0; j--) {
				let parent = node.precursors[j];
				if (node.precursors[j].type != '3') {
					let tempid = node.id;
					let parent_node = getJSONNodeByID(parent.id);
					if (node.child) {
						tempid = node.child;
						console.log(tempid);

					}
					else if(parent_node.parent){
						parent = {"id": parent_node.parent};
						console.log(parent.id);
					}
					if (node.id == "FORR3FL05EU" || node.id == "ROBO2RG05AU") {
						console.log();
					}
					g.setEdge(parent.id, tempid, {curve: d3.curveBasis});
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
			for (let k = jsonData.length - 1; k >= 0; k--) {
				if (jsonData[k].id == d){
					jsonData[k].node = j[i];
				}
			}
		});
	}

	window.addEventListener("load", main, true);
	//window.addEventListener("resize", render, true);
})();